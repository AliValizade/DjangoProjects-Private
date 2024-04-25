from django.urls import path

from . import views

urlpatterns = [
    path('recommend/', views.RecommendHerbsView.as_view(), name='recommend_herbs'),
]
