from django.db import models

class CustomerQuery(models.Model):
    class QueryCategory(models.TextChoices):
        Complaint = 'Complaint', 'شكوى'
        Query = 'Query' , 'استفسار'
        Suggestion= 'Suggestion' , 'اقتراح'

    name = models.CharField(max_length=128)
    email = models.EmailField()
    subject = models.CharField(max_length=128)
    message = models.TextField()
    category = models.CharField(choices=QueryCategory.choices, default= QueryCategory.Query) 
    created_at = models.DateTimeField(auto_now_add=True)
