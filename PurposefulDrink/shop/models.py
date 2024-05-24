from django.db import models
from django.contrib.auth import get_user_model
from cms.models import Herb
from django.core.validators import MinValueValidator, MaxValueValidator
# from cms.models import Herb 
'''
for orders and cart and payment. 

'''
class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_order')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    discount = models.IntegerField(blank=True, null=True, default=None)

    class Meta:
        ordering = ('paid', '-updated')

    def __str__(self):
        return f'{self.user} - {self.id}'

    def get_total_price(self):
        total = sum(item.get_total_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount / 100) *total
            return int(total - discount_price)
        return total



class OrderItems(models.Model):
    TYPE_CHOICE = [
    ('دمنوش', 'دمنوش'),
    ('بسته', 'بسته'),
    ('فله', 'فله')
    ]
    type = models.CharField(max_length=6, choices=TYPE_CHOICE, default='دمنوش')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='item')
    herb = models.ForeignKey(Herb, on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.order} - {self.herb}'

    def get_total_cost(self):
        return self.price * self.quantity

class DiscountCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    valid_from = models.DateTimeField(null=True)
    valid_till = models.DateTimeField(null=True)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)])
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code
    

class Product(models.Model):
    TYPE_CHOICE = [
        ('دمنوش', 'دمنوش'),
        ('بسته', 'بسته'),
        ('فله', 'فله')
    ]
    name = models.CharField(max_length=30)
    herbs = models.ManyToManyField(Herb, related_name='products')
    price = models.IntegerField()
    description = models.TextField()
    type = models.CharField(max_length=6, choices=TYPE_CHOICE, default='دمنوش')

    def __str__(self):
        return self.name