from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response

import numpy as np
import cv2

import os
import urllib
import base64


# Path of face and smile detectors
FACE_DETECTOR_PATH = os.path.join(settings.RESOURCE_ROOT, "haarcascade_frontalface_default.xml")
SMILE_DETECTOR_PATH = os.path.join(settings.RESOURCE_ROOT, "haarcascade_smile.xml")

TRAIN_DATA_PATH = os.path.join(settings.MEDIA_ROOT, "faces")

# Initial conf. maximun distance between face and match
THRESHOLD = 75


# Create the cascade classifiers
detector = cv2.CascadeClassifier(FACE_DETECTOR_PATH)
smiledetector = cv2.CascadeClassifier(SMILE_DETECTOR_PATH)

# Functions
def _grab_image(path=None, base64_string=None, url=None):
	# if path is not None, then load the image from disk
	if path is not None:
		image = cv2.imread(path)

	# otherwise, the image does not reside on disk
	else:
		# if the URL is not Nonem then download the image
		if url is not None:
			with urllib.request.urlopen(url) as resp:
				data = resp.read()
				image = np.asarray(bytearray(data), dtype="uint8")
				image = cv2.imdecode(image, cv2.IMREAD_COLOR)

		# if the stream is not None, then the image has been uploaded
		elif base64_string is not None:
			image = base64.b64decode(base64_string)
			image = np.fromstring(image, dtype=np.uint8)
			image = cv2.imdecode(image, 1)

	return image



# Endpoints
@csrf_exempt
def recognize(request):
	# initialize the data dictionary to be returned by the request
	data = {}
	# check to see if this is a get request
	if request.method == "GET":
		# check to see if an image was uploaded
		if request.GET.get("imageBase64", None) is not None:
			# grab the uploaded image
			image = _grab_image(base64_string=request.GET.get("imageBase64", None))

		# otherwise, assume that a URL was passed in
		else:
			url = request.GET.get("url", None)
			# if the url is None, then return an error
			if url is None:
				data["error"] = "No URL provided"
				return JsonResponse(data)

			image = _grab_image(url=url)

		# Convert the image to grayscale, load the face cascade detector
		# and detect faces in the image
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		rects = image.shape
		#rects = detector.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5,
		#	minSize=(30,30), flags=0)

		# construct a list of bounding boxes from the detection
		#rects = [(int(x), int(y)) for (x, y) in rects]
		if len(rects) == 0:
			data.update({"detected": False})
		else:
			x, y, w, h = rects[0], rects[1], rects[0], rects[1]
			image_val = {
				"x_value": x,
				"y_value": y,
				"w_value": w,
				"h_value": h,
			}

			data.update({"detected": True, "dimensios": image_val})

	# return a JSON response
	return JsonResponse(data)


@csrf_exempt
def test(request):
	# initialize the data dictionary to be returned by the request
	data = {}
	if request.method == "POST":
		# convert string of image data to uint8
		#print("request", request.POST)
		nparr = np.fromstring(request.POST.get('data', ''), np.uint8)
		# decode image
		img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
		#img = request.POST.get('data', None)
		image_encoded = request.POST.get('data', '')
		image_decoded = base64.b64decode(image_encoded)
		image = np.fromstring(image_decoded, dtype=np.uint8)
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)
		print("type of image_decoded", type(image_decoded))
		print("type of image", type(image), image.shape)

		#cv2.imshow('image', image)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()

		# Convert the image to grayscale, load the face cascade detector
		# and detect faces in the image
		#image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		rects = image.shape
		#rects = detector.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5,
		#	minSize=(30,30), flags=0)

		# construct a list of bounding boxes from the detection
		#rects = [(int(x), int(y)) for (x, y) in rects]
		if len(rects) == 0:
			data.update({"message": False})
		else:
			x, y, w, h = rects[0], rects[1], rects[0], rects[1]
			image_val = {
				"x_value": x,
				"y_value": y,
				"w_value": w,
				"h_value": h,
			}

			data.update({"message": True, "dimensions": image_val})

	# return a JSON response
	return JsonResponse(data)