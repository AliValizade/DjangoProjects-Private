# shop/serializers.py
from rest_framework import serializers
from ..models import Order, OrderItems, DiscountCode, Product

class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemsSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField(source='get_total_price')

    class Meta:
        model = Order
        fields = '__all__'

class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
