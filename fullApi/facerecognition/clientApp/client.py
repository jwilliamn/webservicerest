import requests
import json
import cv2
import base64


# Server address
addr = 'http://127.0.0.1:8000'
test_url = addr + '/test/'

# Local media
image_path = '/home/williamn/Downloads/cachorro_autismo.jpg'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

img = cv2.imread('/home/williamn/Downloads/cachorro_autismo.jpg')
# encode image as jpeg
_, img_encoded = cv2.imencode('.jpg', img)

with open(image_path, "rb") as img:
	image_data=img.read()

image_64encode = base64.encodestring(image_data)
print(type(image_64encode))
#print(type(image_data))
files = {'data': image_64encode}

# send http request with image and receive response
response = requests.post(test_url, data=files) #data=img_encoded.tostring()
# decode response
print(json.loads(response.text))