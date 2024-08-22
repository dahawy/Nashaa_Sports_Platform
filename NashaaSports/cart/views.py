from django.shortcuts import render
from django.http import HttpRequest
from academy.models import Program
from cart.models import Cart

def cart_summary_view (request:HttpRequest, cart_id):
    programs = Program.objects.all()
    carts = Cart.objects.get(id=cart_id)
    enrollments = carts.enrollments.all() if carts else []
    print(carts)
    context ={
        "programs":programs,
        "carts":carts,
        "enrollments":enrollments,
    }


    return render(request, "cart_summary.html",context)