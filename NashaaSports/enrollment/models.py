from django.db import models
from account.models import UserProfile
from academy.models import Program
class Enrollment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    health_condition = models.TextField()
    identification = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)