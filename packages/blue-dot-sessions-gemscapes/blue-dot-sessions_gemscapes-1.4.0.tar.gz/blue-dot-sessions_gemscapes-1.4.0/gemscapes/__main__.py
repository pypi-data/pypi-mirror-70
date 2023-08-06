# __main__.py
import math
import functools
import typing
import inspect
import time
import os
import argparse
import logging
import subprocess
import shlex
import shutil
import datetime

import tqdm
import toml
import matplotlib.pyplot as plt
import PIL
import svg_tools
import colour

from .conversion import convert_to_wav
from .audio_visualizer import AudioVisualizer, map_range_factory
from .color import DEFAULT_COLOR_SCHEME_KEY, COLOR_SCHEMES, interpolate_colors_fn_lookup
from .metadata import get_blue_dot_sessions_metadata, BDSMetaDataType

module_logger = logging.getLogger(__name__)


def wav2png(
    file_path,
    image_width: int = 500,
    image_height: int = 171,
    fft_size: int = 2048,
    peak_width: int = 1,
    color_scheme: str = None,
    color_scheme_file_path: str = None,
    color_space: str = "rgb",
    normalize: bool = False,
    track_metadata: BDSMetaDataType = None,
    dry_run: bool = False
) -> str:
    """
    Generate a .png image representation of a .wav file

    Args:
        file_path: Input .wav file path
        image_width: Output image width
        image_height: Output image height
        fft_size: Size of FFT to use in generating PNG output.
            If None or -1 is specified, FFT length will be calculated based on
            `image_width` and `peak_width`
        peak_width: Width of peaks in output PNG
        color_scheme: Name of color scheme
        color_scheme_file_path: Path to TOML file containing color scheme
        color_space: Interpolate in RGB, HSL or use "snap to" colors
        dry_run: Run without modifying anything

    Returns:
        output file path

    """
    visualizer = AudioVisualizer(
        file_path,
        image_width=image_width,
        image_height=image_height,
        fft_size=fft_size,
        peak_width=peak_width
    )

    transform_rnge_kwargs = dict(
        peaks_cut=0.0,
        mu_cut=2.5
    )

    interpolate_fn = interpolate_colors_fn_lookup[color_space]

    background_color, palette = visualizer.get_palette(
        color_scheme,
        color_scheme_file_path=color_scheme_file_path,
        interpolate_fn=interpolate_fn)
    background_color = tuple([255, 255, 255, 0])
    _, palette_small = visualizer.get_palette(
        color_scheme,
        num_colors=20,
        color_scheme_file_path=color_scheme_file_path,
        interpolate_fn=interpolate_fn)

    # visualizer.create_debug_plots(palette_small, **transform_rnge_kwargs)

    waveform_output_filename = visualizer.create_waveform_image(
        palette,
        background_color=background_color,
        **transform_rnge_kwargs,
        smooth=False,
        normalize=normalize,
        dry_run=dry_run
    )

    # waveform_output_alt_0_filename = visualizer.create_waveform_image_alt_0(
    #     palette
    # )

    # spectrogram_output_filename = visualizer.create_spectrogram_image(
    #     palette
    # )

    # return waveform_output_alt_0_filename
    return waveform_output_filename


def _get_formatted_output_dir(output_dir):
    output_dir_dir = os.path.dirname(output_dir)
    endpoint = os.path.basename(output_dir)
    if "%" in endpoint:
        module_logger.debug(f"_get_formatted_output_dir: detected datetime output dir")
        now = datetime.datetime.now()
        endpoint = now.strftime(endpoint)
        module_logger.debug(f"_get_formatted_output_dir: endpoint={endpoint}")
    output_dir = os.path.join(output_dir_dir, endpoint)
    return output_dir


def _get_most_recent_dir(output_dir):
    output_dir_dir = os.path.dirname(output_dir)
    module_logger.debug(f"_get_most_recent_dir: "
                        f"output_dir parent dir {output_dir_dir}")
    sub_dirs = []
    for path in os.listdir(output_dir_dir):
        path = os.path.join(output_dir_dir, path)
        if os.path.isdir(path):
            sub_dirs.append([os.path.getmtime(path), path])

    sorted_sub_dirs = sorted(sub_dirs, key=lambda val: val[0])
    most_recent = sorted_sub_dirs[-1][1]
    module_logger.debug((f"_get_most_recent_dir: most recently "
                         f"modified dir in parent dir {most_recent}"))

    return most_recent


def convert(
    file_path: str,
    output_dir: str = None,
    track_metadata: BDSMetaDataType = None,
    dry_run: bool = False
) -> str:
    """
    Convert mp3 files to wav.

    Args:
        file_path: Input .mp3 file path
        dry_run: Run without modifying anything

    Returns:
        output file path

    """
    output_file_path = None
    if output_dir is not None:
        # output_dir = _get_formatted_output_dir(output_dir)
        output_dir = _get_most_recent_dir(output_dir)
        file_name = os.path.basename(file_path)
        output_file_path = os.path.splitext(os.path.join(output_dir, file_name))[0] + ".wav"

    if not dry_run:
        if output_dir is not None:
            output_dir = _get_formatted_output_dir(output_dir)
            if not os.path.exists(output_dir):
                module_logger.debug(f"convert: {output_dir} didn't exist; creating")
                os.makedirs(output_dir)

        if file_path.endswith(".mp3"):
            output_file_path = convert_to_wav(file_path, output_file_path=output_file_path)

    return output_file_path


def primitive(
    file_path: str,
    primitive_args: str = "-n 30",
    primitive_exec: str = "primitive",
    track_metadata: BDSMetaDataType = None,
    dry_run: bool = False
) -> str:
    """
    Call `primitive` command on some input file. Return the path to the output SVG
    `primitive` command must be on the PATH for this to work correctly.

    Args:
        file_path: Input file path
        primitive_args: Additional arguments to pass to `primitive`. Must at minimum contain `-n <int>`
        primitive_exec: Path to primitive executable
        dry_run: Run without modifying anything

    Returns:
        output file path

    """
    if "-n" not in primitive_args:
        raise RuntimeError(
            "primitive: Need to specify number of shapes (\"-n\") when calling primitive executable")

    output_file_path = "{}.svg".format(os.path.splitext(file_path)[0])

    if not dry_run:
        cmd_str = "{} -i \"{}\" -o \"{}\" {}".format(
            primitive_exec, file_path, output_file_path, primitive_args)
        module_logger.debug("primitive: Running command {}".format(cmd_str))
        cmd = shlex.split(cmd_str)
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True)
        if proc.returncode == 0:
            return output_file_path
        else:
            module_logger.error("primitive: stdout={}".format(proc.stdout))
            module_logger.error("primitive: stderr={}".format(proc.stderr))
            raise RuntimeError(
                "primitive exited with code={}".format(proc.returncode))
    else:
        return output_file_path


def c2c(
    img: PIL.Image, input_c: typing.Tuple[int], output_c: typing.Tuple[int]
) -> PIL.Image:
    """
    Convert one color to another in a PIL Image object.

    Args:
        img: PIL image object
        input_c: Input color in either RGB or RGBA tuple
        output_c: output color in either RGB or RGBA tuple

    Returns:
        modified PIL image object
    """
    if len(input_c) == 4 or len(output_c) == 4:
        module_logger.debug("c2c: converting to RGBA")
        img.convert("RGBA")

    pixdata = img.load()

    width, height = img.size
    for y in range(height):
        for x in range(width):
            if all([pixdata[x, y][idx] == input_c[idx] for idx in range(len(input_c))]):
                pixdata[x, y] = output_c

    return img


def post_wav2png(
    file_path: str,
    vertical_scale_factor: float = 1.0,
    horizontal_scale_factor: float = 1.0,
    track_metadata: BDSMetaDataType = None,
    dry_run: bool = False
) -> str:
    """
    This function runs after wav2png, doing any modification necessary before
    sending to primitive.

    Right now this converts the white background to transparent, and adds
    vertical and horitonal white space

    Args:
        file_path: Input .png file path
        vertical_scale_factor: Scale the vertical axis by this much, adding
            white space. Must be greater than or equal to 1.0. If 1.0, no
            white space will be added.
        horizontal_scale_factor: Scale the horitonal axis by this much, adding
            white space. Must be greater than or equal to 1.0. If 1.0, no
            white space will be added.
        dry_run: Run without modifying anything

    Returns:
        output file path

    """
    output_file_path = "{}.post_wav2png.png".format(os.path.splitext(file_path)[0])
    white = (255, 255, 255)
    transparent = (255, 255, 255, 0)
    # transparent = (0, 0, 0, 0)
    if not dry_run:
        img = PIL.Image.open(file_path)
        img_info = img.info
        width, height = img.size
        img.thumbnail((width, height))
        new_width = int(horizontal_scale_factor * width)
        new_height = int(vertical_scale_factor * height)
        module_logger.debug(f"post_wav2png: old size=({width}, {height})")
        module_logger.debug(f"post_wav2png: new size=({new_width}, {new_height})")
        idx = (new_width - width) / 2
        idy = (new_height - height) / 2
        module_logger.debug(f"post_wav2png: pos=({idx}, {idy})")

        new_img = PIL.Image.new("RGBA", (new_width, new_height), color=white)
        new_img.paste(img, (int(idx), int(idy)))
        new_img = c2c(new_img, white, transparent)
        new_img.save(output_file_path, **img_info)

    return output_file_path


def _hex_dist(hex0: str, hex1: str) -> float:
    """
    Get the normalized distance between two RGB hex color values

    Args:

    """
    def cut_alpha(hex_val):
        if len(hex_val) > 7:
            return hex_val[:7]
        return hex_val

    c0 = colour.Color(cut_alpha(hex0))
    c1 = colour.Color(cut_alpha(hex1))

    unnorm = math.sqrt(
        sum([(val0 - val1)**2 for val0, val1 in zip(c0.rgb, c1.rgb)]))
    norm_factor = math.sqrt(3)

    return unnorm/norm_factor


def _adjust_svg_scale(
    file_path: str,
    horizontal_scale_factor: float,
    vertical_scale_factor: float
) -> str:
    module_logger.debug("_adjust_svg_scale")

    with svg_tools.get_root(file_path) as root:
        width = root.attrib["width"]
        height = root.attrib["height"]
        g = root.find("g")
        transform = g.attrib["transform"]

        module_logger.debug(f"_adjust_svg_scale: svg dim ({width}, {height})")
        module_logger.debug(f"_adjust_svg_scale: g transform {transform}")

        def in_between(target, begin, end):
            idx_start = target.find(begin)
            idx_end = target[idx_start+len(begin):].find(end)
            val = target[idx_start+len(begin):][:idx_end]
            return val

        scale_val = 1.0
        trans_x = 0.0
        trans_y = 0.0

        if "scale" in transform:
            scale_val = float(in_between(transform, "scale(", ")"))

        module_logger.debug(f"_adjust_svg_scale: scale_val={scale_val}")

        if "translate" in transform:
            translate_str = in_between(transform, "translate(", ")")
            trans_x, trans_y = [float(val) for val in translate_str.split(" ")]
        module_logger.debug(f"_adjust_svg_scale: (trans_x, trans_y)=({trans_x}, {trans_y})")




def post_primitive(
    file_path: str,
    thresh: float = 0.05,
    track_metadata: BDSMetaDataType = None,
    horizontal_scale_factor: float = 1.0,
    vertical_scale_factor: float = 1.0,
    dry_run: bool = False
) -> str:
    """
    This function is run after primitive, to do any post-primitive SVG modification

    Right now this gets rid of any dark shapes and applies an `svg_tools` utility
    to modify the primtive SVG output.

    Args:
        file_path: Input .svg file path
        modify_svg_fn: SVG
        dry_run: Run without modifying anything

    Returns:
        output .svg file path
    """
    output_file_path = "{}.post_primitive.svg".format(os.path.splitext(file_path)[0])

    if not dry_run:
        target = "fill=\""
        black = "#000000"
        shutil.copyfile(file_path, output_file_path)

        _adjust_svg_scale(
            output_file_path,
            horizontal_scale_factor=horizontal_scale_factor,
            vertical_scale_factor=vertical_scale_factor)

        for polygon in svg_tools.polygon_iter(output_file_path):
            hexval = polygon.attrib["fill"]
            if hexval == "none":
                continue
            delta = _hex_dist(hexval, black)
            if delta <= thresh:
                polygon.attrib["fill"] = "none"

        if track_metadata is not None:
            polygon_modify_fns = []
            if "Tension" in track_metadata:
                map_range = map_range_factory([0, 9], [0, 10])
                mapped = map_range(track_metadata["Tension"])
                module_logger.debug(f"post_primitive: Tension value {track_metadata['Tension']}, mapped value {mapped}")
                polygon_modify_fns.append(
                    lambda paths: svg_tools.rotate_if_polygon(
                        paths,
                        min_rotation=mapped,
                        max_rotation=mapped+0.1,
                        rotate_if_fn=lambda angle: angle < 15.))

            if "Mood" in track_metadata:
                map_range = map_range_factory([0, 9], [1, 4.5])
                mapped = map_range(track_metadata["Mood"])
                module_logger.debug(f"post_primitive: Mood value {track_metadata['Mood']}, mapped value {mapped}")
                polygon_modify_fns.append(
                    lambda paths: svg_tools.rounded_corner_polygon(paths, mapped))

            svg_tools.modify_svg(
                output_file_path,
                *polygon_modify_fns
            )

    return output_file_path

PipelineFnType = typing.Callable[[str, typing.Optional[bool]], str]

def pipeline(
    convert_fn: PipelineFnType,
    wav2png_fn: PipelineFnType,
    post_wav2png_fn: PipelineFnType,
    primitive_fn: PipelineFnType,
    post_primitive_fn: PipelineFnType
) -> PipelineFnType:
    """
    Run gemscape pipeline consisting of the following stages:

    conversion: Convert .mp3 input to .wav
    wav2png: Create a visual representation of .wav file
    post wav2png: Modify wav2png output before passing to primitive
    primtive: Call `primitive`, creating SVG from PNG
    post primitive: Modify primitive output

    Returns:
        function that takes as input .mp3 file.
    """

    def _time(fn, *args, **kwargs):
        t0 = time.time()
        res = fn(*args, **kwargs)
        delta = time.time() - t0
        return res, delta

    fns = [
        convert_fn,
        wav2png_fn,
        post_wav2png_fn,
        primitive_fn,
        post_primitive_fn
    ]

    fn_names = [
        "convert_fn",
        "wav2png_fn",
        "post_wav2png_fn",
        "primitive_fn",
        "post_primitive_fn"
    ]


    def _pipeline(file_path: str, stages: slice = None) -> str:

        track_metadata = get_blue_dot_sessions_metadata(file_path)
        module_logger.debug(f"pipeline._pipeline: track_metadata={track_metadata}")

        if stages is None:
            stages = slice(None)
        stages = range(len(fns))[stages]

        module_logger.debug(f"pipeline._pipeline: stages={stages}")

        for idx, fn in enumerate(fns):
            # module_logger.debug(f"pipeline._pipeline: idx={idx}, stages[-1]={stages[-1]}")
            if idx == stages[-1] + 1:
                break
            if idx < stages[0]:
                module_logger.debug(f"pipeline: stage {idx}, calling {fn_names[idx]}({file_path}, dry_run=True) ")
                file_path, delta = _time(fn, file_path, dry_run=True, track_metadata=track_metadata)
            else:
                module_logger.debug(f"pipeline: stage {idx}, calling {fn_names[idx]}({file_path})")
                file_path, delta = _time(fn, file_path, track_metadata=track_metadata)
            module_logger.debug(f"pipeline: stage {idx}, {fn_names[idx]} took {delta:.2f} sec")
            yield file_path

    return _pipeline


pipeline_sig = inspect.signature(pipeline)
pipeline_stage_count = len(pipeline_sig.parameters)
pipeline_stage_names = [param for param in pipeline_sig.parameters]


def create_parser():
    interpolate_colors_fn_names = ", ".join([f"'{name}'" for name in interpolate_colors_fn_lookup])
    color_scheme_names = ["'{}'".format(key) for key in COLOR_SCHEMES.keys()]
    color_scheme_str = ", ".join(color_scheme_names)

    pipeline_stage_names_str = ", ".join(pipeline_stage_names)

    parser = argparse.ArgumentParser(description="Create gemscapes from audio files")
    parser.add_argument("file_paths", metavar="file-paths", type=str, nargs="+",
                        help="Files from which to create gemscapes")
    parser.add_argument("-d", "--outdir", action="store", dest="output_dir",
                        help="Put output files in this directory")
    parser.add_argument("-c", "--config", action="store",
                        help="Configuration file to use to modify output gemscapes")
    parser.add_argument("--wav2png.width", dest="image_width", type=int, default=500,
                        help="image width in pixels (default %(default)s)")
    parser.add_argument("--wav2png.height",  dest="image_height", type=int, default=171,
                        help="image height in pixels (default %(default)s)")
    parser.add_argument("--wav2png.fft", dest="fft_size", type=int, default=2048,
                        help="fft size, power of 2 for increased performance (default %(default)s)")
    parser.add_argument("--wav2png.peak-width", dest="peak_width", type=int, default=1,
                        help="Peak width in resulting images (default %(default)s)")
    parser.add_argument("--wav2png.color-scheme-file", action="store",
                        dest="color_scheme_file_path", type=str,
                        help="path to file containing color scheme configurations")
    parser.add_argument("--wav2png.color-scheme", action="store", dest="color_scheme", type=str,
                        default=DEFAULT_COLOR_SCHEME_KEY,
                        help="name of the color scheme to use (one of: {}) (default '%(default)s')".format(color_scheme_str))
    parser.add_argument("--wav2png.color-space", dest="color_space", type=str,
                        default="rgb", help=("Color space in which to do interpolation. "
                                             f"Available values are {interpolate_colors_fn_names}. "
                                             "Defaults to %(default)s."))
    parser.add_argument("--post-wav2png.v-scale",  dest="vertical_scale_factor", type=float, default=1.0,
                        help="Vertical white space scaling factor (default %(default)s)")
    parser.add_argument("--post-wav2png.h-scale",  dest="horizontal_scale_factor", type=float, default=1.0,
                        help="Horizontal white space scaling factor (default %(default)s)")
    parser.add_argument("--primitive.primitive-exec", action="store", dest="primitive_exec", type=str,
                        default="primitive", help="Specify path to primitive executable (default %(default)s).")
    parser.add_argument("--primitive.primitive-args", action="store", dest="primitive_args", type=str,
                        default="-n 30", help="Specify arguments to pass to primitive executable. Must include '-n <int>' argument")
    parser.add_argument("--post_primitive.black-thresh", action="store", dest="thresh", type=float, default=0.15,
                        help="Specify a RGB distance threshold below which to set a shape's color to transparent")

    parser.add_argument("--pipeline-range", action="store", dest="pipeline_stage", type=str,
                        default="0:", help=("Specify which range of pipeline stages to compute. "
                                            "Uses Python range/slice syntax, eg if 1:3 is specified, then the second and third stage are done. "
                                            "If a single number is specified, the pipeline will do up to specified number, ie :{number}. "
                                             f"Total number of stages is {pipeline_stage_count}. "
                                             f"Pipeline stages are {pipeline_stage_names_str}. "
                                             "(default %(default)s)"))
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose output")

    return parser



def load_config(file_path: str) -> dict:
    with open(file_path, "r") as fd:
        config = toml.load(fd)
    return config


def process_pipeline_stages(stages_str: str) -> slice:
    module_logger.debug(f"process_pipeline_stages: stages_str={stages_str}")
    if ":" in stages_str:
        stages = []
        split = stages_str.split(":")
        for val in split:
            try:
                val = int(val)
            except ValueError:
                val = None
            stages.append(val)
        stages = slice(*stages)
    else:
        stages = slice(int(stages_str))
    module_logger.debug(f"process_pipeline_stages: stages={stages}")
    return stages


def main():

    convert_keys = [
    ]

    wav2png_keys = [
        "fft_size",
        "image_width",
        "image_height",
        "peak_width",
        "color_scheme",
        "color_scheme_file_path",
        "color_space"
    ]

    post_wav2png_keys = [
        "vertical_scale_factor",
        "horizontal_scale_factor"
    ]


    primitive_keys = [
        "primitive_args",
        "primitive_exec"
    ]

    post_primitive_keys = [
        "thresh"
    ]


    parser = create_parser()
    parsed = parser.parse_args()

    pipeline_stage = parsed.pipeline_stage

    wav2png_config = vars(parsed)
    post_wav2png_config = vars(parsed)
    primitive_config = vars(parsed)
    convert_config = vars(parsed)
    post_primitive_config = vars(parsed)

    output_dir = parsed.output_dir

    if parsed.config:
        config = load_config(parsed.config)
        wav2png_config = config.get("wav2png", {})
        post_wav2png_config = config.get("post_wav2png", {})
        primitive_config = config.get("primitive", {})
        post_primitive_config = config.get("post_primitive", {})
        convert_config = config.get("convert", {})
        if "output_dir" in config:
            output_dir = config["output_dir"]

    wav2png_config = {key: wav2png_config[key] for
                      key in wav2png_config if key in wav2png_keys}

    post_wav2png_config = {key: post_wav2png_config[key] for
                      key in post_wav2png_config if key in post_wav2png_keys}

    primitive_config = {key: primitive_config[key] for
                        key in primitive_config if key in primitive_keys}

    post_primitive_config = {key: post_primitive_config[key] for
                        key in post_primitive_config if key in post_primitive_keys}


    convert_config = {key: convert_config[key] for
                      key in convert_config if key in convert_keys}

    log_level = logging.ERROR
    if parsed.verbose:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level)
    logging.getLogger("matplotlib").setLevel(logging.ERROR)
    logging.getLogger("eyed3").setLevel(logging.ERROR)
    logging.getLogger("PIL").setLevel(logging.ERROR)

    pipeline_stages = process_pipeline_stages(parsed.pipeline_stage)

    gemscape_gen = pipeline(
        lambda file_path, **kwargs: convert(
            file_path, output_dir=output_dir, **convert_config, **kwargs),
        lambda file_path, **kwargs: wav2png(
            file_path, normalize=True, **wav2png_config, **kwargs
        ),
        functools.partial(post_wav2png, **post_wav2png_config),
        lambda file_path, **kwargs: primitive(
            file_path, **primitive_config, **kwargs
        ),
        functools.partial(post_primitive, **post_primitive_config)
    )

    def progress(iterable):
        if len(iterable) > 1 and not parsed.verbose:
            return tqdm.tqdm(iterable)
        else:
            return iterable


    for file_path in progress(parsed.file_paths):
        for i, res in enumerate(gemscape_gen(file_path, stages=pipeline_stages)):
            pass
            # if i == pipeline_stage:
            #     break
    # plt.show()
main()
