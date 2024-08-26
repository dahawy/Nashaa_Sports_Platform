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
from enrollment.models import Enrollment
from payment.models import Payment
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from babel.dates import format_date
from django.utils.safestring import mark_safe
import json
import random

# def superuser_required(view_func):
#     return login_required(user_passes_test(lambda u: u.is_superuser))
from django.core.exceptions import PermissionDenied

def superuser_required(view_func):
    @login_required
    @user_passes_test(lambda u: u.is_superuser)
    def _wrapped_view_func(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func


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
                content_html = render_to_string("moderator/customer_care_reply.html",{'query':query, 'message':message}) 
                recipient = query.email

                email = EmailMessage(
                    subject,
                    content_html,
                    settings.EMAIL_HOST_USER,
                    [recipient],
                )
                email.content_subtype = "html"
                email.send()
                messages.success(request, "تم إغلاق الحالة وإرسال إيميل للعميل بنجاح", extra_tags="alert-success")
                return redirect('moderator:customers_queries_view',status= 'Open')
        except Exception as e:
            print(e)
            messages.error(request, "لم يتم إرسال الرد.", extra_tags="alert-danger")
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
        

@superuser_required
def moderator_dashboard_view(request:HttpRequest, days_ago: int):
    if request.user.is_superuser:    
        if int(days_ago) in [30, 90]:
            academies = AcademyProfile.objects.filter(approved=True)
            programs = Program.objects.all()
            subscriptions = Enrollment.objects.all()
            users = User.objects.all()
            
            # Get today's date and calculate the date 30 or 90 days ago
            today = timezone.now().date()
            date_days_ago = today - timedelta(days=days_ago)
            # Query to get enrollments for the football category in the specified period with associated payments
            football_payments = Enrollment.objects.filter(
                program__sport_category=Program.SportChoices.FOOTBALL,
                cart__payment__status=True,  #status=True means payment completed
                cart__payment__payment_date__range=[date_days_ago, today]
            )

            # Query to get enrollments for the volleyball category in the specified period with associated payments
            volleyball_payments = Enrollment.objects.filter(
                program__sport_category=Program.SportChoices.VOLLEYBALL,
                cart__payment__status=True,  #status=True means payment completed
                cart__payment__payment_date__range=[date_days_ago, today]
            )

            try:
                # Aggregate fees by payment date
                football_aggregated_payments = football_payments.values('cart__payment__payment_date').annotate(football_sales_total=Sum('program__fees')).order_by('cart__payment__payment_date')
                volleyball_aggregated_payments = volleyball_payments.values('cart__payment__payment_date').annotate(volleyball_sales_total=Sum('program__fees')).order_by('cart__payment__payment_date')
                # Prepare the salesList and datesList
                football_salesList =[]
                football_salesList = [float(item['football_sales_total']) for item in football_aggregated_payments]
                # if list is empty fill it with zero
                football_salesList = football_salesList if football_salesList else [0]
                football_datesList = [format_date(item['cart__payment__payment_date'], format='dd MMMM', locale='ar') for item in football_aggregated_payments]
                volleyball_datesList =[]
                volleyball_salesList = [float(item['volleyball_sales_total']) for item in volleyball_aggregated_payments]
                # if list is empty fill it with zero
                volleyball_salesList = volleyball_salesList if volleyball_salesList else [0]
                volleyball_datesList = [format_date(item['cart__payment__payment_date'], format='dd MMMM', locale='ar') for item in volleyball_aggregated_payments]
                datesList = []

                # Get all unique dates from both lists.
                datesList = list(set(football_datesList + volleyball_datesList))

                # A list of all sport categories
                sport_categories = Program.objects.values_list('sport_category', flat=True).distinct()
                # Get all sport categories labels in Arabic
                #sport_categories_labels = [Program.SportChoices(sport).label for sport in sport_categories]
                sport_categories_labels = []
                for sport in sport_categories:
                    try:
                        label = Program.SportChoices(sport).label
                        sport_categories_labels.append(label)
                    except ValueError:
                        print(f"Invalid sport category: {sport}")

        
                sport_categories_colors = generate_colors(len(sport_categories_labels))
                print(sport_categories_colors)
              

                context = {
                    'football_salesList': mark_safe(json.dumps(football_salesList)),
                    'volleyball_salesList': mark_safe(json.dumps(volleyball_salesList)),
                    'datesList': mark_safe(json.dumps(datesList)),
                    'sales_total': sum(football_salesList) + sum(volleyball_salesList),
                    'academies': academies,
                    'programs': programs,
                    'subscriptions':subscriptions, 
                    'users': users,
                    'sport_categories': mark_safe(json.dumps(sport_categories_labels)),
                    'sport_categories_colors': mark_safe(json.dumps(sport_categories_colors)),
                }
                return render(request, 'moderator/moderator_dashboard.html', context)
            except Exception as e:
                return HttpResponse(f"حدث خطأ: {e}", status=500)
                #messages.success(request,f"حدث خطأ: {e}", extra_tags="alert-red")
            
    else:
        return HttpResponse("لا تمتلك التصريح اللازم للدخول", status=403)



def generate_colors(n):
    # Predefined color list
    
    base_colors = [
        "rgb(112, 214, 255)",
        "rgb(255, 112, 166)",
        "rgb(255, 151, 112)",
        "rgb(255, 214, 112)",
        "rgb(233, 255, 112)",
        "rgb(240, 250, 250)",
        "rgb(203, 243, 240)",  
        "rgb(46, 196, 182)",
        "rgb(51, 161, 253)",
        "rgb(255, 228, 94)",
        "rgb(255, 99, 146)",
        "rgb(159, 160, 255)",
        "rgb(203, 178, 254)",
        "rgb(255, 183, 3)",
        "rgb(33, 158, 188)",
        "rgb(142, 202, 230)",
        "rgb(248, 247, 255)",
        "rgb(255, 238, 221)",
        "rgb(255, 216, 190)",
        "rgb(247, 37, 133)",
        "rgb(72, 149, 239)"
    ]
        

    # If n is greater than the predefined colors, generate random colors
    if n > len(base_colors):
        additional_colors = [
            "rgb({}, {}, {})".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            for _ in range(n - len(base_colors))
        ]
        base_colors.extend(additional_colors)
    
    return base_colors[:n]


