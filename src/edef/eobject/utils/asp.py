# ASP binaries wrapper

from subprocess import run
from typing import List, Union, Optional
from pydantic import validate_call


def arg_to_str(arg) -> str:
    """
    output '10 10' instead of '[10, 10]' for [10, 10]
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
    images_str = arg_to_str(images)
    cameras_str = arg_to_str(cameras)
    opts_str = arg_to_str(opts)

    run("orbitviz {} {} {}".format(opts_str, images_str, cameras_str))


@validate_call
def point2dem(output: str, **opts):
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
