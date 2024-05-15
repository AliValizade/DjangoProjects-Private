from django.urls import path

from . import views

urlpatterns = [
    path('recommend/', views.RecommendHerbsView.as_view(), name='recommendations'),
    # path('ajax/search-diseases/', views.ajax_search_view, name='ajax_search_diseases'),
]
