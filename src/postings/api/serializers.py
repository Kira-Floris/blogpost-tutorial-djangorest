from rest_framework import serializers

from postings.models import BlogPost
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username','email','password')
		extra_kwargs = {'password':{'write_only':True}}

class BlogPostSerializer(serializers.ModelSerializer):
	uri = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = BlogPost
		fields = ['uri','pk','user','title','content','timestamp']
		read_only_fields = ['user']

	def get_uri(self, obj):
		request = self.context.get("request")
		return obj.get_api_url(request=request)

	def validate_title(self, value):
		qs = BlogPost.objects.filter(title__iexact=value).exclude(pk=self.instance.pk)
		# it doesnt allow updating with same title even though its for the same instance of blogpost
		# so we add this function of exclude
		if qs.exists():
			raise serializers.ValidationError("title already exists, try another")
		return value