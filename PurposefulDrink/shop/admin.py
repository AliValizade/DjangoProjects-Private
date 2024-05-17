from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price', 'herb')  # فیلدهایی که می‌خواهید در لیست ادمین نمایش داده شوند
    search_fields = ('name',)  # فیلدهایی که می‌خواهید قابلیت جستجو داشته باشند
    list_filter = ('herb',)  # فیلدهایی که می‌خواهید برای فیلتر کردن استفاده شوند
    ordering = ('name',)  # ترتیب نمایش بر اساس فیلد مشخص شده
