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
            messages.error(request, 'كلمة المرور غير متطابقة!')
            return render(request, 'sign_up.html')
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "إسم الستخدم مسجل مسبقاً", "alert-danger")
            return render(request, "sign_up.html")
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "يوجد مستخدم لديه هذا البريد الإلكتروني بالفعل.", "alert-danger")
            return render(request, "sign_up.html") 
        
    if request.method == "POST":
        try:
            new_user = User.objects.create_user(username = request.POST["username"], password=request.POST["password"], email=request.POST["email"])
            new_user.save()
            messages.success(request, "لقد تم تسجيلك بنجاح", "alert-success")
            #send confirmation email
            content_html = render_to_string("mail/new_user_welcome.html",{"userName":new_user}) #set email
            send_to = new_user.email
            email_message = EmailMessage("مرحباُ بك في منصة نشـء", content_html, settings.EMAIL_HOST_USER, [send_to])
            email_message.content_subtype = "html"
            #email_message.connection = email_message.get_connection(True)
            email_message.send()
            return redirect("account:log_in")
        except IntegrityError:
            messages.error(request, "حدث خطأ أثناء التسجيل! أعد المحاولة", "alert-danger")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}", "alert-danger")
    return render(request, "sign_up.html")

def log_in(request: HttpRequest):
    if request.method == "POST":
    #checking user credentials
        # userProfile = UserProfile.objects.get(user=request.user)
        # academyProfile = AcademyProfile.objects.get(user=request.user)
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user:
            #login the user
            login(request, user)
            messages.success(request, "لقد تم تسجيل الدخول بنجاح", "alert-success")
            # if not userProfile:
            #     redirect("account:create_profile_view", user_id=userProfile)
            # if not academyProfile:
            #     redirect("account:create_academy_profile_view", user_id=academyProfile)
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "يرجى المحاولة مرة أخرى. بريدك الإلكتروني أو كلمة المرور الخاصة بك خاطئة", "alert-danger")
    return render(request, 'log_in.html')

def log_out(request:HttpRequest):
    logout(request)
    messages.success(request, "لقد تم تسجيل خروجك بنجاح", "alert-warning")
    return redirect(request.GET.get("next", "main:home_view"))

@login_required(login_url="account:log_in")
def profile_view(request:HttpRequest, user_id):
    try:
        user = User.objects.get(pk=user_id)
        profile = UserProfile.objects.filter(user=user).first()
        academyProfile = AcademyProfile.objects.filter(user=user).first()
        
        if not profile:
            # Redirect to create_profile_view if profile doesn't exist
            return redirect('account:create_profile_view', user_id=user_id)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return render(request, "Sorry, something wrong")
    return render(request, "profile.html", {"profile": profile,"academyProfile":academyProfile})

@login_required(login_url="account:log_in")
def create_profile_view(request:HttpRequest, user_id):
    user = get_object_or_404(User, pk=user_id)
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
            return redirect('account:profile_view', user_id=user_id)
        except IntegrityError:
            messages.error(request, "حدث خطأ أثناء إنشاء الملف الشخصي.", "alert-danger")
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
            messages.error(request, 'كلمات المرور غير متطابقة!')
            return render(request, 'academy_sign_up.html')
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "يوجد مستخدم يحمل اسم المستخدم هذا بالفعل.", "alert-danger")
            return render(request, "academy_sign_up.html")
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "يوجد مستخدم لديه هذا البريد الإلكتروني بالفعل.", "alert-danger")
            return render(request, "academy_sign_up.html") 
        
    if request.method == "POST":
        try:
            new_academy = User.objects.create_user(username = request.POST["username"], first_name=request.POST["first_name"], last_name=request.POST["last_name"], password=request.POST["password"], email=request.POST["email"],is_staff=True)
            new_academy.save()
            messages.success(request, "لقد تم تسجيلك بنجاح", "alert-success")
            #send confirmation email
            content_html = render_to_string("mail/academy_reg.html",{"academyName":new_academy}) #set email
            send_to = new_academy.email
            email_message = EmailMessage("شكراً لك لإختيارك منصة نشـء", content_html, settings.EMAIL_HOST_USER, [send_to])
            email_message.content_subtype = "html"
            #email_message.connection = email_message.get_connection(True)
            email_message.send()
            return redirect("account:log_in")
        except IntegrityError:
            messages.error(request, "حدث خطأ أثناء التسجيل.", "alert-danger")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}", "alert-danger")
    return render(request, "academy_sign_up.html")

@login_required(login_url="account:log_in")
def academy_profile_view(request:HttpRequest, user_id):
    try:
        user = User.objects.get(pk=user_id)
        profile = AcademyProfile.objects.filter(user=user).first()
        
        if not profile:
            # Redirect to create_profile_view if profile doesn't exist
            return redirect('account:create_academy_profile_view', user_id=user_id)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return render(request, "404 page not found")
    return render(request, "profile.html", {'profile': profile})

@login_required(login_url="account:log_in")
def create_academy_profile_view(request:HttpRequest, user_id):
    user = get_object_or_404(User, pk=user_id)
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
            return redirect('account:academy_profile_view', user_id=user_id)
        except IntegrityError:
            messages.error(request, "حدث خطأ أثناء إنشاء الملف الشخصي.", "alert-danger")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}", "alert-danger")
    return render(request,"create_academy_profile.html", {'user': user, 'UserProfile':UserProfile})

@login_required(login_url="account:log_in")
def update_user_profile(request:HttpRequest):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)

    if request.method == 'POST':
        # Create form fields directly in the view
        name = request.POST.get('name')
        nationality = request.POST.get('nationality')
        id_number = request.POST.get('id_number')
        gender = request.POST.get('gender')
        birth_date = request.POST.get('birth_date')
        health_condition = request.POST.get('health_condition')
        avatar = request.FILES.get('avatar')

        # Validate and update the profile
        if name and nationality and id_number:
            profile.name = name
            profile.nationality = nationality
            profile.id_number = id_number
            profile.gender = gender
            profile.birth_date = birth_date
            profile.health_condition = health_condition
            if avatar:
                profile.avatar = avatar
            profile.save()
            messages.success(request, 'لقد تم تحديث ملفك الشخصي بنجاح.')
            return redirect('account:profile_view',user_id=request.user.id) 
        else:
            messages.error(request, 'يرجى ملء جميع الحقول المطلوبة.')
    
    context = {
        'profile': profile,
    }
    return render(request, 'update_profile.html', context)

@login_required(login_url="account:log_in")
def update_academy_profile(request:HttpRequest):
    try:
        profile = AcademyProfile.objects.get(user=request.user)
    except AcademyProfile.DoesNotExist:
        profile = AcademyProfile(user=request.user)

    if request.method == 'POST':
        description = request.POST.get('description')
        logo = request.FILES.get('logo')

        # Validate and update the profile
        if description:
            profile.description = description
            if logo:
                profile.logo = logo
            profile.save()
            messages.success(request, 'لقد تم تحديث ملفك الشخصي بنجاح.')
            return redirect('account:academy_profile_view',user_id=request.user.id)  
        else:
            messages.error(request, 'يرجى ملء جميع الحقول المطلوبة.')
    
    context = {
        'profile': profile,
    }
    return render(request, 'account:academy_profile_view', context)