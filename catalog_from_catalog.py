import os
import argparse
import pandas as pd
from astropy.io import fits
from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy.coordinates import FK5
from astropy import wcs

"""
Script that takes an object detection catalog and converts it to an LDAC catalog.
"""


def prepare_input_catalog(data):
    # Data should be an astropy Table
    # COMPUTE PIXEL AND WCS PARAMETERS
    coordlist = SkyCoord(data["RA"], data["DEC"], unit="deg", frame=FK5)
    # UPDATE THIS LATER
    # It literally does not matter what the template img is,
    # as long as it has a working WCS and you are consistent
    # when u use it later to convert back from the calibrated scamp output
    with fits.open("templates/template_img.fits") as hdul:
        header = hdul[0].header
    wcs_obj = wcs.WCS(header=header)
    out = wcs.utils.skycoord_to_pixel(coordlist, wcs_obj)

    # ADD NECESSARY COLUMNS
    data["ALPHA_J2000"] = coordlist.ra.value
    data["DELTA_J2000"] = coordlist.dec.value
    data["XWIN_IMAGE"] = out[0]
    data["YWIN_IMAGE"] = out[1]
    # Choosing some arbitrary parameters here...
    data["FLUX_AUTO"] = 10 ** ((data["MAG"] - 22.5) / (-2.5))
    data["FLUXERR_AUTO"] = data["FLUX_AUTO"] * 0.05

    return data


def update_template_values(template, data):
    # UPDATE VALUES IN THE TABLE
    template["Y_IMAGE"] = list(data["YWIN_IMAGE"])
    template["X_IMAGE"] = list(data["XWIN_IMAGE"])
    template["X_WORLD"] = list(data["XWIN_IMAGE"])
    template["Y_WORLD"] = list(data["YWIN_IMAGE"])
    template["XWIN_IMAGE"] = list(data["XWIN_IMAGE"])
    template["YWIN_IMAGE"] = list(data["YWIN_IMAGE"])
    template["ALPHA_J2000"] = list(data["ALPHA_J2000"])
    template["DELTA_J2000"] = list(data["DELTA_J2000"])
    # Choosing some arbitrary parameters here...
    template["ERRAWIN_IMAGE"] = 0.01
    template["ERRBWIN_IMAGE"] = 0.01
    template["ERRA_WORLD"] = 0.01
    template["ERRB_WORLD"] = 0.01
    template["ERRTHETAWIN_IMAGE"] = 25
    template["FLUX_AUTO"] = list(data["FLUX_AUTO"])
    template["FLUXERR_AUTO"] = list(data["FLUXERR_AUTO"])
    template["FLAGS"] = 0
    template["FLAGS_WEIGHT"] = 0

    return template


def copy_to_template(data, output_name):
    with fits.open("templates/template_catalog.fits.cat") as n:
        temp = n[2]

        if len(data) <= len(temp.data):
            template = temp.data[: len(data)]
        else:
            print("Input dataframe too long; functionality not implemented yet")

        # NOW SAVE THE FILE
        temp.data = update_template_values(template, data)
        output_fits = fits.HDUList([n[0], n[1], temp])
        output_fits.writeto(f"{output_name}", overwrite=True)


def argument_parser():
    # PARSES COMMAND LINE ARGUMENTS TO SCRIPT
    result = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    # Where is the list of catalogs to convert to LDAC?
    result.add_argument(
        "-c",
        dest="cat_list",
        type=str,
        default="config_txt_files/catalog_from_catalog.txt",
    )
    # Where should we place the extracted catalogs?
    result.add_argument("-d", dest="output_dir", type=str, default=None)

    result.add_argument("-m", dest="multithread", type=bool, default=False)
    result.add_argument("-v", dest="verbose", type=bool, default=False)

    return result


def setup_environment(cats, output_dir):
    # LOADS VARIABLES, INITIALIZES INPUT VALUES
    directory = os.getcwd()
    # Load the image list
    cat_list = pd.read_csv(f"{directory}/{cats}")
    if len(cat_list) == 0:
        raise ValueError("No fits files found in image list file.")
    # Set the output directory
    outputs = directory if args.output_dir is None else f"{directory}/{output_dir}"
    return directory, cat_list, outputs


if __name__ == "__main__":
    args = argument_parser().parse_args()
    directory, cat_list, outputs = setup_environment(args.cat_list, args.output_dir)
    for i in range(len(cat_list)):
        if args.verbose:
            print(
                f'---------------\nConverting {cat_list.iloc[i]["catalog"]} to LDAC\n---------------'
            )
        with fits.open(cat_list.iloc[i]["catalog"]) as hdul:
            datatable = Table(hdul[2].data)
        data = prepare_input_catalog(datatable)
        copy_to_template(
            data,
            cat_list.iloc[i]["output_name"],
        )
