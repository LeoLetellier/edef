class SpatialImage:
    def __init__(self):
        self.folder_path = ""
        self.file_name = ""
        self.x_dim = None
        self.y_dim = None

    def from_file(self, path):
        pass

    def to_file(self, path):
        pass


class RawImage(SpatialImage):
    pass


class OrthoImage(SpatialImage):
    pass


class CoregImage(SpatialImage):
    pass


class CorrelationImage(SpatialImage):
    pass
