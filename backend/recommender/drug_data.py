"""
Comprehensive drug and disease knowledge base for IDPDR.
This module provides detailed drug information, disease data, interaction data,
and availability information for all modules.
"""

# ─── Drug Knowledge Base ──────────────────────────────────────────
DRUG_KNOWLEDGE = {
    "Lorazepam": {
        "generic_name": "Lorazepam",
        "brand_names": ["Ativan", "Loraz", "Temesta"],
        "drug_class": "Benzodiazepine / Anxiolytic",
        "description": "Lorazepam is a benzodiazepine medication used to treat anxiety disorders, insomnia, and seizures. It works by enhancing the activity of GABA, a neurotransmitter that inhibits brain activity.",
        "active_ingredients": ["Lorazepam"],
        "uses": ["Anxiety disorders", "Panic disorder", "Insomnia", "Seizure prevention", "Pre-operative sedation", "Alcohol withdrawal"],
        "dosage": {
            "adult": "0.5–2 mg orally 2–3 times daily",
            "elderly": "0.5–1 mg orally once or twice daily",
            "max_daily": "10 mg/day",
            "forms": ["Tablet (0.5mg, 1mg, 2mg)", "Oral solution (2mg/mL)", "Injection (2mg/mL, 4mg/mL)"]
        },
        "side_effects": {
            "common": ["Drowsiness", "Dizziness", "Weakness", "Unsteadiness", "Slurred speech", "Memory problems"],
            "serious": ["Respiratory depression", "Paradoxical reactions", "Severe sedation", "Dependence/addiction"],
            "rare": ["Severe allergic reactions", "Jaundice", "Blood disorders"]
        },
        "contraindications": ["Acute narrow-angle glaucoma", "Severe respiratory insufficiency", "Sleep apnea", "Myasthenia gravis"],
        "drug_interactions": ["CNS depressants (additive effect)", "Opioids (respiratory depression risk)", "Alcohol (enhanced sedation)", "Clozapine (respiratory depression)", "Valproic acid (increased lorazepam levels)"],
        "food_interactions": ["Avoid alcohol", "Grapefruit may increase levels"],
        "pregnancy_safety": "Category D — Evidence of fetal risk; use only if benefits outweigh risks",
        "breastfeeding": "Use with caution; excreted in breast milk",
        "kidney_warning": "Use with caution in renal impairment; dose adjustment may be needed",
        "liver_warning": "Use with caution in hepatic impairment; may accumulate",
        "storage": "Store at room temperature (15–30°C), away from moisture and heat. Keep out of reach of children.",
        "overdose": "Symptoms: extreme drowsiness, confusion, impaired coordination, slurred speech, coma. Treatment: Flumazenil (antidote), supportive care, activated charcoal if recent ingestion.",
        "missed_dose": "Take as soon as remembered. If close to next dose, skip. Never double dose.",
        "alternatives": ["Alprazolam (Xanax)", "Diazepam (Valium)", "Clonazepam (Klonopin)", "Buspirone (non-benzodiazepine)"],
        "price_estimate": "₹15–80 per tablet (generic); ₹100–300 per tablet (brand)",
        "availability": "Prescription required. Available at most pharmacies.",
        "manufacturer": "Various (Pfizer, Sun Pharma, Cipla, etc.)",
        "prescription_required": True,
        "controlled_substance": "Schedule IV",
        "pregnancy_category": "D"
    },
    "Metformin": {
        "generic_name": "Metformin Hydrochloride",
        "brand_names": ["Glucophage", "Glycomet", "Obimet", "Cetapin"],
        "drug_class": "Biguanide / Antidiabetic",
        "description": "Metformin is the first-line medication for type 2 diabetes. It reduces glucose production in the liver and improves insulin sensitivity without causing weight gain or hypoglycemia.",
        "active_ingredients": ["Metformin Hydrochloride"],
        "uses": ["Type 2 Diabetes Mellitus", "Prediabetes", "Polycystic Ovary Syndrome (PCOS)", "Metabolic syndrome"],
        "dosage": {
            "adult": "500mg twice daily with meals, increasing to 2000mg/day over several weeks",
            "elderly": "Start at lowest dose; maximum 1000mg/day",
            "max_daily": "2550 mg/day",
            "forms": ["Tablet (500mg, 850mg, 1000mg)", "Extended-release tablet", "Oral solution"]
        },
        "side_effects": {
            "common": ["Nausea", "Vomiting", "Diarrhea", "Stomach upset", "Metallic taste", "Loss of appetite"],
            "serious": ["Lactic acidosis (rare but serious)", "Vitamin B12 deficiency (long-term)"],
            "rare": ["Hepatotoxicity", "Megaloblastic anemia"]
        },
        "contraindications": ["eGFR < 30 mL/min/1.73m²", "Acute kidney injury", "Hepatic impairment", "Alcoholism", "Contrast dye procedures (hold 48h)"],
        "drug_interactions": ["Alcohol (lactic acidosis risk)", "Contrast media (hold before imaging)", "Cimetidine (increases metformin levels)", "Carbonic anhydrase inhibitors"],
        "food_interactions": ["Take with meals to reduce GI side effects", "Avoid excessive alcohol"],
        "pregnancy_safety": "Category B — Generally considered safe; often preferred over insulin in gestational diabetes",
        "breastfeeding": "Generally compatible with breastfeeding",
        "kidney_warning": "Contraindicated in severe renal impairment (eGFR<30). Monitor renal function regularly.",
        "liver_warning": "Avoid in hepatic impairment due to lactic acidosis risk",
        "storage": "Store at room temperature (20–25°C), away from moisture.",
        "overdose": "Symptoms: lactic acidosis, hypoglycemia. Treatment: hemodialysis, supportive care.",
        "missed_dose": "Take with next meal. Do not double dose.",
        "alternatives": ["Glipizide", "Sitagliptin (Januvia)", "Empagliflozin (Jardiance)", "Liraglutide (Victoza)"],
        "price_estimate": "₹5–25 per tablet (generic); ₹30–80 per tablet (brand)",
        "availability": "Widely available. Prescription required.",
        "manufacturer": "Merck, Sun Pharma, Cipla, Lupin, USV",
        "prescription_required": True,
        "pregnancy_category": "B"
    },
    "Amlodipine": {
        "generic_name": "Amlodipine Besylate",
        "brand_names": ["Norvasc", "Amlong", "Amlopres", "Stamlo"],
        "drug_class": "Calcium Channel Blocker / Antihypertensive",
        "description": "Amlodipine is a long-acting calcium channel blocker used for hypertension and angina. It relaxes blood vessels, allowing the heart to pump more efficiently.",
        "active_ingredients": ["Amlodipine Besylate"],
        "uses": ["Hypertension", "Stable angina", "Vasospastic angina", "Coronary artery disease"],
        "dosage": {
            "adult": "5mg once daily; may increase to 10mg/day",
            "elderly": "2.5mg once daily initially",
            "max_daily": "10 mg/day",
            "forms": ["Tablet (2.5mg, 5mg, 10mg)"]
        },
        "side_effects": {
            "common": ["Peripheral edema (ankle swelling)", "Flushing", "Headache", "Dizziness", "Fatigue"],
            "serious": ["Severe hypotension", "Worsening angina (rare)", "Liver function abnormalities"],
            "rare": ["Gingival hyperplasia", "Gynecomastia"]
        },
        "contraindications": ["Cardiogenic shock", "Unstable angina", "Severe aortic stenosis", "Hypersensitivity to dihydropyridines"],
        "drug_interactions": ["CYP3A4 inhibitors increase amlodipine levels", "Cyclosporine (increased levels)", "Simvastatin (limit statin dose to 20mg)", "Tacrolimus"],
        "food_interactions": ["Grapefruit juice can increase blood levels significantly"],
        "pregnancy_safety": "Category C — Use only if potential benefits outweigh risks",
        "breastfeeding": "Not recommended; may be excreted in breast milk",
        "kidney_warning": "Generally safe; no dose adjustment usually needed",
        "liver_warning": "Use with caution; start at lowest dose in hepatic impairment",
        "storage": "Store below 30°C, protect from moisture.",
        "overdose": "Symptoms: severe hypotension, tachycardia, bradycardia. Treatment: IV calcium gluconate, vasopressors.",
        "missed_dose": "Take as soon as remembered if same day; skip if next day. Never double dose.",
        "alternatives": ["Nifedipine (Adalat)", "Felodipine", "Lisinopril (ACE inhibitor)", "Losartan (ARB)"],
        "price_estimate": "₹3–15 per tablet (generic); ₹20–60 per tablet (brand)",
        "availability": "Widely available at all pharmacies. Prescription required.",
        "manufacturer": "Pfizer, Sun Pharma, Cipla, Dr. Reddy's, Torrent",
        "prescription_required": True,
        "pregnancy_category": "C"
    },
    "Sertraline": {
        "generic_name": "Sertraline Hydrochloride",
        "brand_names": ["Zoloft", "Serlift", "Daxid", "Eleva"],
        "drug_class": "SSRI (Selective Serotonin Reuptake Inhibitor) / Antidepressant",
        "description": "Sertraline is an SSRI antidepressant that increases serotonin levels in the brain. It is one of the most prescribed antidepressants globally.",
        "active_ingredients": ["Sertraline Hydrochloride"],
        "uses": ["Major Depressive Disorder", "Panic Disorder", "PTSD", "OCD", "Social Anxiety Disorder", "Premenstrual Dysphoric Disorder"],
        "dosage": {
            "adult": "50mg once daily; may increase to 200mg/day",
            "elderly": "25mg once daily initially",
            "max_daily": "200 mg/day",
            "forms": ["Tablet (25mg, 50mg, 100mg)", "Oral concentrate (20mg/mL)"]
        },
        "side_effects": {
            "common": ["Nausea", "Diarrhea", "Insomnia", "Dry mouth", "Sexual dysfunction", "Increased sweating"],
            "serious": ["Serotonin syndrome", "Suicidal thoughts (especially in young adults)", "Hyponatremia", "Bleeding risk"],
            "rare": ["Seizures", "Manic episodes", "SIADH"]
        },
        "contraindications": ["MAO inhibitor use within 14 days", "Pimozide", "Disulfiram (oral concentrate only)"],
        "drug_interactions": ["MAOIs (serotonin syndrome)", "Tramadol (serotonin syndrome)", "NSAIDs/warfarin (bleeding risk)", "Lithium", "Triptans"],
        "food_interactions": ["Avoid alcohol", "May be taken with or without food"],
        "pregnancy_safety": "Category C — Use when benefits outweigh risks; neonatal withdrawal possible",
        "breastfeeding": "Use with caution; present in low amounts in breast milk",
        "kidney_warning": "Generally safe in renal impairment; no dose adjustment needed",
        "liver_warning": "Use lower dose in hepatic impairment; may increase drug levels",
        "storage": "Store at room temperature (15–30°C), away from moisture.",
        "overdose": "Symptoms: nausea, vomiting, tremor, tachycardia, somnolence. Treatment: supportive care, activated charcoal.",
        "missed_dose": "Take as soon as remembered. If close to next dose, skip. Do not double dose.",
        "alternatives": ["Fluoxetine (Prozac)", "Escitalopram (Lexapro)", "Paroxetine (Paxil)", "Venlafaxine (Effexor)"],
        "price_estimate": "₹10–50 per tablet (generic); ₹60–150 per tablet (brand)",
        "availability": "Available at pharmacies. Prescription required.",
        "manufacturer": "Pfizer, Sun Pharma, Cipla, Lupin",
        "prescription_required": True,
        "pregnancy_category": "C"
    },
    "Salbutamol": {
        "generic_name": "Salbutamol (Albuterol)",
        "brand_names": ["Ventolin", "Asthalin", "Salbetol", "Proventil"],
        "drug_class": "Short-Acting Beta2-Agonist (SABA) / Bronchodilator",
        "description": "Salbutamol is a fast-acting bronchodilator that relieves bronchospasm in asthma and COPD. It relaxes airway smooth muscle within minutes.",
        "active_ingredients": ["Salbutamol Sulphate"],
        "uses": ["Acute asthma attacks", "COPD", "Exercise-induced bronchospasm", "Hyperkalemia (IV form)", "Preterm labor (tocolysis)"],
        "dosage": {
            "adult": "Inhaler: 1–2 puffs (100mcg/puff) every 4–6 hours PRN",
            "elderly": "Same as adult; monitor for cardiovascular effects",
            "max_daily": "800 mcg/day (inhaler)",
            "forms": ["MDI inhaler (100mcg/puff)", "Nebulizer solution (2.5mg/2.5mL)", "Tablet (2mg, 4mg)", "Syrup (2mg/5mL)"]
        },
        "side_effects": {
            "common": ["Tremor", "Palpitations", "Headache", "Muscle cramps", "Tachycardia", "Hypokalemia (high doses)"],
            "serious": ["Paradoxical bronchospasm", "Severe tachycardia", "Hypokalemia with high doses"],
            "rare": ["Allergic reactions", "Lactic acidosis (IV)"]
        },
        "contraindications": ["Hypersensitivity to salbutamol", "Pre-term labor when premature labor is inappropriate"],
        "drug_interactions": ["Beta-blockers (antagonize effect)", "MAOIs/TCAs (cardiovascular effects)", "Digoxin (hypokalemia risk)", "Diuretics (hypokalemia)"],
        "food_interactions": ["No significant food interactions"],
        "pregnancy_safety": "Category C — Generally considered safe for acute asthma; benefits outweigh risks",
        "breastfeeding": "Compatible with breastfeeding; minimal transfer",
        "kidney_warning": "Use with caution in severe renal impairment",
        "liver_warning": "Generally safe",
        "storage": "Store below 30°C; protect from frost. Inhaler: avoid exposing to temperatures >50°C.",
        "overdose": "Symptoms: tremor, tachycardia, hypokalemia, chest pain. Treatment: beta-blocker (cardioselective), supportive care.",
        "missed_dose": "PRN medication — only take when needed. Follow prescribed schedule for regular dosing.",
        "alternatives": ["Levosalbutamol (Levalbuterol)", "Terbutaline", "Ipratropium (different mechanism)", "Formoterol (long-acting)"],
        "price_estimate": "₹50–150 per inhaler (generic); ₹150–300 per inhaler (brand)",
        "availability": "Available at most pharmacies. Prescription recommended.",
        "manufacturer": "GSK, Cipla, Sun Pharma, Systopic",
        "prescription_required": False,
        "pregnancy_category": "C"
    },
    "Omeprazole": {
        "generic_name": "Omeprazole",
        "brand_names": ["Prilosec", "Omez", "Omecip", "Ocid"],
        "drug_class": "Proton Pump Inhibitor (PPI)",
        "description": "Omeprazole reduces acid production in the stomach by irreversibly blocking the hydrogen/potassium ATPase enzyme system. Highly effective for GERD and peptic ulcers.",
        "active_ingredients": ["Omeprazole Magnesium / Omeprazole"],
        "uses": ["GERD", "Peptic Ulcer Disease", "Zollinger-Ellison Syndrome", "H. pylori eradication (with antibiotics)", "NSAID-induced ulcer prevention"],
        "dosage": {
            "adult": "20–40mg once daily before breakfast",
            "elderly": "Same as adult; no adjustment usually needed",
            "max_daily": "80 mg/day (120mg in Z-E syndrome)",
            "forms": ["Capsule (10mg, 20mg, 40mg)", "Tablet", "IV injection (40mg)", "Sachet for suspension"]
        },
        "side_effects": {
            "common": ["Headache", "Nausea", "Diarrhea", "Constipation", "Flatulence", "Abdominal pain"],
            "serious": ["C. difficile infection (long-term)", "Hypomagnesemia", "Bone fractures (long-term)", "Vitamin B12 deficiency"],
            "rare": ["Acute interstitial nephritis", "Clostridium difficile-associated diarrhea"]
        },
        "contraindications": ["Hypersensitivity to omeprazole or substituted benzimidazoles", "Concurrent rilpivirine use"],
        "drug_interactions": ["Clopidogrel (reduces antiplatelet effect)", "Methotrexate (increased levels)", "Ketoconazole/Itraconazole (reduced absorption)", "Warfarin (increased INR)"],
        "food_interactions": ["Best taken 30–60 minutes before meals"],
        "pregnancy_safety": "Category C — Use when benefit outweighs risk",
        "breastfeeding": "Use with caution",
        "kidney_warning": "Generally safe; no dose adjustment needed",
        "liver_warning": "Dose reduction may be needed in severe hepatic impairment",
        "storage": "Store at room temperature; protect from moisture.",
        "overdose": "Relatively low toxicity. Supportive treatment.",
        "missed_dose": "Take as soon as remembered. Skip if close to next dose.",
        "alternatives": ["Pantoprazole (Pantodac)", "Esomeprazole (Nexium)", "Rabeprazole (Razo)", "Lansoprazole"],
        "price_estimate": "₹3–20 per capsule (generic); ₹25–60 per capsule (brand)",
        "availability": "Widely available OTC and by prescription.",
        "manufacturer": "AstraZeneca, Cipla, Sun Pharma, Torrent",
        "prescription_required": False,
        "pregnancy_category": "C"
    },
    "Atorvastatin": {
        "generic_name": "Atorvastatin Calcium",
        "brand_names": ["Lipitor", "Atorva", "Storvas", "Aztor"],
        "drug_class": "HMG-CoA Reductase Inhibitor / Statin / Lipid-Lowering Agent",
        "description": "Atorvastatin is the most prescribed statin worldwide for lowering LDL cholesterol and reducing cardiovascular risk.",
        "active_ingredients": ["Atorvastatin Calcium"],
        "uses": ["High cholesterol (hyperlipidemia)", "Prevention of cardiovascular disease", "Post-MI secondary prevention", "Stroke prevention", "Familial hypercholesterolemia"],
        "dosage": {
            "adult": "10–80mg once daily (evening preferred)",
            "elderly": "Same as adult; start with lower dose",
            "max_daily": "80 mg/day",
            "forms": ["Tablet (10mg, 20mg, 40mg, 80mg)"]
        },
        "side_effects": {
            "common": ["Muscle aches (myalgia)", "Headache", "Nausea", "Diarrhea", "Joint pain", "Nasopharyngitis"],
            "serious": ["Rhabdomyolysis (muscle breakdown)", "Hepatotoxicity", "Myopathy"],
            "rare": ["Immune-mediated necrotizing myopathy", "Interstitial lung disease"]
        },
        "contraindications": ["Active liver disease", "Pregnancy", "Breastfeeding", "Unexplained persistent elevations of liver enzymes"],
        "drug_interactions": ["Cyclosporine (markedly increases atorvastatin)", "Gemfibrozil (myopathy risk)", "Clarithromycin/Erythromycin (increase levels)", "Digoxin"],
        "food_interactions": ["Grapefruit juice increases levels (avoid large quantities)", "Can be taken with or without food"],
        "pregnancy_safety": "Category X — Contraindicated in pregnancy",
        "breastfeeding": "Contraindicated",
        "kidney_warning": "Generally safe; no dose adjustment needed",
        "liver_warning": "Contraindicated in active liver disease; monitor LFTs",
        "storage": "Store below 25°C; protect from moisture.",
        "overdose": "No specific antidote; supportive treatment. Monitor for myopathy.",
        "missed_dose": "Take as soon as remembered same day; skip if next day.",
        "alternatives": ["Rosuvastatin (Crestor)", "Simvastatin", "Pravastatin", "Pitavastatin"],
        "price_estimate": "₹5–30 per tablet (generic); ₹40–120 per tablet (brand)",
        "availability": "Widely available. Prescription required.",
        "manufacturer": "Pfizer, Sun Pharma, Cipla, Dr. Reddy's",
        "prescription_required": True,
        "pregnancy_category": "X"
    },
    "Levothyroxine": {
        "generic_name": "Levothyroxine Sodium (T4)",
        "brand_names": ["Synthroid", "Thyronorm", "Eltroxin", "Levothroid"],
        "drug_class": "Thyroid Hormone / Endocrine Agent",
        "description": "Levothyroxine is a synthetic thyroid hormone used to treat hypothyroidism. It replaces the hormone normally produced by the thyroid gland.",
        "active_ingredients": ["Levothyroxine Sodium"],
        "uses": ["Hypothyroidism", "Thyroid cancer (suppressive therapy)", "Myxedema coma", "Hashimoto's thyroiditis", "Thyroid goiter"],
        "dosage": {
            "adult": "1.6–1.8 mcg/kg/day; usual range 100–200 mcg/day",
            "elderly": "Start at 12.5–25 mcg/day; titrate slowly",
            "max_daily": "Individualized based on TSH levels",
            "forms": ["Tablet (25mcg, 50mcg, 75mcg, 100mcg, 125mcg, 150mcg, 200mcg)", "IV injection"]
        },
        "side_effects": {
            "common": ["Mostly occur with overtreatment: palpitations, tremor, anxiety, insomnia, heat intolerance, weight loss"],
            "serious": ["Cardiac arrhythmias", "Bone loss (osteoporosis with long-term overtreatment)", "Thyrotoxicosis"],
            "rare": ["Adrenal crisis (if adrenal insufficiency present)"]
        },
        "contraindications": ["Untreated adrenal insufficiency", "Acute MI (except for myxedema)", "Thyrotoxicosis"],
        "drug_interactions": ["Antacids/calcium (reduce absorption)", "Warfarin (increased anticoagulation)", "Insulin (may need adjustment)", "Amiodarone", "Rifampin (increased metabolism)"],
        "food_interactions": ["Take on empty stomach 30–60 min before breakfast", "Avoid soy, high-fiber foods, calcium-rich foods close to dose"],
        "pregnancy_safety": "Category A — Safe in pregnancy; dose often needs to increase",
        "breastfeeding": "Safe for breastfeeding",
        "kidney_warning": "Use with caution in renal impairment",
        "liver_warning": "Hepatic impairment may affect drug metabolism",
        "storage": "Store at room temperature (15–30°C); protect from light, heat, moisture.",
        "overdose": "Symptoms: tachycardia, chest pain, tremor, anxiety, seizures. Treatment: supportive care, beta-blockers for cardiovascular symptoms.",
        "missed_dose": "Take as soon as remembered same day; skip if next day. Can take 2 tablets next day occasionally.",
        "alternatives": ["Liothyronine (T3)", "Desiccated thyroid extract (NDT)", "Combination T4/T3 therapy"],
        "price_estimate": "₹5–30 per tablet (generic); ₹30–80 per tablet (brand)",
        "availability": "Available at most pharmacies. Prescription required.",
        "manufacturer": "AbbVie, Cipla, GSK, Merck",
        "prescription_required": True,
        "pregnancy_category": "A"
    },
    "Amoxicillin": {
        "generic_name": "Amoxicillin Trihydrate",
        "brand_names": ["Amoxil", "Novamox", "Moxikind", "Trimox"],
        "drug_class": "Penicillin Antibiotic / Beta-Lactam",
        "description": "Amoxicillin is a widely used broad-spectrum penicillin antibiotic effective against many bacterial infections.",
        "active_ingredients": ["Amoxicillin Trihydrate"],
        "uses": ["Respiratory tract infections", "Ear infections", "Urinary tract infections", "Skin infections", "H. pylori eradication", "Dental infections", "Lyme disease"],
        "dosage": {
            "adult": "250–500mg every 8 hours OR 875mg every 12 hours",
            "elderly": "Same as adult; adjust in renal impairment",
            "max_daily": "3000 mg/day (standard); 4000mg/day (H. pylori)",
            "forms": ["Capsule (250mg, 500mg)", "Tablet (875mg)", "Oral suspension (125mg/5mL, 250mg/5mL)", "IV injection"]
        },
        "side_effects": {
            "common": ["Diarrhea", "Nausea", "Vomiting", "Skin rash", "Stomach pain"],
            "serious": ["Anaphylaxis (allergic reaction)", "Stevens-Johnson Syndrome", "Pseudomembranous colitis"],
            "rare": ["Serum sickness-like reaction", "Crystalluria"]
        },
        "contraindications": ["Penicillin allergy", "History of amoxicillin-associated jaundice"],
        "drug_interactions": ["Warfarin (increased bleeding risk)", "Methotrexate (increased toxicity)", "Oral contraceptives (reduced efficacy)", "Probenecid (increases amoxicillin levels)"],
        "food_interactions": ["Can be taken with or without food"],
        "pregnancy_safety": "Category B — Generally considered safe",
        "breastfeeding": "Compatible; considered safe",
        "kidney_warning": "Dose adjustment required in severe renal impairment (CrCl <30 mL/min)",
        "liver_warning": "Generally safe; use with caution in severe hepatic impairment",
        "storage": "Capsules: store at room temperature. Suspension: refrigerate, discard after 14 days.",
        "overdose": "Relatively low toxicity. GI symptoms. Treatment: supportive. Hemodialysis in severe cases.",
        "missed_dose": "Take as soon as remembered. If close to next dose, skip. Complete full course.",
        "alternatives": ["Ampicillin", "Azithromycin (macrolide)", "Cephalexin (cephalosporin)", "Clarithromycin"],
        "price_estimate": "₹5–25 per capsule (generic); ₹20–60 per capsule (brand)",
        "availability": "Widely available. Prescription required.",
        "manufacturer": "GSK, Cipla, Sun Pharma, Ranbaxy",
        "prescription_required": True,
        "pregnancy_category": "B"
    },
    "Sumatriptan": {
        "generic_name": "Sumatriptan Succinate",
        "brand_names": ["Imitrex", "Suminat", "Migranil", "Immigran"],
        "drug_class": "Triptan / Serotonin 5-HT1B/1D Agonist / Antimigraine",
        "description": "Sumatriptan is a selective serotonin receptor agonist used to treat acute migraine attacks with or without aura.",
        "active_ingredients": ["Sumatriptan Succinate"],
        "uses": ["Acute migraine attacks", "Cluster headaches (injectable form)"],
        "dosage": {
            "adult": "Oral: 50–100mg at onset; may repeat after 2h. Max 200mg/day",
            "elderly": "Use with caution; cardiovascular risk assessment needed",
            "max_daily": "200 mg/day (oral); 12 mg/day (SC injection)",
            "forms": ["Tablet (25mg, 50mg, 100mg)", "Subcutaneous injection (6mg/0.5mL)", "Nasal spray (10mg, 20mg)", "Nasal powder"]
        },
        "side_effects": {
            "common": ["Tingling/numbness", "Flushing", "Dizziness", "Fatigue", "Chest tightness", "Nausea"],
            "serious": ["Coronary artery vasospasm", "Serotonin syndrome (with SSRIs/SNRIs)", "Stroke (rare)", "Hypertensive crisis"],
            "rare": ["Raynaud's phenomenon", "Colonic ischemia"]
        },
        "contraindications": ["Ischemic heart disease", "History of MI or stroke", "Uncontrolled hypertension", "MAO-A inhibitor use", "Hemiplegic/basilar migraine"],
        "drug_interactions": ["MAOIs (serotonin syndrome, contraindicated)", "SSRIs/SNRIs (serotonin syndrome risk)", "Ergotamine (vasoconstriction)", "Other triptans"],
        "food_interactions": ["No significant food interactions"],
        "pregnancy_safety": "Category C — Use when benefit outweighs risk",
        "breastfeeding": "Wait 12 hours after dose before breastfeeding",
        "kidney_warning": "Use with caution in renal impairment",
        "liver_warning": "Use lowest effective dose in hepatic impairment",
        "storage": "Store below 30°C, away from light.",
        "overdose": "Symptoms: tremor, redness, reduced breathing, hypertension. Treatment: supportive care.",
        "missed_dose": "Only taken as needed during migraine attack; not for prevention.",
        "alternatives": ["Rizatriptan (Maxalt)", "Zolmitriptan (Zomig)", "Eletriptan (Relpax)", "Ubrogepant (newer CGRP antagonist)"],
        "price_estimate": "₹30–100 per tablet (generic); ₹150–400 per tablet (brand)",
        "availability": "Available at pharmacies. Prescription required.",
        "manufacturer": "GSK, Sun Pharma, Cipla, Dr. Reddy's",
        "prescription_required": True,
        "pregnancy_category": "C"
    },
    "Zolpidem": {
        "generic_name": "Zolpidem Tartrate",
        "brand_names": ["Ambien", "Stilnox", "Nitrest", "Zolfresh"],
        "drug_class": "Non-Benzodiazepine Sedative-Hypnotic / Z-Drug",
        "description": "Zolpidem is a short-term treatment for insomnia. It acts on GABA receptors to promote sleep onset quickly.",
        "active_ingredients": ["Zolpidem Tartrate"],
        "uses": ["Short-term insomnia", "Sleep onset difficulties"],
        "dosage": {
            "adult": "Men: 5–10mg; Women: 5mg immediately before bed",
            "elderly": "5mg immediately before bed (due to increased sensitivity)",
            "max_daily": "10 mg/day",
            "forms": ["Tablet (5mg, 10mg)", "Extended-release tablet (6.25mg, 12.5mg)", "Sublingual tablet"]
        },
        "side_effects": {
            "common": ["Drowsiness", "Dizziness", "Headache", "Nausea", "Memory problems", "Daytime sedation"],
            "serious": ["Complex sleep behaviors (sleep-driving, sleepwalking)", "Severe allergic reactions", "Paradoxical CNS excitation", "Dependence"],
            "rare": ["Hallucinations", "Aggression", "Amnesia"]
        },
        "contraindications": ["Hypersensitivity to zolpidem", "Acute narrow-angle glaucoma", "Myasthenia gravis", "Severe hepatic impairment", "Sleep apnea"],
        "drug_interactions": ["CNS depressants (enhanced sedation)", "Alcohol (strongly enhanced sedation)", "CYP3A4 inhibitors (increase levels)", "Rifampicin (reduces levels)"],
        "food_interactions": ["Avoid alcohol. High-fat meal delays absorption."],
        "pregnancy_safety": "Category C — Avoid if possible, especially near term",
        "breastfeeding": "Not recommended",
        "kidney_warning": "No dose adjustment needed in mild-moderate renal impairment",
        "liver_warning": "Contraindicated in severe hepatic impairment; use 5mg in mild-moderate",
        "storage": "Store at room temperature (20–25°C).",
        "overdose": "Symptoms: drowsiness, confusion, respiratory depression, coma. Antidote: Flumazenil.",
        "missed_dose": "Only take if you have 7–8 hours before needed to be awake. Do not take if close to waking time.",
        "alternatives": ["Eszopiclone (Lunesta)", "Zaleplon", "Melatonin (OTC)", "Doxylamine (OTC)", "Ramelteon"],
        "price_estimate": "₹15–50 per tablet (generic); ₹80–200 per tablet (brand)",
        "availability": "Prescription required (Controlled substance Schedule IV)",
        "manufacturer": "Sanofi, Sun Pharma, Cipla, Intas",
        "prescription_required": True,
        "controlled_substance": "Schedule IV",
        "pregnancy_category": "C"
    },
    "Ibuprofen": {
        "generic_name": "Ibuprofen",
        "brand_names": ["Brufen", "Advil", "Motrin", "Combiflam (with paracetamol)"],
        "drug_class": "NSAID (Non-Steroidal Anti-Inflammatory Drug)",
        "description": "Ibuprofen is a widely used NSAID that reduces inflammation, pain, and fever by inhibiting COX-1 and COX-2 enzymes.",
        "active_ingredients": ["Ibuprofen"],
        "uses": ["Pain relief (mild to moderate)", "Fever", "Inflammation", "Arthritis", "Dysmenorrhea", "Headache", "Dental pain", "Sports injuries"],
        "dosage": {
            "adult": "200–400mg every 4–6 hours; max 1200mg/day OTC or 3200mg/day Rx",
            "elderly": "Use lowest effective dose; higher GI and renal risk",
            "max_daily": "3200 mg/day (prescription); 1200 mg/day (OTC)",
            "forms": ["Tablet (200mg, 400mg, 600mg, 800mg)", "Syrup (100mg/5mL)", "Gel (topical)", "Capsule (liquid-filled)"]
        },
        "side_effects": {
            "common": ["GI upset", "Nausea", "Heartburn", "Dizziness", "Headache", "Fluid retention"],
            "serious": ["GI bleeding/ulceration", "Cardiovascular events (MI, stroke)", "Acute kidney injury", "Hypertension"],
            "rare": ["Stevens-Johnson Syndrome", "Hepatotoxicity", "Aseptic meningitis"]
        },
        "contraindications": ["Active peptic ulcer", "History of GI bleeding", "Severe renal impairment", "Severe heart failure", "Third trimester pregnancy", "Aspirin-exacerbated respiratory disease"],
        "drug_interactions": ["Aspirin (reduced cardioprotective effect)", "Warfarin (increased bleeding)", "ACE inhibitors/ARBs (reduced efficacy + renal risk)", "Methotrexate", "Corticosteroids"],
        "food_interactions": ["Take with food or milk to reduce GI irritation", "Avoid alcohol"],
        "pregnancy_safety": "Category C (1st/2nd trimester); Category D (3rd trimester) — Avoid in 3rd trimester",
        "breastfeeding": "Compatible with breastfeeding; preferred NSAID for nursing mothers",
        "kidney_warning": "Avoid in renal impairment; can cause acute kidney injury especially with dehydration",
        "liver_warning": "Use with caution; hepatotoxicity possible at high doses",
        "storage": "Store at room temperature (20–25°C), away from moisture.",
        "overdose": "Symptoms: nausea, vomiting, epigastric pain, GI bleeding, acute renal failure. Treatment: supportive care.",
        "missed_dose": "Take as soon as remembered if not close to next dose. (PRN for pain — only take when needed)",
        "alternatives": ["Paracetamol/Acetaminophen (milder)", "Naproxen (longer-acting)", "Diclofenac", "Celecoxib (COX-2 selective, safer GI profile)"],
        "price_estimate": "₹2–10 per tablet (generic); ₹15–40 per tablet (brand)",
        "availability": "Widely available OTC at all pharmacies.",
        "manufacturer": "Various — Abbott, Cipla, Zydus, Pfizer",
        "prescription_required": False,
        "pregnancy_category": "C/D"
    }
}

# ─── Disease Knowledge Base ───────────────────────────────────────
DISEASE_KNOWLEDGE = {
    "Diabetes Type 2": {
        "overview": "Type 2 diabetes is a chronic condition in which the body doesn't use insulin properly (insulin resistance), eventually leading to high blood sugar levels.",
        "symptoms": ["Frequent urination (polyuria)", "Excessive thirst (polydipsia)", "Fatigue and weakness", "Blurred vision", "Slow-healing wounds", "Frequent infections", "Numbness/tingling in hands or feet", "Unexplained weight loss"],
        "causes": ["Insulin resistance", "Genetic factors", "Obesity (especially central/abdominal)", "Sedentary lifestyle", "Unhealthy diet", "Age (risk increases after 45)", "High blood pressure", "History of gestational diabetes"],
        "risk_factors": ["Family history of diabetes", "Overweight/obesity (BMI>25)", "Physical inactivity", "Age >45 years", "Prediabetes", "Gestational diabetes history", "PCOS", "Race/ethnicity (South Asian, African, Hispanic)"],
        "diagnosis": ["Fasting plasma glucose ≥126 mg/dL", "HbA1c ≥6.5%", "2-hour oral glucose tolerance test ≥200 mg/dL", "Random plasma glucose ≥200 mg/dL with symptoms"],
        "treatment": ["Lifestyle modifications (diet + exercise)", "Metformin (first-line medication)", "SGLT2 inhibitors (empagliflozin, dapagliflozin)", "GLP-1 agonists (semaglutide, liraglutide)", "DPP-4 inhibitors (sitagliptin)", "Sulfonylureas", "Insulin (when oral agents inadequate)", "Bariatric surgery (for severe obesity)"],
        "lifestyle": ["Reduce refined carbohydrates and sugars", "Increase fiber and vegetables", "Regular physical activity (150 min/week)", "Maintain healthy weight", "Monitor blood glucose regularly", "Quit smoking", "Limit alcohol"],
        "prevention": ["Maintain healthy weight", "Regular physical activity", "Healthy diet (Mediterranean or DASH)", "Regular health screenings", "Treat prediabetes early"],
        "related_drugs": ["Metformin", "Glipizide", "Sitagliptin", "Empagliflozin", "Insulin Glargine"],
        "emergency_signs": ["Blood sugar >400 mg/dL", "Diabetic ketoacidosis (DKA) — fruity breath, vomiting, rapid breathing", "Hyperosmolar hyperglycemic state", "Severe hypoglycemia — confusion, seizures, loss of consciousness"],
        "complications": ["Heart disease", "Stroke", "Kidney disease (diabetic nephropathy)", "Eye damage (retinopathy)", "Nerve damage (neuropathy)", "Foot problems"]
    },
    "Hypertension": {
        "overview": "Hypertension (high blood pressure) is a chronic condition where blood pressure in the arteries is persistently elevated (≥130/80 mmHg), increasing risk of heart disease and stroke.",
        "symptoms": ["Often 'silent killer' — no symptoms in most cases", "Severe hypertension: headache (especially morning)", "Dizziness or lightheadedness", "Nosebleeds (epistaxis)", "Visual disturbances", "Chest pain", "Shortness of breath"],
        "causes": ["Primary (essential): unknown, multifactorial", "Secondary causes: kidney disease, thyroid disorders, sleep apnea, medications (NSAIDs, oral contraceptives, decongestants)"],
        "risk_factors": ["Age (especially >65)", "Family history", "Obesity", "Physical inactivity", "High sodium diet", "Low potassium diet", "Alcohol use", "Stress", "Smoking", "Diabetes", "Chronic kidney disease"],
        "diagnosis": ["Blood pressure measurements on ≥2 occasions", "Stage 1: 130–139/80–89 mmHg", "Stage 2: ≥140/90 mmHg", "Hypertensive crisis: ≥180/120 mmHg", "Home BP monitoring, ambulatory monitoring"],
        "treatment": ["DASH diet (low sodium, high potassium)", "Regular aerobic exercise", "ACE inhibitors (lisinopril, ramipril)", "ARBs (losartan, valsartan)", "Calcium channel blockers (amlodipine)", "Thiazide diuretics (hydrochlorothiazide)", "Beta-blockers (metoprolol)", "Aldosterone antagonists (spironolactone)"],
        "lifestyle": ["Reduce sodium to <2300mg/day", "DASH diet", "Exercise 150 min/week", "Maintain healthy weight", "Limit alcohol", "Quit smoking", "Reduce stress"],
        "prevention": ["Regular blood pressure checks", "Healthy diet and weight", "Regular exercise", "Limit alcohol and sodium"],
        "related_drugs": ["Amlodipine", "Lisinopril", "Losartan", "Metoprolol", "Hydrochlorothiazide"],
        "emergency_signs": ["BP >180/120 mmHg with chest pain — call emergency", "Hypertensive urgency/emergency", "Symptoms of stroke (FAST: Face drooping, Arm weakness, Speech difficulty, Time to call)"],
        "complications": ["Heart attack", "Stroke", "Heart failure", "Aneurysm", "Kidney damage", "Vision loss"]
    },
    "Depression": {
        "overview": "Major depressive disorder (MDD) is a mood disorder characterized by persistent sadness, loss of interest, and various emotional and physical problems.",
        "symptoms": ["Persistent sad, empty, or 'down' mood", "Loss of interest or pleasure in activities", "Sleep disturbances (insomnia or hypersomnia)", "Fatigue and loss of energy", "Feelings of worthlessness or guilt", "Difficulty thinking, concentrating", "Appetite changes (weight loss or gain)", "Psychomotor changes", "Thoughts of death or suicide"],
        "causes": ["Biological factors (serotonin, norepinephrine imbalance)", "Genetic predisposition", "Major life events (trauma, loss)", "Medical conditions", "Certain medications", "Substance use"],
        "risk_factors": ["Personal or family history of depression", "Trauma or stressful life events", "Chronic illness", "Substance use disorders", "Social isolation", "Women at higher risk"],
        "diagnosis": ["DSM-5 criteria: ≥5 symptoms for ≥2 weeks", "PHQ-9 screening questionnaire", "Ruling out medical causes", "Clinical interview by mental health professional"],
        "treatment": ["Psychotherapy (CBT, IPT)", "SSRIs (sertraline, fluoxetine, escitalopram)", "SNRIs (venlafaxine, duloxetine)", "TCAs (amitriptyline)", "MAOIs", "Atypical antidepressants (bupropion, mirtazapine)", "ECT (for treatment-resistant)", "Combination therapy"],
        "lifestyle": ["Regular physical exercise", "Adequate sleep hygiene", "Social connections", "Mindfulness and meditation", "Healthy diet", "Avoid alcohol and drugs"],
        "prevention": ["Early treatment of mild depression", "Stress management", "Strong social support", "Regular exercise", "Limiting alcohol"],
        "related_drugs": ["Sertraline", "Fluoxetine", "Escitalopram", "Venlafaxine", "Bupropion"],
        "emergency_signs": ["Suicidal ideation — immediate professional help", "Psychotic symptoms", "Complete inability to function", "Self-harm behavior"],
        "complications": ["Substance abuse", "Social isolation", "Relationship problems", "Increased physical health problems", "Suicide risk"]
    },
    "Anxiety": {
        "overview": "Anxiety disorders involve excessive, persistent worry and fear that interferes with daily activities. They are the most common mental health disorders.",
        "symptoms": ["Excessive, uncontrollable worry", "Restlessness or feeling on edge", "Fatigue", "Difficulty concentrating", "Irritability", "Muscle tension", "Sleep disturbances", "Panic attacks (in panic disorder)"],
        "causes": ["Genetics", "Brain chemistry (GABA, serotonin)", "Trauma and stress", "Medical conditions (thyroid disorders, heart disease)", "Substance use", "Personality factors"],
        "risk_factors": ["Female gender", "Childhood trauma", "Chronic medical illness", "Other mental health disorders", "Substance use", "Family history"],
        "diagnosis": ["GAD-7 screening questionnaire", "Clinical interview", "Rule out medical causes (thyroid, cardiac)", "DSM-5 criteria"],
        "treatment": ["Cognitive Behavioral Therapy (CBT)", "SSRIs (first-line pharmacotherapy)", "SNRIs", "Buspirone", "Benzodiazepines (short-term only)", "Beta-blockers (situational anxiety)", "Hydroxyzine"],
        "lifestyle": ["Regular exercise", "Relaxation techniques (deep breathing, progressive muscle relaxation)", "Mindfulness meditation", "Adequate sleep", "Limit caffeine and alcohol"],
        "prevention": ["Early intervention", "Stress management", "Regular exercise", "Mindfulness practice"],
        "related_drugs": ["Lorazepam", "Alprazolam", "Buspirone", "Escitalopram", "Venlafaxine"],
        "emergency_signs": ["Severe panic attack with chest pain — rule out cardiac event", "Agoraphobia preventing leaving home", "Suicidal thoughts", "Complete inability to function"],
        "complications": ["Depression (frequently co-occurs)", "Substance abuse", "Social isolation", "Physical health problems"]
    },
    "Asthma": {
        "overview": "Asthma is a chronic inflammatory disease of the airways causing recurring episodes of wheezing, breathlessness, chest tightness, and coughing.",
        "symptoms": ["Wheezing (whistling sound when breathing)", "Shortness of breath", "Chest tightness", "Coughing (especially at night or early morning)", "Exercise-induced symptoms"],
        "causes": ["Allergic triggers (pollen, dust mites, pet dander)", "Non-allergic triggers (cold air, exercise, infections)", "Air pollution and irritants", "Workplace exposures", "Genetic predisposition"],
        "risk_factors": ["Family history of asthma", "Allergies (atopy, eczema, rhinitis)", "Childhood respiratory infections", "Obesity", "Smoking", "Air pollution exposure"],
        "diagnosis": ["Spirometry (FEV1/FVC ratio)", "Peak flow meter monitoring", "Bronchodilator reversibility test", "Methacholine challenge test", "Allergy testing"],
        "treatment": ["Short-acting beta-agonists (salbutamol — rescue inhaler)", "Inhaled corticosteroids (budesonide, fluticasone)", "Long-acting beta-agonists (formoterol, salmeterol)", "Leukotriene modifiers (montelukast)", "Biologics (dupilumab, omalizumab for severe asthma)", "Oral steroids (for acute exacerbations)"],
        "lifestyle": ["Identify and avoid triggers", "Monitor peak flow", "Use inhaler correctly", "Maintain healthy weight", "Exercise regularly (in controlled settings)", "Avoid smoking"],
        "prevention": ["Avoid known triggers", "Vaccination (influenza, pneumococcal)", "Regular controller medication", "HEPA air filters at home"],
        "related_drugs": ["Salbutamol", "Budesonide", "Formoterol", "Montelukast", "Prednisolone"],
        "emergency_signs": ["Severe breathing difficulty not responding to reliever inhaler", "Cyanosis (bluish lips/fingernails)", "Peak flow <50% of personal best", "Asthmatic status — call emergency"],
        "complications": ["Severe asthma attacks", "Reduced quality of life", "Respiratory failure in severe cases", "Medication side effects"]
    },
    "Migraine": {
        "overview": "Migraine is a neurological disorder characterized by recurrent episodes of moderate-to-severe unilateral throbbing headache, often with nausea, vomiting, and sensitivity to light and sound.",
        "symptoms": ["Severe, throbbing headache (usually one-sided)", "Nausea and vomiting", "Photophobia (light sensitivity)", "Phonophobia (sound sensitivity)", "Aura (visual/sensory/speech disturbances in ~30%)", "Prodrome (mood changes, yawning, food cravings before attack)"],
        "causes": ["Neurological changes (cortical spreading depression)", "Trigeminovascular activation", "Genetic predisposition", "Hormonal fluctuations"],
        "risk_factors": ["Family history", "Female gender (hormonal influence)", "Ages 15–55", "Hormonal changes (menstruation, pregnancy)", "Sleep disruption", "Stress", "Certain foods and drinks"],
        "diagnosis": ["Clinical diagnosis based on ICHD-3 criteria", "Neurological examination", "MRI/CT to rule out secondary causes when needed"],
        "treatment": ["Acute: triptans (sumatriptan), NSAIDs, antiemetics", "Preventive: topiramate, propranolol, amitriptyline, valproate, CGRP antagonists", "CGRP monoclonal antibodies (erenumab, fremanezumab) for chronic migraine", "Botox (for chronic migraine)"],
        "lifestyle": ["Identify and avoid personal triggers", "Regular sleep schedule", "Stress management", "Stay hydrated", "Regular meals", "Exercise"],
        "prevention": ["Keep migraine diary", "Regular preventive medications", "Identify and avoid triggers", "Magnesium supplementation"],
        "related_drugs": ["Sumatriptan", "Topiramate", "Propranolol", "Amitriptyline", "Naproxen"],
        "emergency_signs": ["Thunderclap headache (worst headache of your life — subarachnoid hemorrhage)", "Headache with fever and stiff neck (meningitis)", "Headache with neurological deficits", "Headache after head injury"],
        "complications": ["Chronic migraine (>15 headache days/month)", "Medication overuse headache", "Migraine with prolonged aura", "Migrainous infarction (rare)"]
    },
    "GERD": {
        "overview": "Gastroesophageal Reflux Disease (GERD) is a chronic condition where stomach acid flows back into the esophagus, causing heartburn, regurgitation, and other symptoms.",
        "symptoms": ["Heartburn (burning sensation in chest)", "Regurgitation (acid taste in mouth)", "Chest pain", "Dysphagia (difficulty swallowing)", "Chronic cough", "Hoarseness", "Worsening of symptoms when lying down or after meals"],
        "causes": ["Lower esophageal sphincter (LES) weakness", "Hiatal hernia", "Delayed gastric emptying", "Excess stomach acid"],
        "risk_factors": ["Obesity", "Pregnancy", "Smoking", "Hiatal hernia", "Delayed gastric emptying", "Connective tissue disorders", "Certain medications (NSAIDs, calcium channel blockers, antihistamines)"],
        "diagnosis": ["Upper endoscopy (EGD)", "Ambulatory 24-hour pH monitoring", "Esophageal manometry", "Barium swallow study"],
        "treatment": ["Lifestyle modifications", "PPIs (omeprazole, pantoprazole, esomeprazole)", "H2 blockers (ranitidine, famotidine)", "Antacids (for quick relief)", "Prokinetics (metoclopramide)", "Surgical fundoplication (severe/refractory cases)"],
        "lifestyle": ["Eat smaller meals", "Avoid trigger foods (spicy, fatty, acidic, caffeine, alcohol)", "Don't lie down for 3 hours after eating", "Elevate head of bed", "Maintain healthy weight", "Quit smoking"],
        "prevention": ["Maintain healthy weight", "Avoid trigger foods and habits", "Not smoking", "Eat smaller, more frequent meals"],
        "related_drugs": ["Omeprazole", "Pantoprazole", "Esomeprazole", "Famotidine", "Sucralfate"],
        "emergency_signs": ["Severe chest pain (rule out heart attack)", "Difficulty swallowing with weight loss", "Vomiting blood or dark stools", "Signs of perforation"],
        "complications": ["Esophagitis", "Esophageal stricture", "Barrett's esophagus", "Esophageal adenocarcinoma (rare)"]
    },
    "High Cholesterol": {
        "overview": "Hypercholesterolemia is a condition of elevated cholesterol levels in the blood, particularly LDL ('bad') cholesterol, increasing risk of cardiovascular disease.",
        "symptoms": ["Usually asymptomatic", "Xanthomas (fatty deposits under skin) in severe cases", "Xanthelasmas (deposits around eyes)", "Corneal arcus"],
        "causes": ["Dietary (saturated fats, trans fats)", "Genetic factors (familial hypercholesterolemia)", "Obesity", "Physical inactivity", "Hypothyroidism", "Diabetes", "Kidney disease", "Certain medications"],
        "risk_factors": ["Diet high in saturated and trans fats", "Sedentary lifestyle", "Obesity", "Family history", "Age and sex (men and post-menopausal women)", "Diabetes", "Hypothyroidism"],
        "diagnosis": ["Lipid panel blood test (total cholesterol, LDL, HDL, triglycerides)", "Fasting vs non-fasting levels", "Cardiovascular risk assessment"],
        "treatment": ["Dietary changes", "Exercise", "Statins (atorvastatin, rosuvastatin — first-line)", "Ezetimibe (reduces intestinal absorption)", "PCSK9 inhibitors (evolocumab) for high-risk/familial cases", "Bile acid sequestrants", "Fibrates (for high triglycerides)"],
        "lifestyle": ["Mediterranean or DASH diet", "Increase soluble fiber", "Exercise 150 min/week", "Maintain healthy weight", "Quit smoking", "Limit alcohol"],
        "prevention": ["Regular cholesterol screening", "Healthy diet from early life", "Regular physical activity", "Not smoking"],
        "related_drugs": ["Atorvastatin", "Rosuvastatin", "Simvastatin", "Ezetimibe", "Fenofibrate"],
        "emergency_signs": ["Sudden chest pain (heart attack)", "Signs of stroke", "Severe abdominal pain (from pancreatitis due to very high triglycerides)"],
        "complications": ["Coronary artery disease", "Heart attack", "Stroke", "Peripheral artery disease", "Pancreatitis (very high triglycerides)"]
    },
    "Hypothyroidism": {
        "overview": "Hypothyroidism is a condition where the thyroid gland doesn't produce enough thyroid hormone, slowing down many body functions.",
        "symptoms": ["Fatigue and sluggishness", "Increased sensitivity to cold", "Constipation", "Pale, dry skin", "Puffy face", "Brittle nails", "Hair loss or thinning", "Weight gain", "Hoarse voice", "Muscle aches and stiffness", "Slow heart rate", "Depression", "Memory problems"],
        "causes": ["Autoimmune disease (Hashimoto's thyroiditis — most common)", "Thyroidectomy", "Radiation therapy", "Iodine deficiency", "Certain medications (amiodarone, lithium)", "Pituitary disorder", "Congenital hypothyroidism"],
        "risk_factors": ["Female gender (5–8× more common)", "Family history", "Age >60", "Autoimmune diseases", "Pregnancy/postpartum", "Previous thyroid surgery or radiation"],
        "diagnosis": ["TSH (thyroid-stimulating hormone) — elevated in primary hypothyroidism", "Free T4 — low", "Anti-TPO antibodies (Hashimoto's)", "Thyroid ultrasound"],
        "treatment": ["Levothyroxine (T4 replacement) — first-line", "Liothyronine (T3) — sometimes added", "Desiccated thyroid extract (NDT) — alternative", "Iodine supplementation (if deficiency)", "Regular TSH monitoring"],
        "lifestyle": ["Take medication consistently on empty stomach", "Avoid calcium/iron supplements within 4 hours of medication", "Regular monitoring every 6–12 months", "Balanced diet"],
        "prevention": ["Adequate iodine intake", "Regular thyroid screening (especially women >35)", "Monitoring in pregnancy"],
        "related_drugs": ["Levothyroxine", "Liothyronine", "Desiccated thyroid", "Iodine supplements"],
        "emergency_signs": ["Myxedema coma (severe hypothyroidism) — hypothermia, decreased consciousness, bradycardia", "Rapid weight gain with edema", "Severe chest pain"],
        "complications": ["Heart problems", "Peripheral neuropathy", "Infertility", "Birth defects", "Myxedema (very severe)", "Mental health problems"]
    },
    "Infection": {
        "overview": "Bacterial infections occur when harmful bacteria invade the body and multiply, causing various symptoms depending on the site and organism involved.",
        "symptoms": ["Fever and chills", "Inflammation (redness, swelling, warmth)", "Pain at infection site", "Fatigue", "Swollen lymph nodes", "Specific symptoms by site (UTI: dysuria; pneumonia: cough; skin: wound changes)"],
        "causes": ["Bacteria (Streptococcus, Staphylococcus, E. coli, etc.)", "Entry via cuts, inhalation, ingestion, or sexual contact"],
        "risk_factors": ["Weakened immune system", "Diabetes", "HIV/AIDS", "Cancer treatment", "Advanced age", "Poor nutrition", "Recent surgery or hospitalization", "Antibiotic use disrupting normal flora"],
        "diagnosis": ["Blood cultures", "Wound cultures", "Urine culture and sensitivity", "CBC (elevated WBC)", "Imaging (X-ray, CT for localization)", "Specific tests (strep test, TB test)"],
        "treatment": ["Antibiotics (specific to organism — culture and sensitivity)", "Common antibiotics: amoxicillin, azithromycin, ciprofloxacin, doxycycline", "Supportive care (fluids, rest)", "Surgery (drainage of abscess)", "Complete full antibiotic course"],
        "lifestyle": ["Hand hygiene (most effective prevention)", "Stay hydrated during infection", "Rest", "Complete antibiotic courses", "Nutrition support"],
        "prevention": ["Handwashing", "Vaccination", "Food safety", "Safe sex practices", "Wound care", "Avoid sharing personal items"],
        "related_drugs": ["Amoxicillin", "Azithromycin", "Ciprofloxacin", "Doxycycline", "Metronidazole"],
        "emergency_signs": ["Sepsis: fever/chills with rapid heart rate, rapid breathing, confusion — medical emergency", "Meningitis: stiff neck, photophobia, fever", "Necrotizing fasciitis: rapidly spreading red, painful skin"],
        "complications": ["Septicemia/sepsis", "Organ failure", "Antibiotic resistance", "Abscess formation", "Bacteremia", "Endocarditis"]
    },
    "Insomnia": {
        "overview": "Insomnia is a common sleep disorder characterized by difficulty falling asleep, staying asleep, or getting restful sleep, affecting daytime function.",
        "symptoms": ["Difficulty falling asleep", "Waking up frequently", "Waking too early", "Unrefreshing sleep", "Daytime sleepiness", "Difficulty concentrating", "Irritability", "Anxiety about sleep"],
        "causes": ["Stress and anxiety", "Poor sleep habits (sleep hygiene)", "Medical conditions (pain, GERD, sleep apnea)", "Mental health disorders", "Medications (stimulants, SSRIs)", "Caffeine, alcohol, nicotine", "Environmental factors", "Jet lag"],
        "risk_factors": ["Stress", "Female gender", "Older age", "Mental health disorders", "Irregular work schedule (shift work)", "Chronic illness", "Certain medications"],
        "diagnosis": ["Sleep diary", "Epworth Sleepiness Scale", "Polysomnography (sleep study)", "Actigraphy", "Rule out underlying conditions"],
        "treatment": ["Cognitive Behavioral Therapy for Insomnia (CBT-I) — first-line", "Sleep hygiene education", "Stimulus control therapy", "Sleep restriction therapy", "Relaxation techniques", "Zolpidem, eszopiclone (short-term only)", "Melatonin (mild insomnia)", "Low-dose doxepin"],
        "lifestyle": ["Maintain consistent sleep schedule", "Optimize sleep environment (dark, quiet, cool)", "Avoid screens before bed", "Limit caffeine after noon", "Regular exercise (but not close to bedtime)", "Relaxation routine"],
        "prevention": ["Consistent sleep schedule", "Good sleep hygiene", "Stress management", "Limit alcohol and caffeine"],
        "related_drugs": ["Zolpidem", "Eszopiclone", "Melatonin", "Doxylamine", "Diphenhydramine"],
        "emergency_signs": ["Insomnia combined with severe depression or suicidal thoughts", "Suspected sleep apnea with oxygen desaturation"],
        "complications": ["Depression and anxiety", "Poor concentration and memory", "Increased accidents", "Reduced quality of life", "Immune suppression"]
    },
    "Pain": {
        "overview": "Pain management encompasses the treatment of acute and chronic pain from various causes including musculoskeletal, neuropathic, visceral, and inflammatory origins.",
        "symptoms": ["Acute: sharp, sudden pain following injury or illness", "Chronic: persistent pain lasting >3 months", "Neuropathic: burning, tingling, shooting pain", "Musculoskeletal: aching, stiffness"],
        "causes": ["Injury or trauma", "Inflammation (arthritis)", "Neuropathy (nerve damage)", "Cancer", "Post-surgical pain", "Fibromyalgia", "Musculoskeletal disorders"],
        "risk_factors": ["Previous injury or surgery", "Chronic disease (arthritis, diabetes)", "Psychological factors (depression, anxiety)", "Sedentary lifestyle", "Obesity"],
        "diagnosis": ["Pain assessment scales (VAS, NRS)", "Detailed history and physical examination", "Imaging (X-ray, MRI, CT)", "Nerve conduction studies", "Diagnostic blocks"],
        "treatment": ["Non-pharmacological: PT, exercise, TENS, acupuncture, CBT", "Non-opioid analgesics: acetaminophen, NSAIDs", "Topical agents: lidocaine patches, capsaicin", "Neuropathic: gabapentinoids, SNRIs, TCAs", "Opioids (for severe pain — last resort, with caution)", "Interventional: nerve blocks, spinal cord stimulation", "Surgery"],
        "lifestyle": ["Regular, gentle physical activity", "Physical therapy", "Heat/cold therapy", "Mind-body techniques (meditation, yoga)", "Good posture and ergonomics", "Maintain healthy weight"],
        "prevention": ["Safe lifting techniques", "Regular exercise and stretching", "Healthy posture", "Adequate calcium and vitamin D", "Injury prevention"],
        "related_drugs": ["Ibuprofen", "Paracetamol", "Naproxen", "Tramadol", "Pregabalin"],
        "emergency_signs": ["Sudden severe chest pain (heart attack)", "Sudden severe abdominal pain (emergency)", "Pain with neurological deficit", "Pain with fever and stiff neck (meningitis)"],
        "complications": ["Chronic pain syndrome", "Depression and anxiety", "Sleep disturbance", "Reduced quality of life", "Opioid dependence (if opioids used)"]
    }
}

# ─── Drug Interaction Database ─────────────────────────────────────
DRUG_INTERACTIONS = {
    ("Lorazepam", "Zolpidem"): {
        "severity": "major",
        "effect": "Enhanced CNS depression, severe respiratory depression, sedation, and potential coma.",
        "mechanism": "Additive CNS depressant effects through GABA potentiation.",
        "management": "Avoid combination. If necessary, use lowest doses and monitor closely.",
        "color": "#dc2626"
    },
    ("Lorazepam", "Sertraline"): {
        "severity": "moderate",
        "effect": "Increased sedation and psychomotor impairment. CNS depression may be enhanced.",
        "mechanism": "Additive CNS depression; sertraline may also inhibit CYP2C19.",
        "management": "Use with caution. Monitor for excessive sedation.",
        "color": "#d97706"
    },
    ("Atorvastatin", "Amoxicillin"): {
        "severity": "minor",
        "effect": "No clinically significant interaction expected.",
        "mechanism": "No known pharmacokinetic or pharmacodynamic interaction.",
        "management": "No special precautions needed.",
        "color": "#059669"
    },
    ("Sertraline", "Sumatriptan"): {
        "severity": "moderate",
        "effect": "Risk of serotonin syndrome (agitation, tachycardia, hyperthermia, muscle rigidity).",
        "mechanism": "Additive serotonergic effects.",
        "management": "Monitor for symptoms of serotonin syndrome. Can use with caution.",
        "color": "#d97706"
    },
    ("Metformin", "Ibuprofen"): {
        "severity": "moderate",
        "effect": "NSAIDs can reduce renal function, increasing metformin accumulation and lactic acidosis risk.",
        "mechanism": "NSAIDs reduce renal blood flow; decreased metformin clearance.",
        "management": "Monitor renal function. Avoid in patients with renal impairment. Short-term use is usually acceptable.",
        "color": "#d97706"
    },
    ("Amlodipine", "Atorvastatin"): {
        "severity": "moderate",
        "effect": "Amlodipine inhibits CYP3A4, potentially increasing atorvastatin plasma levels and myopathy risk.",
        "mechanism": "CYP3A4 inhibition by amlodipine increases atorvastatin bioavailability.",
        "management": "Limit atorvastatin dose to 40mg when used with amlodipine. Monitor for muscle symptoms.",
        "color": "#d97706"
    },
    ("Levothyroxine", "Metformin"): {
        "severity": "minor",
        "effect": "No direct interaction. However, both affect metabolism and weight; monitor thyroid function.",
        "mechanism": "No direct pharmacokinetic interaction.",
        "management": "Monitor thyroid function periodically in diabetic patients.",
        "color": "#059669"
    },
    ("Ibuprofen", "Lorazepam"): {
        "severity": "minor",
        "effect": "No significant pharmacokinetic interaction expected.",
        "mechanism": "Different mechanisms of action.",
        "management": "Monitor for additive GI effects.",
        "color": "#059669"
    },
    ("Amoxicillin", "Metformin"): {
        "severity": "minor",
        "effect": "No significant direct pharmacokinetic interaction.",
        "mechanism": "No known interaction.",
        "management": "Standard precautions for antibiotic use in diabetics (monitor blood glucose).",
        "color": "#059669"
    },
    ("Sertraline", "Ibuprofen"): {
        "severity": "moderate",
        "effect": "Increased risk of bleeding (especially GI bleeding). SSRIs inhibit platelet function.",
        "mechanism": "Additive antiplatelet effects; serotonin depletion in platelets combined with NSAID-induced GI effects.",
        "management": "Avoid combination or add gastroprotective agent (PPI). Monitor for bleeding.",
        "color": "#d97706"
    },
    ("Omeprazole", "Metformin"): {
        "severity": "minor",
        "effect": "No significant interaction. PPIs may slightly increase metformin levels in some individuals.",
        "mechanism": "Omeprazole may inhibit organic cation transporter (OCT1).",
        "management": "Usually no clinically significant issue. Monitor if patient develops GI symptoms.",
        "color": "#059669"
    }
}

# ─── Pharmacy / Availability Data ─────────────────────────────────
PHARMACY_AVAILABILITY = {
    "Lorazepam": {
        "online_pharmacies": [
            {"name": "1mg", "url": "https://www.1mg.com", "note": "Prescription required for upload"},
            {"name": "PharmEasy", "url": "https://pharmeasy.in", "note": "Doctor prescription mandatory"},
            {"name": "Apollo Pharmacy", "url": "https://www.apollopharmacy.in", "note": "In-store or online with Rx"}
        ],
        "generic_available": True,
        "generic_brands": ["Ativan (Wyeth)", "Loraz (generic)"],
        "prescription_required": True,
        "controlled": True,
        "availability_status": "Controlled — In stock at licensed pharmacies with valid prescription",
        "price_range": "₹15–80/tablet",
        "tip": "Requires Schedule H1 prescription. Cannot be purchased without a valid doctor's prescription in India."
    },
    "Metformin": {
        "online_pharmacies": [
            {"name": "1mg", "url": "https://www.1mg.com", "note": "Wide availability, upload Rx"},
            {"name": "PharmEasy", "url": "https://pharmeasy.in", "note": "Available with or without Rx"},
            {"name": "Netmeds", "url": "https://www.netmeds.com", "note": "Upload prescription to order"}
        ],
        "generic_available": True,
        "generic_brands": ["Glycomet (USV)", "Obimet (IPCA)", "Glucophage (Merck)"],
        "prescription_required": True,
        "controlled": False,
        "availability_status": "Widely available across India",
        "price_range": "₹5–25/tablet",
        "tip": "One of the most affordable antidiabetics. Generic versions (Glycomet 500) widely available at all pharmacies."
    },
    "Amlodipine": {
        "online_pharmacies": [
            {"name": "1mg", "url": "https://www.1mg.com", "note": "Very affordable generics"},
            {"name": "PharmEasy", "url": "https://pharmeasy.in", "note": "Bulk packs available"},
            {"name": "Apollo Pharmacy", "url": "https://www.apollopharmacy.in", "note": "Same-day delivery in major cities"}
        ],
        "generic_available": True,
        "generic_brands": ["Amlong (Micro Labs)", "Amlopres (Cipla)", "Stamlo (Dr. Reddy's)"],
        "prescription_required": True,
        "controlled": False,
        "availability_status": "Widely available at all pharmacies",
        "price_range": "₹3–15/tablet",
        "tip": "Very affordable and widely available. Ask for generic (Amlong/Stamlo) for significant cost savings."
    },
    "Atorvastatin": {
        "online_pharmacies": [
            {"name": "1mg", "url": "https://www.1mg.com", "note": "Strong discounts on generics"},
            {"name": "PharmEasy", "url": "https://pharmeasy.in", "note": "Subscribe for monthly refills"},
            {"name": "Netmeds", "url": "https://www.netmeds.com", "note": "Good pricing on 90-day supply"}
        ],
        "generic_available": True,
        "generic_brands": ["Atorva (Zydus)", "Aztor (Sun Pharma)", "Storvas (Ranbaxy/Sun)"],
        "prescription_required": True,
        "controlled": False,
        "availability_status": "Widely available",
        "price_range": "₹5–30/tablet",
        "tip": "Lipitor is the original brand but generic Atorvastatin is equally effective and much cheaper. Ask your doctor for generic."
    },
    "Omeprazole": {
        "online_pharmacies": [
            {"name": "1mg", "url": "https://www.1mg.com", "note": "OTC availability"},
            {"name": "PharmEasy", "url": "https://pharmeasy.in", "note": "No prescription needed for lower doses"},
            {"name": "Apollo Pharmacy", "url": "https://www.apollopharmacy.in", "note": "OTC and Rx versions"}
        ],
        "generic_available": True,
        "generic_brands": ["Omez (Dr. Reddy's)", "Ocid (Cipla)", "Omecip (Cipla)"],
        "prescription_required": False,
        "controlled": False,
        "availability_status": "OTC — Available everywhere",
        "price_range": "₹3–20/capsule",
        "tip": "Available OTC in 10–20mg doses. One of the cheapest and most effective PPIs. Omez 20mg is extremely cost-effective."
    }
}

def get_drug_info(drug_name: str) -> dict:
    """Get drug information by name (case-insensitive partial match)."""
    drug_name_clean = drug_name.strip()
    # Exact match first
    if drug_name_clean in DRUG_KNOWLEDGE:
        return DRUG_KNOWLEDGE[drug_name_clean]
    # Case-insensitive match
    for k, v in DRUG_KNOWLEDGE.items():
        if k.lower() == drug_name_clean.lower():
            return v
    # Partial match
    for k, v in DRUG_KNOWLEDGE.items():
        if drug_name_clean.lower() in k.lower() or k.lower() in drug_name_clean.lower():
            return v
    return None

def get_disease_info(disease_name: str) -> dict:
    """Get disease information by name (case-insensitive)."""
    disease_name_clean = disease_name.strip()
    if disease_name_clean in DISEASE_KNOWLEDGE:
        return DISEASE_KNOWLEDGE[disease_name_clean]
    for k, v in DISEASE_KNOWLEDGE.items():
        if k.lower() == disease_name_clean.lower():
            return v
    for k, v in DISEASE_KNOWLEDGE.items():
        if disease_name_clean.lower() in k.lower() or k.lower() in disease_name_clean.lower():
            return v
    return None

def get_drug_interaction(drug1: str, drug2: str) -> dict:
    """Check interaction between two drugs."""
    for (d1, d2), interaction in DRUG_INTERACTIONS.items():
        if (d1.lower() == drug1.lower() and d2.lower() == drug2.lower()) or \
           (d1.lower() == drug2.lower() and d2.lower() == drug1.lower()):
            return interaction
    return None

def get_all_drug_names() -> list:
    return list(DRUG_KNOWLEDGE.keys())

def get_all_disease_names() -> list:
    return list(DISEASE_KNOWLEDGE.keys())
