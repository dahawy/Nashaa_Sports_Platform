from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

def sign_up (request: HttpRequest):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        # Check password match
        if password != repeat_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'sign_up.html')
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "A user with that username already exists.", "alert-danger")
            return render(request, "sign_up.html")
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with that email already exists.", "alert-danger")
            return render(request, "sign_up.html") 
        
    if request.method == "POST":
        try:
            new_user = User.objects.create_user(username = request.POST["username"], password=request.POST["password"], email=request.POST["email"])
            new_user.save()
            messages.success(request, "You have been Registered Successfully", "alert-success")
            #send confirmation email
            content_html = render_to_string("mail/welcoming.html",{"userName":new_user}) #set email
            send_to = new_user.email
            email_message = EmailMessage("welcoming", content_html, settings.EMAIL_HOST_USER, [send_to])
            email_message.content_subtype = "html"
            #email_message.connection = email_message.get_connection(True)
            email_message.send()
            return redirect("account:log_in")
        except IntegrityError:
            messages.error(request, "An error occurred during registration.", "alert-danger")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}", "alert-danger")
    return render(request, "sign_up.html")

def log_in(request: HttpRequest):
        
    if request.method == "POST":
    #checking user credentials
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user:
            #login the user
            login(request, user)
            messages.success(request, "You are Logged in successfully", "alert-success")
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "Please try again. You credentials are wrong", "alert-danger")
    return render(request, 'log_in.html')


def log_out(request:HttpRequest):
    logout(request)
    messages.success(request, "You are logged out successfully", "alert-warning")

    return redirect(request.GET.get("next", "main:home_view"))
