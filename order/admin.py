from django.contrib import admin

from .models import CustomerOrder, OrderItem

admin.site.register(CustomerOrder)
admin.site.register(OrderItem)
