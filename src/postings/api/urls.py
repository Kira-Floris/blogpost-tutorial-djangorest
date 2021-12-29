from django.urls import path
from .views import *


urlpatterns = [
    path('<str:pk>/', BlogPostRudView.as_view(), name="post-rud"),
    path('', BlogPostAPIView.as_view(), name="post-listcreate"),
]