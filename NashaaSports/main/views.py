from django.shortcuts import render
from django.http import HttpRequest
from academy.models import Program
from cart.models import Cart
from django.db.models import Avg
from django.db.models import Avg, IntegerField
from django.db.models.functions import Cast
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db.models.functions import ExtractDay, ExtractWeekDay
import math
from account.models import AcademyProfile
from django.db.models import F, Q



def home_view(request:HttpRequest):
    programs = Program.objects.all()
    carts = Cart.objects.filter(user=request.user.id, status='Active').first()
    enrollments = carts.enrollments.all() if carts else []
    print(carts)
    context ={
        "programs":programs,
        "carts":carts,
        "enrollments":enrollments,
    }
    return render(request, "index.html",context)

def programs_view(request:HttpRequest):
    programs = Program.objects.annotate(
    avg_review=Avg(Cast("review__rating", IntegerField())),
    start_days=ExtractDay(F('start_date')),
    end_days=ExtractDay(F('end_date')),).annotate(
    
    duration=ExpressionWrapper(
        (F('end_days') - F('start_days')) / 7,
        output_field=IntegerField()  
    ),

    
    )
    return render(request,"programs.html",{"programs":programs})


def program_detail_view(request:HttpRequest , program_id):
    user = request.user
    programs = Program.objects.get(id=program_id)
    images = programs.programimage_set.all()
    context ={
        "programs":programs,
        "image":images,
        "user":user,
    }
    return render(request, "program_detail.html",context)
def academies_view(request:HttpRequest):
    search_query = request.GET.get('search', '').strip()  

    if search_query:  
        Academies = AcademyProfile.objects.filter(
            Q(academy_name__icontains=search_query) & Q(approved=True)
        )
    else:  
        Academies = AcademyProfile.objects.filter(approved=True)
    return render(request,'academies.html',{"academies":Academies})