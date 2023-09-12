from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from customer.models import *

from .views import *
from .models import *
from .serializers import *

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


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
            email      = "test1@savannahinformatics.com",
            password   = "passkey"
        )

        admins = Group.objects.create(name="admin")
        customer.groups.add(admins)

        content_type = ContentType.objects.get_for_model(
            Customer)
        try:
            permission = Permission.objects.get(
                id=Permission.objects.filter(
                    content_type=content_type,
                    codename__icontains='view_').values(
                    'id')[0]['id'])
        except:
            permission = Permission.objects.create(
                codename="view_user",
                content_type=content_type1
            )
        admins.permissions.add(permission)

class CustomerTest(APITestCase):

    def setUp(self):
        set_up = SetUpMd().setUp()

    def test_CustomerCreateAPIView(self):
        url = reverse("register_new_customer")
        valid_data = {
            "first_name":"first_name1",
            "last_name":"last_name1",
            "username":"username1",
            "phone_number":"0710123456",
            "email":"test@savannahinformatics.com",
            "password":"password"
        }
        response = self.client.post(url, valid_data, format='json')
        data_with_user_already_exists = {
            "first_name":"first_name1",
            "last_name":"last_name1",
            "username":"username1",
            "phone_number":"0710123456",
            "email":"test1@savannahinformatics.com",
            "password":"password"
        }
        response1 = self.client.post(url, data_with_user_already_exists, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(Customer.objects.all().count(), 2)
        self.assertEqual(Customer.objects.filter(
            email="test@savannahinformatics.com").exists(), True)

    def test_UserLoginAPIView(self):
        url = reverse("user_login")
        valid_data = {
            "username":"username",
            "password":"passkey"
        }
        response = self.client.post(url, valid_data, format='json')
        data = {
           'Username': 'username',
           'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9'
        }
        data_with_invalid_user = {
            "username":"someusername",
            "password":"password"
        }
        response1 = self.client.post(url, data_with_invalid_user, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(dict(response.data).keys(), data.keys())
        self.assertEqual(response1.status_code, 400)

    def test_CustomerListView(self):
        url = reverse("user_list")
        self.client.credentials(
            HTTP_AUTHORIZATION=token_retrieve(self))
        response = self.client.get(url, format='json')
        data = {
            "first_name":"first_name1",
            "last_name":"last_name1",
            "username":"username1",
            "phone_number":"0710123456",
            "email":"test1@savannahinformatics.com"
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(dict(response.data[0]).keys(), data.keys())