from django.urls import path
from .views import *


urlpatterns = [
    path('<str:pk>/', BlogPostRudView.as_view(), name="post-rud"),
    path('auth', BlogPostAPIView.as_view(), name="post-listcreate"),
    path('', BlogPostCustomerAPIView.as_view(), name="post-listcustomer")
]