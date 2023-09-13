# -*- coding: utf-8 -*-
from rest_framework import serializers

from customer.serializers import CustomerSerializer

from .models import CustomerOrder, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model  = OrderItem
        fields = ('id', 'order', 'cleared',
                  'description', 'updated')

class OrderSerializer(serializers.ModelSerializer):
    customer   = CustomerSerializer(read_only=True)
    orderitems = OrderItemSerializer(read_only=True, many=True)

    class Meta:
        model  = CustomerOrder
        fields = ('id', 'customer', 'description', 
                  'cleared', 'updated','orderitems')
