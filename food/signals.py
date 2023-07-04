from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import Food
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_cart(sender, instance, created , **kwargs):
    if created:
        Food.objects.create(user=instance)
        print('Food created')
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_cart(sender,instance,created, **kwargs):
    if created == False:
        instance.food.save()
        print('Food updated!')