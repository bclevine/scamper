import os
import argparse
import subprocess
import pandas as pd


"""
Script that takes a list of fits images and uses SExtractor to create LDAC detection catalogs.
"""


def argument_parser():
    # PARSES COMMAND LINE ARGUMENTS TO SCRIPT
    result = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    # Where is the list of images to source extract?
    result.add_argument("-c", dest="img_list", type=str, default="img_list.txt")
    # Where should we place the extracted catalogs?
    result.add_argument("-d", dest="output_dir", type=str, default="catalogs.nosync")

    result.add_argument("-m", dest="multithread", type=bool, default=False)
    result.add_argument("-v", dest="verbose", type=bool, default=False)

    return result


def setup_environment(imgs, output_dir):
    # LOADS VARIABLES, INITIALIZES INPUT VALUES
    directory = os.getcwd()
    # Load the image list
    img_list = pd.read_csv(f"{directory}/{imgs}")
    if len(img_list) == 0:
        raise ValueError("No fits files found in image list file.")
    # Set the output directory
    outputs = directory if args.output_dir is None else f"{directory}/{output_dir}"
    return directory, img_list, outputs


def source_extract(directory, filename, weight_map, output_name, outputs):
    # CALLS SOURCE EXTRACTOR FROM THE COMMAND LINE
    subprocess.run(
        [
            "sex",
            f"{directory}/{filename}",
            "-c",
            "default.se",
            "-CATALOG_NAME",
            f"{outputs}/{output_name}.cat",
            "-CATALOG_TYPE",
            "FITS_LDAC",
            "-WEIGHT_TYPE",
            "MAP_WEIGHT",
            "-WEIGHT_IMAGE",
            f"{directory}/{weight_map}",
        ]
    )


if __name__ == "__main__":
    args = argument_parser().parse_args()
    directory, img_list, outputs = setup_environment(args.img_list, args.output_dir)
    for i in range(len(img_list)):
        if args.verbose:
            print(
                f'---------------\nSource extracting {img_list.iloc[i]["image"]}\n---------------'
            )
        source_extract(
            directory,
            img_list.iloc[i]["image"],
            img_list.iloc[i]["weight"],
            img_list.iloc[i]["output_name"],
            outputs,
        )
