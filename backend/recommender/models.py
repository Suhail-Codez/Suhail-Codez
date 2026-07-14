from django.db import models
from django.utils import timezone


class DrugReview(models.Model):
    SENTIMENT_CHOICES = [('positive','Positive'),('neutral','Neutral'),('negative','Negative')]

    drug_name       = models.CharField(max_length=200, db_index=True)
    condition       = models.CharField(max_length=200, db_index=True)
    review          = models.TextField()
    rating          = models.FloatField()
    useful_count    = models.IntegerField(default=0)
    sentiment       = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default='neutral')
    sentiment_score = models.FloatField(default=0.0)
    pos_score       = models.FloatField(default=0.0)
    neg_score       = models.FloatField(default=0.0)
    neu_score       = models.FloatField(default=0.0)
    compound_score  = models.FloatField(default=0.0)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Drug Review'

    def __str__(self):
        return f"{self.drug_name} | {self.condition} | {self.rating}/10"


class Prediction(models.Model):
    symptoms            = models.TextField()
    predicted_condition = models.CharField(max_length=200, db_index=True)
    nb_prediction       = models.CharField(max_length=200, blank=True)
    rf_prediction       = models.CharField(max_length=200, blank=True)
    svm_prediction      = models.CharField(max_length=200, blank=True)
    lr_prediction       = models.CharField(max_length=200, blank=True)
    nb_confidence       = models.FloatField(default=0)
    rf_confidence       = models.FloatField(default=0)
    svm_confidence      = models.FloatField(default=0)
    lr_confidence       = models.FloatField(default=0)
    model_used          = models.CharField(max_length=100, default='ensemble')
    created_at          = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Disease Prediction'

    def __str__(self):
        return f"{self.predicted_condition} [{self.created_at.strftime('%Y-%m-%d')}]"


class DrugComparison(models.Model):
    condition   = models.CharField(max_length=200)
    drug_a      = models.CharField(max_length=200)
    drug_b      = models.CharField(max_length=200)
    winner      = models.CharField(max_length=200, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.drug_a} vs {self.drug_b} ({self.condition})"


class UserProfile(models.Model):
    ROLE_CHOICES = [('patient', 'Patient'), ('admin', 'Administrator')]
    user           = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    role           = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    phone          = models.CharField(max_length=20, blank=True)
    age            = models.IntegerField(null=True, blank=True)
    gender         = models.CharField(max_length=10, blank=True)
    bio            = models.CharField(max_length=300, blank=True)
    email_notifications = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    @property
    def is_admin(self):
        return self.role == 'admin'


class SavedDiagnosis(models.Model):
    user        = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='diagnoses')
    symptoms    = models.TextField()
    condition   = models.CharField(max_length=200)
    top_drug    = models.CharField(max_length=200, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.condition}"


class DrugInteractionCheck(models.Model):
    """Stores user drug interaction checks for audit/analytics."""
    drugs_checked   = models.TextField()  # JSON list of drug names
    interactions_found = models.IntegerField(default=0)
    severity        = models.CharField(max_length=20, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Drug Interaction Check'

    def __str__(self):
        return f"Interaction check: {self.drugs_checked[:60]} ({self.created_at.strftime('%Y-%m-%d')})"


class DiagnosisReport(models.Model):
    """
    A complete, persisted Disease Diagnosis Report.

    This is intentionally a separate model from the lightweight
    `SavedDiagnosis` (kept as-is for backward compatibility) because a full
    report needs to capture a snapshot of patient info, confidence score,
    recommended drugs/tests, precautions, lifestyle advice, and notes at the
    moment the report was generated -- so the report a user views/downloads
    later never silently changes if the underlying prediction data changes.
    """
    user                    = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                                                 related_name='diagnosis_reports', null=True, blank=True)
    prediction              = models.ForeignKey('Prediction', on_delete=models.SET_NULL,
                                                 null=True, blank=True, related_name='reports')

    # Patient information (snapshot at time of report generation)
    patient_name            = models.CharField(max_length=200, default='Guest Patient')
    patient_age             = models.IntegerField(null=True, blank=True)
    patient_gender          = models.CharField(max_length=20, blank=True)

    # Clinical content
    symptoms                = models.TextField()
    predicted_disease       = models.CharField(max_length=200)
    confidence_score        = models.FloatField(null=True, blank=True)
    recommended_drugs       = models.JSONField(default=list, blank=True)
    recommended_tests       = models.JSONField(default=list, blank=True)
    precautions             = models.JSONField(default=list, blank=True)
    lifestyle_recommendations = models.JSONField(default=list, blank=True)
    doctor_notes            = models.TextField(blank=True, default=(
        "This report was generated by an AI-assisted recommendation system and is intended "
        "for informational purposes only. It does not constitute a medical diagnosis. "
        "Please consult a licensed physician for confirmation and treatment."
    ))

    created_at              = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Disease Diagnosis Report'

    def __str__(self):
        return f"Diagnosis Report: {self.predicted_disease} for {self.patient_name} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class SearchLog(models.Model):
    """Tracks drug/condition searches for analytics."""
    query       = models.CharField(max_length=300)
    search_type = models.CharField(max_length=50, default='drug')  # drug, condition, symptom
    results     = models.IntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.search_type}: {self.query}"


class Drug(models.Model):
    """
    Admin-manageable drug catalogue entries. This supplements the built-in,
    code-based drug knowledge base (`recommender/drug_database.py`) with
    entries administrators can create/edit/delete at runtime through the
    Admin Dashboard's Drug Database Management page -- both sources are
    merged together when a patient searches for or views a drug report.
    """
    name                    = models.CharField(max_length=200, unique=True, db_index=True)
    generic_name            = models.CharField(max_length=200, blank=True)
    brand_names             = models.CharField(max_length=300, blank=True, help_text="Comma-separated")
    drug_class              = models.CharField(max_length=200, blank=True)
    condition               = models.CharField(max_length=200, blank=True)
    description             = models.TextField(blank=True)
    dosage                  = models.CharField(max_length=300, blank=True)
    side_effects            = models.TextField(blank=True, help_text="Comma-separated")
    contraindications       = models.TextField(blank=True, help_text="Comma-separated")
    price_inr               = models.CharField(max_length=100, blank=True)
    prescription_required   = models.BooleanField(default=True)
    is_active               = models.BooleanField(default=True)
    created_by              = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='drugs_created')
    created_at              = models.DateTimeField(auto_now_add=True)
    updated_at               = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Managed Drug'

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            "generic_name": self.generic_name or self.name,
            "brand_names": [b.strip() for b in self.brand_names.split(',') if b.strip()],
            "drug_class": self.drug_class or "Prescription/OTC Medication",
            "description": self.description or f"{self.name} is a medication used in the treatment of {self.condition or 'the associated condition'}.",
            "uses": [self.condition] if self.condition else [],
            "dosage": {"adult": self.dosage} if self.dosage else {},
            "side_effects": [s.strip() for s in self.side_effects.split(',') if s.strip()],
            "contraindications": [c.strip() for c in self.contraindications.split(',') if c.strip()],
            "drug_interactions": [],
            "food_interactions": [],
            "pregnancy": "Consult a licensed pharmacist or physician.",
            "breastfeeding": "Consult a licensed pharmacist or physician.",
            "kidney_warning": "Consult a licensed pharmacist or physician.",
            "liver_warning": "Consult a licensed pharmacist or physician.",
            "storage": "Store as directed on the package label.",
            "overdose": "Contact emergency services or a poison control center immediately.",
            "missed_dose": "Follow the instructions on your prescription label.",
            "alternatives": [],
            "price_inr": self.price_inr or "Consult pharmacist",
            "prescription_required": self.prescription_required,
            "manufacturer": "Various",
            "availability": "Added via Admin Dashboard",
            "condition": self.condition or "",
        }


class AuditLog(models.Model):
    """
    Records security- and admin-relevant actions across the application:
    logins/logouts, registrations, password changes, role changes, and
    admin CRUD operations. Viewable on the Admin Dashboard's Audit Logs page.
    """
    ACTION_CHOICES = [
        ('login', 'Login'), ('logout', 'Logout'), ('register', 'Register'),
        ('password_change', 'Password Changed'), ('password_reset', 'Password Reset'),
        ('profile_update', 'Profile Updated'), ('role_change', 'Role Changed'),
        ('user_activated', 'User Activated'), ('user_deactivated', 'User Deactivated'),
        ('user_deleted', 'User Deleted'), ('drug_created', 'Drug Created'),
        ('drug_updated', 'Drug Updated'), ('drug_deleted', 'Drug Deleted'),
        ('settings_updated', 'Settings Updated'),
    ]
    user            = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    username_snapshot = models.CharField(max_length=150, blank=True)
    action          = models.CharField(max_length=30, choices=ACTION_CHOICES, db_index=True)
    detail          = models.TextField(blank=True)
    ip_address      = models.CharField(max_length=64, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Audit Log'

    def __str__(self):
        return f"{self.get_action_display()} — {self.username_snapshot} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class SystemSettings(models.Model):
    """Singleton row holding global, admin-editable application settings."""
    allow_registration = models.BooleanField(default=True, help_text="Allow new patients to self-register")
    maintenance_mode    = models.BooleanField(default=False, help_text="Block non-admin logins while enabled")
    site_name           = models.CharField(max_length=100, default='IDPDR')
    support_email       = models.CharField(max_length=200, default='support@idpdr.ai')
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'System Settings'
        verbose_name_plural = 'System Settings'

    def __str__(self):
        return "System Settings"

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
