from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.views.admin_views import OrderViewSet, OrderItemsViewSet, DiscountCodeViewSet, ProductViewSet, CartViewSet, CartItemViewSet

app_name = 'shop_admin'

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemsViewSet)
router.register(r'discount-codes', DiscountCodeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]