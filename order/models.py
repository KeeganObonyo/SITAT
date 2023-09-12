# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from customer.models import Customer

class CustomerOrder(models.Model):
    customer     = models.ForeignKey(Customer, related_name="customer_order")
    description  = models.CharField(max_length=200, null=True, blank=True)
    currency     = models.CharField(max_length=200)
    cost         = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    created      = models.DateTimeField(auto_now_add=True)
    cleared      = models.NullBooleanField(default=False, null=True, blank=True)
    updated      = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('updated',)

    def get_order_status(self):
        state = []
        for item in self.orderitems.all():
            state.extend([item.check_status()])
        if 'false' in state:
            return 'False'
        else:
            return 'True'

    def get_order_cost(self):
        return sum(item.get_cost()
         for item in self.orderitems.all())

class OrderItem(models.Model):
    order       = models.ForeignKey(CustomerOrder, related_name='orderitems', null=True)
    cleared     = models.NullBooleanField(default=False, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    cost        = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    updated     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('updated',)

    def check_status(self):
        return self.cleared
    def get_cost(self):
        return self.cost