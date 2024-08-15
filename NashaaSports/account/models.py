from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    class Gender(models.TextChoices):
        Male = 'Male', 'ذكر'
        Female = 'Female' , 'أنثى'
    class Nationality(models.TextChoices):
        EGYPTIAN = 'EG', 'مصري'
        SAUDI = 'SA', 'سعودي'
        ALGERIAN = 'DZ', 'جزائري'
        EMIRATI = 'AE', 'إماراتي'
        AMERICAN = 'US', 'أمريكي'
        IRAQI = 'IQ', 'عراقي'
        JORDANIAN = 'JO', 'أردني'
        BRITISH = 'GB', 'بريطاني'
        KUWAITI = 'KW', 'كويتي'
        LEBANESE = 'LB', 'لبناني'
        LIBYAN = 'LY', 'ليبي'
        MOROCCAN = 'MA', 'مغربي'
        OMANI = 'OM', 'عماني'
        PALESTINIAN = 'PS', 'فلسطيني'
        QATARI = 'QA', 'قطري'
        SYRIAN = 'SY', 'سوري'
        SUDANESE = 'SD', 'سوداني'
        TUNISIAN = 'TN', 'تونسي'
        YEMENI = 'YE', 'يمني'
        BAHRAINI = 'BH', 'بحريني'
        SOMALI = 'SO', 'صومالي'
        MAURITANIAN = 'MR', 'موريتاني'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    nationality = models.CharField(choices=Nationality.choices, default=Nationality.SAUDI )
    id_number =  models.IntegerField()
    gender = models.CharField(choices=Gender.choices)
    birth_date = models.DateField()
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
    approved = models.BooleanField(default=False)
    created_at= models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.academy_name