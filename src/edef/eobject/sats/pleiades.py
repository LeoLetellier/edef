import xml.etree.ElementTree as ET
from os import listdir
from os.path import join, dirname, basename, splitext, isdir
from fnmatch import fnmatch
import xmltodict
from datetime import datetime

from edef.eobject.boundary import Bbox


class PleiadesDim:
    def __init__(self, dim_path):
        self.path = dim_path
        dim_dict = xmltodict.parse(self.path)
        self.dimap = Dimap(dim_dict)

        self.img_paths = ""
        self.bbox = []
        self.top_angles = None
        self.center_angles = None
        self.bottom_angles = None


class Dimap:
    supported_version = "2.15"

    def __init__(self, dim_dict: dict):
        dim = dim_dict["Dimap_Document"]
        self.metadata_identification = dim["Metadata_Identification"]
        self.dataset_identification = dim["Dataset_Identification"]
        self.dataset_content = dim["Dataset_Content"]
        self.product_information = dim["Product_Information"]
        self.coordinate_reference_system = dim["Coordinate_Reference_System"]
        self.geoposition = dim["Geoposition"]
        self.processing_information = dim["Processing_Information"]
        self.raster_data = dim["Raster_Data"]
        self.radiometric_data = dim["Radiometric_Data"]
        self.geometric_data = dim["Geometric_Data"]
        self.quality_assessment = dim["Quality_Assessment"]
        self.dataset_sources = dim["Dataset_sources"]

        self.__check_version()

    def __check_version(self):
        if self.metadata_identification["METADAT_FORMAT"]["@version"] != "2.15":
            raise Exception(
                "Dimap format not supported. Unexpected behaviour can occur."
            )


class PleiadesGeometry:
    def __init__(self, geom_dict: dict):
        self.time = geom_dict["TIME"]
        self.geometric_gliding = geom_dict["GEOMETRIC_GLIDING"]
        angles = geom_dict["Acquisition_Angles"]
        self.azimuth = angles["AZIMUTH_ANGLE"]
        self.viewing_angle_across_track = angles["VIEWING_ANGLE_ACROSS_TRACK"]
        self.viewing_angle_along_track = angles["VIEWING_ANGLE_ALONG_TRACK"]
        self.viewing_angle = angles["VIEWING_ANGLE"]
        self.incidence_angle_across_track = angles["INCIDENCE_ANGLE_ACROSS_TRACK"]
        self.incidence_angle_along_track = angles["INCIDENCE_ANGLE_ALONG_TRACK"]
        self.incidence_angle = angles["INCIDENCE_ANGLE"]
        self.sun_azimuth = geom_dict["Solar_Incidences"]["SUN_AZIMUTH"]
        self.sun_elevation = geom_dict["Solar_Incidences"]["SUN_ELEVATION"]
        self.gsd_across_track = geom_dict["Ground_Sample_Distance"]["GSD_ACROSS_TRACK"]
        self.gsd_along_track = geom_dict["Ground_Sample_Distance"]["GSD_ALONG_TRACK"]

    def azimuth(self):
        return self.azimuth

    def roll(self):
        return self.viewing_angle_across_track

    def pitch(self):
        return self.viewing_angle_along_track

    def combined(self):
        return self.viewing_angle

    def time(self):
        return datetime.strptime(self.time, "%Y-%m-%dT%H:%M:%S.%fZ")


class Pleiades:
    """Handling for Pleiades image archive"""

    __acquisition_type = ["mono", "bistereo", "tristereo"]
    __acquisition_mode = ["P", "MS"]

    def __init__(self, paths):
        """Initiate a new archive handler

        The archive folder must be: `IMG_PHR1[A/B]_[MS/P]_NNN` (it can be renamed but the content should be preserved)

        Arguments:
            paths: path to the archive, or to all archives for stereo acquisitions
        """
        self.folder_paths, self.acquisiton_type = Pleiades.__check_paths(paths)

        self.dim_files = self.__fetch_dims()

        # parse DEM

    @staticmethod
    def __check_paths(paths):
        if paths is str:
            paths = [paths]

        if paths is list and paths:
            if all([isdir(p) for p in paths]):
                return paths, Pleiades.__acquisition_type[len(paths) - 1]
            else:
                raise NotADirectoryError
        else:
            raise ValueError("paths input is not valid")

    def _img_nb(self):
        for i in range(3):
            if self.acquisiton_type == Pleiades.__acquisition_type[i]:
                return i

    def __fetch_dims(self):
        all_dims = []
        for p in self.folder_paths:
            dim = []
            for f in listdir(p):
                if fnmatch(f, "DIM_PHR*.XML"):
                    dim.append(f)
            if len(dim) != 1:
                raise ValueError(
                    "The Pleiades folder is not valid, need to find a single DIM file."
                )
            all_dims.append(basename(dim[0]))
        return all_dims


def ortho_from_pleiades(raw: Pleiades):
    pass


if __name__ == "__main__":
    pass
