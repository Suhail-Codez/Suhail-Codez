"""
IDPDR — Intelligent Disease Prediction & Drug Recommendation — Django REST API Views
All ML inference, sentiment analysis, drug recommendation, analytics, 
drug report, interaction checker, and disease info endpoints.
"""
import os, json, joblib, re, datetime
import numpy as np
from collections import Counter

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from django.conf import settings
from django.db.models import Avg, Count, Q
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import DrugReview, Prediction, DrugComparison, DrugInteractionCheck, SearchLog, DiagnosisReport, Drug
from .pdf_utils import build_pdf
from .drug_data import DRUG_INTERACTIONS  # bugfix: check_interactions() referenced this without importing it (NameError/500 on every call)


def _merged_drug_database():
    """
    Merge the built-in, code-based drug knowledge base with any active
    drugs an admin has added/edited through the Admin Dashboard's Drug
    Database Management page. Admin-managed entries take precedence over a
    curated entry of the same name (so an admin can override/correct a
    built-in entry), and are included for every module that searches or
    reports on drugs (Drug Search, Drug Report).
    """
    merged = dict(DRUG_DATABASE)
    for d in Drug.objects.filter(is_active=True):
        merged[d.name] = d.as_dict()
    return merged

# ── Lazy model loader ──────────────────────────────────────────
_cache = {}

def _load():
    if _cache: return
    d = settings.MODELS_DIR
    for k, f in [("nb","naive_bayes.pkl"),("rf","random_forest.pkl"),
                  ("svm","svm.pkl"),("lr","logistic_regression.pkl"),
                  ("le","label_encoder.pkl"),("vader","vader.pkl")]:
        p = os.path.join(d, f)
        if os.path.exists(p):
            _cache[k] = joblib.load(p)
    for k, f in [("recs","recommendations.json"),("syms","symptoms_map.json"),
                  ("results","model_results.json"),("trends","trends.json")]:
        p = os.path.join(d, f)
        if os.path.exists(p):
            with open(p) as fp:
                _cache[k] = json.load(fp)

# ── Text preprocessing ─────────────────────────────────────────
_sw = None; _lm = None
def _clean(text):
    global _sw, _lm
    if _sw is None:
        try:
            _sw = set(stopwords.words("english"))
        except LookupError:
            nltk.download('stopwords', quiet=True)
            _sw = set(stopwords.words("english"))
        try:
            _lm = WordNetLemmatizer()
            _lm.lemmatize("test")
        except LookupError:
            nltk.download('wordnet', quiet=True)
            _lm = WordNetLemmatizer()
    text = re.sub(r"[^a-z\s]", " ", str(text).lower())
    return " ".join(_lm.lemmatize(t) for t in text.split() if t not in _sw and len(t)>2)


# ── Helpers ────────────────────────────────────────────────────
def _predict_one(model, text):
    clean = _clean(text)
    idx = model.predict([clean])[0]
    cond = _cache["le"].inverse_transform([idx])[0]
    conf = None
    clf = model.named_steps["clf"]
    if hasattr(clf, "predict_proba"):
        conf = round(float(max(model.predict_proba([clean])[0]))*100, 1)
    elif hasattr(clf, "decision_function"):
        s = model.decision_function([clean])[0]
        e = [2.718**x for x in s]
        conf = round(max(e)/sum(e)*100, 1)
    return cond, conf

def _vader(text):
    _load()
    scores = _cache["vader"].polarity_scores(str(text))
    c = scores["compound"]
    return {
        "sentiment": "positive" if c>=0.05 else "negative" if c<=-0.05 else "neutral",
        "compound": round(c, 4),
        "pos": round(scores["pos"],4),
        "neg": round(scores["neg"],4),
        "neu": round(scores["neu"],4),
        "sentiment_score": round((c+1)*5, 2),
    }


# -- Drug Database (Extended) -- imported from consolidated master module --
from .drug_database import DRUG_DATABASE, get_drug_info, all_drug_names, build_fallback_profile

# Disease Information Database
DISEASE_DATABASE = {
    "Diabetes Type 2": {
        "description": "A chronic metabolic disorder where the body doesn't use insulin properly, leading to elevated blood glucose levels.",
        "symptoms": ["Frequent urination", "Excessive thirst", "Unexplained weight loss", "Fatigue", "Blurred vision", "Slow-healing sores", "Frequent infections"],
        "causes": ["Insulin resistance", "Obesity", "Physical inactivity", "Genetic factors", "Poor diet"],
        "risk_factors": ["Overweight/Obesity (BMI > 25)", "Age > 45", "Family history", "Prediabetes", "Gestational diabetes history", "Sedentary lifestyle"],
        "diagnosis": ["Fasting blood glucose ≥ 126 mg/dL", "HbA1c ≥ 6.5%", "2-hour glucose tolerance test ≥ 200 mg/dL", "Random glucose ≥ 200 mg/dL with symptoms"],
        "treatment": ["Lifestyle modification", "Metformin (first-line)", "GLP-1 agonists", "SGLT-2 inhibitors", "Insulin (advanced cases)", "DPP-4 inhibitors"],
        "lifestyle": ["Exercise 150 min/week", "Low-glycemic diet", "Weight reduction", "Regular blood glucose monitoring", "Foot care", "Smoking cessation"],
        "prevention": ["Healthy weight maintenance", "Regular physical activity", "Balanced diet", "Avoiding processed sugars", "Regular health screenings"],
        "emergency_signs": ["Blood glucose > 400 mg/dL", "Severe confusion", "Loss of consciousness", "Fruity breath (DKA)", "Rapid breathing", "Vomiting + abdominal pain"],
        "related_medicines": ["Metformin", "Ozempic", "Glipizide", "Empagliflozin", "Sitagliptin", "Insulin"]
    },
    "Hypertension": {
        "description": "A condition where blood pressure in the arteries is persistently elevated, defined as ≥ 130/80 mmHg.",
        "symptoms": ["Often asymptomatic", "Headache (severe)", "Shortness of breath", "Nosebleeds", "Dizziness", "Chest pain", "Visual changes"],
        "causes": ["Primary: unknown (essential hypertension)", "Secondary: kidney disease, hormonal disorders, medications"],
        "risk_factors": ["Age", "Family history", "Obesity", "High sodium diet", "Alcohol", "Physical inactivity", "Stress", "Smoking"],
        "diagnosis": ["Multiple BP readings ≥ 130/80 mmHg", "24-hour ambulatory BP monitoring", "Blood tests (kidney function, electrolytes)", "ECG"],
        "treatment": ["ACE inhibitors", "ARBs", "Calcium channel blockers", "Thiazide diuretics", "Beta-blockers", "Lifestyle changes"],
        "lifestyle": ["DASH diet", "Reduce sodium (< 2g/day)", "Regular aerobic exercise", "Weight loss", "Limit alcohol", "Stress management"],
        "prevention": ["Healthy diet", "Regular exercise", "Normal weight", "Moderate alcohol", "No smoking", "Stress reduction"],
        "emergency_signs": ["BP > 180/120 mmHg", "Severe headache", "Vision loss", "Chest pain", "Difficulty breathing", "Stroke symptoms (FAST)"],
        "related_medicines": ["Lisinopril", "Amlodipine", "Losartan", "Hydrochlorothiazide", "Metoprolol", "Valsartan"]
    },
    "Depression": {
        "description": "A common mental health disorder characterized by persistent feelings of sadness, hopelessness, and loss of interest lasting at least 2 weeks.",
        "symptoms": ["Persistent sadness", "Loss of interest/pleasure", "Fatigue", "Sleep disturbances", "Appetite changes", "Difficulty concentrating", "Suicidal thoughts"],
        "causes": ["Neurochemical imbalances", "Genetics", "Life events (trauma, loss)", "Hormonal changes", "Medical conditions", "Medications"],
        "risk_factors": ["Family history", "Previous depression", "Major life stressors", "Chronic illness", "Substance abuse", "Isolation"],
        "diagnosis": ["DSM-5 criteria", "PHQ-9 screening", "Clinical interview", "Rule out medical causes", "Blood tests (thyroid, vitamin D)"],
        "treatment": ["SSRIs (first-line)", "SNRIs", "Cognitive Behavioral Therapy", "Interpersonal Therapy", "Combination therapy", "ECT (severe cases)"],
        "lifestyle": ["Regular exercise", "Structured routine", "Social connection", "Sleep hygiene", "Mindfulness meditation", "Avoid alcohol"],
        "prevention": ["Stress management", "Strong social support", "Therapy for risk factors", "Regular exercise", "Purpose and meaning"],
        "emergency_signs": ["Active suicidal ideation with plan", "Self-harm", "Psychotic symptoms", "Complete inability to function", "Refusing food/water"],
        "related_medicines": ["Sertraline", "Fluoxetine", "Escitalopram", "Venlafaxine", "Mirtazapine", "Bupropion"]
    },
    "Asthma": {
        "description": "A chronic inflammatory lung disease causing reversible airway narrowing, leading to recurrent episodes of wheezing, shortness of breath, and coughing.",
        "symptoms": ["Wheezing", "Shortness of breath", "Chest tightness", "Persistent cough (especially at night)", "Difficulty breathing during exercise"],
        "causes": ["Airway inflammation and hyperresponsiveness", "Allergens", "Exercise", "Cold air", "Respiratory infections", "Irritants"],
        "risk_factors": ["Allergies", "Family history", "Childhood respiratory infections", "Obesity", "Smoking exposure", "Air pollution"],
        "diagnosis": ["Spirometry (FEV1/FVC < 0.7)", "Peak flow monitoring", "Bronchodilator reversibility test", "Allergy testing", "FeNO test"],
        "treatment": ["Short-acting bronchodilators (SABA)", "Inhaled corticosteroids", "Long-acting bronchodilators", "Leukotriene modifiers", "Biologics (severe)"],
        "lifestyle": ["Identify and avoid triggers", "Use air purifiers", "No smoking", "Regular preventer inhaler use", "Action plan for attacks"],
        "prevention": ["Avoid allergens/triggers", "Influenza vaccination", "Maintain healthy weight", "Regular follow-up", "Correct inhaler technique"],
        "emergency_signs": ["Severe breathlessness at rest", "Unable to speak full sentences", "Blue lips or fingertips (cyanosis)", "Confusion", "Not responding to reliever inhaler"],
        "related_medicines": ["Salbutamol", "Budesonide", "Formoterol", "Montelukast", "Fluticasone", "Tiotropium"]
    },
    "Migraine": {
        "description": "A neurological disorder causing recurrent moderate-to-severe headaches, often unilateral and pulsating, lasting 4–72 hours.",
        "symptoms": ["Severe throbbing headache", "Nausea/vomiting", "Photophobia", "Phonophobia", "Aura (visual/sensory changes in some)", "Neck stiffness"],
        "causes": ["Exact cause unknown", "Trigeminovascular system activation", "Serotonin fluctuations", "Genetic predisposition"],
        "risk_factors": ["Female sex (3x more common)", "Family history", "Hormonal changes", "Stress", "Sleep disruption", "Certain foods/drinks"],
        "diagnosis": ["Clinical diagnosis (ICHD-3 criteria)", "No headache on > 15 days/month", "Rule out secondary causes", "Neuroimaging if atypical"],
        "treatment": ["Triptans (acute)", "NSAIDs", "Anti-nausea medications", "Preventive: propranolol, topiramate, amitriptyline", "CGRP inhibitors"],
        "lifestyle": ["Identify and track triggers", "Regular sleep schedule", "Stress management", "Hydration", "Regular meals", "Limit caffeine"],
        "prevention": ["Trigger avoidance diary", "Preventive medications if > 4/month", "Biofeedback", "Botulinum toxin injections"],
        "emergency_signs": ["Thunderclap headache (worst of life)", "Headache with fever + stiff neck", "Headache after head injury", "Progressive worsening", "New onset > 50 years"],
        "related_medicines": ["Sumatriptan", "Rizatriptan", "Topiramate", "Propranolol", "Amitriptyline", "Ibuprofen"]
    },
    "GERD": {
        "description": "Gastroesophageal Reflux Disease — chronic condition where stomach acid flows back into the esophagus, causing heartburn and damage.",
        "symptoms": ["Heartburn", "Regurgitation", "Chest pain", "Difficulty swallowing", "Sour taste in mouth", "Chronic cough", "Hoarseness"],
        "causes": ["Weakened lower esophageal sphincter", "Hiatal hernia", "Delayed gastric emptying", "Obesity"],
        "risk_factors": ["Obesity", "Pregnancy", "Smoking", "Certain foods (fatty, spicy)", "Alcohol", "Lying down after meals", "Certain medications"],
        "diagnosis": ["Clinical diagnosis from symptoms", "Upper endoscopy", "pH monitoring", "Esophageal manometry", "Barium swallow"],
        "treatment": ["PPIs (mainstay)", "H2 blockers", "Antacids", "Prokinetics", "Surgery (Nissen fundoplication) for severe cases"],
        "lifestyle": ["Elevate head of bed", "Small, frequent meals", "Avoid trigger foods", "No eating 3 hours before sleep", "Weight loss", "Quit smoking"],
        "prevention": ["Maintain healthy weight", "Avoid trigger foods", "No smoking", "Limit alcohol", "Avoid tight clothing"],
        "emergency_signs": ["Difficulty swallowing (dysphagia)", "Vomiting blood", "Black tarry stools", "Unexplained weight loss", "Severe chest pain"],
        "related_medicines": ["Omeprazole", "Pantoprazole", "Ranitidine", "Esomeprazole", "Antacids", "Metoclopramide"]
    },
    "Anxiety": {
        "description": "A group of mental health disorders characterized by excessive, persistent worry or fear that interferes with daily activities.",
        "symptoms": ["Excessive worry", "Restlessness", "Rapid heartbeat", "Muscle tension", "Difficulty concentrating", "Sleep disturbances", "Irritability"],
        "causes": ["Genetics", "Brain chemistry", "Stressful life events", "Trauma", "Medical conditions", "Substance use"],
        "risk_factors": ["Family history", "Chronic stress", "Trauma history", "Other mental health conditions", "Chronic illness", "Caffeine/stimulant use"],
        "diagnosis": ["Clinical interview (DSM-5 criteria)", "GAD-7 screening", "Rule out medical causes (thyroid, cardiac)", "Physical examination"],
        "treatment": ["SSRIs/SNRIs (first-line)", "Buspirone", "Benzodiazepines (short-term)", "Cognitive Behavioral Therapy", "Relaxation techniques"],
        "lifestyle": ["Regular exercise", "Limit caffeine and alcohol", "Sleep hygiene", "Mindfulness/meditation", "Structured routine", "Social support"],
        "prevention": ["Stress management", "Early intervention", "Healthy coping strategies", "Regular physical activity", "Adequate sleep"],
        "emergency_signs": ["Panic attack with chest pain", "Suicidal thoughts", "Inability to function", "Severe dissociation", "Self-harm urges"],
        "related_medicines": ["Sertraline", "Lorazepam", "Buspirone", "Alprazolam", "Clonazepam", "Escitalopram"]
    },
    "Hypothyroidism": {
        "description": "A condition in which the thyroid gland does not produce enough thyroid hormone, slowing the body's metabolism.",
        "symptoms": ["Fatigue", "Weight gain", "Cold intolerance", "Dry skin", "Hair loss", "Constipation", "Depression", "Muscle weakness"],
        "causes": ["Hashimoto's thyroiditis (autoimmune)", "Iodine deficiency", "Thyroid surgery/radiation", "Certain medications", "Pituitary disorders"],
        "risk_factors": ["Female sex", "Age > 60", "Family history of thyroid disease", "Autoimmune conditions", "Previous thyroid treatment"],
        "diagnosis": ["TSH (elevated)", "Free T4 (low)", "Thyroid antibody tests", "Thyroid ultrasound if nodules suspected"],
        "treatment": ["Levothyroxine (first-line)", "Liothyronine (combination in select cases)", "Desiccated thyroid extract", "Regular TSH monitoring"],
        "lifestyle": ["Consistent medication timing (empty stomach)", "Balanced diet with adequate iodine", "Regular follow-up labs", "Manage weight and energy expectations"],
        "prevention": ["Adequate dietary iodine", "Regular screening if at risk", "Monitor thyroid function after neck radiation/surgery"],
        "emergency_signs": ["Myxedema coma (confusion, hypothermia)", "Severe bradycardia", "Loss of consciousness", "Severe swelling"],
        "related_medicines": ["Levothyroxine", "Liothyronine", "Armour Thyroid"]
    },
    "Insomnia": {
        "description": "A sleep disorder characterized by persistent difficulty falling asleep, staying asleep, or waking too early despite adequate opportunity to sleep.",
        "symptoms": ["Difficulty falling asleep", "Frequent night waking", "Waking too early", "Daytime fatigue", "Irritability", "Difficulty concentrating"],
        "causes": ["Stress/anxiety", "Poor sleep habits", "Medical conditions", "Medications", "Caffeine/alcohol use", "Shift work/jet lag"],
        "risk_factors": ["Stress", "Irregular schedule", "Mental health conditions", "Chronic pain", "Older age", "Excessive screen time before bed"],
        "diagnosis": ["Clinical history and sleep diary", "Insomnia Severity Index", "Polysomnography (if other sleep disorder suspected)"],
        "treatment": ["Cognitive Behavioral Therapy for Insomnia (CBT-I, first-line)", "Z-drugs (zolpidem, eszopiclone)", "Low-dose doxepin/trazodone", "Melatonin"],
        "lifestyle": ["Consistent sleep-wake schedule", "Limit caffeine/alcohol, especially evening", "Screen-free wind-down routine", "Cool, dark, quiet bedroom", "Regular daytime exercise"],
        "prevention": ["Good sleep hygiene", "Stress management", "Limit naps", "Consistent bedtime routine"],
        "emergency_signs": ["Severe sleep deprivation affecting safety (e.g., driving)", "Signs of underlying sleep apnea (choking, gasping)", "Suicidal ideation"],
        "related_medicines": ["Zolpidem", "Eszopiclone", "Trazodone", "Doxepin", "Melatonin"]
    },
    "Pain": {
        "description": "An unpleasant sensory and emotional experience associated with actual or potential tissue damage; may be acute or chronic.",
        "symptoms": ["Localized or diffuse ache", "Sharp or throbbing sensation", "Swelling", "Stiffness", "Reduced range of motion", "Sleep disturbance"],
        "causes": ["Injury/trauma", "Inflammation", "Musculoskeletal strain", "Chronic conditions (arthritis)", "Nerve damage"],
        "risk_factors": ["Physical labor/overuse", "Obesity", "Prior injury", "Age", "Sedentary lifestyle", "Certain occupations/sports"],
        "diagnosis": ["Clinical history and physical exam", "Imaging (X-ray/MRI) if indicated", "Pain scale assessment", "Blood tests if inflammatory cause suspected"],
        "treatment": ["Acetaminophen", "NSAIDs (ibuprofen, naproxen)", "Topical analgesics", "Physical therapy", "Short-course opioids for severe acute pain"],
        "lifestyle": ["Rest and gradual return to activity", "Ice/heat therapy", "Stretching and strengthening exercises", "Ergonomic adjustments", "Weight management"],
        "prevention": ["Proper body mechanics", "Regular exercise and stretching", "Adequate rest between activities", "Ergonomic workspace setup"],
        "emergency_signs": ["Sudden severe pain with numbness/weakness", "Chest pain", "Signs of fracture or deformity", "Pain with loss of bladder/bowel control"],
        "related_medicines": ["Ibuprofen", "Naproxen", "Acetaminophen", "Celecoxib", "Tramadol"]
    },
    "Infection": {
        "description": "Invasion and multiplication of microorganisms (bacteria, viruses, fungi) in body tissues, potentially causing local or systemic illness.",
        "symptoms": ["Fever", "Localized redness/swelling", "Pain", "Fatigue", "Chills", "Discharge/pus", "Swollen lymph nodes"],
        "causes": ["Bacterial invasion", "Viral infection", "Fungal infection", "Compromised immune system", "Poor wound care"],
        "risk_factors": ["Weakened immune system", "Chronic illness (diabetes)", "Recent surgery/wounds", "Close contact with infected individuals", "Poor hygiene"],
        "diagnosis": ["Clinical examination", "Complete blood count (elevated WBC)", "Culture and sensitivity testing", "Imaging if deep infection suspected"],
        "treatment": ["Antibiotics (bacterial)", "Antivirals (viral, if indicated)", "Antifungals (fungal)", "Supportive care (fluids, rest, fever control)"],
        "lifestyle": ["Complete the full antibiotic course", "Rest and hydration", "Proper wound care/hygiene", "Isolate if contagious"],
        "prevention": ["Hand hygiene", "Vaccination", "Wound care", "Avoiding contact with infected individuals", "Safe food/water practices"],
        "emergency_signs": ["High fever (>103°F/39.4°C)", "Difficulty breathing", "Rapid heart rate with confusion (sepsis signs)", "Spreading redness/red streaking"],
        "related_medicines": ["Amoxicillin", "Azithromycin", "Doxycycline", "Cephalexin", "Ciprofloxacin"]
    },
    "High Cholesterol": {
        "description": "A condition marked by elevated levels of LDL (\"bad\") cholesterol in the blood, increasing the risk of heart disease and stroke.",
        "symptoms": ["Usually asymptomatic", "Xanthomas (fatty deposits under skin, severe cases)", "Chest pain (if coronary disease develops)"],
        "causes": ["Diet high in saturated/trans fats", "Genetics (familial hypercholesterolemia)", "Obesity", "Sedentary lifestyle", "Diabetes"],
        "risk_factors": ["Family history", "Poor diet", "Obesity", "Physical inactivity", "Smoking", "Diabetes", "Age"],
        "diagnosis": ["Lipid panel (total cholesterol, LDL, HDL, triglycerides)", "Fasting blood test", "Cardiovascular risk assessment"],
        "treatment": ["Statins (first-line)", "Ezetimibe", "PCSK9 inhibitors (severe cases)", "Dietary and lifestyle modification"],
        "lifestyle": ["Reduce saturated/trans fat intake", "Increase fiber intake", "Regular aerobic exercise", "Weight management", "Quit smoking"],
        "prevention": ["Heart-healthy diet", "Regular exercise", "Routine lipid screening", "Avoid tobacco", "Limit alcohol"],
        "emergency_signs": ["Chest pain/pressure", "Sudden weakness or numbness (stroke signs)", "Shortness of breath", "Severe leg pain (peripheral artery disease)"],
        "related_medicines": ["Atorvastatin", "Rosuvastatin", "Simvastatin", "Pravastatin", "Ezetimibe"]
    }
}


# ═══════════════════════════════════════════════════════════════
# API VIEWS
# ═══════════════════════════════════════════════════════════════

@api_view(["GET"])
@ensure_csrf_cookie
def health(request):
    """
    Public health-check endpoint. Also intentionally the CSRF-priming
    endpoint the sign-in/register pages call before authenticating —
    @ensure_csrf_cookie is required here because without it Django never
    actually issues the csrftoken cookie on a plain GET (the frontend was
    previously reading an always-empty cookie, which is why login/register
    had been marked @csrf_exempt as a workaround instead of a real fix).
    """
    _load()
    return Response({"status":"ok","models_loaded":len([k for k in ["nb","rf","svm","lr"] if k in _cache]),"version":"3.0"})


@api_view(["GET"])
def conditions_list(request):
    _load()
    data = [{"condition":c,"symptoms":s,"drug_count":len(_cache["recs"].get(c,[]))}
            for c,s in _cache.get("syms",{}).items()]
    return Response({"conditions":data,"total":len(data)})


@api_view(["POST"])
def predict(request):
    """Predict disease using all 4 models + majority vote."""
    _load()
    symptoms = request.data.get("symptoms","").strip()
    if not symptoms:
        return Response({"error":"Symptoms required"},status=400)

    results = {}
    model_map = {"Naive Bayes":"nb","Random Forest":"rf","SVM":"svm","Logistic Regression":"lr"}
    for name, key in model_map.items():
        if key in _cache:
            try:
                cond, conf = _predict_one(_cache[key], symptoms)
                results[name] = {"condition":cond,"confidence":conf}
            except Exception as e:
                results[name] = {"condition":"Error","confidence":0,"error":str(e)}

    conditions = [v["condition"] for v in results.values() if "condition" in v and v["condition"]!="Error"]
    majority = Counter(conditions).most_common(1)[0][0] if conditions else None
    votes = Counter(conditions)

    pred_obj = Prediction.objects.create(
        symptoms=symptoms,
        predicted_condition=majority or "",
        nb_prediction=results.get("Naive Bayes",{}).get("condition",""),
        rf_prediction=results.get("Random Forest",{}).get("condition",""),
        svm_prediction=results.get("SVM",{}).get("condition",""),
        lr_prediction=results.get("Logistic Regression",{}).get("condition",""),
        nb_confidence=results.get("Naive Bayes",{}).get("confidence",0) or 0,
        rf_confidence=results.get("Random Forest",{}).get("confidence",0) or 0,
        svm_confidence=results.get("SVM",{}).get("confidence",0) or 0,
        lr_confidence=results.get("Logistic Regression",{}).get("confidence",0) or 0,
        model_used="ensemble_majority_vote",
    )

    acc = {k.replace("_"," ").title():round(v*100,1) for k,v in _cache.get("results",{}).items()}

    # Get top drug for predicted condition
    top_drug = None
    if majority and majority in _cache.get("recs", {}):
        recs = _cache["recs"][majority]
        if recs:
            top_drug = recs[0]["drugName"]

    # Disease info summary
    disease_info = DISEASE_DATABASE.get(majority, {})

    return Response({
        "id": pred_obj.id,
        "input_symptoms": symptoms,
        "predictions": results,
        "majority_vote": majority,
        "vote_counts": dict(votes),
        "model_accuracies": acc,
        "recommended_condition": majority,
        "top_drug": top_drug,
        "disease_summary": {
            "description": disease_info.get("description", ""),
            "treatment": disease_info.get("treatment", [])[:3],
            "emergency_signs": disease_info.get("emergency_signs", [])[:3],
        }
    })


@api_view(["GET"])
def recommend(request):
    """Get top drug recommendations for a condition."""
    _load()
    condition = request.GET.get("condition","").strip()
    if not condition:
        return Response({"error":"condition required"},status=400)

    recs = _cache.get("recs",{}).get(condition)
    if not recs:
        return Response({"error":f"No data for: {condition}"},status=404)

    out = []
    for i, r in enumerate(recs[:5], 1):
        fs = round(r["final_score"],2)
        drug_info = DRUG_DATABASE.get(r["drugName"], {})
        out.append({
            "rank": i,
            "drug_name": r["drugName"],
            "avg_rating": round(r["avg_rating"],2),
            "sentiment_score": round(r["avg_sentiment"],2),
            "weighted_score": round(r["weighted_score"],2),
            "final_score": fs,
            "review_count": int(r["review_count"]),
            "badge": "⭐ Top Pick" if i==1 else "✅ Highly Recommended" if fs>=7 else "👍 Recommended",
            "strength_pct": min(round(fs/10*100), 100),
            "drug_class": drug_info.get("drug_class", ""),
            "generic_name": drug_info.get("generic_name", r["drugName"]),
            "prescription_required": drug_info.get("prescription_required", True),
            "price_inr": drug_info.get("price_inr", "Consult pharmacist"),
        })

    return Response({
        "condition": condition,
        "recommendations": out,
        "methodology": "Final Score = (0.7×Rating + 0.3×VADER_Sentiment + Bayesian_Average) / 2",
        "total": len(out),
    })


@api_view(["GET"])
def recommend_all(request):
    """Return top drug for every condition."""
    _load()
    out = {}
    for cond, recs in _cache.get("recs",{}).items():
        if recs:
            r = recs[0]
            out[cond] = {"top_drug":r["drugName"],"score":round(r["final_score"],2),
                         "top3":[x["drugName"] for x in recs[:3]]}
    return Response({"all":out})


@api_view(["POST"])
def sentiment(request):
    """VADER sentiment analysis on a drug review."""
    review      = request.data.get("review","").strip()
    drug_name   = request.data.get("drug_name","Unknown")
    condition   = request.data.get("condition","Unknown")
    rating      = float(request.data.get("rating", 5))
    if not review:
        return Response({"error":"review required"},status=400)

    s = _vader(review)
    label_map = {"positive":"Positive 😊","negative":"Negative 😞","neutral":"Neutral 😐"}
    color_map = {"positive":"#10b981","negative":"#ef4444","neutral":"#f59e0b"}

    DrugReview.objects.create(
        drug_name=drug_name, condition=condition, review=review,
        rating=rating, sentiment=s["sentiment"],
        sentiment_score=s["sentiment_score"],
        pos_score=s["pos"], neg_score=s["neg"],
        neu_score=s["neu"], compound_score=s["compound"],
    )

    return Response({
        "review": review,
        "drug_name": drug_name,
        "condition": condition,
        "sentiment": s["sentiment"],
        "sentiment_label": label_map[s["sentiment"]],
        "color": color_map[s["sentiment"]],
        "scores": {"positive":s["pos"],"negative":s["neg"],"neutral":s["neu"],"compound":s["compound"]},
        "sentiment_score_10": s["sentiment_score"],
        "interpretation": (
            f"The review conveys {'strong ' if abs(s['compound'])>0.6 else ''}{s['sentiment']} sentiment "
            f"(compound={s['compound']}). This contributes 30% weight to the drug's overall recommendation score."
        ),
    })


@api_view(["GET", "POST"])
def compare_drugs(request):
    """Compare two drugs for a condition."""
    _load()
    data      = request.data if request.method == "POST" else request.GET
    condition = data.get("condition","")
    drug_a    = data.get("drug_a","")
    drug_b    = data.get("drug_b","")
    if not all([condition, drug_a, drug_b]):
        return Response({"error":"condition, drug_a, drug_b required"},status=400)

    recs = {r["drugName"]:r for r in _cache.get("recs",{}).get(condition,[])}
    def _info(name):
        r = recs.get(name)
        if not r: return None
        db = DRUG_DATABASE.get(name, {})
        return {
            "drug":name,"avg_rating":round(r["avg_rating"],2),
            "sentiment":round(r["avg_sentiment"],2),"weighted":round(r["weighted_score"],2),
            "final":round(r["final_score"],2),"reviews":int(r["review_count"]),
            "drug_class": db.get("drug_class", ""),
            "generic_name": db.get("generic_name", name),
            "price_inr": db.get("price_inr", "N/A"),
            "pregnancy": db.get("pregnancy", "Consult doctor"),
            "prescription": db.get("prescription_required", True),
            "side_effects": db.get("side_effects", []),
            "kidney_warning": db.get("kidney_warning", "Consult doctor"),
            "liver_warning": db.get("liver_warning", "Consult doctor"),
            "manufacturer": db.get("manufacturer", "Various"),
        }

    a, b = _info(drug_a), _info(drug_b)
    if not a or not b:
        return Response({"error":"Drug not found for this condition"},status=404)

    winner = drug_a if a["final"]>=b["final"] else drug_b
    DrugComparison.objects.create(condition=condition,drug_a=drug_a,drug_b=drug_b,winner=winner)

    def _normalise(d):
        return {
            "drug_name": d["drug"],
            "generic_name": d["generic_name"],
            "drug_class": d["drug_class"],
            "avg_rating": d["avg_rating"],
            "sentiment_score": d["sentiment"],
            "weighted_score": d["weighted"],
            "final_score": d["final"],
            "review_count": d["reviews"],
            "price_inr": d["price_inr"],
            "pregnancy": d["pregnancy"],
            "prescription_required": d["prescription"],
            "side_effects": d["side_effects"][:4],
            "kidney_warning": d["kidney_warning"],
            "liver_warning": d["liver_warning"],
            "manufacturer": d["manufacturer"],
            "recommendation_strength": (
                "Highly Recommended" if d["final"] >= 8
                else "Recommended" if d["final"] >= 6
                else "Moderately Recommended"
            ),
        }
    return Response({"condition":condition,"drug_a":_normalise(a),"drug_b":_normalise(b),
                     "winner":winner,"margin":round(abs(a["final"]-b["final"]),2)})


@api_view(["GET"])
def dashboard(request):
    """Comprehensive dashboard stats."""
    _load()
    total_reviews    = DrugReview.objects.count()
    total_preds      = Prediction.objects.count()
    pos_count        = DrugReview.objects.filter(sentiment="positive").count()
    neg_count        = DrugReview.objects.filter(sentiment="negative").count()
    neu_count        = DrugReview.objects.filter(sentiment="neutral").count()

    top_conditions = (Prediction.objects.values("predicted_condition")
                      .annotate(count=Count("id")).order_by("-count")[:5])

    acc = {k.replace("_"," ").title():round(v*100,1) for k,v in _cache.get("results",{}).items()}

    top_drugs = []
    for cond, recs in list(_cache.get("recs",{}).items())[:8]:
        if recs:
            top_drugs.append({"condition":cond,"drug":recs[0]["drugName"],"score":round(recs[0]["final_score"],2)})

    labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    trend_data = list(_cache.get("trends",{}).values())[:3]
    while len(trend_data)<3: trend_data.append([7]*12)

    total_comparisons = DrugComparison.objects.count()
    total_interactions = DrugInteractionCheck.objects.count()

    return Response({
        "total_reviews": total_reviews,
        "total_predictions": total_preds,
        "total_comparisons": total_comparisons,
        "total_interaction_checks": total_interactions,
        "conditions_supported": len(_cache.get("syms",{})),
        "models_available": len([k for k in ["nb","rf","svm","lr"] if k in _cache]),
        "drug_database_size": len(DRUG_DATABASE),
        "sentiment_distribution": {"positive":pos_count,"neutral":neu_count,"negative":neg_count},
        "top_predicted_conditions": list(top_conditions),
        "model_accuracies": acc,
        "top_drugs_by_condition": top_drugs,
        "trend_months": labels,
        "trend_series": trend_data[:3],
    })


@api_view(["GET"])
def recent_reviews(request):
    reviews = DrugReview.objects.all()[:10]
    data = [{"id":r.id,"drug":r.drug_name,"condition":r.condition,"rating":r.rating,
             "sentiment":r.sentiment,"score":r.compound_score,"date":r.created_at.strftime("%b %d, %Y")}
            for r in reviews]
    return Response({"reviews":data,"total":DrugReview.objects.count()})


@api_view(["GET"])
def recent_predictions(request):
    preds = Prediction.objects.all()[:10]
    data = [{"id":p.id,"condition":p.predicted_condition,"symptoms":p.symptoms[:60]+"…",
             "date":p.created_at.strftime("%b %d, %Y")} for p in preds]
    return Response({"predictions":data,"total":Prediction.objects.count()})


@api_view(["GET"])
def drug_detail(request):
    """Get detailed info for a specific drug across all reviews."""
    drug = request.GET.get("drug","")
    if not drug:
        return Response({"error":"drug required"},status=400)
    reviews = DrugReview.objects.filter(drug_name__iexact=drug)
    agg = reviews.aggregate(avg_rating=Avg("rating"),avg_compound=Avg("compound_score"),count=Count("id"))
    recent = [{"review":r.review[:120],"rating":r.rating,"sentiment":r.sentiment}
              for r in reviews[:5]]
    return Response({"drug":drug,"total_reviews":agg["count"],"avg_rating":round(agg["avg_rating"] or 0,2),
                     "avg_compound":round(agg["avg_compound"] or 0,3),"recent_reviews":recent})


@api_view(["GET"])
def drug_report(request):
    """
    Generate a comprehensive drug report for ANY searchable drug.
    Every response contains a fully populated set of fields — if a drug
    isn't in the hand-curated database (shouldn't happen for the 58 drugs
    IDPDR knows about, but this keeps the endpoint robust for any future
    drug added to the review dataset), a complete fallback profile is built
    instead of returning a partial/blank report.
    """
    drug_name = request.GET.get("drug", "").strip()
    if not drug_name:
        return Response({"error": "drug name required"}, status=400)

    # Log the search
    SearchLog.objects.create(query=drug_name, search_type="drug_report")

    # Case-insensitive lookup: admin-managed entries take precedence over
    # the curated, code-based database (lets an admin override/correct a
    # built-in entry from the Admin Dashboard).
    managed = Drug.objects.filter(name__iexact=drug_name, is_active=True).first()
    if managed:
        canonical_name, drug_info = managed.name, managed.as_dict()
    else:
        canonical_name, drug_info = get_drug_info(drug_name)

    _load()
    reviews = DrugReview.objects.filter(drug_name__iexact=drug_name)
    agg = reviews.aggregate(avg_rating=Avg("rating"), count=Count("id"), avg_compound=Avg("compound_score"))

    if not drug_info:
        # Not in the curated database — build a complete, non-blank fallback
        # profile instead of a partial/blank report.
        condition = reviews.first().condition if reviews.exists() else None
        drug_info = build_fallback_profile(drug_name, condition=condition)
        canonical_name = drug_name
        found_in_database = False
    else:
        found_in_database = True
        drug_name = canonical_name

    return Response({
        "drug_name": drug_name,
        "found_in_database": found_in_database,
        "generic_name": drug_info.get("generic_name"),
        "brand_names": drug_info.get("brand_names", []),
        "drug_class": drug_info.get("drug_class"),
        "description": drug_info.get("description"),
        "uses": drug_info.get("uses", []),
        "dosage": drug_info.get("dosage", {}),
        "side_effects": drug_info.get("side_effects", []),
        "contraindications": drug_info.get("contraindications", []),
        "drug_interactions": drug_info.get("drug_interactions", []),
        "food_interactions": drug_info.get("food_interactions", []),
        "pregnancy_safety": drug_info.get("pregnancy"),
        "breastfeeding_safety": drug_info.get("breastfeeding"),
        "kidney_warning": drug_info.get("kidney_warning"),
        "liver_warning": drug_info.get("liver_warning"),
        "storage_instructions": drug_info.get("storage"),
        "overdose_information": drug_info.get("overdose"),
        "missed_dose_instructions": drug_info.get("missed_dose"),
        "alternatives": drug_info.get("alternatives", []),
        "price_estimate": drug_info.get("price_inr"),
        "availability": drug_info.get("availability"),
        "manufacturer": drug_info.get("manufacturer"),
        "prescription_required": drug_info.get("prescription_required", True),
        "condition": drug_info.get("condition"),
        "review_data": {
            "total_reviews": agg["count"] or 0,
            "avg_rating": round(agg["avg_rating"] or 0, 2),
            "avg_sentiment": round(agg["avg_compound"] or 0, 3),
        },
        "disclaimer": "⚠️ This information is for educational purposes only and should not replace professional medical advice. Always consult a qualified healthcare provider before making any medication decisions.",
    })


@api_view(["GET"])
def drug_search(request):
    """
    Search for drugs by name, generic name, brand name, or condition.
    - Partial keyword search (substring match, not exact-match-only)
    - Case-insensitive (all comparisons are done in lowercase)
    - Generic name and brand name are both searched, in addition to the
      primary drug name
    - Empty query ("browse all") returns every drug in the database so the
      Search Drug module can list/browse the full catalogue, not just the
      top handful of results
    """
    query = request.GET.get("q", "").strip()
    limit_param = request.GET.get("limit", "").strip()
    try:
        limit = max(1, min(int(limit_param), 200)) if limit_param else 50
    except ValueError:
        limit = 50

    SearchLog.objects.create(query=query or "(browse all)", search_type="drug_search")

    q = query.lower()
    results = []
    all_drugs = _merged_drug_database()

    # Search across the full, consolidated drug database (every drug the
    # system knows about — 58+ built-in drugs plus any admin-managed
    # entries — covering all drugs used by the recommendation model).
    for drug_name, info in all_drugs.items():
        score = 0
        if not q:
            score = 1  # browse-all mode: include every drug
        else:
            name_l = drug_name.lower()
            generic_l = info.get("generic_name", "").lower()
            condition_l = info.get("condition", "").lower()
            brands_l = [b.lower() for b in info.get("brand_names", [])]

            if q == name_l:
                score += 5
            elif name_l.startswith(q):
                score += 4
            elif q in name_l:
                score += 3

            if q in generic_l:
                score += 2
            for brand in brands_l:
                if q in brand:
                    score += 2
                    break
            if q in condition_l:
                score += 1

        if score > 0:
            results.append({
                "drug_name": drug_name,
                "generic_name": info.get("generic_name"),
                "brand_names": info.get("brand_names", []),
                "drug_class": info.get("drug_class"),
                "condition": info.get("condition"),
                "price_inr": info.get("price_inr"),
                "prescription_required": info.get("prescription_required"),
                "relevance_score": score,
            })

    results.sort(key=lambda x: -x.get("relevance_score", 0))
    return Response({
        "query": query,
        "results": results[:limit],
        "total": len(results),
        "database_size": len(all_drugs),
    })


@api_view(["POST"])
def check_interactions(request):
    """Check drug interactions between multiple drugs."""
    drugs = request.data.get("drugs", [])
    if not drugs or len(drugs) < 2:
        return Response({"error": "At least 2 drugs required"}, status=400)

    interactions_found = []
    checked_pairs = set()

    for i, drug1 in enumerate(drugs):
        for drug2 in drugs[i+1:]:
            pair = tuple(sorted([drug1, drug2]))
            if pair in checked_pairs:
                continue
            checked_pairs.add(pair)

            # Check both orderings
            interaction = (DRUG_INTERACTIONS.get((drug1, drug2)) or
                          DRUG_INTERACTIONS.get((drug2, drug1)))

            if interaction:
                interactions_found.append({
                    "drug1": drug1,
                    "drug2": drug2,
                    "severity": interaction["severity"],
                    "description": interaction["description"],
                    "recommendation": interaction["recommendation"],
                    "color": {"major": "#ef4444", "moderate": "#f59e0b", "minor": "#10b981"}.get(interaction["severity"], "#94a3b8"),
                })

    # Log the check
    severity_levels = [i["severity"] for i in interactions_found]
    top_severity = "major" if "major" in severity_levels else ("moderate" if "moderate" in severity_levels else ("minor" if "minor" in severity_levels else "none"))

    DrugInteractionCheck.objects.create(
        drugs_checked=json.dumps(drugs),
        interactions_found=len(interactions_found),
        severity=top_severity,
    )

    # Sort by severity
    severity_order = {"major": 0, "moderate": 1, "minor": 2}
    interactions_found.sort(key=lambda x: severity_order.get(x["severity"], 3))

    return Response({
        "drugs_checked": drugs,
        "interactions": interactions_found,
        "total_interactions": len(interactions_found),
        "has_major": any(i["severity"] == "major" for i in interactions_found),
        "summary": (
            f"Found {len(interactions_found)} interaction(s) — "
            f"{sum(1 for i in interactions_found if i['severity']=='major')} major, "
            f"{sum(1 for i in interactions_found if i['severity']=='moderate')} moderate, "
            f"{sum(1 for i in interactions_found if i['severity']=='minor')} minor"
        ),
        "disclaimer": "⚠️ This tool is for educational purposes only. Always consult a pharmacist or doctor before combining medications.",
    })


@api_view(["GET"])
def disease_info(request):
    """Get comprehensive information about a disease/condition."""
    condition = request.GET.get("condition", "").strip()
    if not condition:
        return Response({"conditions": list(DISEASE_DATABASE.keys())})

    info = DISEASE_DATABASE.get(condition)
    if not info:
        # Fuzzy search
        matches = [c for c in DISEASE_DATABASE if condition.lower() in c.lower()]
        if matches:
            return Response({"suggestions": matches, "error": f"Exact condition not found. Did you mean: {', '.join(matches)}"}, status=404)
        return Response({"error": f"Condition '{condition}' not found"}, status=404)

    _load()
    # Get drug recommendations for this condition
    recs = _cache.get("recs", {}).get(condition, [])
    top_drugs = [r["drugName"] for r in recs[:3]]

    return Response({
        "condition": condition,
        "description": info["description"],
        "symptoms": info["symptoms"],
        "causes": info["causes"],
        "risk_factors": info["risk_factors"],
        "diagnosis": info["diagnosis"],
        "treatment": info["treatment"],
        "lifestyle_changes": info["lifestyle"],
        "prevention": info["prevention"],
        "emergency_warning_signs": info["emergency_signs"],
        "related_medicines": info["related_medicines"],
        "top_recommended_drugs": top_drugs,
        "disclaimer": "⚠️ This information is for educational purposes. Seek professional medical care for diagnosis and treatment.",
    })


@api_view(["POST"])
def symptom_recommend(request):
    """Smart drug recommendation based on symptoms + patient profile."""
    _load()
    symptoms = request.data.get("symptoms", "").strip()
    age = request.data.get("age")
    gender = request.data.get("gender", "")
    allergies = request.data.get("allergies", [])

    if not symptoms:
        return Response({"error": "Symptoms required"}, status=400)

    # First predict condition
    predictions = {}
    for name, key in [("Naive Bayes","nb"),("Random Forest","rf"),("SVM","svm"),("Logistic Regression","lr")]:
        if key in _cache:
            try:
                cond, conf = _predict_one(_cache[key], symptoms)
                predictions[name] = {"condition": cond, "confidence": conf}
            except:
                pass

    conditions = [v["condition"] for v in predictions.values() if v["condition"] != "Error"]
    majority = Counter(conditions).most_common(1)[0][0] if conditions else None

    if not majority:
        return Response({"error": "Could not determine condition from symptoms"}, status=400)

    # Get recommendations
    recs = _cache.get("recs", {}).get(majority, [])

    # Filter by allergies (basic)
    filtered_recs = [r for r in recs if r["drugName"] not in allergies]

    # Build recommendation list
    recommendations = []
    for i, r in enumerate(filtered_recs[:5], 1):
        drug_info = DRUG_DATABASE.get(r["drugName"], {})
        recommendations.append({
            "rank": i,
            "drug_name": r["drugName"],
            "generic_name": drug_info.get("generic_name", r["drugName"]),
            "drug_class": drug_info.get("drug_class", ""),
            "final_score": round(r["final_score"], 2),
            "avg_rating": round(r["avg_rating"], 2),
            "review_count": int(r["review_count"]),
            "choice_label": "First Choice" if i == 1 else "Alternative" if i <= 3 else "Second-Line",
            "confidence": min(round(r["final_score"] / 10 * 100), 95),
            "prescription_required": drug_info.get("prescription_required", True),
            "price_inr": drug_info.get("price_inr", "Consult pharmacist"),
            "notes": drug_info.get("description", "")[:100] + "..." if drug_info.get("description") else "",
        })

    # Age-specific notes
    age_notes = []
    if age:
        age = int(age)
        if age < 18:
            age_notes.append("Pediatric dosing required — consult pediatrician")
        if age > 65:
            age_notes.append("Geriatric patients may need dose adjustment and closer monitoring")

    return Response({
        "input_symptoms": symptoms,
        "predicted_condition": majority,
        "confidence": round(Counter(conditions).most_common(1)[0][1] / len(conditions) * 100, 0) if conditions else 0,
        "recommendations": recommendations,
        "age_notes": age_notes,
        "allergies_excluded": allergies,
        "disclaimer": "⚠️ This AI recommendation is for educational purposes ONLY. Consult a qualified doctor or pharmacist before taking any medication.",
        "medical_advice": "Always seek professional medical advice. Self-medication can be dangerous."
    })


@api_view(["GET"])
def where_to_buy(request):
    """Medicine availability and purchase information."""
    drug_name = request.GET.get("drug", "").strip()
    if not drug_name:
        return Response({"error": "drug name required"}, status=400)

    drug_info = DRUG_DATABASE.get(drug_name, {})

    online_options = [
        {
            "platform": "1mg (Tata Health)",
            "url": f"https://www.1mg.com/search/all?name={drug_name.replace(' ','+')}",
            "note": "Compare prices from multiple sellers"
        },
        {
            "platform": "PharmEasy",
            "url": f"https://pharmeasy.in/search/all?name={drug_name.replace(' ','+')}",
            "note": "Fast delivery in major cities"
        },
        {
            "platform": "Netmeds",
            "url": f"https://www.netmeds.com/catalogsearch/result?q={drug_name.replace(' ','+')}",
            "note": "Genuine medicines from licensed pharmacies"
        },
    ]

    return Response({
        "drug_name": drug_name,
        "prescription_required": drug_info.get("prescription_required", True),
        "estimated_price": drug_info.get("price_inr", "Consult pharmacist"),
        "availability": drug_info.get("availability", "Available at licensed pharmacies"),
        "online_options": online_options,
        "offline_availability": "Available at local pharmacies and hospital dispensaries",
        "generic_alternatives": drug_info.get("alternatives", [])[:3],
        "important_notice": [
            "⚠️ Purchase medicines ONLY from licensed pharmacies (look for CDSCO-approved pharmacies)",
            "Always carry original prescription for Schedule H/H1 drugs",
            "Verify medicine authenticity using hologram/QR code on packaging",
            "Do not purchase from unlicensed online platforms",
            "Generic alternatives may be significantly cheaper — ask your pharmacist"
        ],
        "disclaimer": "IDPDR does not sell or facilitate the sale of medicines. The above links are for reference only. Always consult your doctor before purchasing prescription medicines."
    })


# ═══════════════════════════════════════════════════════════════
# DISEASE DIAGNOSIS REPORT MODULE
# ═══════════════════════════════════════════════════════════════
# Root cause of "diagnosis report not generated": (1) DISEASE_DATABASE only
# covered 6 of the 12 predictable conditions, so disease_summary/report
# content was silently empty for the other 6 (now fixed above — see
# DISEASE_DATABASE), and (2) there was no dedicated report model/endpoint
# at all — the UI only showed inline prediction results with no persisted,
# viewable/downloadable/printable report. Both are addressed below.

def _build_diagnosis_report_data(*, symptoms, condition, confidence, patient_name,
                                  patient_age, patient_gender, extra_notes=""):
    """Assemble the full, structured content of a Disease Diagnosis Report."""
    _load()
    disease_info = DISEASE_DATABASE.get(condition, {})

    recommended_drugs = []
    recs = _cache.get("recs", {}).get(condition, [])
    for r in recs[:5]:
        info = DRUG_DATABASE.get(r["drugName"], {})
        recommended_drugs.append({
            "drug_name": r["drugName"],
            "generic_name": info.get("generic_name", r["drugName"]),
            "dosage": info.get("dosage", {}),
            "avg_rating": round(r.get("avg_rating", 0), 2) if r.get("avg_rating") is not None else None,
        })
    if not recommended_drugs:
        for name in disease_info.get("related_medicines", [])[:5]:
            info = DRUG_DATABASE.get(name, {})
            recommended_drugs.append({
                "drug_name": name,
                "generic_name": info.get("generic_name", name),
                "dosage": info.get("dosage", {}),
                "avg_rating": None,
            })

    recommended_tests = disease_info.get("diagnosis", []) or ["Clinical evaluation by a licensed physician"]
    precautions = list(disease_info.get("emergency_signs", []) or []) + list(disease_info.get("prevention", []) or [])
    if not precautions:
        precautions = ["Consult a licensed physician for a full evaluation and personalized precautions."]
    lifestyle = disease_info.get("lifestyle", []) or ["Follow general healthy lifestyle guidance and consult a physician for tailored advice."]

    notes = (
        "This report was generated by an AI-assisted recommendation system and is intended "
        "for informational purposes only. It does not constitute a medical diagnosis. "
        "Please consult a licensed physician for confirmation and treatment."
    )
    if extra_notes:
        notes = f"{notes}\n\nAdditional notes: {extra_notes}"

    return {
        "patient_name": patient_name or "Guest Patient",
        "patient_age": patient_age,
        "patient_gender": patient_gender or "",
        "symptoms": symptoms,
        "predicted_disease": condition,
        "disease_description": disease_info.get("description", ""),
        "confidence_score": confidence,
        "recommended_drugs": recommended_drugs,
        "recommended_tests": recommended_tests,
        "precautions": precautions,
        "lifestyle_recommendations": lifestyle,
        "doctor_notes": notes,
    }


def _serialize_report(report):
    return {
        "id": report.id,
        "patient_name": report.patient_name,
        "patient_age": report.patient_age,
        "patient_gender": report.patient_gender,
        "symptoms": report.symptoms,
        "predicted_disease": report.predicted_disease,
        "disease_description": DISEASE_DATABASE.get(report.predicted_disease, {}).get("description", ""),
        "confidence_score": report.confidence_score,
        "recommended_drugs": report.recommended_drugs,
        "recommended_tests": report.recommended_tests,
        "precautions": report.precautions,
        "lifestyle_recommendations": report.lifestyle_recommendations,
        "doctor_notes": report.doctor_notes,
        "generated_at": report.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "date": report.created_at.strftime("%B %d, %Y"),
        "time": report.created_at.strftime("%I:%M %p"),
        "pdf_url": f"/api/diagnosis/report/{report.id}/pdf/",
    }


@api_view(["POST"])
def diagnosis_report_create(request):
    """
    Generate (and persist) a complete Disease Diagnosis Report.
    Accepts EITHER:
      - {"prediction_id": <id>} to build the report from a previous /predict/ result, or
      - {"symptoms": "...", "condition": "..."} to build one directly.
    Optional patient info: patient_name, patient_age, patient_gender, notes.
    """
    data = request.data
    prediction_id = data.get("prediction_id")
    patient_name = (data.get("patient_name") or "").strip()
    patient_gender = (data.get("patient_gender") or "").strip()
    extra_notes = (data.get("notes") or "").strip()
    try:
        patient_age = int(data.get("patient_age")) if data.get("patient_age") not in (None, "") else None
    except (TypeError, ValueError):
        patient_age = None

    prediction_obj = None
    if prediction_id:
        prediction_obj = Prediction.objects.filter(id=prediction_id).first()
        if not prediction_obj:
            return Response({"error": f"Prediction {prediction_id} not found"}, status=404)
        symptoms = prediction_obj.symptoms
        condition = prediction_obj.predicted_condition
        confs = [prediction_obj.nb_confidence, prediction_obj.rf_confidence,
                 prediction_obj.svm_confidence, prediction_obj.lr_confidence]
        confs = [c for c in confs if c]
        confidence = round(sum(confs) / len(confs), 1) if confs else None
    else:
        symptoms = (data.get("symptoms") or "").strip()
        condition = (data.get("condition") or "").strip()
        confidence = data.get("confidence")
        if not symptoms or not condition:
            return Response({"error": "Either prediction_id, or both symptoms and condition, are required"}, status=400)

    if not patient_name:
        patient_name = (request.user.get_full_name() or request.user.username) if request.user.is_authenticated else "Guest Patient"
    profile = getattr(request.user, "profile", None) if request.user.is_authenticated else None
    if patient_age is None and profile:
        patient_age = profile.age
    if not patient_gender and profile:
        patient_gender = profile.gender

    payload = _build_diagnosis_report_data(
        symptoms=symptoms, condition=condition, confidence=confidence,
        patient_name=patient_name, patient_age=patient_age, patient_gender=patient_gender,
        extra_notes=extra_notes,
    )

    report = DiagnosisReport.objects.create(
        user=request.user if request.user.is_authenticated else None,
        prediction=prediction_obj,
        patient_name=payload["patient_name"],
        patient_age=payload["patient_age"],
        patient_gender=payload["patient_gender"],
        symptoms=payload["symptoms"],
        predicted_disease=payload["predicted_disease"],
        confidence_score=payload["confidence_score"],
        recommended_drugs=payload["recommended_drugs"],
        recommended_tests=payload["recommended_tests"],
        precautions=payload["precautions"],
        lifestyle_recommendations=payload["lifestyle_recommendations"],
        doctor_notes=payload["doctor_notes"],
    )

    return Response(_serialize_report(report), status=201)


@api_view(["GET"])
def diagnosis_report_list(request):
    """List the signed-in user's saved diagnosis reports."""
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required"}, status=401)
    reports = DiagnosisReport.objects.filter(user=request.user)[:50]
    return Response({"reports": [
        {"id": r.id, "predicted_disease": r.predicted_disease, "patient_name": r.patient_name,
         "confidence_score": r.confidence_score, "created_at": r.created_at.strftime("%b %d, %Y %I:%M %p")}
        for r in reports
    ]})


@api_view(["GET"])
def diagnosis_report_detail(request, report_id):
    """Retrieve a single saved diagnosis report as JSON (for the 'view' action)."""
    report = DiagnosisReport.objects.filter(id=report_id).first()
    if not report:
        return Response({"error": "Report not found"}, status=404)
    if report.user_id and (not request.user.is_authenticated or report.user_id != request.user.id) and not request.user.is_staff:
        return Response({"error": "You do not have permission to view this report"}, status=403)
    return Response(_serialize_report(report))


@api_view(["GET"])
def diagnosis_report_pdf(request, report_id):
    """Render a saved diagnosis report as a downloadable / printable PDF."""
    report = DiagnosisReport.objects.filter(id=report_id).first()
    if not report:
        return Response({"error": "Report not found"}, status=404)
    if report.user_id and (not request.user.is_authenticated or report.user_id != request.user.id) and not request.user.is_staff:
        return Response({"error": "You do not have permission to view this report"}, status=403)

    meta_rows = [
        ("Patient Name", report.patient_name),
        ("Age", report.patient_age if report.patient_age else "Not specified"),
        ("Gender", report.patient_gender or "Not specified"),
        ("Date & Time", report.created_at.strftime("%B %d, %Y at %I:%M %p")),
    ]

    drugs_content = [
        f"{d.get('drug_name')} ({d.get('generic_name', '')}) — {d.get('dosage', {}).get('adult', 'See prescribing information')}"
        for d in (report.recommended_drugs or [])
    ] or ["Consult a physician for medication recommendations."]

    confidence_str = f"  (Confidence: {report.confidence_score}%)" if report.confidence_score else ""
    sections = [
        ("Symptoms Reported", report.symptoms or "Not specified"),
        (f"Predicted Disease: {report.predicted_disease}{confidence_str}",
         DISEASE_DATABASE.get(report.predicted_disease, {}).get("description", "")),
        ("Recommended Drugs", drugs_content),
        ("Recommended Tests", report.recommended_tests or ["Consult a physician."]),
        ("Precautions", report.precautions or ["Consult a physician."]),
        ("Lifestyle Recommendations", report.lifestyle_recommendations or ["Consult a physician."]),
        ("Doctor / System Notes", report.doctor_notes),
    ]

    pdf_bytes = build_pdf(
        title="IDPDR — Disease Diagnosis Report",
        subtitle=f"Report #{report.id} - Generated {report.created_at.strftime('%B %d, %Y %I:%M %p')}",
        meta_rows=meta_rows,
        sections=sections,
        disclaimer=("This report is generated by an AI-assisted recommendation system for informational "
                    "purposes only. It is NOT a substitute for professional medical diagnosis or treatment. "
                    "Always consult a licensed physician."),
    )

    disposition = "attachment" if request.GET.get("download") else "inline"
    resp = HttpResponse(pdf_bytes, content_type="application/pdf")
    resp["Content-Disposition"] = f'{disposition}; filename="diagnosis_report_{report.id}.pdf"'
    return resp


@api_view(["GET"])
def drug_report_pdf(request):
    """Render a Drug Report as a downloadable / printable PDF (mirrors drug_report())."""
    drug_name = request.GET.get("drug", "").strip()
    if not drug_name:
        return Response({"error": "drug name required"}, status=400)

    managed = Drug.objects.filter(name__iexact=drug_name, is_active=True).first()
    if managed:
        canonical_name, drug_info = managed.name, managed.as_dict()
    else:
        canonical_name, drug_info = get_drug_info(drug_name)
    if not drug_info:
        _load()
        reviews = DrugReview.objects.filter(drug_name__iexact=drug_name)
        condition = reviews.first().condition if reviews.exists() else None
        drug_info = build_fallback_profile(drug_name, condition=condition)
        canonical_name = drug_name

    meta_rows = [
        ("Generic Name", drug_info.get("generic_name")),
        ("Brand Names", ", ".join(drug_info.get("brand_names", [])) or "N/A"),
        ("Drug Class", drug_info.get("drug_class")),
        ("Condition", drug_info.get("condition")),
    ]
    sections = [
        ("Description", drug_info.get("description", "")),
        ("Uses / Indications", drug_info.get("uses", [])),
        ("Dosage", drug_info.get("dosage", {})),
        ("Side Effects", drug_info.get("side_effects", [])),
        ("Contraindications", drug_info.get("contraindications", [])),
        ("Drug Interactions", drug_info.get("drug_interactions", [])),
        ("Food Interactions", drug_info.get("food_interactions", [])),
        ("Pregnancy / Breastfeeding", {
            "Pregnancy": drug_info.get("pregnancy", ""),
            "Breastfeeding": drug_info.get("breastfeeding", ""),
        }),
        ("Kidney / Liver Warnings", {
            "Kidney": drug_info.get("kidney_warning", ""),
            "Liver": drug_info.get("liver_warning", ""),
        }),
        ("Storage Information", drug_info.get("storage", "")),
        ("Overdose Information", drug_info.get("overdose", "")),
        ("Missed Dose Instructions", drug_info.get("missed_dose", "")),
        ("Alternatives", drug_info.get("alternatives", [])),
    ]

    pdf_bytes = build_pdf(
        title=f"IDPDR — Drug Report: {canonical_name}",
        subtitle=f"Generated {timezone.now().strftime('%B %d, %Y %I:%M %p')}",
        meta_rows=meta_rows,
        sections=sections,
        disclaimer=("This information is for educational purposes only and should not replace "
                    "professional medical advice. Always consult a qualified healthcare provider."),
    )

    disposition = "attachment" if request.GET.get("download") else "inline"
    resp = HttpResponse(pdf_bytes, content_type="application/pdf")
    resp["Content-Disposition"] = f'{disposition}; filename="drug_report_{canonical_name}.pdf"'
    return resp
