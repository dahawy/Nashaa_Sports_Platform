from django.shortcuts import render, redirect
from django.http import HttpRequest
from account.models import UserProfile
from django.contrib import messages
from .models import ProgramBookmark, Program
from django.contrib.auth.models import User
from django.core.paginator import Paginator

# Create your views here.

def add_bookmark_view(request:HttpRequest, program_id):
    if not request.user.is_authenticated:
        messages.error(request, "فقط الأعضاء المسجلون يمكنهم إضافة برامج للمفضلة","alert-danger")
        return redirect("account:log_in")


    try:
        program = Program.objects.get(pk=program_id)
        user_profile=UserProfile.objects.filter(user=User.objects.get(pk=request.user.id)).first()

        bookmark = ProgramBookmark.objects.filter(program=program, user=user_profile).first()
        if not bookmark:
            
            new_bookmark = ProgramBookmark(user=user_profile, program=program)
            new_bookmark.save()
            messages.success(request, "تمت الإضافة للمفضلة", "alert-success")
        else:
            bookmark.delete()
            messages.warning(request, "تمت الإزالة من المفضلة", "alert-warning")

    except Exception as e:
        print(e)
    return redirect("academy:program_detail_view", program_id=program_id)



def bookmark_view(request:HttpRequest, user_id):
    bookmarks = ProgramBookmark.objects.filter(id=user_id).select_related('program')
    context={
        'bookmarks':bookmarks,

    }
    
    return render(request,"my_bookmark.html",context)