from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from academy.models import Program 
from account.models import UserProfile, AcademyProfile
from academy.models import TimeSlot
from enrollment.models import Enrollment
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator

from django.core.mail import EmailMessage

@login_required(login_url="account:log_in")
def enroll_in_program_view(request:HttpRequest, program_id):
    profile = UserProfile.objects.filter(user_id=request.user).first()
    if not profile:
        messages.warning(request,"رجاء أكمل معلومتك الشخصية أولاً!")
        return redirect("account:create_profile_view", user_id=request.user.id)
    else:
        programs = Program.objects.get(id=program_id)
        user = UserProfile.objects.get(user_id=request.user)
        time_slots = TimeSlot.objects.filter(program=programs)
        context={
        "programs":programs,
        "time_slots": time_slots,
    }

    if not request.user.is_authenticated:
        messages.error(request, "نرجوا منك التسجيل لإكمال الاشتراك")
        return redirect("account:log_in")
    
    if request.method == "POST":
        try:
            first_name= request.POST.get('first_name')
            father_name =request.POST.get('father_name')
            last_name= request.POST.get('last_name')
            health_condition= request.POST.get('health_condition')
            id_number= request.POST.get('id_number')
            time_slot_id= request.POST.get('time_slot')

            time_slot = TimeSlot.objects.get(id=time_slot_id) #find time slot object by id then assign it to variable
            new_enrollment= Enrollment(
                user=user,
                program=programs,
                time_slot=time_slot,
                first_name=first_name,
                father_name=father_name,
                last_name=last_name,
                health_condition=health_condition,
                id_number=id_number,
            )
            new_enrollment.save()
            messages.success(request, "تم إضافة الأشتراك بنجاح")
            return redirect("academy:program_detail_view", programs.id) 
        except Exception as e:
            messages.error(request, f"حدث خطأ: {str(e)}")

    return render(request, "enrollment_page.html", context)

@login_required(login_url="account:log_in")
def remove_enrollment_from_cart(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)

    if request.method == 'POST':
        cart = enrollment.cart
        enrollment.delete()

        messages.success(request, 'تمت إزالة التسجيل من سلة التسوق.')
        return redirect(request.GET.get("next", "/"))  # Adjust this to the correct cart view URL name

    messages.error(request, 'Invalid request.')
    return redirect(request.GET.get("next", "/"))


@login_required(login_url="account:log_in")
def my_enrollment_view(request:HttpRequest, user_id):
    enrollments = Enrollment.objects.filter(user=UserProfile.objects.filter(user=user_id).first())

    paginator = Paginator(enrollments, 5)
    page_number = request.GET.get("page", 1)
    product_page = paginator.get_page(page_number)
    context={
        "enrollments":enrollments,
        'page_number':page_number,
        'paginator':paginator,
        'product_page':product_page,
    }
    return render(request, 'my_enrollment_view.html', context)

def pending_enrollment_status_view(request:HttpRequest,enrollment_id:int):
    enrollment=Enrollment.objects.get(pk=enrollment_id)
    enrollment.status="pending"
    subject = "تحديث حالة اشتراكك"
    message = f"تم تحديث حالة اشتراكك بأسم {enrollment.first_name} {enrollment.last_name} الى جاري في برنامج {enrollment.program.program_name} من قبل ألاكاديمية"
    recipient = enrollment.user.user.email 
    email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [recipient],
        )
    enrollment.save()
    email.send()
    
    return redirect(request.GET.get('next','/'))
def in_progress_enrollment_status_view(request:HttpRequest,enrollment_id:int):
    enrollment=Enrollment.objects.get(pk=enrollment_id)
    enrollment.status="in_progress"
    subject = "تحديث حالة اشتراكك"
    message = f"تم تحديث حالة اشتراكك بأسم {enrollment.first_name} {enrollment.last_name} الى جاري في برنامج {enrollment.program.program_name} من قبل ألاكاديمية"
    recipient = enrollment.user.user.email 
    email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [recipient],
        )
    enrollment.save()
    email.send()
    return redirect(request.GET.get('next','/'))
