from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from academy.models import Program 
from account.models import UserProfile, AcademyProfile
from academy.models import TimeSlot
from enrollment.models import Enrollment
from django.contrib import messages

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
            return redirect("main:program_detail_view", programs.id) 
        except Exception as e:
            messages.error(request, f"حدث خطأ: {str(e)}")

    context={
        "programs":programs,
        "time_slots": time_slots,
    }
    return render(request, "enrollment_page.html", context)

# For test, I will remove it later depending on UI Design
@login_required(login_url="account:log_in")
def add_enrollment_view(request:HttpRequest):

    if not request.user.is_authenticated:
        messages.error(request, "نرجوا منك التسجيل لإكمال الاشتراك")
        return redirect("account:log_in")
    if request.method == "POST":
        try:
            # user_profile = request.user.userprofile
            # program = Program.objects.get(id=program_id)
            user1 = UserProfile.objects.get(id=request.POST['user'])
            program = Program.objects.get(id=request.POST['program'])
            first_name= request.POST.get('first_name')
            father_name =request.POST.get('father_name')
            last_name= request.POST.get('last_name')
            health_condition= request.POST.get('health_condition')
            id_number= request.POST.get('id_number')

            new_enrollment= Enrollment(
                user1=user1,
                program=program,
                first_name=first_name,
                father_name=father_name,
                last_name=last_name,
                health_condition=health_condition,
                id_number=id_number,
            )
            new_enrollment.save()
            messages.success(request, "تم إضافة الأشتراك بنجاح")
            return redirect("main:program_detail_view", program) 
        except Exception as e:
            messages.error(request, f"حدث خطأ: {str(e)}")
    return render(request,"enrollment_page.html")

