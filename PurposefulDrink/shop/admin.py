from django.contrib import admin
from .models import Order, OrderItems, DiscountCode, Product
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItems
    fields = ['id', 'product', 'price', 'quantity', ]
    # raw_id_fields = ('herb', )
    extra = 0
    min_num = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'updated', 'paid')
    list_filter = ('paid',)
    inlines = (OrderItemInline, )


admin.site.register(DiscountCode)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_herbs')

    def display_herbs(self, obj):
        return ", ".join([herb.name for herb in obj.herbs.all()])
    
    display_herbs.short_description = 'Herbs'


# class CartItemInline(admin.TabularInline):
#     model = CartItem
#     fields = ['id', 'product', 'quantity', ]
#     extra = 0
#     min_num = 1

# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ('id', 'created_at', )
#     inlines = (CartItemInline, )
