from django.shortcuts import render
from django.http import HttpRequest
from academy.models import Program 


def home_view(request:HttpRequest):
    programs = Program.objects.all()

    context ={
        "programs":programs,
    }
    return render(request, "index.html",context)

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
