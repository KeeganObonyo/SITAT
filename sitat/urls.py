from django.conf.urls import include, url
from django.contrib import admin

from customer.views import (
    UserLoginAPIView,
    CustomerCreateAPIView,
    CustomerListView,
)
from order.views import (
    Order, 
    AddOrderItem, 
    ExecuteOrderItem,
    OrderItemListView, 
    OrderListView
)
urlpatterns = [
    url(r'^api/sitat/register/$', CustomerCreateAPIView.as_view(), name='register_new_customer'),
    url(r'^api/sitat/get_token/$', UserLoginAPIView.as_view(), name='user_login'),
    url(r'^api/sitat/users', CustomerListView.as_view(), name='user_list'),
    url(r'admin/', admin.site.urls),
    url(r'^add_order/$', view=Order.as_view(), name='add_order'),
    url(r'^add_order_item/$', view=AddOrderItem.as_view(), name='add_order_item'),
    url(r'^execute_order_item/$', view=ExecuteOrderItem.as_view(), name='execute_order_item'),
    url(r'^list_order_items/$', view=OrderItemListView.as_view(), name='list_order_items'),
    url(r'^list_orders/$', view=OrderListView.as_view(), name='list_orders'),
]