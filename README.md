# IDPDR — An Intelligent Disease Prediction and Drug Recommendation Prototype (Using Multiple Approaches of Machine Learning Algorithms)
**MCA Final Year Project** | Django + ML + NLP | Production-Ready

---

## 🚀 Features

| Module | Description |
|--------|-------------|
| 🔬 Disease Diagnosis | 4 ML models (NB, RF, SVM, LR) + ensemble majority vote |
| 💊 Drug Recommendations | Bayesian + VADER weighted scoring (Rating 70% + Sentiment 30%) |
| 📋 Drug Report | 23-field comprehensive drug profile with PDF/CSV export |
| 🤖 Smart AI Recommend | Symptom + demographics → personalised drug recommendations |
| ⚖️ Drug Comparison | Side-by-side drug comparison with 12+ metrics |
| ⚡ Interaction Checker | Multi-drug interaction severity checker (Major/Moderate/Minor) |
| 🏥 Disease Info | Full disease profiles: symptoms, treatment, emergency signs |
| 🛒 Where to Buy | Pharmacy availability + online purchase reference links |
| 💬 Sentiment Analysis | VADER NLP on drug reviews |
| 📊 Analytics Dashboard | Live stats + Chart.js visualisations |
| 🔌 REST API | 17 documented endpoints |
| 🔐 Auth | JWT-ready session auth with role-based access (Admin/User) |

---

## 🛠️ Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **ML Models**: Naive Bayes, Random Forest, SVM, Logistic Regression (scikit-learn)
- **NLP**: VADER Sentiment Analysis (vaderSentiment + NLTK)
- **Frontend**: Vanilla JS SPA, Chart.js 4, Google Fonts (Inter + Syne)
- **Database**: SQLite (dev) / MySQL (production-ready)
- **Theme**: Dark/Light toggle, fully responsive

---

## ⚡ Quick Start

### 1. Clone / Extract
```bash
unzip MediRec_v3.zip -d medirec_v3
cd medirec_v3
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Download NLTK Data
```python
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"
```

### 5. Apply Migrations & Create Superuser
```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
# OR use the management command to seed admin:
python manage.py shell -c "
from django.contrib.auth.models import User
from recommender.models import UserProfile
u, _ = User.objects.get_or_create(username='admin')
u.set_password('admin123'); u.is_staff=True; u.is_superuser=True; u.save()
UserProfile.objects.get_or_create(user=u, defaults={'role':'admin'})
print('Admin created: admin / admin123')
"
```

### 6. Run the Server
```bash
python manage.py runserver
```

### 7. Open in Browser
```
http://127.0.0.1:8000/
```

---

## 📁 Project Structure

```
medirec_v3/
├── backend/
│   ├── config/
│   │   ├── settings.py        # Django settings
│   │   ├── urls.py            # URL routing (17 API + 6 page routes)
│   │   └── wsgi.py
│   ├── recommender/
│   │   ├── models.py          # 6 database models
│   │   ├── views.py           # 17 API view functions
│   │   ├── auth_views.py      # Auth API + page views
│   │   ├── urls.py            # API URL patterns
│   │   ├── admin.py           # Django admin registration
│   │   └── serializers.py
│   ├── templates/
│   │   ├── index.html         # Main SPA (dark/light, 13 pages)
│   │   ├── signin.html        # Sign-in page
│   │   └── register.html      # Registration page
│   ├── manage.py
│   └── requirements.txt
├── models_pkl/
│   ├── naive_bayes.pkl
│   ├── random_forest.pkl
│   ├── svm.pkl
│   ├── logistic_regression.pkl
│   ├── label_encoder.pkl
│   ├── vader.pkl
│   ├── recommendations.json   # Scored drug recommendations
│   ├── symptoms_map.json      # Condition → symptom mapping
│   ├── model_results.json     # Model accuracy scores
│   └── trends.json            # Drug score trend data
└── README.md
```

---

## 🔌 API Reference

Base URL: `http://localhost:8000/api/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health/` | System health + models loaded |
| GET | `/api/conditions/` | All 12 conditions + symptoms |
| POST | `/api/predict/` | 4-model disease diagnosis |
| GET | `/api/recommend/?condition=X` | Top 5 scored drugs |
| GET | `/api/recommend/all/` | Top drugs for all conditions |
| POST | `/api/sentiment/` | VADER review sentiment |
| GET | `/api/compare/?condition=X&drug_a=Y&drug_b=Z` | Drug comparison |
| GET | `/api/dashboard/` | Live stats + chart data |
| GET | `/api/drug/report/?drug=X` | Full 23-field drug report ✨ |
| GET | `/api/drug/search/?q=X` | Drug search by name/generic ✨ |
| GET | `/api/drug/buy/?drug=X` | Availability + pharmacy refs ✨ |
| POST | `/api/interactions/` | Multi-drug interaction check ✨ |
| GET | `/api/disease/?condition=X` | Disease info + emergency signs ✨ |
| POST | `/api/smart-recommend/` | AI personalised recommendation ✨ |
| GET | `/api/reviews/` | Recent drug reviews |
| GET | `/api/predictions/` | Recent prediction history |
| GET | `/api/drug/?drug=X` | Drug detail from reviews |

✨ = New in v3.0

---

## 🗄️ Database Models

| Model | Fields |
|-------|--------|
| `DrugReview` | drug_name, condition, review, rating, sentiment, sentiment_score, compound_score |
| `Prediction` | symptoms, predicted_condition, nb/rf/svm/lr predictions + confidences |
| `DrugComparison` | condition, drug_a, drug_b, winner |
| `UserProfile` | user (FK), role (admin/user), phone, age, gender |
| `SavedDiagnosis` | user (FK), symptoms, condition, top_drug |
| `DrugInteractionCheck` | drugs_checked, interactions_found, severity |
| `SearchLog` | query, search_type, results |

---

## 🔐 Authentication

| Route | Access |
|-------|--------|
| `/` | Authenticated users |
| `/signin/` | Public |
| `/register/` | Public |
| `/admin-dashboard/` | Admin role only |
| `/admin/` | Django superuser |

Default credentials (after setup):
- **Admin**: `admin` / `admin123`

---

## 🏥 Supported Conditions

Anxiety · Asthma · Depression · Diabetes Type 2 · GERD · High Cholesterol · Hypertension · Hypothyroidism · Infection · Insomnia · Migraine · Pain

---

## 💊 Drug Database (v3.0)

Metformin · Ozempic · Lisinopril · Sertraline · Salbutamol · Sumatriptan · Omeprazole · Levothyroxine · Atorvastatin · Amoxicillin

Each drug includes: generic name, brand names, drug class, description, uses, dosage, side effects, contraindications, drug interactions, food interactions, pregnancy/breastfeeding safety, kidney/liver warnings, storage, overdose info, missed dose instructions, alternatives, price estimate, availability, manufacturer, prescription status.

---

## 🎓 Academic Information

- **Project**: MCA Final Year Project
- **Tech**: Python · Django · scikit-learn · NLTK · VADER · Chart.js · Vanilla JS
- **ML Algorithms**: Naive Bayes, Random Forest, SVM, Logistic Regression
- **NLP**: VADER Sentiment Analysis
- **Architecture**: MVC + REST API + SPA Frontend
- **Database**: SQLite (SQLAlchemy-compatible, MySQL-ready)

---

## ⚠️ Disclaimer

IDPDR is strictly for **educational and academic purposes**. All drug and medical information provided by this system is for informational use only and **must not** substitute professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.

---

*IDPDR v1.0 — An Intelligent Disease Prediction and Drug Recommendation Prototype, Built for MCA Final Year Project*
