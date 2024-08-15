from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    nationality = models.CharField(max_length=20)
    id_number =  models.IntegerField()
    gender = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    health_condition = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", default="avatar/defaultAvatar.png")
    created_at= models.DateField(auto_now_add=True)


    def __str__(self) -> str:
        return self.name
    
class AcademyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    academy_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    logo =  models.ImageField(upload_to="logos/", default="avatar/defaultAvatar.png")
    status = models.CharField(default=False)
    created_at= models.DateField(auto_now_add=True)


    def __str__(self) -> str:
        return self.academy_name