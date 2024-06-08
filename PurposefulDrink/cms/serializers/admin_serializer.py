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
    # seasonal_scores = SeasonalScoreSerializer(many=True)
    # job_scores = JobScoreSerializer(many=True)
    # pollution_scores = JobPollutionLevelScoreSerializer(many=True)
    # suitability_herb = SuitabilitySerializer(many=True)
    class Meta:
        model = Herb
        fields = '__all__'

    # def create(self, validated_data):
    #     seasonal_scores_data = validated_data.pop('seasonal_scores')
    #     job_scores_data = validated_data.pop('job_scores')
    #     pollution_scores_data = validated_data.pop('pollution_scores')
    #     suitability_data = validated_data.pop('suitability_herb')

    #     herb = Herb.objects.create(**validated_data)

    #     for score_data in seasonal_scores_data:
    #         SeasonalScore.objects.create(herb=herb, **score_data)

    #     for score_data in job_scores_data:
    #         JobScore.objects.create(herb=herb, **score_data)

    #     for score_data in pollution_scores_data:
    #         JobPollutionLevelScore.objects.create(herb=herb, **score_data)

    #     for suitability in suitability_data:
    #         Suitability.objects.create(herb=herb, **suitability)
    #     herb = Herb(**validated_data)
    #     herb.save()

    #     return herb

    # def update(self, instance, validated_data):
    #     seasonal_scores_data = validated_data.pop('seasonal_scores')
    #     job_scores_data = validated_data.pop('job_scores')
    #     pollution_scores_data = validated_data.pop('pollution_scores')
    #     suitability_data = validated_data.pop('suitability_herb')

    #     instance.name = validated_data.get('name', instance.name)
    #     instance.herb_flavor = validated_data.get('herb_flavor', instance.herb_flavor)
    #     instance.temperament = validated_data.get('temperament', instance.temperament)
    #     instance.save()

    #     instance.seasonal_scores.all().delete()
    #     for score_data in seasonal_scores_data:
    #         SeasonalScore.objects.create(herb=instance, **score_data)

    #     instance.job_scores.all().delete()
    #     for score_data in job_scores_data:
    #         JobScore.objects.create(herb=instance, **score_data)

    #     instance.pollution_scores.all().delete()
    #     for score_data in pollution_scores_data:
    #         JobPollutionLevelScore.objects.create(herb=instance, **score_data)

    #     instance.suitability_herb.all().delete()
    #     for suitability in suitability_data:
    #         Suitability.objects.create(herb=instance, **suitability)

    #     return instance

class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'

class AgeRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeRange
        fields = '__all__'
