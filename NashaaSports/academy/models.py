from django.db import models
from account.models import AcademyProfile

class Branch(models.Model):
    academy = models.ForeignKey(AcademyProfile, on_delete=models.CASCADE)
    branch_name = models.CharField(max_length=128)
    branch_location = models.CharField(max_length=64)
    register_no = models.CharField(max_length=64)

class Program(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    program_name = models.CharField(max_length=255)
    description = models.TextField()
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    no_of_seats = models.IntegerField()
    age_group = models.CharField(max_length=255)
class Coach(models.Model):
    id = models.UUIDField(primary_key=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    birth_date = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=32)
    experience = models.IntegerField()
    nationality = models.CharField(max_length=64)
    gender = models.CharField(max_length=32)
    avatar = models.ImageField(upload_to='coach_avatars/')
    created_at = models.DateTimeField(auto_now_add=True)

class TimeSlot(models.Model):
    id = models.UUIDField(primary_key=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

class ProgramImage(models.Model):
    id = models.UUIDField(primary_key=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='program_images/')

class ProgramVideo(models.Model):
    id = models.UUIDField(primary_key=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    video = models.FileField(upload_to='program_videos/')


