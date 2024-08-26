from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from academy.models import Program 
from account.models import UserProfile, AcademyProfile
from academy.models import TimeSlot
from enrollment.models import Enrollment
from django.contrib import messages
from django.conf import settings

from django.core.mail import EmailMessage

@login_required(login_url="account:log_in")
def enroll_in_program_view(request:HttpRequest, program_id, user_id):
    programs = Program.objects.get(id=program_id)
    user = UserProfile.objects.get(user_id=user_id)
    time_slots = TimeSlot.objects.filter(program=programs)
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

    context={
        "programs":programs,
        "time_slots": time_slots,
    }
    return render(request, "enrollment_page.html", context)

# For test, I will remove it later depending on UI Design
# @login_required(login_url="account:log_in")
# def add_enrollment_view(request:HttpRequest):

#     if not request.user.is_authenticated:
#         messages.error(request, "نرجوا منك التسجيل لإكمال الاشتراك")
#         return redirect("account:log_in")
#     if request.method == "POST":
#         try:
#             # user_profile = request.user.userprofile
#             # program = Program.objects.get(id=program_id)
#             user1 = UserProfile.objects.get(id=request.POST['user'])
#             program = Program.objects.get(id=request.POST['program'])
#             first_name= request.POST.get('first_name')
#             father_name =request.POST.get('father_name')
#             last_name= request.POST.get('last_name')
#             health_condition= request.POST.get('health_condition')
#             id_number= request.POST.get('id_number')

#             new_enrollment= Enrollment(
#                 user1=user1,
#                 program=program,
#                 first_name=first_name,
#                 father_name=father_name,
#                 last_name=last_name,
#                 health_condition=health_condition,
#                 id_number=id_number,
#             )
#             new_enrollment.save()
#             messages.success(request, "تم إضافة الأشتراك بنجاح")
#             return redirect("academy:program_detail_view", program) 
#         except Exception as e:
#             messages.error(request, f"حدث خطأ: {str(e)}")
#     return render(request,"enrollment_page.html")


@login_required(login_url="account:log_in")
def my_enrollment_view(request:HttpRequest, user_id):
    user= UserProfile.objects.get(user_id= user_id)
    enrollment = Enrollment.objects.filter(user=user)
    
    context={
        "enrollments":enrollment,
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
