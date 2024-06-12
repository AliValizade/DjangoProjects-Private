from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from shop.views.admin_views import OrderViewSet, OrderItemsViewSet, DiscountCodeViewSet, ProductViewSet, CartViewSet, CartItemViewSet

app_name = 'shop_admin'

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemsViewSet)
router.register(r'discount-codes', DiscountCodeViewSet)
router.register(r'products', ProductViewSet, basename='product')
router.register(r'carts', CartViewSet)
# router.register(r'cart-items', CartItemViewSet)

cart_items_router = NestedDefaultRouter(router, 'carts', lookup='cart')
cart_items_router.register(r'items', CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + cart_items_router.urls