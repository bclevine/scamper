import os
import shutil
import configparser
import pandas as pd
from run_scamp import scamp


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    directory = os.getcwd()
    os.makedirs("SCAMPER_TEMP", exist_ok=True)

    # LOAD IMAGE LIST
    file_list = pd.read_csv(f"{directory}/{config['DEFAULT']['path_to_data']}")
    if len(file_list) == 0:
        raise ValueError("File list is empty.")

    # RUN ON IMAGES
    if config["DEFAULT"]["image_or_catalog"] == "image":
        from importlib import import_module
        from catalog_from_img import source_extract
        from scamp_to_img import load_parameters

        # SOURCE EXTRACT
        for i in range(len(file_list)):
            source_extract(
                directory,
                file_list.iloc[i]["science_data"],
                file_list.iloc[i]["weight_data"],
                "SCAMPER_TEMP/" + file_list.iloc[i]["file_to_update"],
                directory,
            )

        # RUN SCAMP
        # First create the list of files to run Scamp on:
        lines = list("SCAMPER_TEMP/" + file_list["file_to_update"] + ".cat")
        with open("SCAMPER_TEMP/scamp_files.txt", "w") as f:
            for line in lines:
                f.write(line)
                f.write("\n")
        # Now run Scamp
        scamp(
            "SCAMPER_TEMP/scamp_files.txt",
            config["DEFAULT"]["path_to_reference"],
            scamp_command=config["DEFAULT"]["scamp_command"],
        )

        # UPDATE FITS FILES
        for i in range(len(file_list)):
            pars = load_parameters(
                "SCAMPER_TEMP/" + file_list.iloc[i]["file_to_update"] + ".head"
            )
            adjustment_func = import_module(config["DEFAULT"]["image_adjustment_file"])
            adjustment_func.adjust_wcs(file_list.iloc[i]["file_to_update"], pars)

        # CLEAN UP
        # shutil.rmtree("SCAMPER_TEMP")

    # RUN ON CATALOGS
