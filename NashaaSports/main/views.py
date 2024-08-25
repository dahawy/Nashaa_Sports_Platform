from django.shortcuts import render, redirect
from django.http import HttpRequest
from academy.models import Program,Branch
from cart.models import Cart
from account.models import User, UserProfile, AcademyProfile
from django.db.models import Avg
from django.db.models import Avg, IntegerField,FloatField
from django.db.models.functions import Cast ,Round
from django.db.models import F, ExpressionWrapper
from django.db.models.functions import ExtractDay
import math
from django.db.models import F, Q




def home_view(request:HttpRequest):

    programs = Program.objects.all()
    if request.user.is_authenticated:
        user = UserProfile.objects.get(user_id=request.user.id)
        carts = Cart.objects.filter(user=user, status='Active').first()
        enrollments = carts.enrollments.all() if carts else []
    else:
        carts = Cart.objects.filter(user=request.user.id, status='Active').first()
        enrollments = carts.enrollments.all() if carts else []


    context ={
        "programs":programs,
        "carts":carts,
        "enrollments":enrollments,
    }
    return render(request, "index.html",context)


def programs_view(request:HttpRequest):
    search_query = request.GET.get('search', '')
    price_filter = request.GET.get('price', '')
    age_filter = request.GET.get('age', '')
    length_filter = request.GET.get('length', '')
    city_filter = request.GET.get('city', '')
    category_filter = request.GET.get('category', '')
    programs = Program.objects.annotate(
    avg_rating=Round(Avg(Cast('review__rating', FloatField())), 1), # Calculate the average rating for each program
    start_days=ExtractDay(F('start_date')),
    end_days=ExtractDay(F('end_date'))
        ).annotate(
    duration =ExpressionWrapper(
    ExtractDay(F('end_date') - F('start_date')) / 7,
    output_field=IntegerField()
            )
    )
    if length_filter == 'short':
        programs = programs.filter(duration__gte=1, duration__lte=4)
    elif length_filter == 'medium':
        programs = programs.filter(duration__gte=5, duration__lte=12)
    elif length_filter == 'long':
        programs = programs.filter(duration__gte=13)
    if age_filter=='children':
        min_age=1
        max_age=12
    elif age_filter=='teens':
        min_age=13
        max_age=17
    elif age_filter=='adults':
        min_age=18
        max_age=100
    else:
        min_age = 1  # Default minimum age
        max_age = 100 
    

    programs = programs.filter(
    Q(is_available=True)&
    Q(is_active=True)&
    Q(admin_activtion=True)&
    Q(program_name__icontains=search_query)&
    Q(branch__branch_city__icontains=city_filter)&
    Q(sport_category__icontains=category_filter)&
    Q(min_age__lte=max_age) &  # Program's min_age should be less than or equal to the selected max_age
    Q(max_age__gte=min_age) 

            )

    if price_filter == 'high_to_low':
        programs = programs.order_by('-fees')  # Assuming 'fees' is the price field
    elif price_filter == 'low_to_high':
        programs = programs.order_by('fees')
   
    
    price_choices = [
        ('high_to_low', 'من الاعلى الى الاقل'),
        ('low_to_high', 'من الاقل الى الاعلى'),
    ]

    age_choices = [
        ('children', '1-12'),
        ('teens', '13-17'),
        ('adults', '18 فأكثر'),
    ]

    length_choices = [
        ('short', '1-4 اسبوع'),
        ('medium', "5-12 اسبوع"),
        ('long', '13 فأكثر'),
    ]
    context={'age_choices':age_choices,'length_choices':length_choices,'price_choices':price_choices,'programs':programs,"sport_choices":Program.SportChoices.choices,'cities':Branch.Cities.choices}
    return render(request,"programs.html",context)


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



def mode_view(request:HttpRequest, mode):

    response = redirect(request.GET.get("next", "/"))

    if mode == "light":
        response.set_cookie("mode", "light")
    elif mode == "dark":
        response.set_cookie("mode", "dark")
    return response