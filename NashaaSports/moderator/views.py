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


def moderator_dashboard_view(request:HttpRequest):
    if request.user.is_superuser:
        #user=UserProfile.objects.filter(user=User.objects.get(pk=user_id)).first()
        # user=User.objects.get(pk=user_id)
        # print(user, "+++++++########++++++##############0000000000000000000")
        return render(request,"moderator/moderator_dashboard.html")
    else:
        return HttpResponse("You are not authorized!")



def customers_queries_view(request: HttpRequest, status):
    if status == 'Open':
        queries = CustomerQuery.objects.filter(status='Open').order_by('-created_at') 
    elif status == 'Closed':
        queries = CustomerQuery.objects.filter(status='Closed').order_by('-created_at') 
    elif status == 'all':
        queries = CustomerQuery.objects.all().order_by('-created_at') 

    return render(request, 'moderator/customers_queries.html', {'queries': queries})


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
                messages.success(request, "تم إغلاق الحالة وإرسال إيميل للعميل بنجاح", extra_tags="green")
                return redirect('moderator:customers_queries_view')
        except Exception as e:
            print(e)
            messages.error(request, "لم يتم إسال الرد. حدث خطأ: {e}", extra_tags="red")
    else:
        form = ReplyForm(initial={'subject': f"Re: {query.subject}"})
    return render(request, 'moderator/query_detail.html', {'query': query, 'form': form})


def academies_for_approval_view(request: HttpRequest):
    
    academies = AcademyProfile.objects.filter(approved=False).order_by('-created_at')  

    return render(request, 'moderator/academies_for_approval.html', {'academies': academies})

def academy_detail_view(request: HttpRequest, academy_id):
    
    academy = AcademyProfile.objects.get(pk=academy_id) 

    return render(request, 'moderator/academy_detail.html', {'academy': academy})


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
