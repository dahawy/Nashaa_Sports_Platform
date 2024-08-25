from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from account.models import UserProfile
from cart.models import Cart
from payment.models import Payment
from enrollment.models import Enrollment
import datetime as datetime
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def process_payment(request, cart_id):

    cart = get_object_or_404(Cart, id=cart_id)
    total=calculate_cart_total(cart)
    tax= float(total)*0.15
    total_with_tax= float(tax) + float(total)

    if request.method == "POST":
        try:
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
                content_html = render_to_string("mail/user_reg.html") #set email
                send_to = payment.cart.user.user.email
                print(send_to)
                email_message = EmailMessage("Payment Confirmed", content_html, settings.EMAIL_HOST_USER, [send_to])
                email_message.content_subtype = "html"
                #email_message.connection = email_message.get_connection(True)
                email_message.send()

                messages.success(request, "Payment was successful!")
            
            elif action == 'cancel':
                cart.status = Cart.CartStatus.Cancelled
                cart.save()

                messages.info(request, "Payment was cancelled.")
        except Exception as e:
            messages.error(request,f"حدث خطأ: {str(e)}")
        
        # return redirect('/', cart_id=cart.id)
        return redirect('/')

    context = {
        'cart': cart,
        'total': total,
        'tax': tax,
        'total_with_tax': total_with_tax,
    }
    return render(request, 'payment_process_page.html', context)

def calculate_cart_total(cart):
    total = 0
    enrollments = Enrollment.objects.filter(cart=cart)
    for enrollment in enrollments:
        total += enrollment.program.fees
    return total
