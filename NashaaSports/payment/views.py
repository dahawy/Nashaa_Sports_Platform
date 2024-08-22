from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from account.models import UserProfile
from cart.models import Cart
from payment.models import Payment
from enrollment.models import Enrollment
import datetime as datetime


def process_payment(request, cart_id):
    # user = UserProfile.objects.get(id=request.user)
    # print(user)
    cart = get_object_or_404(Cart, id=cart_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'pay':
            # payment processing logic happens here
            #  integrating with a payment gateway

            # If payment is successful, create a Payment record
            payment = Payment.objects.create(
                cart=cart,
                total=calculate_cart_total(cart),
                payment_date=datetime.datetime.now(),
                payment_method='Credit Card',  # This can be dynamic based on user input
                status=True
            )
            payment.save()

            cart.status = Cart.CartStatus.Paid
            cart.save()

            messages.success(request, "Payment was successful!")
        elif action == 'cancel':
            cart.status = Cart.CartStatus.Cancelled
            cart.save()

            messages.info(request, "Payment was cancelled.")
        
        # return redirect('/', cart_id=cart.id)
        return redirect('/')

    context = {
        'cart': cart,
    }
    return render(request, 'payment_process_page.html', context)

def calculate_cart_total(cart):
    total = 0
    enrollments = Enrollment.objects.filter(cart=cart)
    for enrollment in enrollments:
        total += enrollment.program.fees
    return total