#!/usr/bin/env python3

import os
import json
import requests
import shutil

from PIL import Image
from acquisition import AcquisitionStep
from xattrfile import XattrFile
from time import sleep
from datetime import datetime

MFDATA_DIR = os.environ["MFDATA_CURRENT_PLUGIN_DIR"]
INCOMING_DIR = os.environ["MFDATA_NGINX_UPLOAD_DIR"] + "/"


class file_downloader(AcquisitionStep):

    plugin_name = "image_treatment"
    plugin_step_name = "main"

    def __init__(self):
        self.data = self.get_json()
        self.file = dict()
        for name in self.data:
            self.file[name] = ""

        self.log_creation = ["File(s) created: "]

    def get_json(self):
        """Import information in file urls."""
        with open("urls.json") as file_url:
            return json.load(file_url)

    def http_request(self, key_name):
        """Create new file from http get if not already existing."""
        now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        url = self.data[key_name]["url"]

        if "http_referer" in self.data[key_name]:
            header = self.data[key_name]["http_referer"]
        request = requests.Session()
        if header:
            request.headers.update({'referer': header})
        try:
            request = request.get(url, timeout=10)
        except (TimeoutError,
                requests.exceptions.Timeout,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout):
            self.warning('TIMEOUT: "%s"' % url)
            return 1
        except requests.exceptions.ConnectionError:
            self.error('ConnectionError with "%s"' % url)
        if request.status_code == 200:
            if request.content != self.file[key_name]:
                path = "files/got/%s_%s" % (key_name, now)
                with open(path, "wb") as filer:
                    self.file[key_name] = request.content
                    filer.write(self.file[key_name])
                    self.add_tags_and_copy(key_name, path)
                    self.log_creation.append(key_name)
        else:
            self.warning("Error: request status = %s for url %s"
                         % (request.status_code, url))

    def file_is_truncated(self, file_path):
        dir_path = file_path[10:]
        try:
            image_file = Image.open(file_path)
            image_file.close()
        except IOError:
            self.warning("IOError: Image %s truncated send to truncated folder"
                         % file_path)
            shutil.move(file_path,
                        "files/truncated_files/truncated_" + dir_path[10:])
            return 1
        return 0

    def add_tags_and_copy(self, name, file_path):
        """
        Add tags to the given file.

        Attention, json tag can't have anything different from strings
        Use load_parameters_from to get dict in json.
        """
        tagger = XattrFile(file_path)
        tagger.tags["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.load_parameters(tagger, name)
        tagger.commit()
        tagger.copy(INCOMING_DIR + file_path[10:])

    def load_parameters(self, xaf, name):
        for label in self.data[name]:
            if isinstance(self.data[name][label], str):
                xaf.tags[label] = self.data[name][label]
            elif type(self.data[name][label]) == list:
                xaf.tags[label] = ",".join(self.data[name][label])
            else:
                self.warning("%s %s: %s json label type"
                             % (name, label, type(self.data[name][label])))

    def print_log_creation(self):
        if len(self.log_creation) > 1:
            self.info(self.log_creation[0] + ", ".join(self.log_creation[1:]))
            self.log_creation = [self.log_creation[0]]

    def run(self):
        print("\n------------------  Starting main.py  -------------------")
        while True:
            for camera_name in self.data:
                self.http_request(camera_name)
            self.print_log_creation()
            sleep(60)


if __name__ == '__main__':
    x = file_downloader()
    x.run()
