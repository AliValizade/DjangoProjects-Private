from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Herb, Disease, AgeRange, Suitability, Post, SeasonalScore, JobScore, JobPollutionLevelScore
from ..serializers import HerbSerializer, DiseaseSerializer, AgeRangeSerializer, SuitabilitySerializer, PostSerializer, SeasonalScoreSerializer, JobScoreSerializer, JobPollutionLevelScoreSerializer


class HerbViewSet(viewsets.ModelViewSet):
    queryset = Herb.objects.all().prefetch_related('seasonal_scores', 'job_scores', 'pollution_scores', 'suitability_herb', 'inappropriate_age_ranges', 'interaction_herb')
    serializer_class = HerbSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['name', 'temperament']
    search_fields = ['name']
    # filterset_fields = ['']

class DiseaseViewSet(viewsets.ModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [IsAdminUser]

class AgeRangeViewSet(viewsets.ModelViewSet):
    queryset = AgeRange.objects.all()
    serializer_class = AgeRangeSerializer
    permission_classes = [IsAdminUser]

class SuitabilityViewSet(viewsets.ModelViewSet):
    queryset = Suitability.objects.select_related('herb', 'disease').all()
    serializer_class = SuitabilitySerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['disease_id', 'herb_id', 'score', 'alert_states']
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminUser]

# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAdminUser]

# class VoteViewSet(viewsets.ModelViewSet):
#     queryset = Vote.objects.all()
#     serializer_class = VoteSerializer
#     permission_classes = [IsAdminUser]

class SeasonalScoreViewSet(viewsets.ModelViewSet):
    queryset = SeasonalScore.objects.select_related('herb').all()
    serializer_class = SeasonalScoreSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['herb_id', 'score', 'allergy_aggravator']

class JobScoreViewSet(viewsets.ModelViewSet):
    queryset = JobScore.objects.select_related('herb').all()
    serializer_class = JobScoreSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['herb_id', 'score']

class JobPollutionLevelScoreViewSet(viewsets.ModelViewSet):
    queryset = JobPollutionLevelScore.objects.select_related('herb').all()
    serializer_class = JobPollutionLevelScoreSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['herb_id', 'score']
