import numpy as np
from osgeo.osr import SpatialReference
from typing import Optional, Union


class Bbox:
    """Bounding Box - Manipulate boundary box from different sources

    Attributes:
        xmin: minimum x value of the bbox
        xmax: maximum x value of the bbox
        ymin: minimum y value of the bbox
        ymax: maximum y value of the bbox
        srs: spatial reference system
    """

    def __init__(
        self,
        xmin: Union[float, int],
        xmax: Union[float, int],
        ymin: Union[float, int],
        ymax: Union[float, int],
        srs: Optional[SpatialReference],
    ):
        if xmin > xmax:
            raise ValueError(
                f"The x minimum value is higher than the maximum value {xmin}>{xmax}"
            )
        if ymin > ymax:
            raise ValueError(
                f"The y minimum value is higher than the maximum value {ymin}>{ymax}"
            )

        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.srs = srs

    def __eq__(self, value):
        return (
            self.xmin == value.xmin
            and self.xmax == value.xmax
            and self.ymin == value.ymin
            and self.ymax == value.ymax
            and self.srs == value.srs
        )

    @staticmethod
    def new(xmin, xmax, ymin, ymax):
        return Bbox(xmin, xmax, ymin, ymax)

    @staticmethod
    def from_ul_lr(ulx, uly, lrx, lry):
        """
        upper left x | y
        lower right x | y
        """
        return Bbox(ulx, lrx, lry, uly)

    def to_ul_lr(self):
        return self.xmin, self.ymax, self.xmax, self.ymin

    def to_xia_yia(self):
        return self.xmin, self.xmax, self.ymin, self.ymax

    def x_amp(self):
        return self.xmax - self.xmin

    def y_amp(self):
        return self.ymax - self.ymin

    def pad_value(self, value):
        if value is float or value is int:
            value = [value, value]
        x_pad = value[0]
        y_pad = value[1]
        return Bbox(
            self.xmin - x_pad, self.xmax + x_pad, self.ymin - y_pad, self.y_max + y_pad
        )

    def pad_ratio(self, value):
        if value is float or value is int:
            value = [value, value]
        x_pad = value[0] * self.x_amp()
        y_pad = value[1] * self.y_amp()
        return self.pad_value([x_pad, y_pad])

    def pad_percent(self, value):
        if value is float or value is int:
            value = [value, value]
        x_pad = value[0] / 100
        y_pad = value[1] / 100
        return self.pad_ratio([x_pad, y_pad])

    @staticmethod
    def from_min_bbox(bboxs: list):
        bboxs = np.asarray([list(b.to_xia_lia()) for b in bboxs])
        try:
            bbox = Bbox(
                np.max(bboxs[:, 0]),
                np.min(bboxs[:, 1]),
                np.max(bboxs[:, 2]),
                np.min(bboxs[:, 3]),
            )
        except ValueError:
            return None  # No overlapping between all bboxs
        return bbox

    @staticmethod
    def from_max_bbox(bboxs: list):
        bboxs = np.asarray([list(b.to_xia_lia()) for b in bboxs])
        return Bbox(
            np.min(bboxs[:, 0]),
            np.max(bboxs[:, 1]),
            np.min(bboxs[:, 2]),
            np.max(bboxs[:, 3]),
        )

    @staticmethod
    def from_points(points: list):
        min = np.min(points, axis=0)
        max = np.max(points, axis=0)
        return Bbox(min[0], max[0], min[1], max[1])


class Sbox:
    """Shaping Box -"""

    def __init__(self):
        pass


if __name__ == "__main__":
    print("Boundary")
