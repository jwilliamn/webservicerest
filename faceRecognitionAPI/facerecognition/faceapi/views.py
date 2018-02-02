from django.shortcuts import render
from django.conf import settings
import os

from rest_framework import generics
from django.http import Http404
from rest_framework.response import Response
from rest_framework import views
from django.http import JsonResponse

import cv2
import matplotlib.pyplot as plt
from faceapi.facerec import prepare_training_data, train_faces, predict


# Load data directories
dir_path = os.path.join(settings.MEDIA_ROOT, 'training-data')

# Write results to output
res_path = os.path.join(settings.OUTPUT_ROOT)

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

		# trainig of the images
		face_recognizer = train_faces(faces, labels)

		# Prediction of images
		print("Predicting images...")

		# load test images
		test_img1 = cv2.imread(os.path.join(settings.MEDIA_ROOT, 'test-data/test1.jpg'))
		test_img2 = cv2.imread(os.path.join(settings.MEDIA_ROOT, 'test-data/test2.jpg'))

		# perform a prediction
		predicted_img1, lb, lbtxt = predict(test_img1, face_recognizer)
		predicted_img2, _, _ = predict(test_img2, face_recognizer)

		# create a figure of 2 plots (one for each test image)
		#f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))

		# display test image1 and image2
		#plt.imshow(cv2.cvtColor(predicted_img1, cv2.COLOR_BGR2RGB))
		#plt.show()
		#plt.close()
		cv2.cvtColor(predicted_img1, cv2.COLOR_BGR2RGB)
		cv2.cvtColor(predicted_img2, cv2.COLOR_BGR2RGB)
		#ax1.imshow(cv2.cvtColor(predicted_img1, cv2.COLOR_BGR2RGB))
		#ax2.imshow(cv2.cvtColor(predicted_img2, cv2.COLOR_BGR2RGB))

		# display both images
		#cv2.imshow("Tom cruise test", predicted_img1)
		#cv2.imshow("Shahrukh Khan test", predicted_img2)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		#cv2.waitKey(1)
		#cv2.destroyAllWindows()
		cv2.imwrite(os.path.join(res_path, "out1.png"), predicted_img1)

		# Return it in your custom format
		return JsonResponse({
			"complex_result": complex_result,
			"label": lb,
			"label text": lbtxt
		})