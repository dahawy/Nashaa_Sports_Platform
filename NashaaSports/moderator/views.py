from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest,HttpResponse
from contactUs.models import CustomerQuery
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .forms import ReplyForm
import os
from django.conf import settings
from account.models import User,UserProfile,AcademyProfile
from academy.models import Program
from django.contrib.auth.decorators import login_required, user_passes_test


# def superuser_required(view_func):
#     return login_required(user_passes_test(lambda u: u.is_superuser))
from django.core.exceptions import PermissionDenied

def superuser_required(view_func):
    @login_required
    @user_passes_test(lambda u: u.is_superuser)
    def _wrapped_view_func(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

superuser_required
def moderator_dashboard_view(request:HttpRequest):
    if request.user.is_superuser:
        academies = AcademyProfile.objects.filter(approved=True)
        programs = Program.objects.all()
        users = User.objects.all()
        return render(request,"moderator/moderator_dashboard.html",{'academies': academies, 'programs': programs, 'users': users})
    else:
        return HttpResponse("You are not authorized!")


@superuser_required
def customers_queries_view(request: HttpRequest, status):
    if status == 'Open':
        queries = CustomerQuery.objects.filter(status='Open').order_by('-created_at') 
    elif status == 'Closed':
        queries = CustomerQuery.objects.filter(status='Closed').order_by('-created_at') 
    elif status == 'all':
        queries = CustomerQuery.objects.all().order_by('-created_at') 

    return render(request, 'moderator/customers_queries.html', {'queries': queries})


@superuser_required
def query_detail_view(request, query_id):
    query = get_object_or_404(CustomerQuery, pk=query_id)
    if request.method == 'POST':
        try:
            query.status = 'Closed'
            query.save()
            form = ReplyForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                recipient = query.email

                email = EmailMessage(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [recipient],
                )
                email.send()
                #email.send(fail_silently=False)
                messages.success(request, "تم إغلاق الحالة وإرسال إيميل للعميل بنجاح", extra_tags="alert-success")
                return redirect('moderator:customers_queries_view',status= 'Open')
        except Exception as e:
            print(e)
            messages.error(request, "لم يتم إسال الرد.", extra_tags="alert-danger")
    else:
        form = ReplyForm(initial={'subject': f"Re: {query.subject}"})
    return render(request, 'moderator/query_detail.html', {'query': query, 'form': form})


@superuser_required
def academies_for_approval_view(request: HttpRequest):
    
    academies = AcademyProfile.objects.filter(approved=False).order_by('-created_at')  

    return render(request, 'moderator/academies_for_approval.html', {'academies': academies})


@superuser_required
def approved_academies_view(request: HttpRequest):
    
    academies = AcademyProfile.objects.filter(approved=True).order_by('-created_at')  

    return render(request, 'moderator/approved_academies.html', {'academies': academies})

@superuser_required
def academy_detail_view(request: HttpRequest, academy_id):
    
    academy = AcademyProfile.objects.get(pk=academy_id) 

    return render(request, 'moderator/academy_detail.html', {'academy': academy})


@superuser_required
def approve_academy_view(request: HttpRequest, academy_id):
    try:
        academy = AcademyProfile.objects.get(pk=academy_id)
        academy.approved = True
        academy.save()
        subject = "تهانينا..تم اعتماد منشأتكم"
        message = f"نبارك لكم اعتماد منشأتكم: {academy.academy_name} ونتطلع لمزيد من التعاون... منصة نشء"
        recipient = academy.user.email

        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [recipient],
        )
        email.send() 
        messages.success(request, f"تم اعتماد {academy.academy_name} وإبلاغهم عبر الإيميل", extra_tags="alert-success")
    except Exception as e:
        print(e)
    return redirect('moderator:academies_for_approval_view')

@superuser_required
def users_view(request: HttpRequest, user_type):
    if user_type == 'academy':
        users = AcademyProfile.objects.all() 
    elif user_type == 'individual':
        users = UserProfile.objects.all()
    elif user_type == 'all':
        users = User.objects.all()

    return render(request, 'moderator/users.html', {'users': users, 'user_type':user_type})


@superuser_required
def programs_view(request: HttpRequest, academy_id):
    academy = AcademyProfile.objects.get(id=academy_id)
    programs = Program.objects.filter(branch__academy_id=academy_id).order_by('branch__branch_city')
    return render(request, 'moderator/programs.html', {'academy': academy, 'programs': programs})

@superuser_required
def deactivate_program_view(request: HttpRequest,academy_id):
    if request.method == 'POST':
        try:
            # Update the program activation status
            program_id = request.POST.get('program_id')
            program = Program.objects.get(id=program_id)
            is_active = 'is_active' in request.POST
            program.admin_activtion = is_active
            program.save()
            return redirect('moderator:programs_view', academy_id=academy_id)
        except Program.DoesNotExist:
            return redirect('moderator:programs_view', academy_id=academy_id)