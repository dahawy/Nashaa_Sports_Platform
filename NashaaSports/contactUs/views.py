from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from contactUs.models import CustomerQuery
from .forms import CustomerQueryForm
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


def customer_query_view(request: HttpRequest):
    categories = CustomerQuery.QueryCategory.choices
    if request.method == 'POST':
        try:
            customerQuery_form = CustomerQueryForm(request.POST)
            if customerQuery_form.is_valid():
                query = customerQuery_form.save(commit=False)  # Don't save to the database just yet
                query.status = 'Open'  # Explicitly set the status to 
                query.save()  
                messages.success(request, "لقد تم ارسال رسالتك بنجاح", extra_tags="alert-success")
                content_html = render_to_string("mail/respond.html",{"query":query}) #set email
                send_to = query.email
                email_message = EmailMessage("شكراً لك لإختيارك منصة نشـء", content_html, settings.EMAIL_HOST_USER, [send_to])
                email_message.content_subtype = "html"
                email_message.send()
                return redirect('main:home_view')
        except Exception as e:
            print(e)
            messages.error(request, "لا يمكن إرسال الرسالة!", extra_tags="alert-danger")
    else:
        customerQuery_form = CustomerQueryForm()
   

    return render(request, 'contactUs/customer_query.html', {'customerQuery_form': customerQuery_form})








    