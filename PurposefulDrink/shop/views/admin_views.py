# shop/api_views.py
from rest_framework import generics
from ..models import Order, OrderItems, DiscountCode, Product
from ..serializers.admin_serializer import OrderSerializer, OrderItemsSerializer, DiscountCodeSerializer, ProductSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemsListCreateView(generics.ListCreateAPIView):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer

class OrderItemsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer

class DiscountCodeListCreateView(generics.ListCreateAPIView):
    queryset = DiscountCode.objects.all()
    serializer_class = DiscountCodeSerializer

class DiscountCodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DiscountCode.objects.all()
    serializer_class = DiscountCodeSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
