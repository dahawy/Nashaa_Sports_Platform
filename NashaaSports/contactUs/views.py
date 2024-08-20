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
                return redirect('main:home_view')
        except Exception as e:
            messages.error(request, "Message can't be sent! Error: {e}", extra_tags="alert-danger")
    else:
        customerQuery_form = CustomerQueryForm()
   

    return render(request, 'contactUs/customer_query.html', {'customerQuery_form': customerQuery_form})








    