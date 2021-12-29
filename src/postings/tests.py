from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

# from rest_framework_simplejwt.settings import api_settings

# payload_handler = api_settings.SIMPLEJWT_PAYLOAD_HANDLER
# encode_handler = api_settings.JWT_ENCODE_HANDLER

# Create your tests here.

from postings.models import *
User = get_user_model()


class BlogPostAPITestCase(APITestCase):
	def setUp(self):
		user_obj = User(username='testpostings', email="test@test.com")
		user_obj.set_password("somerandompass")
		user_obj.save()
		blogpost = BlogPost.objects.create(
			user=user_obj,
			title='some randome title',
			content="some random content"
			)

	def test_single_user_count(self):
		user_count = User.objects.count()
		self.assertEqual(user_count,1)

	def test_single_post_count(self):
		blog_count = BlogPost.objects.count()
		self.assertEqual(blog_count,1)

	def test_listcreate_list_item_unauthorized(self):
		data = {}
		url = api_reverse('post-listcreate')
		response = self.client.get(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_listcreate_create_item_unauthorized(self):
		data = {"title":"hiss","content":"nothing"}
		url = api_reverse('post-listcreate')
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


	# with token auth

	def test_get_list_authorized_token(self):
		data = {}
		url = api_reverse('post-listcreate')
		user = User.objects.first()
		refresh = RefreshToken.for_user(user)
		self.client.credentials(HTTP_AUTHORIZATION='Bearer '+str(refresh.access_token))
		response = self.client.get(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
			

	def test_create_item_authorized_token(self):
		data = {"title":"hello nothings", "content":"some random content"}
		url = api_reverse('post-listcreate')
		user = User.objects.first()
		refresh = RefreshToken.for_user(user)
		self.client.credentials(HTTP_AUTHORIZATION='Bearer '+str(refresh.access_token))
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_retrieve_item_unauthorized(self):
		blog = BlogPost.objects.first()
		data = {}
		url = blog.get_api_url()
		response = self.client.get(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_update_item_unauthorized(self):
		blog = BlogPost.objects.first()
		data = {"title":"hellows", "content":"nothing"}
		url = blog.get_api_url()
		response = self.client.put(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_delete_item_unauthorized(self):
		blog = BlogPost.objects.first()
		url = blog.get_api_url()
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)





	# test for authenticated with token

	def test_retrieve_item_unauthorized_authenticated_token(self):
		blog = BlogPost.objects.first()
		data = {}
		url = blog.get_api_url()
		user_obj = User(username='test', email="tests@test.com")
		user_obj.set_password("somerandompass")
		user_obj.save()
		user = User.objects.last()
		refresh = RefreshToken.for_user(user)
		self.client.credentials(HTTP_AUTHORIZATION='Bearer '+str(refresh.access_token))
		response = self.client.get(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_update_item_unauthorized_authenticated_token(self):
		blog = BlogPost.objects.first()
		data = {"title":"hellows", "content":"nothing"}
		url = blog.get_api_url()
		user_obj = User(username='test', email="tests@test.com")
		user_obj.set_password("somerandompass")
		user_obj.save()
		user = User.objects.last()
		refresh = RefreshToken.for_user(user)
		self.client.credentials(HTTP_AUTHORIZATION='Bearer '+str(refresh.access_token))
		response = self.client.put(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_delete_item_unauthorized_authenticated_token(self):
		blog = BlogPost.objects.first()
		url = blog.get_api_url()
		user_obj = User(username='test', email="tests@test.com")
		user_obj.set_password("somerandompass")
		user_obj.save()
		user = User.objects.last()
		refresh = RefreshToken.for_user(user)
		self.client.credentials(HTTP_AUTHORIZATION='Bearer '+str(refresh.access_token))
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



	def test_retrieve_item_authorized_authenticated_token(self):
		blog = BlogPost.objects.first()
		data = {}
		url = blog.get_api_url()
		user = User.objects.first()
		refresh = RefreshToken.for_user(user)
		self.client.credentials(HTTP_AUTHORIZATION='Bearer '+str(refresh.access_token))
		response = self.client.get(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_update_item_authorized_authenticated_token(self):
		blog = BlogPost.objects.first()
		data = {"title":"hellows", "content":"nothing"}
		url = blog.get_api_url()
		user = User.objects.first()
		refresh = RefreshToken.for_user(user)
		self.client.credentials(HTTP_AUTHORIZATION='Bearer '+str(refresh.access_token))
		response = self.client.put(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)


	def test_delete_item_authorized_authenticated_token(self):
		blog = BlogPost.objects.first()
		url = blog.get_api_url()
		user = User.objects.first()
		refresh = RefreshToken.for_user(user)
		self.client.credentials(HTTP_AUTHORIZATION='Bearer '+str(refresh.access_token))
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



	# basic login basic login

	def test_get_list_authorized(self):
		data = {}
		url = api_reverse('post-listcreate')
		self.client.login(username='testpostings', password='somerandompass')
		response = self.client.get(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
			

	def test_create_item_authorized(self):
		data = {"title":"hello nothings", "content":"some random content"}
		url = api_reverse('post-listcreate')
		self.client.login(username='testpostings', password='somerandompass')
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_retrieve_item_unauthorized_authenticated(self):
		blog = BlogPost.objects.first()
		data = {}
		url = blog.get_api_url()
		user_obj = User(username='test', email="tests@test.com")
		user_obj.set_password("somerandompass")
		user_obj.save()
		self.client.login(username='test', password='somerandompass')
		response = self.client.get(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_update_item_unauthorized_authenticated(self):
		blog = BlogPost.objects.first()
		data = {"title":"hellows", "content":"nothing"}
		url = blog.get_api_url()
		user_obj = User(username='test', email="tests@test.com")
		user_obj.set_password("somerandompass")
		user_obj.save()
		self.client.login(username='test', password='somerandompass')
		response = self.client.put(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_delete_item_unauthorized_authenticated(self):
		blog = BlogPost.objects.first()
		url = blog.get_api_url()
		user_obj = User(username='test', email="tests@test.com")
		user_obj.set_password("somerandompass")
		user_obj.save()
		self.client.login(username='test', password='somerandompass')
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_retrieve_item_authorized_authenticated(self):
		blog = BlogPost.objects.first()
		data = {}
		url = blog.get_api_url()
		self.client.login(username='testpostings', password='somerandompass')
		response = self.client.get(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_update_item_authorized_authenticated(self):
		blog = BlogPost.objects.first()
		data = {"title":"hellows", "content":"nothing"}
		url = blog.get_api_url()
		self.client.login(username='testpostings', password='somerandompass')
		response = self.client.put(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)


	def test_delete_item_authorized_authenticated(self):
		blog = BlogPost.objects.first()
		url = blog.get_api_url()
		self.client.login(username='testpostings', password='somerandompass')
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	# test user login and register
	def test_user_login(self):
		data = {
			"username":"testpostings",
			"password":"somerandompass"
		}
		url = api_reverse("token_obtain_pair")
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		# unauthorized

		data = {
			"username":"testpostingss",
			"password":"somerandompass"
		}
		url = api_reverse("token_obtain_pair")
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		

	def test_user_refresh_token(self):
		data = {
			"username":"testpostings",
			"password":"somerandompass"
		}
		url = api_reverse("token_obtain_pair")
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		if response.status_code == status.HTTP_200_OK:
			uri = api_reverse("token_refresh")
			resp = self.client.post(uri, {"refresh":response.data['refresh']}, format='json')
			self.assertEqual(resp.status_code, status.HTTP_200_OK)

		data = {
			"username":"testpostingss",
			"password":"somerandompass"
		}
		url = api_reverse("token_obtain_pair")
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		if response.status_code != status.HTTP_401_UNAUTHORIZED:
			uri = api_reverse("token_refresh")
			resp = self.client.post(uri, {"refresh":response.data['refresh']}, format='json')
			self.assertEqual(resp.status_code, status.HTTP_200_OK)


	def test_user_register(self):
		url = api_reverse("register")
		data = {
			"username":"hi",
			"email":"hi@hi.com",
			"password":"hi",

		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		# testing invalid input 

		url = api_reverse("register")
		data = {
			"username":"hi",
			"email":"hihi.com",
			"password":"hi",

		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)