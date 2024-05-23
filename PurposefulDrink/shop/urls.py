from django.urls import path
from . import views
app_name = 'shop'

urlpatterns = [
    path('', views.ShopView.as_view(), name='shop'),
    path('recommend/', views.RecommendProductsView.as_view(), name='recommended_products')
]
