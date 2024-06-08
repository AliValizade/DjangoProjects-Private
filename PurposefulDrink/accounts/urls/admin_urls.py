from django.urls import path, include
from ..views.admin_views import UserViewSet
from rest_framework.routers import DefaultRouter

from ..views import user_views


app_name = 'accounts_admin'

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', user_views.ObtainTokenByPhoneNumber.as_view(), name='login'),
]
