from osgeo import gdal
import os


def open_tif(full_path):
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"File {full_path} not found")
    ds = gdal.OpenEx(full_path, allowed_drivers=["GTiff"])
    ds_band = ds.GetRasterBand(1)
    values = ds_band.ReadAsArray(0, 0, ds.RasterXSize, ds.RasterYSize)
    ncols, nlines = ds.RasterYSize, ds.RasterXSize
    proj = ds.GetProjection()
    geotransform = ds.GetGeoTransform()
    return (values, nlines, ncols, proj, geotransform)


def save_tif(full_path, data, ncol, nrow, proj, geotransform):
    drv = gdal.GetDriverByName("GTiff")
    dst_ds = drv.Create(full_path, ncol, nrow, 1, gdal.GDT_Float32)
    dst_band = dst_ds.GetRasterBand(1)
    dst_ds.SetGeoTransform(geotransform)
    dst_ds.SetProjection(proj)
    dst_band.WriteArray(data)
    dst_ds.FlushCache()


if __name__ == "__main__":
    pass
