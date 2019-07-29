#!/usr/bin/env python3


import json
import requests
import shutil

from PIL import Image
from acquisition import AcquisitionStep
from xattrfile import XattrFile
from time import sleep
from datetime import datetime


class file_downloader(AcquisitionStep):

    plugin_name = "image_treatment"
    plugin_step_name = "main"

    def __init__(self):
        """Initialization: self.link needs the http request you seek."""
        self.data = self.get_json()
        self.file = dict()
        for name in self.data:
            self.file[name] = ""

        self.log_creation = ["File(s) created: "]

    def get_json(self):
        """Import information in file urls."""
        with open("urls.json") as file_url:
            return json.load(file_url)

    def http_request(self, url, name, header=None):
        """Create new file from http get if not already existing."""
        now = datetime.now().strftime("%m_%d_%Y_%H:%M:%S")

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
            if request.content != self.file[name]:
                path = "files/got/%s_%s.jpg" % (name, now)
                with open(path, "wb") as filer:
                    self.file[name] = request.content
                    filer.write(self.file[name])
                    if self.file_is_truncated(path):
                        return 1
                    self.add_tags_and_copy(name, path)
                    self.log_creation.append(name)
        else:
            self.warning("Error: request status = %s for url %s"
                         % (request.status_code, url))

    def file_is_truncated(self, file_path):
        try:
            image_file = Image.open(file_path)
            image_file.close()
        except IOError:
            self.warning("IOError: Image %s truncated send to truncated folder"
                         % file_path)
            shutil.move(file_path,
                        "truncated_files/truncated_" + file_path[10:])
            return 1
        return 0

    def add_tags_and_copy(self, name, file_path):
        """
        Add tags to the given file.

        Attention, json tag can't have anything different from strings
        Use load_parameters_from to get dict in json.
        """
        tagger = XattrFile(file_path)
        if self.data[name]["actions"]:
            tagger.tags["actions"] = ",".join(self.data[name]["actions"])
        else:
            tagger.tags["actions"] = ""
        self.load_parameters_from("crop", tagger, name)
        self.get_string_from("location", tagger, name)
        tagger.commit()
        tagger.copy("/home/mfdata/var/in/incoming/%s" % file_path[10:])

    def get_string_from(self, key, xaf, name):
        content = self.data[name].get(key)
        if content:
            xaf.tags[key] = content
        else:
            self.info('No "%s" parameter found in json of %s' % (key, name))

    def load_parameters_from(self, key, xaf, name):
        if self.data[name][key]:
            for label in self.data[name][key]:
                xaf.tags[label] = self.data[name][key][label]

    def print_log_creation(self):
        if len(self.log_creation) > 1:
            self.info(self.log_creation[0] + ", ".join(self.log_creation[1:]))
            self.log_creation = [self.log_creation[0]]

    def run(self):
        """
        Run the program.

        Differenciate refere and no header to
        get jpg images.
        """
        print("\n------------------  Starting main.py  -------------------")
        while True:
            for data in self.data:
                if self.data[data]["http_referer"]:
                    self.http_request(self.data[data]["url"], data,
                                      self.data[data]["http_referer"])
                else:
                    self.http_request(self.data[data]["url"], data)
            self.print_log_creation()
            sleep(60)


if __name__ == '__main__':
    x = file_downloader()
    x.run()
