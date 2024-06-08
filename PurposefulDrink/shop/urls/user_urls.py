from django.urls import path
from ..views import user_views



urlpatterns = [
    path('', user_views.CmsView.as_view(), name='cmsview')
]
