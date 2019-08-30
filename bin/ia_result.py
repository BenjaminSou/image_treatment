#!/usr/bin/env python3

from acquisition import AcquisitionStep
import requests
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

PLUGIN_DIR = os.environ["MFDATA_CURRENT_PLUGIN_DIR"]
INCOMING_DIR = os.environ["MFDATA_NGINX_UPLOAD_DIR"]
LOCALHOST_PORT = os.environ.get("MFDATA_IMAGE_TREATMENT_LOCALHOST_PORT",
                                "18942")


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
        self.model.load_weights(PLUGIN_DIR +
                                "/IA/MobileNet_5.weights.150-0.41.my_model")

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
        at.tags["actions"] = ""
        at.tags["weather"] = self.use_model(at.filepath)
        new_file_name = (at.tags["first.core.original_basename"]
                           .decode("utf-8"))
        at.copy(PLUGIN_DIR + "/files/final/%s"
                % new_file_name)

        with open((PLUGIN_DIR + "/files/final/%s"
                   % new_file_name), "rb") as file:
            requests.put('http://localhost:%s/storage/map_snow/%s/%s.jpg'
                         % (LOCALHOST_PORT,
                            at.tags["date"].decode("utf-8")[:-9],
                            new_file_name),
                         data=file.read())

        at.tags["actions"] = "db"
        at.move_or_copy(INCOMING_DIR + "/%s" % new_file_name)


if __name__ == "__main__":
    x = Image_treatmentIaStep()
    x.run()
