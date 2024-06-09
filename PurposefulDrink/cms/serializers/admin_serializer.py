from rest_framework import serializers
from ..models import Herb, Disease, AgeRange, Suitability, SeasonalScore, JobScore, JobPollutionLevelScore

class SeasonalScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonalScore
        fields = '__all__'

class JobScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobScore
        fields = '__all__'

class JobPollutionLevelScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPollutionLevelScore
        fields = '__all__'

class SuitabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Suitability
        fields = '__all__'

class HerbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Herb
        fields = '__all__'

class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'

class AgeRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeRange
        fields = '__all__'
