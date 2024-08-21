from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404

from .models import Review
from academy.models import Program
from account.models import UserProfile
# from publishers.models import Publisher

from django.db.models import Q, F, Count, Avg, Sum, Max, Min
from django.core.paginator import Paginator

from django.contrib import messages
from review.models import Review
from django.contrib.auth.models import User

# Create your views here.


def add_review_view(request:HttpRequest, program_id):
    
    
    if not request.user.is_authenticated:
        messages.error(request, "Only registered user can add review","alert-danger")
        return redirect("account:log_in")

    if request.method == "POST":
        user=User.objects.get(pk=request.user.id)
        if  UserProfile.objects.filter(user=user).first() :
        
            program_object = Program.objects.get(pk=program_id)
            new_review = Review(program=program_object,user=UserProfile.objects.filter(user=user).first(),review=request.POST["comment"],rating=request.POST["rating"])
            
            
            new_review.save()
            messages.success(request, "تمت إضافة تعليقك بنجاح", "alert-success")
        else: 
            messages.error(request, "please complete your profile","red")

        

    return redirect(request.GET['next'])


def delete_review_view(request:HttpRequest, review_id):


    try:
        review = Review.objects.get(pk=review_id)
        program_id=review.program.id

        if not ( request.user.is_staff and request.user.has_perm("programs.delete_review")) and review.user != request.user:
            messages.warning(request, "You can't delete this review","alert-warning")
        else:
            review.delete()
            messages.success(request, "تم حذف التعليق", "alert-success")
    except Exception as e:
        messages.error(request, "فشل حذف التعليق", "alert-danger")


    return redirect("academy:program_detail_view", program_id=program_id)
