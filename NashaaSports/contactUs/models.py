from django.db import models
class CustomerQuery(models.Model):
    class QueryCategory(models.TextChoices):
        Complaint = 'Complaint', 'شكوى'
        Query = 'Query' , 'استفسار'
        Suggestion= 'Suggestion' , 'اقتراح'
    class StatusOfMessage(models.TextChoices):
        Open = 'Open', 'مفتوح'
        Closed = 'Closed' , 'مغلق'
    class SenderType(models.TextChoices):
        Academy = 'Academy', 'أكاديمية'
        Individual = 'Individual' , 'فرد'

    name = models.CharField(max_length=128)
    status = models.CharField(choices=StatusOfMessage.choices, default=StatusOfMessage.Open)
    sender_type = models.CharField(choices=SenderType.choices, default=SenderType.Individual)
    email = models.EmailField()
    subject = models.CharField(max_length=128)
    message = models.TextField()
    category = models.CharField(choices=QueryCategory.choices, default= QueryCategory.Query) 
    created_at = models.DateTimeField(auto_now_add=True)
