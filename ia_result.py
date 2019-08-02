#!/usr/bin/env python3

from acquisition import AcquisitionStep
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


class Image_treatmentIaStep(AcquisitionStep):

    plugin_name = "image_treatment"
    step_name = "ia"

    def init(self):
        self.model = MobileNetV2(layers=layers,
                                 weights=None, include_top=True, classes=3)
        self.model.load_weights("MobileNet_5.weights.150-0.41.my_model")

    def process(self, xaf):
        self.info("process for file %s" % xaf.filepath)
        self.add_weather(xaf)
        return True

    def use_model(self, path):
        tuple_data = myIterator(path)
        data = tuple_data[0]
        data_exp = preprocess(data)
        prediction = self.model.predict(data_exp)
        pred_label = prediction[0]

        return str(np.argmax(pred_label))

    def add_weather(self, at):
        del at.tags["actions"]
        at.tags["weather"] = self.use_model(at.filepath)
        at.move_or_copy("files/final/%s"
                        % (at.tags["first.core.original_basename"]
                           .decode("utf-8")))


if __name__ == "__main__":
    x = Image_treatmentIaStep()
    x.run()
