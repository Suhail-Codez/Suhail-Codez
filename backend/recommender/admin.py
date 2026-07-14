from django.contrib import admin
from .models import (DrugReview, Prediction, DrugComparison, UserProfile, SavedDiagnosis,
                      DrugInteractionCheck, SearchLog, DiagnosisReport)

@admin.register(DrugReview)
class DrugReviewAdmin(admin.ModelAdmin):
    list_display = ['drug_name', 'condition', 'rating', 'sentiment', 'compound_score', 'created_at']
    list_filter = ['sentiment', 'condition']
    search_fields = ['drug_name', 'condition', 'review']
    ordering = ['-created_at']

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['predicted_condition', 'symptoms', 'model_used', 'created_at']
    list_filter = ['predicted_condition', 'model_used']
    search_fields = ['symptoms', 'predicted_condition']
    ordering = ['-created_at']

@admin.register(DrugComparison)
class DrugComparisonAdmin(admin.ModelAdmin):
    list_display = ['drug_a', 'drug_b', 'condition', 'winner', 'created_at']
    list_filter = ['condition']
    ordering = ['-created_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'age', 'gender', 'created_at']
    list_filter = ['role', 'gender']

@admin.register(SavedDiagnosis)
class SavedDiagnosisAdmin(admin.ModelAdmin):
    list_display = ['user', 'condition', 'top_drug', 'created_at']
    list_filter = ['condition']
    search_fields = ['user__username', 'condition']

@admin.register(DrugInteractionCheck)
class DrugInteractionCheckAdmin(admin.ModelAdmin):
    list_display = ['drugs_checked', 'interactions_found', 'severity', 'created_at']
    list_filter = ['severity']

@admin.register(DiagnosisReport)
class DiagnosisReportAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'predicted_disease', 'confidence_score', 'user', 'created_at']
    list_filter = ['predicted_disease']
    search_fields = ['patient_name', 'predicted_disease', 'symptoms']
    ordering = ['-created_at']

@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ['query', 'search_type', 'results', 'created_at']
    list_filter = ['search_type']
