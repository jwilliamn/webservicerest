from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from simpleApp.serializers import UserSerializer, GroupSerializer, ProductSerializer

from rest_framework import generics
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import views
from simpleApp.models import Product
from simpleApp.serializers import IncredibleInputSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #print(serializer_class.Meta.fields)

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class IncredibleView(views.APIView):
    def get(self, request):
        # Validate incoming input
        serializer = IncredibleInputSerializer(data = request.query_params)
        serializer.is_valid(raise_exception=True)

        # Get the model input
        data = serializer.validated_data
        input_x = data["input_x"]
        input_y = data["input_y"]

        # Perform the complex calculations
        complex_result = input_x + input_y

        # Return it in your custom format
        return Response({
            "complex_result": complex_result,
            })