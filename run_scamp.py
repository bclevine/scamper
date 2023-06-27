import os
import argparse
import subprocess


"""
Script that takes a list of LDAC catalogs and runs Scamp on them.
"""


def argument_parser():
    # PARSES COMMAND LINE ARGUMENTS TO SCRIPT
    result = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    # Where is the reference catalog?
    result.add_argument("-r", dest="ref_cat", type=str)
    # Where is the list of catalogs to Scamp?
    result.add_argument("-c", dest="cat_list", type=str, default="scamp_list.txt")

    result.add_argument("-v", dest="verbose", type=bool, default=False)

    return result


def scamp(
    filename,
    reference,
    scamp_command="./scamp",
):
    # CALLS SOURCE EXTRACTOR FROM THE COMMAND LINE
    subprocess.run(
        [
            scamp_command,
            f"@{os.getcwd()}/{filename}",
            "-ASTREFCAT_NAME",
            reference,
            "-ASTREF_CATALOG",
            "FILE",
            "-HEADER_SUFFIX",
            ".head",
            "-ASTREFMAG_KEY",
            "FLUX_APER",
            "-ASTREFMAGERR_KEY",
            "FLUXERR_APER",
        ]
    )


if __name__ == "__main__":
    args = argument_parser().parse_args()
    if args.verbose:
        print(
            f"---------------\nRunning Scamp on reference {args.ref_cat}\n---------------"
        )
    scamp(
        args.cat_list,
        args.ref_cat,
        scamp_command="./scamp/scamp-2.10.0/src/scamp",
    )
