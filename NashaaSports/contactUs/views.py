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
                customerQuery_form.save()
                messages.success(request, "Your message sent successfully", extra_tags="alert-success")
                return redirect('main:home_view')
        except Exception as e:
            print(e)  
    else:
        messages.error(request, "Message can't be sent", extra_tags="alert-danger")
        
        customerQuery_form = CustomerQueryForm()
   

    return render(request, 'contactUs/customer_query.html', {'customerQuery_form': customerQuery_form})








    