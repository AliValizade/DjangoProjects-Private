from django.urls import path
from .views import recommend_herbs

urlpatterns = [
    path('', recommend_herbs, name='index'),
    path('recommend/', recommend_herbs, name='recommend_herbs'),
]
