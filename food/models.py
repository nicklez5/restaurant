from django.db import models
from django.conf import settings
class Food(models.Model):
    img_url = models.URLField(max_length=500)
    price = models.FloatField()
    name = models.CharField(max_length=100)
# Create your models here.
