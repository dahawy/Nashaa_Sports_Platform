from django.shortcuts import render, redirect
from cart.models import Cart
from account.models import UserProfile
from academy.models import Program
from academy.models import AcademyProfile

def cart_data(request):
    programs = Program.objects.all()
    count_item = 0  # Initialize count_item with a default value
    total_fees = 0  # Initialize total_fees with a default value

    if request.user.is_authenticated:
        try:
            user = UserProfile.objects.get(user_id=request.user.id)
            carts = Cart.objects.filter(user=user, status='Active').first()
            if carts:
                enrollments = carts.enrollments.all()  # This is a QuerySet
                count_item = enrollments.count()  # count() is valid here
                total_fees = sum(enrollment.program.fees for enrollment in enrollments)
            else:
                enrollments = []
        except UserProfile.DoesNotExist:
            # Handle the case where UserProfile does not exist
            carts = None
            enrollments = []
    else:
        # If the user is not authenticated, set default values
        carts = None
        enrollments = []
        count_item = 0
        total_fees = 0

    return {
        "programs": programs,
        "carts": carts,
        "enrollments": enrollments,
        "total_fees": total_fees,
        "count_item": count_item,
    }
