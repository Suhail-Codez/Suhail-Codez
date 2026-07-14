import pandas as pd, numpy as np, random, json, os, joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk, re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import warnings; warnings.filterwarnings("ignore")

random.seed(42); np.random.seed(42)
OUT = "/home/claude/medirec_v2/models_pkl"
os.makedirs(OUT, exist_ok=True)

# ── Condition data ──────────────────────────────────────────
condition_phrases = {
    "Diabetes Type 2":   ["frequent urination high blood sugar thirst insulin resistance glucose management","blood glucose control diabetes medication hyperglycemia fatigue weight management","sugar levels stabilized diabetes treatment glycated hemoglobin HbA1c control"],
    "Hypertension":      ["high blood pressure headache dizziness antihypertensive","systolic diastolic pressure management hypertension bp reduction","cardiovascular pressure heart rate blood pressure medication"],
    "Depression":        ["sadness hopeless mood antidepressant serotonin","persistent low mood anxiety depression mental health","depressive episode treatment medication mood stabilizer"],
    "Anxiety":           ["anxiety panic attack worry restless nervous","anxious overthinking stress generalized anxiety disorder","nervousness tension panic medication anxiety relief"],
    "Asthma":            ["wheezing shortness breath inhaler bronchospasm airway","respiratory bronchodilator breathing difficulty asthma attack","breathing problem airway inflammation asthma medication"],
    "Migraine":          ["severe headache throbbing migraine aura nausea light sensitivity","migraine attack pain relief cluster headache","pulsating head pain migraine medication sound sensitivity"],
    "GERD":              ["heartburn acid reflux stomach burning gastroesophageal","stomach acid regurgitation throat burn esophagus proton pump","acid indigestion heartburn relief antacid medication"],
    "Hypothyroidism":    ["thyroid fatigue weight gain cold sensitivity underactive","thyroid hormone replacement metabolism slow levothyroxine TSH","hypothyroid medication energy cold intolerance thyroid function"],
    "Insomnia":          ["sleep insomnia waking night trouble falling asleep","sleep disorder medication sedative sleep quality","insomnia sleep disturbance treatment sleep aid"],
    "Pain":              ["pain relief inflammation painkiller analgesic treatment","chronic pain NSAID anti-inflammatory joint muscle pain","arthritis pain swelling relief pain management"],
    "Infection":         ["bacterial infection antibiotic fever chills body ache","infection treatment antibiotic course antimicrobial","fever body ache infection clearing antibiotic"],
    "High Cholesterol":  ["high cholesterol LDL statin cardiovascular lipid","cholesterol reduction hypercholesterolemia HDL triglycerides","lipid lowering medication heart risk cholesterol management"],
}
conditions_drugs = {
    "Diabetes Type 2":   ["Metformin","Glipizide","Januvia","Jardiance","Ozempic"],
    "Hypertension":      ["Lisinopril","Amlodipine","Losartan","Metoprolol","Hydrochlorothiazide"],
    "Depression":        ["Sertraline","Fluoxetine","Escitalopram","Bupropion","Venlafaxine"],
    "Anxiety":           ["Alprazolam","Buspirone","Clonazepam","Lorazepam","Escitalopram"],
    "Asthma":            ["Albuterol","Fluticasone","Montelukast","Budesonide","Salmeterol"],
    "Migraine":          ["Sumatriptan","Topiramate","Propranolol","Amitriptyline","Rizatriptan"],
    "GERD":              ["Omeprazole","Pantoprazole","Ranitidine","Lansoprazole","Esomeprazole"],
    "Hypothyroidism":    ["Levothyroxine","Liothyronine","Armour Thyroid"],
    "Insomnia":          ["Zolpidem","Trazodone","Melatonin","Eszopiclone","Doxepin"],
    "Pain":              ["Ibuprofen","Naproxen","Acetaminophen","Tramadol","Celecoxib"],
    "Infection":         ["Amoxicillin","Azithromycin","Ciprofloxacin","Doxycycline","Cephalexin"],
    "High Cholesterol":  ["Atorvastatin","Rosuvastatin","Simvastatin","Pravastatin","Ezetimibe"],
}
symptoms_map = {
    "Diabetes Type 2":   ["frequent urination","increased thirst","fatigue","blurred vision","slow healing wounds","unexplained weight loss"],
    "Hypertension":      ["headache","dizziness","chest pain","shortness of breath","nosebleed","vision changes"],
    "Depression":        ["persistent sadness","loss of interest","fatigue","sleep problems","difficulty concentrating","hopelessness"],
    "Anxiety":           ["excessive worry","restlessness","rapid heartbeat","sweating","trembling","difficulty breathing"],
    "Asthma":            ["wheezing","coughing","chest tightness","shortness of breath","difficulty breathing","night cough"],
    "Migraine":          ["severe headache","nausea","light sensitivity","sound sensitivity","visual disturbances","throbbing pain"],
    "GERD":              ["heartburn","chest pain","regurgitation","difficulty swallowing","sour taste","chronic cough"],
    "Hypothyroidism":    ["fatigue","weight gain","cold sensitivity","constipation","dry skin","hair loss"],
    "Insomnia":          ["trouble falling asleep","waking during night","fatigue","irritability","difficulty concentrating","daytime sleepiness"],
    "Pain":              ["localized pain","swelling","tenderness","inflammation","limited mobility","joint stiffness"],
    "Infection":         ["fever","chills","fatigue","body aches","redness and swelling","pus or discharge"],
    "High Cholesterol":  ["chest pain","fatigue","yellowish skin patches","shortness of breath","numbness in limbs"],
}
pos = ["great effective works well improved better excellent highly recommend","amazing results works perfectly symptoms gone life changing","fantastic medication excellent results quick relief","very effective notable improvement highly satisfied"]
neu = ["okay moderate average side effects tolerable mixed results","works somewhat decent average improvement moderate results","acceptable results some side effects overall manageable"]
neg = ["did not work side effects severe bad ineffective poor","terrible side effects worsened no improvement not recommended","severe reaction stopped using poor results disappointing"]

records = []
for _ in range(9000):
    cond = random.choice(list(conditions_drugs.keys()))
    drug = random.choice(conditions_drugs[cond])
    rating = random.choices(range(1,11), weights=[2,3,4,6,8,10,12,20,20,15])[0]
    phrase = random.choice(condition_phrases[cond])
    if rating>=8: tail=random.choice(pos); sentiment="positive"
    elif rating>=5: tail=random.choice(neu); sentiment="neutral"
    else: tail=random.choice(neg); sentiment="negative"
    records.append({"drugName":drug,"condition":cond,"review":phrase+" "+tail,
                     "rating":rating,"usefulCount":random.randint(0,500),"sentiment":sentiment})

df = pd.DataFrame(records)
df.to_csv("/home/claude/medirec_v2/data/drug_reviews.csv", index=False)
with open("/home/claude/medirec_v2/data/symptoms_map.json","w") as f: json.dump(symptoms_map,f,indent=2)
print(f"Dataset: {len(df)} records")

# ── Preprocessing ───────────────────────────────────────────
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
def preprocess(text):
    text = re.sub(r"[^a-z\s]"," ",str(text).lower())
    return " ".join(lemmatizer.lemmatize(t) for t in text.split() if t not in stop_words and len(t)>2)

df["clean"] = df["review"].apply(preprocess)
le = LabelEncoder(); df["label"] = le.fit_transform(df["condition"])
joblib.dump(le, f"{OUT}/label_encoder.pkl")

X_train,X_test,y_train,y_test = train_test_split(df["clean"],df["label"],test_size=0.2,random_state=42)

# ── Train 4 models ──────────────────────────────────────────
models = {
    "naive_bayes": Pipeline([("tfidf",TfidfVectorizer(max_features=8000,ngram_range=(1,2))),("clf",MultinomialNB(alpha=0.1))]),
    "random_forest": Pipeline([("tfidf",TfidfVectorizer(max_features=8000,ngram_range=(1,2))),("clf",RandomForestClassifier(n_estimators=150,random_state=42,n_jobs=-1))]),
    "svm": Pipeline([("tfidf",TfidfVectorizer(max_features=8000,ngram_range=(1,2))),("clf",LinearSVC(max_iter=2000,C=1.0))]),
    "logistic_regression": Pipeline([("tfidf",TfidfVectorizer(max_features=8000,ngram_range=(1,2))),("clf",LogisticRegression(max_iter=1000,C=1.0,solver="lbfgs"))]),
}
results = {}
for name,pipe in models.items():
    pipe.fit(X_train,y_train)
    acc = accuracy_score(y_test,pipe.predict(X_test))
    results[name] = acc
    joblib.dump(pipe, f"{OUT}/{name}.pkl")
    print(f"  {name}: {acc:.4f}")

joblib.dump(SentimentIntensityAnalyzer(), f"{OUT}/vader.pkl")

# ── Drug scores ─────────────────────────────────────────────
analyser = SentimentIntensityAnalyzer()
df["sentiment_score"] = df["review"].apply(lambda t: (analyser.polarity_scores(t)["compound"]+1)*5)
df["weighted_score"] = 0.7*df["rating"] + 0.3*df["sentiment_score"]
C = df["rating"].mean(); m = 10
drug_scores = df.groupby(["condition","drugName"]).agg(
    avg_rating=("rating","mean"), avg_sentiment=("sentiment_score","mean"),
    weighted_score=("weighted_score","mean"), review_count=("review","count"),
    useful_count=("usefulCount","mean")).reset_index()
drug_scores["bayesian_score"] = (drug_scores["review_count"]*drug_scores["avg_rating"]+m*C)/(drug_scores["review_count"]+m)
drug_scores["final_score"] = (drug_scores["weighted_score"]+drug_scores["bayesian_score"])/2
drug_scores.to_csv(f"{OUT}/drug_scores.csv",index=False)

rec_dict = {}
for cond,grp in drug_scores.groupby("condition"):
    top = grp.nlargest(5,"final_score")
    rec_dict[cond] = top[["drugName","avg_rating","avg_sentiment","weighted_score","final_score","review_count"]].to_dict("records")
with open(f"{OUT}/recommendations.json","w") as f: json.dump(rec_dict,f,indent=2)
with open(f"{OUT}/model_results.json","w") as f: json.dump(results,f,indent=2)
with open(f"{OUT}/symptoms_map.json","w") as f: json.dump(symptoms_map,f,indent=2)

# Per-condition monthly trend (synthetic for charts)
trend = {}
for cond in conditions_drugs:
    trend[cond] = [round(random.uniform(6,9.5),2) for _ in range(12)]
with open(f"{OUT}/trends.json","w") as f: json.dump(trend,f,indent=2)

print("\nAll models saved!")
print(results)
