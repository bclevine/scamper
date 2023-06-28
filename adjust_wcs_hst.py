from astropy.io import fits

wcs_keys = ["RAW_LTV1", "RAW_LTV2", "LTM1_1", "LTM2_2", "RA_APER", "DEC_APER"]


def adjust_wcs(imgfile, pars):
    val1, val2 = pars
    # UPDATE WCS VALUES IN IMAGE
    fits.setval(imgfile, "RA_APER", value=val1, ext=1)
    fits.setval(imgfile, "DEC_APER", value=val2, ext=1)
    fits.setval(imgfile, "CRVAL1", value=val1, ext=1)
    fits.setval(imgfile, "CRVAL2", value=val2, ext=1)
    with fits.open(imgfile, "update") as f:
        for key in fits.getheader(imgfile, 1).keys():
            if key in wcs_keys:
                f[0].header.append((key, fits.getheader(imgfile, 1)[key]))
        f[0].header["RA_APER"] = val1
        f[0].header["DEC_APER"] = val2
