# Web Service Implementation
I have been developing python apps, mostly backend apps that run on a bash shell. They work just as I want. 
But recently I needed to integrate my python apps to apps written in other languages. Eventhough that there are tools that can help us with the task, I find it difficult. 
To do the integration an easy task I adopted what cloud App providers do. Provide services through an API to the client application.

## Basic Rest API
Since I am new to web services I'll start from basic implementation using Django Rest framework
you can learn more [here](http://www.django-rest-framework.org/)


## Face Recognition API

### Requests
You can use the API by making a `GET` request to the following endpoints:

| Endpoint     | Description    |
| ------------- |:-------------:|
| `/facerec`   | Used to recognize a person |

In facerec endpoint I use chunks of code of this amazing [tutorial](https://github.com/informramiz/opencv-face-recognition-python)


## Full API

### Requests
This API accepts `GET` or `POST` requests in the following endpoints:

| Endpoint     | Method         | Description|
| ------------- |:-------------:|:----------:|
| `/recognize` | `GET`          | http://localhost:8000/recognize/?url=http:url/path/to/image|
| `/test`      | `POST`         | make request post given: (url, data=files)|

This is a basic API that uses the most used methods `GET` and `POST`. In clientApp subdirectory I wrote client.py that send post requests of encoded images to the `/test` endpoint.

To get this done I used the following references:
[client side](https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594), eventhough that this reference uses Flask, I adapted to Django.

[server side](https://github.com/wassgha/FaceRecognitionAPI/blob/master/api/views.py)
