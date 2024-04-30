from django.urls import path

from . import views

urlpatterns = [
    path('recommend/', views.RecommendHerbsView.as_view(), name='recommendations'),
    # path('recommendations/', views.HerbRecommendationsView.as_view(), name='recommendations'),
]
