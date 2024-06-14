from rest_framework import serializers
from django.db import transaction

from accounts.models import User
from ..models import Order, OrderItems, DiscountCode, Product
from accounts.serializers.admin_serializer import UserAdminSerializer


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'type', 'price']

class OrderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullname', 'email']
        
class OrderItemsSerializer(serializers.ModelSerializer):
    product = OrderProductSerializer()
    class Meta:
        model = OrderItems
        fields = ['id', 'product', 'quantity', 'price']

class OrderItemsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['product', 'quantity', 'price']

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemsCreateSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'paid', 'items', 'discount']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItems.objects.create(order=order, **item_data)
        return order
    
class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['paid']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemsSerializer(many=True)
    user = OrderUserSerializer()
    class Meta:
        model = Order
        fields = ['id', 'user', 'paid', 'created', 'updated', 'items', 'discount']



# class CartProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'price', ]

# class UpdateCartItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CartItem
#         fields = ['quantity', ]

# class AddCartItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CartItem
#         fields = ['id', 'product', 'quantity', ]

#     def create(self, validated_data):
#         cart_id = self.context['cart_pk']
#         product = validated_data.get('product')
#         quantity = validated_data.get('quantity')

#         try:
#             cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product.id)
#             cart_item.quantity += quantity
#             cart_item.save()
#         except CartItem.DoesNotExist:
#             cart_item = CartItem.objects.create(cart_id=cart_id, **validated_data)

#         self.instance = cart_item
#         return cart_item

# class CartItemSerializer(serializers.ModelSerializer):
#     product = CartProductSerializer(read_only=True)
#     item_total = serializers.SerializerMethodField()
#     class Meta:
#         model = CartItem
#         fields = ['id', 'product', 'quantity', 'item_total', ]

#     def get_item_total(self, cart_item):
#         return cart_item.quantity * cart_item.product.price

# class CartSerializer(serializers.ModelSerializer):
#     items = CartItemSerializer(many=True, read_only=True)
#     total_price = serializers.SerializerMethodField()
#     class Meta:
#         model = Cart
#         fields = ['id', 'items', 'total_price', ]
#         read_only_fields = ['id', ]

#     def get_total_price(self, cart):
#         return sum([item.quantity * item.product.price for item in cart.items.all()])


# class OrderCreateSerializer(serializers.Serializer):
#     pass
    # cart_id = serializers.UUIDField()

    # def validate_cart_id(self, cart_id):
    #     if not Cart.objects.filter(id=cart_id).exists():
    #         raise serializers.ValidationError('There is no cart with this cart id.')
    #     if CartItem.objects.filter(cart_id=cart_id).count() == 0:
    #         raise serializers.ValidationError('Your cart is Empty, Please add some products to cart.')
    #     return cart_id

    # def save(self, **kwargs):
    #     with transaction.atomic():
    #         cart_id = self.validated_data['cart_id']
    #         user_id = self.context['user_id']
    #         user = User.objects.get(id=user_id)

    #         order = Order()
    #         order.user = user
    #         order.save()

    #         cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)

    #         order_items = [
    #             OrderItems(
    #                 order = order,
    #                 product_id = cart_item.product_id,
    #                 quantity = cart_item.quantity,
    #                 price = cart_item.product.price,
    #             ) for cart_item in cart_items
    #         ]
            
    #         OrderItems.objects.bulk_create(order_items)

    #         Cart.objects.get(id=cart_id).delete()

    #         return order

