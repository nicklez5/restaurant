from django.db import models
from django.conf import settings
from food.models import Food
class CartItem(models.Model):
    cart = models.ForeignKey('Cart',on_delete=models.CASCADE,related_name='order_items')
    product = models.ForeignKey(Food,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
class Cart(models.Model):
    order_user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    total = models.FloatField(default=0.00)
    ordered_items = models.ManyToManyField(Food,related_name='carts')

    

# Create your models here.
