import numpy as np
import keras
import tensorflow as tf
from keras import layers
from keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
import os
from PIL import Image
import matplotlib.pyplot as plt
from PIL import ImageFile
from keras.preprocessing import image
from skimage.transform import resize

model = MobileNetV2(layers=layers, weights=None, include_top=True, classes=3)
model.summary()
model.load_weights("MobileNet_5.weights.150-0.41.my_model")
height = 224
width = 224

train_path = 'Data/Train'
validation_path = 'Data/Validation'
test_path = 'Data/Test'


def preprocess(x):
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x.astype(np.float32))
    return x


def preprocess2(x):
    return preprocess(x)[0]


def myIterator(path):
    l = []
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    filesWithDir = [os.path.join(path, file) for file in files]

    for i, elt in enumerate(filesWithDir):
        # Open the file
        img = plt.imread(elt)
        matrix = resize(img, (height, width, 3)) * 255
        t = (matrix, img, elt)
        l.append(t)

    return l


all_data = myIterator("test")

predictions = []

for tuple_data in all_data:
    data = tuple_data[0]
    data_exp = preprocess(data)
    prediction = model.predict(data_exp)
    pred_label = prediction[0]
    elt = pred_label, tuple_data[1], tuple_data[2], tuple_data[0]
    predictions.append(elt)

for elt in predictions:
    pred_label, image, name_of_image, img = elt
    print(pred_label)
    print('Le nom de l image : ', name_of_image)
