from rest_framework import generics, mixins, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.db.models import Q
from postings.models import BlogPost
from .serializers import *
from .permissions import *


class RegisterAPI(generics.GenericAPIView):
	serializer_class = RegisterSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		return Response({"response":"registration successful"})

class BlogPostAPIView(mixins.CreateModelMixin, generics.ListAPIView): # can also use listcreateapiview
	serializer_class = BlogPostSerializer
	permission_classes = [IsOwnerOrReadOnly]

	def get_queryset(self):
		# 127.0.0.1:8000/api/postings/?q=posts hi
		if self.request.user.is_authenticated:
			qs = BlogPost.objects.filter(user=self.request.user) # requires to login user in tests
		else:
			raise PermissionDenied("cannot get anonymous")
		query = self.request.GET.get("q")
		if query is not None:
			qs = qs.filter(Q(title__icontains=query)|Q(content__icontains=query)).distinct()

		return qs

	def perform_create(self, serializer):
		if self.request.user.is_authenticated:
			serializer.save(user=self.request.user)
		else:
			raise PermissionDenied("cannot post anonymous")

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	# to add the port and main url, add this to the serializer context and the
	# get it in the serializer class get_url
	# and pass it in models get_api_url as argument
	def get_serializer_context(self, *args, **kwargs):
		return {"request":self.request}



class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView):
	lookup_field = 'pk'
	serializer_class = BlogPostSerializer
	permission_classes = [IsOwnerOrReadOnly]

	def get_queryset(self):
		if self.request.user.is_authenticated:
			return BlogPost.objects.filter(user=self.request.user)
		else:
			raise PermissionDenied("cannot get anonymous")

	# to add the port and main url, add this to the serializer context and the
	# get it in the serializer class get_url
	# and pass it in models get_api_url as argument
	def get_serializer_context(self, *args, **kwargs):
		return {"request":self.request}
