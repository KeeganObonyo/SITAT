# -*- coding: utf-8 -*-
from django.http import Http404
from django.db.models import Q

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework_jwt.settings import api_settings
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

import africastalking

from  sitat.settings import *

from customer.models import Customer

from .models import CustomerOrder, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

def get_auth(request=None):
    try:
        user_id = jwt_decode_handler(request.auth)["user_id"]
    except Exception as e:
        return str(e)
    return user_id

def send_sms(self,message=None,recipients=None):
    username = AFRICASTALKING_USERNAME
    api_key  = AFRICASTALKING_APIKEY

    africastalking.initialize(username, api_key)
    self.sms = africastalking.SMS
    sender   = AFRICASTALKING_SENDER_ID
    try:
        response = self.sms.send(message, recipients, sender)
        return response
    except Exception as e:
        return Response(data={"Error": str(e)},
                        status=status.HTTP_400_BAD_REQUEST)

class Order(generics.CreateAPIView):
    """
    View for adding an order which includes multiple order itemns.
    The expected structure is:
    {
        "order_items":[{"cost":100.0,
                        "description":"One sample order itemn"},],
        "description":"A sample order"

    }

    """
    queryset   = CustomerOrder.objects.all()
    model_list = [CustomerOrder, OrderItem]

    def post(self, request, format=None):
        try:
            order_items = request.data['order_items']
            try:
                description = request.data['description']
            except:
                description = None
            customer = Customer.objects.get(id=get_auth(request))
            order = CustomerOrder.objects.create(
                description = description,
                customer    = customer,
                currency    = request.data['currency']
            )
            for item in order_items:
                try:
                    description = item['description']
                except:
                    description = None
                OrderItem.objects.create(
                    order       = order,
                    description = description,
                    cost        = item['cost']
                )
            order.cost = order.get_order_cost()
            order.save()
            response = send_sms(self,message="Your order has been received",recipients=[customer.phone_number])
            if response.status_code == 200:
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(data={"Error": "Message wasn't sent to customer"},
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Error": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class AddOrderItem(generics.CreateAPIView):
    """
    View for adding an order item to an existing order.
    Returns a 201 upon creation.
    The expected structure is:
    {
     "description":"a sample order item",
     "order":"order_id"
     "cost":120.0
    }
    """
    queryset = OrderItem.objects.all()
    model_list = [CustomerOrder, OrderItem]

    def post(self, request, format=None):
        try:
            order = CustomerOrder.objects.get(
               id = request.data['order_id']
            )
            try:
                description = request.data['description']
            except:
                description = None
            OrderItem.objects.create(
                order       = order,
                description = description,
                cost        = request.data['cost']
            )
            order.cost    = order.get_order_cost()
            order.cleared = 'False'
            order.save()
            response = send_sms(self,message="Your order has been modified",recipients=[order.customer.phone_number])
            if response.status_code == 200:
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(data={"Error": "Message wasn't sent to customer"},
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"Error": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        
class ExecuteOrderItem(generics.CreateAPIView):
    """
    View for executing an order item.
    Returns a 201 upon creation.
    The expected structure is:
    {
     "item":1
    }"""
    queryset = OrderItem.objects.all()
    model_list = [OrderItem, Order]

    def post(self, request, format=None):
        try:
            try:
                order_item = OrderItem.objects.get(
                    id=request.data['item'])
                if order_item.cleared == True:
                    return Response(data="The order item has already been cleared",
                                    status=status.HTTP_400_BAD_REQUEST
                )
                order = CustomerOrder.objects.get(
                    id=order_item.order_id
                )
            except:
                raise Http404
            order_item.cleared = 'True'
            order_item.save()
            order.cleared = order.get_order_status()
            order.save()
            if order.get_order_status() == True:
                response = send_sms(self,message="Your order has been cleared",recipients=[order.customer.phone_number])
                if response.status_code == 200:
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(data={"Error": "Order is cleared but Message wasn't sent to customer"},
                                    status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class OrderListView(generics.ListAPIView):
    """
    Returns a list of the orders in the system with a status 200. While allowing for filtering with order id.
    """
    serializer_class = OrderSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = CustomerOrder.objects.all().order_by('updated')
        query = self.request.GET.get("qo")
        if query is not None:
            queryset_list = queryset_list.filter(
                Q(order_id=query)
            ).distinct()
            return queryset_list
        else:
            return queryset_list

class OrderItemListView(generics.ListAPIView):
    """
    Returns a list of order items while allowing for filtering with order item id with a status 200.

    """
    serializer_class = OrderItemSerializer
    queryset         = OrderItem.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset_list = OrderItem.objects.all().order_by('updated')
        query = self.request.GET.get("qo")
        if query is not None:
            queryset_list = queryset_list.filter(
                Q(order_id=query)
            ).distinct()
            return queryset_list
        else:
            return queryset_list