from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.contrib.auth.models import User
from account.models import UserProfile
from account.models import AcademyProfile
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.db import IntegrityError

# User Registration
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

@login_required(login_url="account:log_in")
def profile_view(request:HttpRequest, user_name):
    try:
        user = User.objects.get(username=user_name)
        profile = UserProfile.objects.filter(user=user).first()
        academyProfile = AcademyProfile.objects.filter(user=user).first()
        
        if not profile:
            # Redirect to create_profile_view if profile doesn't exist
            return redirect('account:create_profile_view', user_name=user_name)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return render(request, "Sorry, something wrong")
    return render(request, "profile.html", {'profile': profile,"AcademyProfile":academyProfile})

@login_required(login_url="account:log_in")
def create_profile_view(request:HttpRequest, user_name):
    user = get_object_or_404(User, username=user_name)
    if request.method == "POST":
        try:
            new_profile = UserProfile(
                user=user, 
                name=request.POST["name"],
                nationality=request.POST["nationality"],
                id_number=request.POST["id_number"],
                gender=request.POST["gender"],
                birth_date=request.POST["birth_date"],
                health_condition=request.POST["health_condition"],
            )
            if 'avatar' in request.FILES:
                new_profile.avatar = request.FILES["avatar"]
            new_profile.save()
            messages.success(request, "Profile Created Successfully")
            return redirect('account:profile_view', user_name=user_name)
        except IntegrityError:
            messages.error(request, "An error occurred during Creating profile.", "alert-danger")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}", "alert-danger")
    return render(request,"create_profile.html", {'user': user, 'UserProfile':UserProfile})

#Academy Registration

def sing_up_asAcademy_view(request: HttpRequest):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
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
            new_user = User.objects.create_user(username = request.POST["username"], first_name=request.POST["first_name"], last_name=request.POST["last_name"], password=request.POST["password"], email=request.POST["email"])
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
    return render(request, "academy_sign_up.html")

@login_required(login_url="account:log_in")
def academy_profile_view(request:HttpRequest, user_name):
    try:
        user = User.objects.get(username=user_name)
        profile = AcademyProfile.objects.filter(user=user).first()
        
        if not profile:
            # Redirect to create_profile_view if profile doesn't exist
            return redirect('account:create_academy_profile_view', user_name=user_name)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return render(request, "404 page not found")
    return render(request, "profile.html", {'profile': profile})

@login_required(login_url="account:log_in")
def create_academy_profile_view(request:HttpRequest, user_name):
    user = get_object_or_404(User, username=user_name)
    if request.method == "POST":
        try:
            new_profile = AcademyProfile(
                user=user, 
                academy_name=request.POST["academy_name"],
                description=request.POST["description"],
            )
            if 'logo' in request.FILES:
                new_profile.logo = request.FILES["logo"]
            new_profile.save()
            messages.success(request, "Academy profile Created Successfully")
            return redirect('account:academy_profile_view', user_name=user_name)
        except IntegrityError:
            messages.error(request, "An error occurred during Creating profile.", "alert-danger")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}", "alert-danger")
    return render(request,"create_academy_profile.html", {'user': user, 'UserProfile':UserProfile})