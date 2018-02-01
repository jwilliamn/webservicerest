from django.shortcuts import render
from django.conf import settings
import os

from rest_framework import generics
from django.http import Http404
from rest_framework.response import Response
from rest_framework import views
from django.http import JsonResponse

from faceapi.facerec import prepare_training_data


# Load data directories
dir_path = os.path.join(settings.MEDIA_ROOT, 'training-data')

# Create your views here.
class IncredibleView(views.APIView):
    def get(self, request):
        # Get the model input
        print("Preparing data...")
        faces, labels = prepare_training_data(dir_path)
        print("Total faces: ", len(faces))
        print("Total labels: ", len(labels))

        # Perform the complex calculations
        complex_result = len(faces) + len(labels)
        print("complex_result: ", complex_result)

        # Return it in your custom format
        return JsonResponse({
            "complex_result": complex_result,
            })