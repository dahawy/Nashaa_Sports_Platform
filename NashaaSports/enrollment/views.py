from django.shortcuts import render
from django.http import HttpRequest
from academy.models import Program 
from account.models import UserProfile 


def enroll_in_program_view(request:HttpRequest, program_id, user_id):
    programs = Program.objects.get(id=program_id)
    user = UserProfile.objects.get(id=user_id)
    context={
        "programs":programs,
        "user":user
    }

    return render(request, "enrollment_page.html", context)


