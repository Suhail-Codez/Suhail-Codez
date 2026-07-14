from rest_framework import serializers
from .models import DrugReview, Prediction, DrugComparison, SavedDiagnosis

class DrugReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugReview
        fields = '__all__'

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'

class DrugComparisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugComparison
        fields = '__all__'

class SavedDiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedDiagnosis
        fields = '__all__'
