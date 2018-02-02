import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

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

	
	## detecting all faces
	#print("Found {0} faces!".format(len(faces)))
	## Draw a rectangle around the faces
	#for (x, y, w, h) in faces:
	#	cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

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
			#cv2.imshow("Training on image...", image)
			#cv2.waitKey(100)
			#plt.imshow(image)
			#plt.show()

			# detect face
			face, rect = detect_face(image)

			# Step 4: Ignore faces that are not detected
			if face is not None:
				faces.append(face)
				labels.append(label)

	#cv2.destroyAllWindows()
	#cv2.waitKey(1)
	#cv2.destroyAllWindows()

	return faces, labels


def train_faces(faces, labels):
	# Create the lbph face recognizer
	face_recognizer = cv2.face.LBPHFaceRecognizer_create()
	#or use EigenFaceRecognizer by replacing above line with 
	#face_recognizer = cv2.face.createEigenFaceRecognizer()

	#or use FisherFaceRecognizer by replacing above line with 
	#face_recognizer = cv2.face.createFisherFaceRecognizer()
	face_recognizer.train(faces, np.array(labels))

	return face_recognizer


# Funtion to draw rectangle on images
def draw_rectangle(img, rect):
	(x, y, w, h) = rect
	cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Function to draw text on given image
def draw_text(img, text, x, y):
	cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

# prediction of the person given an image
def predict(test_img, face_recog):
	img = test_img.copy()
	# detect face from the image
	face, rect = detect_face(img)

	# predict the image using our face recognizer
	label = face_recog.predict(face)
	print("label:", label)

	# get name of respective label returned by face recognizer
	label_text = subjects[max(label)]

	# draw_rectangle around the face detected and the name of the predicted person
	draw_rectangle(img, rect)
	draw_text(img, label_text, rect[0], rect[1]-5)

	#plt.imshow(img)
	#plt.show()

	return img, label, label_text