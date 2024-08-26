from django.contrib import admin
from payment.models import Payment


class CustomPayment(admin.ModelAdmin):
    list_display = ('id', 'cart', 'payment_method', 'status', 'total', 'payment_date')

admin.site.register(Payment, CustomPayment)