#!/usr/bin/env python3


import json
import requests
from xattrfile import XattrFile
from time import sleep
from datetime import datetime


class file_downloader():

    def __init__(self):
        """Initialization: self.link needs the http request you seek."""
        self.data = self.get_json()
        self.file = dict()
        for name in self.data:
            self.file[name] = ""

    def get_json(self):
        """Import information in file urls."""
        with open("urls.json") as file_url:
            return json.load(file_url)

    def http_request(self, url, name, header=None):
        """Create new file from http get if not already existing."""
        now = datetime.now().strftime("%m_%d_%Y_%H:%M:%S")
        if header:
            request = requests.Session()
            request.headers.update({'referer': header})
            request = request.get(url, timeout=20)
        else:
            request = requests.get(url, timeout=20)
        if request.status_code == 200:
            if request.content != self.file[name]:
                path = "files/got/%s_%s.jpg" % (name, now)
                with open(path, "wb") as filer:
                    self.file[name] = request.content
                    filer.write(self.file[name])
                    self.add_tags_and_copy(name, path)
                    print("File %s_%s.jpg created" % (name, now))
        else:
            print("Error: request status = %s for url %s\nheader = %s"
                  % (request.status_code, url, header))

    def add_tags_and_copy(self, name, file_path):
        """
        Add tags to the given file.

        Attention, json tag can't have anything different from strings
        Use load_parameters_from to get dict in json.
        """
        tagger = XattrFile(file_path)
        if self.data[name]["actions"]:
            tagger.tags["actions"] = ",".join(self.data[name]["actions"])
        self.load_parameters_from("crop", tagger, name)
        tagger.commit()
        tagger.copy("/home/mfdata/var/in/incoming/%s" % file_path[10:])

    def load_parameters_from(self, key, xaf, name):
        if self.data[name][key]:
            for label in self.data[name][key]:
                xaf.tags[label] = self.data[name][key][label]

    def run(self):
        """
        Run the program.

        Differenciate refere and no header to
        get jpg images.
        """
        while True:
            print("\n--- New image downloading loop beginning ---")
            for data in self.data:
                if self.data[data]["http_referer"]:
                    self.http_request(self.data[data]["url"], data,
                                      self.data[data]["http_referer"])
                else:
                    self.http_request(self.data[data]["url"], data)
            sleep(60)


if __name__ == '__main__':
    x = file_downloader()
    x.run()
