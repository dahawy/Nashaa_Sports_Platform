from django.db import models
from account.models import UserProfile
from enrollment.models import Enrollment

class Cart(models.Model):
    class CartStatus(models.TextChoices):
        Active = 'Active', 'نشط'
        Paid = 'Paid' , 'مدفوع'
        Cancelled = 'Cancelled' , 'ملغي'

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    status = models.CharField(choices=CartStatus.choices, default= CartStatus.Active)
    created_at = models.DateTimeField(auto_now_add=True)

