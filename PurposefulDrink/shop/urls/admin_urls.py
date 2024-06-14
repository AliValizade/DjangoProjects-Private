from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from shop.views.admin_views import CartViewSet, OrderViewSet, OrderItemsViewSet, DiscountCodeViewSet, ProductViewSet

app_name = 'shop_admin'

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemsViewSet)
router.register(r'discount-codes', DiscountCodeViewSet)
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')

# cart_items_router = NestedDefaultRouter(router, 'carts', lookup='cart')
# cart_items_router.register(r'items', CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('', include(router.urls)),
    # path('cart/', CartAPIView.as_view(), name='cart'),
]