import os
import argparse
from importlib import import_module
from astropy.io import fits
import pandas as pd


"""
Script that takes a list of .head Scamp outputs and adjusts the relevant .fits file WCS headers.
"""


def argument_parser():
    # PARSES COMMAND LINE ARGUMENTS TO SCRIPT
    result = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    # Where is the list of images to source extract?
    result.add_argument("-c", dest="header_list", type=str, default="scamp_to_img.txt")
    result.add_argument("-f", dest="adjust_func", type=str, default="adjust_wcs_hst.py")

    result.add_argument("-m", dest="multithread", type=bool, default=False)
    result.add_argument("-v", dest="verbose", type=bool, default=False)

    return result


def setup_environment(imgs):
    # LOADS VARIABLES, INITIALIZES INPUT VALUES
    directory = os.getcwd()
    # Load the image list
    img_list = pd.read_csv(f"{directory}/{imgs}")
    if len(img_list) == 0:
        raise ValueError("No files found in image list file.")
    return img_list


def load_parameters(headerfile):
    # READ THE WCS VALUES FROM THE HEADER
    for line in open(headerfile):
        if line.startswith("CRVAL1"):
            val1 = line.split()[2]
        elif line.startswith("CRVAL2"):
            val2 = line.split()[2]
    return val1, val2


if __name__ == "__main__":
    args = argument_parser().parse_args()
    adjustment_func = import_module(f"{args.adjust_func}.adjust_wcs")
    img_list = setup_environment(args.header_list)
    for i in range(len(img_list)):
        if args.verbose:
            print(
                f'---------------\nUpdating WCS for {img_list.iloc[i]["original_file"]}\n---------------'
            )
        pars = load_parameters(img_list.iloc[i]["scamp_header"])
        adjustment_func(img_list.iloc[i]["original_file"], pars)
