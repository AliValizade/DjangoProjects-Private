from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.admin_views import HerbViewSet, DiseaseViewSet, AgeRangeViewSet, SuitabilityViewSet, PostViewSet, SeasonalScoreViewSet, JobScoreViewSet, JobPollutionLevelScoreViewSet

app_name = 'cms_admin'

router = DefaultRouter()
router.register(r'herbs', HerbViewSet)
router.register(r'diseases', DiseaseViewSet)
router.register(r'age-ranges', AgeRangeViewSet)
router.register(r'suitabilities', SuitabilityViewSet)
router.register(r'posts', PostViewSet)
# router.register(r'comments', CommentViewSet)
# router.register(r'votes', VoteViewSet)
router.register(r'seasonal-scores', SeasonalScoreViewSet)
router.register(r'job-scores', JobScoreViewSet)
router.register(r'job-pollution-scores', JobPollutionLevelScoreViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]