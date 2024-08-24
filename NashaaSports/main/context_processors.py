# your_app_name/context_processors.py

from cart.models import Cart
from account.models import UserProfile
from academy.models import Program

def cart_data(request):
    programs = Program.objects.all()
    if request.user.is_authenticated:
        user = UserProfile.objects.get(user_id=request.user.id)
        carts = Cart.objects.filter(user=user, status='Active').first()
        enrollments = carts.enrollments.all() if carts else []
        total_fees = sum(enrollment.program.fees for enrollment in enrollments)
        # TODO : fix cart counting problem 
    #     count_item = enrollments.count()
    # elif  count_item == 0:
    #     count_item = 0
    else:
        carts = Cart.objects.filter(user=request.user.id, status='Active').first()
        enrollments = carts.enrollments.all() if carts else []
        total_fees = sum(enrollment.program.fees for enrollment in enrollments)
        # count_item = 0
    return {
        "programs":programs,
        "carts":carts,
        "enrollments":enrollments,
        "total_fees":total_fees,
        # "count_item":count_item,
    }
