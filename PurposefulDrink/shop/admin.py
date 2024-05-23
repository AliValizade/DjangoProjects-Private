from django.contrib import admin
from .models import Order, OrderItems, DiscountCode, Product
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItems
    raw_id_fields = ('herb', )

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ('id', 'user', 'updated', 'paid')
    list_filter = ('paid',)
    inlines = (OrderItemInline, )


admin.site.register(DiscountCode)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
