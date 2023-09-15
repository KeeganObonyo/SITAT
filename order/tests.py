from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, User
from rest_framework.test import APITestCase

from customer.models import Customer

from .models import CustomerOrder, OrderItem

def token_retrieve(self):
    login_cred = {
        "username": "username",
        "password": "passkey"
    }
    url = reverse('user_login')
    response = self.client.post(url, login_cred, format='json')
    token    = "JWT " + response.json()["token"]
    return token


class SetUpMd(APITestCase):

    @classmethod
    def setUp(cls):
        customer = Customer.objects.create(
            first_name = "first_name",
            last_name  = "last_name",
            username   = "username",
            email      = "email1",
            password   = "passkey"
        )
        admins = Group.objects.create(name="admin")
        customer.groups.add(admins)

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
        admins.permissions.add(permission1)
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
        admins.permissions.add(permission2)
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
        admins.permissions.add(permission3)
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
        admins.permissions.add(permission4)
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
        admins.permissions.add(permission5)
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
        admins.permissions.add(permission6)
        order = CustomerOrder.objects.create(
            description = "None",
            customer    = customer,
        )
        orderitem = OrderItem.objects.create(
            order       = order,
            description = "None",
            cost        = 130.0
        )

class OrderTest(APITestCase):

    def setUp(self):
        set_up = SetUpMd().setUp()

    def test_Order(self):
        url = reverse("add_order")
        self.client.credentials(
            HTTP_AUTHORIZATION=token_retrieve(self))
        valid_data = {
            "order_items": [
                {"cost": 100.0,
                 "description": "A Text too"},],
            "description": "A text",
            "currency":"KES"
        }
        response = self.client.post(url, valid_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"Error": "Message wasn't sent to customer"})
        self.assertEqual(CustomerOrder.objects.all().count(), 2)
        self.assertEqual(OrderItem.objects.all().count(), 2)
        self.assertEqual(CustomerOrder.objects.filter(
            description="A text").exists(), True)
        self.assertEqual(OrderItem.objects.filter(
            description="A Text too").exists(), True)

    def test_AddOrderItem(self):
        url = reverse("add_order_item")
        self.client.credentials(
            HTTP_AUTHORIZATION=token_retrieve(self))
        valid_data = {
            "description": "Another Text",
            "order_id": 1,
            "cost"    : 120.0
        }
        response      = self.client.post(url, valid_data, format='json')
        updated_order = CustomerOrder.objects.get(id = 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"Error": "Message wasn't sent to customer"})
        self.assertEqual(OrderItem.objects.all().count(), 2)
        self.assertEqual(OrderItem.objects.filter(
            description="Another Text").exists(), True)
        self.assertEqual(updated_order.cost, 250.00)

    def test_ExecuteOrderItem(self):
        url = reverse("execute_order_item")
        self.client.credentials(
            HTTP_AUTHORIZATION=token_retrieve(self))
        valid_data = {
            "item":1
        }
        response           = self.client.post(url, valid_data, format='json')
        updated_order      = CustomerOrder.objects.get(id = 1)
        updated_order_item = OrderItem.objects.get(id = 1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(updated_order_item.cleared, True)
        self.assertEqual(updated_order.cleared, True)

    def test_OrderListView(self):
        url = reverse("list_orders")
        self.client.credentials(
            HTTP_AUTHORIZATION=token_retrieve(self))
        data = {
            'description': 'None',
            'id': 1,
            'cleared': False,
            'updated': '2020-09-11T11:42:53.114790Z',
            'customer': {
                'id': 1,
                'username': 'username',
                'email': 'email1',
                'first_name': 'first_name',
                'last_name': 'last_name'
            },
            'orderitems': [{
                'id': 1,
                'cleared': False,
                'description': 'None',
                'updated': '2020-09-11T11:42:53.114790Z',
                'cost':130.0
            }],
        }
        response = self.client.get(url, format='json')
        self.assertEqual(dict(response.data[0]).keys(), data.keys())
        self.assertEqual(response.status_code, 200)

    def test_OrderItemListView(self):
        url = reverse("list_order_items")
        self.client.credentials(
            HTTP_AUTHORIZATION=token_retrieve(self))
        data = {
            'id': 1,
            'order': 1,
            'cleared': False,
            'description': 'None',
            'updated': '2020-09-11T11:42:53.114790Z',
        }
        response = self.client.get(url, format='json')
        self.assertEqual(dict(response.data[0]).keys(), data.keys())
        self.assertEqual(response.status_code, 200)