from django.db.models.signals import post_save
from django.contrib.auth.models import User 
from django.dispatch import receiver
from .models import Cart, Order, OrderItem


@receiver(signal=post_save, sender=User)
def createCart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@receiver(signal=post_save, sender=Order)
def clearCart(sender, instance, created, *args, **kwargs):
    if created:
        for cartitem in instance.user.cart.cart_items.all():
            OrderItem.objects.create(
                order=instance,
                menu_item = cartitem.menu_item,
                quantity=cartitem.quantity
            )
            cartitem.delete()