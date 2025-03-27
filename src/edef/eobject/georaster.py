from osgeo import gdal, osr
import numpy as np
from boundary import Bbox

# class GeoMask ?
# could handle transition between raster and vector masks
# doesnt need all the compute methods of GeoRaster

class GeoRaster:

    def __init__(self, dataset, **kwargs):
        if dataset:
            self.dataset = dataset
        else:
            self.dataset = None
        self.srs = osr.SpatialReference()
        self.geotransform = None
        self.projection = None
        self.metadata = None
        self.bbox = None
        self.dim = None
        self.path = ""

    @staticmethod
    def from_file(path):
        """open with gdal
        read metadata only ?
        open in readonly ?"""
        pass

    def array_full():
        "Load all the tiff"
        pass

    def array_view():
        """Load a portion of the tiff based on offset and size"""
        pass

    def save():
        pass

    def gradient():
        """First derivative"""
        pass

    def laplacien():
        """second derivative"""
        pass

    def divergence():
        pass

    def rotational():
        pass

    def hessian():
        pass

    def slope():
        """Get the slope at each pixel
        """
        pass

    def aspect():
        """Get the aspect at each pixel
        """
        pass

    def hillshade():
        """Create an hillshade view
        """
        pass

    def curvature():
        """
        """
        pass

    def edges():
        pass

    def watershed():
        pass

    def hydro_network():
        pass

    def search_artifacts():
        """Ouptut a mask
        """
        pass

    def ramp_to():
        pass

    def gaussian_filter():
        pass

    def set_resolution():
        pass

    def set_spatial_coverage():
        pass
    
    def get_spatial_coverage():
        pass


def r_align():
    """Padd the array for pixel correspondance"""
    pass


def r_mosaicking():
    """Merging"""
    pass
