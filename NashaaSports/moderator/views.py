from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from contactUs.models import CustomerQuery
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .forms import ReplyForm
import os
from django.conf import settings



def customers_queries_view(request: HttpRequest):
    queries = CustomerQuery.objects.all().order_by('-created_at') 

    return render(request, 'moderator/customers_queries.html', {'queries': queries})


def query_detail_view(request, query_id):
    query = CustomerQuery.objects.get(pk=query_id)
    if request.method == 'POST':
        try:
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
                messages.success(request, "An email has been sent to the customer successfully", extra_tags="alert-success")
                return redirect('moderator:customers_queries_view')
        except Exception as e:
            print(e)
    else:
        form = ReplyForm(initial={'subject': f"Re: {query.subject}"})
       
        

    return render(request, 'moderator/query_detail.html', {'query': query, 'form': form})


