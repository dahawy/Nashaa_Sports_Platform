from django.db import models
from account.models import UserProfile
from academy.models import Program
class ProgramBookmark(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
