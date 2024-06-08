from django.urls import path
from ..views.admin_views import OrderListCreateView, OrderDetailView, OrderItemsListCreateView, OrderItemsDetailView, DiscountCodeListCreateView, DiscountCodeDetailView, ProductListCreateView, ProductDetailView

app_name = 'shop_admin'

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order-items/', OrderItemsListCreateView.as_view(), name='orderitems-list-create'),
    path('order-items/<int:pk>/', OrderItemsDetailView.as_view(), name='orderitems-detail'),
    path('discount-codes/', DiscountCodeListCreateView.as_view(), name='discountcode-list-create'),
    path('discount-codes/<int:pk>/', DiscountCodeDetailView.as_view(), name='discountcode-detail'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]
