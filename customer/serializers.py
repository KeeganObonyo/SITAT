from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers
from rest_framework.serializers import (
    EmailField,
    ModelSerializer,
)

from order.models import ( 
    CustomerOrder,
    OrderItem
)
from .models import Customer

class CustomerSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'username',
            'phone_number',
            'email',
        ]

class CustomerCreateSerializer(ModelSerializer):
    email = EmailField(label='Email Address')

    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'username',
            'phone_number',
            'email',
            'password',
        ]
        extra_kwargs = {"password":
                        {"write_only": True}
                        }

    def validate(self, value):
        data = self.get_initial()
        email1 = data.get("email1")
        user_qs = Customer.objects.filter(email=email1)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")

        return value

    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        username = validated_data['username']
        phone_number = validated_data['phone_number']
        email = validated_data['email']
        password = validated_data['password']

        customer_obj = Customer(
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone_number=phone_number,
            email=email
        )
        customer_obj.set_password(password)
        customer_obj.save()
        try:
            customers = Group.objects.get(name='customers')
        except:
            customers = Group.objects.create(name="customers")

        customer_obj.groups.add(customers)

        content_type1 = ContentType.objects.get_for_model(
            CustomerOrder)
        try:
            permission1 = Permission.objects.get(
                id=Permission.objects.filter(
                    content_type=content_type1,
                    codename__icontains='add_').values(
                    'id')[0]['id'])
        except:
            permission1 = Permission.objects.create(
                codename="add_order",
                content_type=content_type1)
        customers.permissions.add(permission1)
        try:
            permission2 = Permission.objects.get(
                id=Permission.objects.filter(
                    content_type=content_type1,
                    codename__icontains='view_').values(
                    'id')[0]['id'])
        except:
            permission2 = Permission.objects.create(
                codename="view_order",
                content_type=content_type1)
        customers.permissions.add(permission2)
        try:
            permission3 = Permission.objects.get(
                id=Permission.objects.filter(
                    content_type=content_type1,
                    codename__icontains='change_').values(
                    'id')[0]['id'])
        except:
            permission3 = Permission.objects.create(
                codename="change_order",
                content_type=content_type1)
        customers.permissions.add(permission3)
        content_type2 = ContentType.objects.get_for_model(
            OrderItem)
        try:
            permission4 = Permission.objects.get(
                id=Permission.objects.filter(
                    content_type=content_type2,
                    codename__icontains='add_').values(
                    'id')[0]['id'])
        except:
            permission4 = Permission.objects.create(
                codename="add_orderitem",
                content_type=content_type2)
        customers.permissions.add(permission4)
        try:
            permission5 = Permission.objects.get(
                id=Permission.objects.filter(
                    content_type=content_type2,
                    codename__icontains='view_').values(
                    'id')[0]['id'])
        except:
            permission5 = Permission.objects.create(
                codename="view_orderitem",
                content_type=content_type2)
        customers.permissions.add(permission5)
        try:
            permission6 = Permission.objects.get(
                id=Permission.objects.filter(
                    content_type=content_type2,
                    codename__icontains='change_').values(
                    'id')[0]['id'])
        except:
            permission6 = Permission.objects.create(
                codename="change_orderitem",
                content_type=content_type2)
        customers.permissions.add(permission6)
        return validated_data