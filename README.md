# scamper
A flexible framework to match WCS of images and catalogs using the [Scamp](https://www.astromatic.net/software/scamp/) tool.

## Dependencies 
The catalog downloader requires the following packages, which should come with standard Conda distributions: *os, shutil, configparser, argparse, importlib, subprocess, astropy* and *pandas*.

## Running the Script
### Download the Repository
First, download this repository onto your device. You can either manually download, or navigate to your chosen directory and run:

```
git clone https://github.com/bclevine/scamper.git
```

### Setup
Create the following empty folders in the `scamper` directory: `templates`, `reference_data`, `data`. 

Then, place two template files in the `templates` folder: 
- `template_catalog.fits.cat`: a Source Extractor catalog in the `fits LDAC` format
- `template_img.fits`: a `fits` image file with a valid WCS header

Next, place your reference catalog (also in the `fits LDAC` format) in the `reference_data` directory.

Finally, place any `fits` images and/or catalogs that you want to process with the script in the `data` directory.

_Note that you may specify different locations and names for the `reference_data` and `data` directories in the `config.ini` file._

### Configuration

You will need one additional Python script to adjust the WCS for your input image `fits` files. This script will be dependent on the format of these files; an example tailored for HST ACS images is provided.

Open `config.ini` and adjust the configuration according to your use case. You can only align images or catalogs at the same time; not both. (This may be changed later). Also remember to set `image_adjustment_file` to the script described above.

### Run The Script
It's time to run the script. In your terminal, navigate to the main `scamper` directory and type the following command:

```
python3 scamper.py
```

No flags are available, but verbose mode will be added in the near future.

Files will be modified in place.

## Running individual parts of the script

The script is designed to be highly modular and compatible with both command line usage and python imports. Each of the scripts in the folder may be run from the command line using flags to specify various options and textfiles to specify the files to analyze and/or modify. 
