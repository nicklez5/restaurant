from django.db.models.signals import post_save 
from django.conf import settings
from django.dispatch import receiver
from .models import Cart

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
        print('Canvas created!')

#post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_cart(sender, instance, created, **kwargs):
    if created == False:
        instance.cart.save()
        print('Canvas updated!')