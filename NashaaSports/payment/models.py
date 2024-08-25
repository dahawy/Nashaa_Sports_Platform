from django.db import models
from cart.models import Cart

class Payment(models.Model):

    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='payment')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    status = models.BooleanField(default=False)