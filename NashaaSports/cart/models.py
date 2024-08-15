from django.db import models
from account.models import UserProfile
from enrollment.models import Enrollment

class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    status = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[])