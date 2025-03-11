import gdal
import os
from os.path import join, dirname, basename, splitext
from edef.eobject.sats.satellites import SATELLITES

DEM_SOURCE = SATELLITES.keys + ["MIX", "EXT"]

DEM_FORMAT = {"GeoTiff": [".tif", ".tiff"]}


class Dem:
    def __init__(self):
        self.folder_path = ""
        self.file_name = ""
        self.format = ""

    def from_source(self, path):
        self.folder_path = dirname(path)
        self.file_name, ext = splitext(basename(path))

        for format in DEM_FORMAT:
            for e in format:
                if e == ext:
                    self.format = format
                    break
        if len(format) == 0:
            raise TypeError(f"File format with extension {ext} is not supported!")


if __name__ == "__main__":
    pass
