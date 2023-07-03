import os
import argparse
import pandas as pd
from astropy.io import fits
from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy.coordinates import FK5
from astropy import wcs

"""
Script that takes a list of .head Scamp outputs and adjusts the relevant catalogs.
"""


WCS_pars_str = ["CTYPE1", "CTYPE2"]
WCS_pars_float = [
    "CRVAL1",
    "CRVAL2",
    "CRPIX1",
    "CRPIX2",
    "CD1_1",
    "CD1_2",
    "CD2_1",
    "CD2_2",
]


def argument_parser():
    # PARSES COMMAND LINE ARGUMENTS TO SCRIPT
    result = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    # Where is the list of images to source extract?
    result.add_argument(
        "-c",
        dest="header_list",
        type=str,
        default="config_txt_files/scamp_to_catalog.txt",
    )

    result.add_argument("-m", dest="multithread", type=bool, default=False)
    result.add_argument("-v", dest="verbose", type=bool, default=False)

    return result


def load_parameters(headerfile):
    # READ THE WCS VALUES FROM THE HEADER
    par_dict = {}
    for line in open(headerfile):
        if line.split()[0] in WCS_pars_str:
            par_dict[line.split()[0]] = line.split()[2][1:-1]
        elif line.split()[0] in WCS_pars_float:
            par_dict[line.split()[0]] = float(line.split()[2])
    with fits.open("templates/template_img.fits") as hdul:
        header = hdul[0].header
    par_dict["NAXIS1"] = header["NAXIS1"]
    par_dict["NAXIS2"] = header["NAXIS2"]
    return par_dict


def update_catalog_wcs(data, headerfile):
    # Data should be an astropy Table
    # COMPUTE PIXEL AND WCS PARAMETERS
    wcs_obj = wcs.WCS(header=load_parameters(headerfile))
    coordlist = wcs.utils.pixel_to_skycoord(
        data["XWIN_IMAGE"], data["YWIN_IMAGE"], wcs_obj
    ).transform_to(FK5)
    data["ALPHA_J2000"] = coordlist.ra.value
    data["DELTA_J2000"] = coordlist.dec.value
    return data


if __name__ == "__main__":
    args = argument_parser().parse_args()
    directory = os.getcwd()
    cat_list = pd.read_csv(f"{directory}/{args.header_list}")
    for i in range(len(cat_list)):
        if args.verbose:
            print(
                f'---------------\nUpdating coordinates for {cat_list.iloc[i]["original_file"]}\n---------------'
            )
        with fits.open(cat_list.iloc[i]["original_file"], "update") as hdul:
            datatable = hdul[2].data
            hdul[2].data = update_catalog_wcs(
                datatable, cat_list.iloc[i]["scamp_header"]
            )
            hdul.flush()
