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


height = 224
width = 224


def preprocess(x):
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x.astype(np.float32))
    return x


def preprocess2(x):
    return preprocess(x)[0]


def myIterator(path):
    # Open the file
    img = plt.imread(path)
    matrix = resize(img, (224, 224, 3)) * 255
    return (matrix, img, path)


def main_function(path):
    model = MobileNetV2(layers=layers,
                        weights=None, include_top=True, classes=3)
    model.load_weights("MobileNet_5.weights.150-0.41.my_model")

    tuple_data = myIterator(path)

    data = tuple_data[0]
    data_exp = preprocess(data)
    prediction = model.predict(data_exp)
    pred_label = prediction[0]

    return np.argmax(pred_label)


def main(path):
    print(main_function(path))
