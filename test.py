#!/usr/bin/env python3

from acquisition import AcquisitionStep


class CropperMainStep(
        AcquisitionStep):

    plugin_name = "placer"
    step_name = "place"

    def process(self, xaf):
        self.info("process for file %s" % xaf.filepath)
        self.hello_world(xaf)
        return True

    def hello_world(self, at):
        at.tags["actions"] = \
            ",".join((at.tags["actions"].decode('utf-8')).split(",")[1:])
        print(at.tags["actions"])
        at.move_or_copy("/home/mfdata/var/in/incoming/placed_%s"
                        % (at.tags["first.core.original_basename"]))


if __name__ == "__main__":
    x = CropperMainStep()
    x.run()
