# ASP binaries wrapper

from subprocess import run
from typing import List, Union, Optional
from pydantic import validate_call


def arg_to_str(arg) -> str:
    """
    [10, 10] > "10 10"
    [var1, var2] > "str(var1) str(var2)"
    var > str(var)
    None > ""
    """
    if not arg:
        if arg is list:
            # Concatenate multiples elements with space
            return " ".join([str(a) for a in arg])
        # Return element as string
        return str(arg)
    # return empty string
    return ""


@validate_call
def bundle_adjust(
    images: Union[List[str], str],
    cameras: Union[List[str], str],
    optional_ground_control_points: Optional[Union[List[str], str]],
    output_prefix: str,
    **opts,
):
    """ Bundle Adjustement
 
    Correct satellite position and orientation errors that introduce 
    systematic errors in the overall position and slope of the DEM.

    Arguments:
        images
        cameras
        optional_ground_control_points
        output_prefix
        opts

    ASP Docs:
        * [bundle_adjust](https://stereopipeline.readthedocs.io/en/latest/tools/bundle_adjust.html)
        * [Bundle Adjustement](https://stereopipeline.readthedocs.io/en/latest/bundle_adjustment.html)
    
    """
    images_str = arg_to_str(images)
    cameras_str = arg_to_str(cameras)
    gcp_str = arg_to_str(optional_ground_control_points)

    if output_prefix is not str:
        raise TypeError("Output prefix should be string")

    opts_str = " ".join([key + " " + arg_to_str(value) for key, value in opts])

    run(
        "bundle_adjust {} {} {} -o {} {}".format(
            images_str,
            cameras_str,
            gcp_str,
            output_prefix,
            opts_str,
        )
    )


@validate_call
def mapproject(
    dem: str, camera_image: str, camera_model: str, output_image: str, opts: dict
):
    """ Map Projection

    Orthorectify a camera image onto a DEM or datum.
    If used for stereo, all mapprojected images should have the same grid size and projection.

    Arguments:
        dem
        camera_image
        camera_model
        output_image
        opts

    ASP Docs
        [mapproject](https://stereopipeline.readthedocs.io/en/latest/tools/mapproject.html)

    """
    opts_str = " ".join([key + " " + arg_to_str(value) for key, value in opts])

    run(
        "mapproject {} {} {} {} {}".format(
            opts_str,
            dem,
            camera_image,
            camera_model,
            output_image,
        )
    )


@validate_call
def parallel_stereo(
    images: Union[List[str], str],
    cameras: Optional[Union[List[str], str]],
    output_file_prefix: str,
    **opts,
):
    """ Stereo Primary Tool

    Create a point cloud from overlapping pair of images.

    Arguments:
        images
        cameras
        output_file_prefix
        opts

    ASP Docs
        [parallel_stereo](https://stereopipeline.readthedocs.io/en/latest/tools/parallel_stereo.html)
    
    """
    images_str = arg_to_str(images)
    cameras_str = arg_to_str(cameras)
    opts_str = arg_to_str(opts)

    run(
        "parallel_stereo {} {} {} {}".format(
            opts_str,
            images_str,
            cameras_str,
            output_file_prefix,
        )
    )


@validate_call
def orbitviz(
    images: Union[List[str], str],
    cameras: Union[List[str], str],
    **opts,
):
    """ Orbit Visualization

    Produce a KML for visualizing camera positions.

    Arguments:
        images
        cameras
        opts

    ASP Docs:
        [orbitviz](https://stereopipeline.readthedocs.io/en/latest/tools/parallel_stereo.html)

    """
    images_str = arg_to_str(images)
    cameras_str = arg_to_str(cameras)
    opts_str = arg_to_str(opts)

    run("orbitviz {} {} {}".format(opts_str, images_str, cameras_str))


@validate_call
def point2dem(output: str, **opts):
    """ Point to DEM

    Produce a Digital elevation Model (GeoTiff) from a set of point clouds.

    Arguments:
        output

    ASP Docs:
        [point2dem](https://stereopipeline.readthedocs.io/en/latest/tools/point2dem.html)
    
    """
    # TODO check for input pcs indication in cmd
    opts_str = arg_to_str(opts)

    run(
        "point2dem {} {}".format(
            output,
            opts_str,
        )
    )


@validate_call
def pc_align(
    reference_cloud: str,
    source_cloud: str,
    output_prefix: str,
    max_displacement: float,
    **opts,
):
    """ Point Clouds Alignment

    Aligns two point clouds.

    Arguments:
        reference_cloud
        source_cloud
        output_prefix
        max_displacement
        opts
    
    ASP Docs:
        [pc_align](https://stereopipeline.readthedocs.io/en/latest/tools/pc_align.html)
        
    """
    max_disp_str = arg_to_str(max_displacement)
    opts_str = arg_to_str(opts)

    run(
        "pc_align --max-displacement {} {} {} {} -o {}".format(
            max_disp_str,
            opts_str,
            reference_cloud,
            source_cloud,
            output_prefix,
        )
    )


@validate_call
def pc_merge(
    pc_inputs: Union[List[str], str],
    pc_output: str,
    **opts,
):
    """ Point Clouds Merging

    Combine multiple ASP-generated point cloud files.

    Arguments: 
        pc_inputs
        pc_output
        opts

    ASP Docs:
        [pc_merge](https://stereopipeline.readthedocs.io/en/latest/tools/pc_merge.html)

    """
    pc_inputs_str = arg_to_str(pc_inputs)
    opts_str = arg_to_str(opts)

    run(
        "pc_merge {} {} -o {}".format(
            opts_str,
            pc_inputs_str,
            pc_output,
        )
    )


@validate_call
def image_align(
    ref_img: str,
    src_img: str,
    out_img: str,
    **opts,
):
    """ Image Alignment

    Align a seecond image to a first image.
    Use the georeferencement of the first image.

    Arguments:
        ref_img
        src_img
        out_img
        opts

    ASP Docs:
        [image_align](https://stereopipeline.readthedocs.io/en/latest/tools/image_align.html)

    """
    opts_str = arg_to_str(opts)

    run(
        "image_align {} {} {} -o {}".format(
            opts_str,
            ref_img,
            src_img,
            out_img,
        )
    )


@validate_call
def geodiff(
    dem1: str,
    dem2: str,
    output_file_prefix: Optional[str],
    **opts,
):
    """ Geotiff Difference

    Substract a second DEM to a first DEM (DEM1 - DEM2).
    The grid is taken from the first DEM.

    Arguments:
        dem1
        dem2
        output_file_prefix
        opts
    
    ASP Docs:
        [geodiff](https://stereopipeline.readthedocs.io/en/latest/tools/geodiff.html)

    """
    out_str = arg_to_str(output_file_prefix)
    if out_str:
        out_str = "-o " + out_str
    opts_str = arg_to_str(opts)

    run(
        "geodiff {} {} {} {}".format(
            opts_str,
            dem1,
            dem2,
            out_str,
        )
    )


@validate_call
def n_align(
    cloud_files: List[str],
    output_prefix: str,
    **opts,
):
    """ Multiple Point Clouds Alignment

    Align a set of two or more point clouds (extends pc_align).
    Produce a joint alignment instead of a pairwise alignment.

    Arguments:
        cloud_files
        output_prefix
        opts

    ASP Docs:
        [n_align](https://stereopipeline.readthedocs.io/en/latest/tools/n_align.html)

    """
    opts_str = arg_to_str(opts)
    cloud_str = arg_to_str(cloud_files)

    run(
        "n_align {} {} -o {}".format(
            opts_str,
            cloud_str,
            output_prefix,
        )
    )


@validate_call
def corr_eval(
    left_img: str,
    right_img: str,
    disparity_img: str,
    output_prefix: str,
    **opts,
):
    """ Correlation Evaluation

    Evaluate the normalized cross-correlation of the stereo results from the 
    input left and right aligned images and a disparity map.

    Arguments:
        left_img
        right_img
        disparity_img
        output_prefix
        opts

    ASP Docs:
        [corr_eval](https://stereopipeline.readthedocs.io/en/latest/tools/corr_eval.html)

    """
    opts_str = arg_to_str(opts)

    run(
        "corr_eval {} {} {} {} {}".format(
            opts_str,
            left_img,
            right_img,
            disparity_img,
            output_prefix,
        )
    )


@validate_call
def disparitydebug(
    disparity_map: str
):
    """ Disparity Debug

    Produce visualizable images from disparity maps.
    Extract the horizontal and vertical disparity into two normalized TIFF image files.

    Can also be extracted using gdal_translate by taking the right band as followed:

    ```bash
    for b in 1 2 3; do
        gdal_translate -b $b F.tif F_b${b}.tif
    done

    t=1e+6
    for b in 1 2; do
        image_calc -c "(var_0 + $t)*var_1 - $t" \
        --output-nodata-value -$t               \
        F_b${b}.tif F_b3.tif                    \
        -o F_b${b}_nodata.tif
    done
    ```

    Arguments:
        disparity_map

    ASP Docs:
        [disparitydebug](https://stereopipeline.readthedocs.io/en/latest/tools/disparitydebug.html)
        [Extract Disparity Bands](https://stereopipeline.readthedocs.io/en/latest/tools/image_calc.html#mask-disparity)
    """
    run(
        "disparitydebug {}".format(
            disparity_map
        )
    )
