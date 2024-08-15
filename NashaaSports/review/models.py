from django.db import models
from academy.models import Program
from account.models import UserProfile
class Review(models.Model):
    class RatingChoices(models.IntegerChoices):
        STAR1 = 1, "One Star"
        STAR2 = 2, "Two Stars"
        STAR3 = 3, "Three Stars"
        STAR4 = 4, "Four Stars"
        STAR5 = 5, "Five Stars"
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.CharField(choices=RatingChoices.choices)  
    created_at = models.DateTimeField(auto_now_add=True)
