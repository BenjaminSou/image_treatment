#!/usr/bin/env python3

import os
import cv2
from acquisition import AcquisitionStep
from PIL import Image
from xattrfile import XattrFile

MFDATA_DIR = os.environ["MFDATA_CURRENT_PLUGIN_DIR"]
INCOMING_DIR = os.environ["MFDATA_NGINX_UPLOAD_DIR"]


class Image_treatmentCropStep(
        AcquisitionStep):

    plugin_name = "image_treatment"
    step_name = "crop"

    def process(self, xaf):
        self.original_file_name = (xaf.tags["first.core.original_basename"]
                                   .decode('utf-8'))
        self.info("process for file %s" % xaf.filepath)
        self.image_crop_and_export(xaf,
                                   xaf.tags[b"crop_x"],
                                   xaf.tags[b"crop_y"],
                                   xaf.tags[b"crop_width"],
                                   xaf.tags[b"crop_height"])
        return True

    def image_crop_and_export(self, input_file, x=0,
                              y=0, w=10, h=10):
        try:
            x, y, w, h = int(x), int(y), int(w), int(h)
        except ValueError as e:
            print(e, "(wrong crop var type)")
        # Cropping part
        try:
            img = cv2.imread(input_file.filepath)
            height, width, depth = img.shape
            resized_image =\
                cv2.resize(img, (1280, int(height * 1280 / width)))
            cv2.imwrite(MFDATA_DIR + "/files/final/%s.jpg"
                        % self.original_file_name, resized_image)

            imageObject = Image.open(input_file.filepath)
        except IOError:
            self.error("IOError: Can't open %s (%s)"
                       % (input_file.filepath, self.original_file_name))
            return 1
        if x + y + w + h:
            output = "cropped_%s" % (self.original_file_name)
            try:
                cropped = imageObject.crop((x, y, w, h))
            except OSError:
                truncated_file_name = ("truncated_%s"
                                       % (self.original_file_name))
                imageObject.save(MFDATA_DIR + "files/truncated_files/%s"
                                 % truncated_file_name)
                imageObject.close()
                self.error("OSError truncated file %s"
                           "sent to truncated_files dir"
                           % truncated_file_name)
                return 1
            cropped.save(output, format="jpeg")
            cropped.close()

        # Xattr part
            output_attr = XattrFile(output)
            for key in input_file.tags:
                output_attr.tags[key] = input_file.tags[key]
            if all(key in input_file.tags for key in (b"crop_x", b"crop_y",
                                                      b"crop_width",
                                                      b"cropp_height")):
                del input_file.tags[b"crop_x"]
                del input_file.tags[b"crop_y"]
                del input_file.tags[b"crop_width"]
                del input_file.tags[b"crop_heigth"]
            output_attr.tags["actions"] = ",".join((output_attr.tags["actions"]
                                                    .decode('utf-8'))
                                                   .split(",")[1:])
            output_attr.commit()
            output_attr.move_or_copy(INCOMING_DIR + "/%s"
                                     % (output))
        else:
            print("No crop options")
        imageObject.close()


if __name__ == "__main__":
    x = Image_treatmentCropStep()
    x.run()
