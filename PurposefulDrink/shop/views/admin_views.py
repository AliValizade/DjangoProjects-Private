from django.db.models import Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Order, OrderItems, DiscountCode, Product
from ..serializers.admin_serializer import OrderCreateSerializer, OrderSerializer, OrderItemsSerializer, OrderUpdateSerializer, ProductSerializer, DiscountCodeSerializer 

class OrderViewSet(viewsets.ModelViewSet):
    # http_method_names = ['get', 'post', 'patch', 'delete', 'options', 'head']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = Order.objects.prefetch_related(
            Prefetch(
                'items',
                queryset=OrderItems.objects.select_related('product'),
            )
        ).select_related('user').all()

        user = self.request.user

        if user.is_staff:
            return queryset
        return queryset.filter(user_id=user.id)
    
    def get_serializer_class(self):
        # if self.request.method == 'POST':
        #     return OrderCreateSerializer
        # if self.request.method == 'PATCH':
        #     return OrderUpdateSerializer 
        # return OrderSerializer
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OrderUpdateSerializer
        return OrderSerializer
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
    
    def create(self, request, *args, **kwargs):
        create_order_serializer = OrderCreateSerializer(data=request.data, context={'user_id': self.request.user.id})
        create_order_serializer.is_valid(raise_exception=True)
        created_order = create_order_serializer.save()

        serializer = OrderSerializer(created_order)

        return Response(serializer.data)
        
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
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(user=request.user)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user, paid=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# class CartAPIView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request, *args, **kwargs):
#         serializer = OrderCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             order = serializer.save(user=request.user)
#             return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CartViewSet(viewsets.ModelViewSet):
#     serializer_class = CartSerializer
#     permission_classes = [IsAdminUser]
#     queryset = Cart.objects.all().prefetch_related('items__product')

# class CartItemViewSet(viewsets.ModelViewSet):
#     http_method_names = ['get', 'post', 'patch', 'delete']
#     def get_queryset(self):
#         cart_pk = self.kwargs['cart_pk']
#         return CartItem.objects.select_related('product').filter(cart_id=cart_pk).all()
    
#     def get_serializer_class(self):
#         if self.request.method == 'POST':   
#             return AddCartItemSerializer
#         elif self.request.method == 'PATCH':
#             return UpdateCartItemSerializer
#         return CartItemSerializer

#     def get_serializer_context(self):
#         return {'cart_pk': self.kwargs['cart_pk']}
    