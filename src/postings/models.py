from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.reverse import reverse as api_reverse # usefull to get the complete url with port and route

# Create your models here.

class BlogPost(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
	title = models.CharField(max_length=200, null=True, blank=True)
	content = models.TextField(max_length=200,null=True,blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.user.username)

	@property
	def owner(self):
		return self.user

	# def get_absolute_url(self):
	# 	return reverse("post-rud", kwargs={"pk":self.pk})

	def get_api_url(self, request=None):
		return api_reverse("post-rud", kwargs={'pk':self.pk}, request=request)
