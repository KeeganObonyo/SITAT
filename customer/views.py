from rest_framework import generics
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .custom_jwt import jwt_payload_handler
from rest_framework_jwt.settings import api_settings
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from .models import Customer
from .serializers import (
    CustomerCreateSerializer,
    CustomerSerializer
)

class CustomerCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class   = CustomerCreateSerializer
    queryset           = Customer.objects.all()

class UserLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny, ]
    queryset           = Customer.objects.all()

    def post(self, request, format=None):
        try:
            user = Customer.objects.get(username=request.data["username"])
            if request.data["password"] == user.password:
                payload = jwt_payload_handler(user)
                token   = jwt_encode_handler(payload)

                return Response(data={"Username": user.username, "token": token},
                                status=status.HTTP_200_OK)
            else:
                return Response(data={"Info": "Invalid login credentials"},
                                status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(data={"Error": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class CustomerListView(generics.ListAPIView):
    serializer_class = CustomerSerializer
    queryset         = Customer.objects.all()