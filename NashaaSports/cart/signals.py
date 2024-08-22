from django.db.models.signals import post_save
from django.dispatch import receiver
from enrollment.models import Enrollment
from cart.models import Cart

@receiver(post_save, sender=Enrollment)
def create_cart_for_enrollment(sender, instance, created, **kwargs):
    if created:
        # Check if the user already has an active cart, if not create a new one
        cart, created_cart = Cart.objects.get_or_create(user=instance.user, status=Cart.CartStatus.Active)
        
        # Link the enrollment to the cart
        instance.cart = cart
        instance.save()