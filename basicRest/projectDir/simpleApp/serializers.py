from django.contrib.auth.models import User, Group
from rest_framework import serializers

from simpleApp.models import Product


class UserSerializer(serializers.HyperlinkedModelSerializer):
	"""docstring for UserSerializer"""
	#def __init__(self, arg):
	#	super(UserSerializer, self).__init__()
	#	self.arg = arg
	
	class Meta:
		model = User
		fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ('id', 'name', 'description', 'price')


class IncredibleInputSerializer(serializers.Serializer):
	input_x = serializers.IntegerField()
	input_y = serializers.IntegerField()