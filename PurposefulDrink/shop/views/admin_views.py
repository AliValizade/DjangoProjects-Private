from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Order, OrderItems, DiscountCode, Product, Cart, CartItem
from ..serializers.admin_serializer import OrderSerializer, OrderItemsSerializer, DiscountCodeSerializer, ProductSerializer, CartSerializer, CartItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemsViewSet(viewsets.ModelViewSet):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer

class DiscountCodeViewSet(viewsets.ModelViewSet):
    queryset = DiscountCode.objects.all()
    serializer_class = DiscountCodeSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().prefetch_related('cart_items')
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['name', 'herbs']
    search_fields = ['name']
    filterset_fields = ['herbs', 'price', 'type']

    def get_serializer_context(self):
        return {'request': self.request}

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all().prefetch_related('items__product')
    serializer_class = CartSerializer
    permission_classes = [IsAdminUser]

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer