from django.db import models

class CustomerQuery(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    subject = models.CharField(max_length=128)
    message = models.TextField()
    category = models.CharField(max_length=64, choices=[])  # Add choices as needed
    created_at = models.DateTimeField(auto_now_add=True)
