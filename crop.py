#!/usr/bin/env python3

from acquisition import AcquisitionStep
from PIL import Image
from xattrfile import XattrFile
import os

class CropperMainStep(
        AcquisitionStep):

    plugin_name = "cropper"
    step_name = "crop"

    def process(self, xaf):
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
        if x + y + w + h:
            imageObject = Image.open(input_file.filepath)
            output = "cropped_%s" % (input_file.
                                     tags["first.core.original_basename"]
                                     .decode('utf-8'))
            cropped = imageObject.crop((x, y, w, h))
            cropped.save(output, format="jpeg")

        # Xattr part
            output_attr = XattrFile(output)
            for key in input_file.tags:
                output_attr.tags[key] = input_file.tags[key]
        # r=root, d=directories, f = files
            for r, d, f in os.walk("/home/mfdata/var/in/tmp/cropper.crop/",
                                   topdown=False):
                for files in f:
                    print(os.path.join(r, files))
            if all(key in input_file.tags for key in (b"crop_x", b"crop_y",
                                                      b"crop_width",
                                                      b"cropp_height")):
                del input_file.tags[b"crop_x"]
                del input_file.tags[b"crop_y"]
                del input_file.tags[b"crop_width"]
                del input_file.tags[b"crop_heigth"]
            output_attr.tags[b"actions"] = output_attr.tags["actions"][5:]
            output_attr.commit()
            output_attr.move_or_copy("/home/mfdata/var/in/incoming/%s"
                                     % (output))
            print("%s added to incoming successfully"
                  % (output))
        else:
            print("No crop options")


if __name__ == "__main__":
    x = CropperMainStep()
    x.run()
