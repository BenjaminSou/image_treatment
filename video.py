#!/usr/bin/env python3

import cv2
from acquisition import AcquisitionStep
from xattrfile import XattrFile


class CropperMainStep(AcquisitionStep):

    plugin_name = "placer"
    step_name = "place"

    def process(self, xaf):
        self.info("process for file %s" % xaf.filepath)
        self.getFirstFrame(xaf)
        return True

    def getFirstFrame(self, at):
        at.tags["actions"] = \
            ",".join((at.tags["actions"].decode('utf-8')).split(",")[1:])
        vidcap = cv2.VideoCapture(at.filepath)
        success, image = vidcap.read()
        if success:
            cv2.imwrite("frame.jpg", image)
        vidcap.release()
        output_attr = XattrFile("frame.jpg")
        for key in at.tags:
            output_attr.tags[key] = at.tags[key]
        output_attr.commit()
        output_attr.move_or_copy("/home/mfdata/var/in/incoming/test")


if __name__ == "__main__":
    x = CropperMainStep()
    x.run()
