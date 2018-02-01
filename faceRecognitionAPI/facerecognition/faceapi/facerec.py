import cv2
import os
import numpy as np
#import matplotlib.pyplot as plt

from django.conf import settings

# Load OpenCV face detector
haar_classifier = 'haarcascade_frontalface_alt.xml'
lbp_classifier = 'lbpcascade_frontalface.xml'

lbp_path = os.path.join(settings.RESOURCE_ROOT, lbp_classifier)

# Labels
subjects = ["", "Tom Cruise", "Shahrukh Khan"]


# Function to detect face using OpenCV
def detect_face(img):
	# convert the test image to gray image as opencv face detector expects gray images
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# load OpenCV face detector, LBP(Local Binary Classifier) cascade classifier which is faster
	# than Haar classifier (But this one is more accurate)
	face_cascade = cv2.CascadeClassifier(lbp_path)

	# multiscale detection of images, the result is a list of faces
	faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

	# if no faces are detected then return original image
	if (len(faces) == 0):
		return None, None

	# Assuming that ther is only one face
	(x, y, w, h) = faces[0]

	# return only the face part of the image
	return gray[y:y + w, x:x + h], faces[0]

# Prepare training data
def prepare_training_data(data_folder_path):
	# Step 1: get directories (one dir for each subject) in data folder
	dirs = os.listdir(data_folder_path)

	# list to hold all subjects faces
	faces = []

	# list to hold labels for all subjects
	labels = []

	# read images of each directory
	for dir_name in dirs:
		if not dir_name.startswith('s'):
			continue

		# Step 2: Extract labels
		label = int(dir_name.replace('s',''))

		# build path of directory that contains images
		subject_dir_path = data_folder_path + "/" + dir_name

		# get the images names
		subject_images_names = os.listdir(subject_dir_path)

		# Step 3: read images and detect faces
		for image_name in subject_images_names:
			if image_name.startswith("."):
				continue

			# build image path
			image_path = subject_dir_path + "/" + image_name

			# read image
			image = cv2.imread(image_path)

			# some displays
			cv2.imshow("Training on image...", image)
			cv2.waitKey(100)

			# detect face
			face, rect = detect_face(image)

			# Step 4: Ignore faces that are not detected
			if face is not None:
				faces.append(face)
				labels.append(label)

	cv2.destroyAllWindows()
	cv2.waitKey(1)
	cv2.destroyAllWindows()

	return faces, labels