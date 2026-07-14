# IDPDR — An Intelligent Disease Prediction and Drug Recommendation Prototype — Quick Setup Guide

## ✅ Step-by-Step (Windows)

Open Command Prompt / PowerShell in the extracted folder:

```bat
cd MediRec_v3_Fixed\medirec_enhanced\backend

:: Create virtual environment
python -m venv venv
venv\Scripts\activate

:: Install dependencies
pip install -r requirements.txt

:: Download NLTK data (one-time)
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"

:: Setup database
python manage.py migrate

:: Create admin user  <-- IMPORTANT, run this every time after migrate
python manage.py seed_admin

:: Start server
python manage.py runserver
```

Then open: **http://127.0.0.1:8000**

Login: `admin` / `admin123`

---

## ❓ Login Not Working?

Run this to reset the admin password:
```bat
python manage.py seed_admin
```

Or manually via Django shell:
```bat
python manage.py shell
```
```python
from django.contrib.auth.models import User
from recommender.models import UserProfile
u, _ = User.objects.get_or_create(username='admin')
u.set_password('admin123')
u.is_active = True
u.save()
UserProfile.objects.get_or_create(user=u, defaults={'role': 'admin'})
print("Done! Login: admin / admin123")
exit()
```

---

## 📁 Folder Structure
```
medirec_enhanced/
  backend/          ← cd HERE before running manage.py
    manage.py
    config/
    recommender/
    templates/
  models_pkl/       ← ML model files
  README.md
  SETUP.md
```
