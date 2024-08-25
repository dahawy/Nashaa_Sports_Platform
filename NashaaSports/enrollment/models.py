from django.db import models
from account.models import UserProfile
from academy.models import Program
from cart.models import Cart
from academy.models import TimeSlot
class Enrollment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='enrollments', blank=True, null=True)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='enrollments', blank=True, null=True) 
    first_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    health_condition = models.TextField(blank=True, null=True)
    id_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
