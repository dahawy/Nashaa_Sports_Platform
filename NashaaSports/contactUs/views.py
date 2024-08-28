from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from contactUs.models import CustomerQuery
from .forms import CustomerQueryForm
from django.contrib import messages

# Create your views here.



def customer_query_view(request: HttpRequest):
    categories = CustomerQuery.QueryCategory.choices
    if request.method == 'POST':
        try:
            customerQuery_form = CustomerQueryForm(request.POST)
            if customerQuery_form.is_valid():
                query = customerQuery_form.save(commit=False)  # Don't save to the database just yet
                query.status = 'Open'  # Explicitly set the status to 'open'
                query.save()  # Now save the instance
                messages.success(request, "Your message sent successfully", extra_tags="alert-success")
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
                return redirect('main:home_view')
        except Exception as e:
            print(e)
            messages.error(request, "Message can't be sent!", extra_tags="alert-danger")
    else:
        customerQuery_form = CustomerQueryForm()
   

    return render(request, 'contactUs/customer_query.html', {'customerQuery_form': customerQuery_form})








    