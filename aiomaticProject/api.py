from django.http import HttpRequest, HttpResponse

# Source for the following code: https://pythonprogramming.net/convolutional-neural-network-kats-vs-dogs-machine-learning-tutorial/
# Being used purely for testing and proof of concept. Slight edits made.
##################################################################################################
import cv2                 # working with, mainly resizing, images
import numpy as np         # dealing with arrays
import os                  # dealing with directories
from random import shuffle # mixing up or currently ordered data that might lead our network astray in training.
from tqdm import tqdm      # a nice pretty percentage bar for tasks. Thanks to viewer Daniel BA1/4hler for this suggestion
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import tensorflow as tf
import zipfile

TRAIN_DIR = './aiomaticProject/server_train'
TEST_DIR = './test'
IMG_SIZE = 50
LR = 1e-3

MODEL_NAME = 'dogsvscats-{}-{}.model'.format(LR, '2conv-basic') # just so we remember which saved model is which, sizes must match


def label_img(img):
    word_label = img.split('.')[-3]
    # conversion to one-hot array [cat,dog]
    if word_label == 'cat':  # [much cat, no dog]
        return [1, 0]
    elif word_label == 'dog':  # [no cat, very doggo]
        return [0, 1]


def create_train_data():
    training_data = []
    print("Creating training data...")
    for img in tqdm(os.listdir(TRAIN_DIR + '/train')):
        try: # Some of the images will fail, not sure exactly why
            label = label_img(img)
            path = os.path.join(TRAIN_DIR + '/train/', img)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            training_data.append([np.array(img), np.array(label)])
        except Exception as err:
            print("There was an error: {}, with {}".format(err, img))
    shuffle(training_data)
    np.save(TRAIN_DIR + '/train_data.npy', training_data)
    return training_data


# Might not need this. This may be for visualizing test data against trained model
def process_test_data():
    testing_data = []
    for img in tqdm(os.listdir(TEST_DIR)):
        path = os.path.join(TEST_DIR, img)
        img_num = img.split('.')[0]
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        testing_data.append([np.array(img), img_num])

    shuffle(testing_data)
    np.save('test_data.npy', testing_data)
    return testing_data


def create_trained_model(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # Create the preprocessed training data
        zipf = request.FILES['archive']
        with zipfile.ZipFile(zipf, 'r') as z:
            z.extractall(TRAIN_DIR)

        # This file is just used to display thumbnails in finder. It is not necessary, and it will fail when training
        os.remove(TRAIN_DIR +'/train/Thumbs.db')

        train_data = create_train_data()

        print("Starting convolutional neural network...")
        # Making the convolutional neural network. Adding more layers can train the model better,
        #   but having too many could overfit
        convnet = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 1], name='input')

        convnet = conv_2d(convnet, 32, 5, activation='relu')
        convnet = max_pool_2d(convnet, 5)

        convnet = conv_2d(convnet, 64, 5, activation='relu')
        convnet = max_pool_2d(convnet, 5)

        convnet = conv_2d(convnet, 128, 5, activation='relu')
        convnet = max_pool_2d(convnet, 5)

        convnet = conv_2d(convnet, 64, 5, activation='relu')
        convnet = max_pool_2d(convnet, 5)

        convnet = conv_2d(convnet, 32, 5, activation='relu')
        convnet = max_pool_2d(convnet, 5)

        convnet = fully_connected(convnet, 1024, activation='relu')
        convnet = dropout(convnet, 0.8)

        convnet = fully_connected(convnet, 2, activation='softmax')
        convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

        model = tflearn.DNN(convnet, tensorboard_dir='log')

        train = train_data[:-500]
        test = train_data[-500:]

        X = np.array([i[0] for i in train]).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
        Y = [i[1] for i in train]

        test_x = np.array([i[0] for i in test]).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
        test_y = [i[1] for i in test]

        print("Fitting model...")
        model.fit({'input': X}, {'targets': Y}, n_epoch=3, validation_set=({'input': test_x}, {'targets': test_y}),
            snapshot_step=500, show_metric=True, run_id=MODEL_NAME)

        response = HttpResponse(model)

    elif request.method == "GET":
        response = HttpResponse("This is a GET request. Send a POST request with data to train and the server will return\
                                a trained model!")
    else:
        response = HttpResponse("Please either send a POST request or go to \
                                http://127.0.0.1:8000/aiomaticProject/api (GET request)")

    return response
##################################################################################################

