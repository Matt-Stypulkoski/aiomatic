import requests
import os
from django.views.decorators.csrf import csrf_exempt
import zipfile

# NOTE: THIS CURRENTLY ONLY WORKS IF THE 'django.middleware.csrf.CsrfViewMiddleware' IN THE settings.py
#       FILE IS COMMENTED OUT. IF IT IS NOT COMMENTED OUT, YOU RECEIVE AN "CSRF Cookie Not Set" Error

# Send a POST request to api
URL = 'http://127.0.0.1:8000/aiomaticProject/api'
TRAIN_DATA_DIR = './train/'

@csrf_exempt
def train_model(training_data_path):
    zipf = zipfile.ZipFile('data.zip', 'w')
    print("Sending data...")
    for img in os.listdir(training_data_path):
        zipf.write(os.path.join(training_data_path, img))
    zipf.close()
    print("Data has been sent.")

    response = requests.post(url=URL, files={'archive': open('data.zip', 'rb')})

    trained_model = response.content

    test_model(trained_model)


# TODO
def test_model(model):
    print("Will test the trained model returned by the server response in this function")
    print(model)


train_model(TRAIN_DATA_DIR)