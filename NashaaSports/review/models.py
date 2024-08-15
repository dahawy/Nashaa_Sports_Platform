from django.db import models
from academy.models import Program
from account.models import UserProfile
class Review(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.CharField(max_length=20, choices=[])  # Add choices as needed
    created_at = models.DateTimeField(auto_now_add=True)
