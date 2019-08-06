#!/usr/bin/env python3

from acquisition import AcquisitionStep
import psycopg2


class Image_treatmentDatabaseStep(
        AcquisitionStep):

    plugin_name = "image_treatment"
    step_name = "database"

    def process(self, xaf):
        self.info("process for file %s" % xaf.filepath)
        self.write_db(xaf)
        return True

    def write_db(self, at):
        conn =\
            psycopg2.connect("dbname=plugin_map_snow "
                             "user=plugin_map_snow "
                             "host=localhost "
                             "port=7432 "
                             "password=plugin_map_snow")
        cur = conn.cursor()

        name_camera = at.tags["name"]
        date = at.tags["date"]
        location = at.tags["location"]
        weather = at.tags["weather"]
        image_path = at.tags[("files/final/%s"
                              % at["first.core.original_basename"].
                              convert("utf-8"))]

        cur.execut("INSERT INTO image"
                   "(name_camera, date, location, weather, file_path)"
                   "VALUES (%s, %s, %s, %s, %s);" %
                   (name_camera, date, location, weather, image_path))

        cur.close()
        conn.close()


if __name__ == "__main__":
    x = Image_treatmentDatabaseStep()
    x.run()
