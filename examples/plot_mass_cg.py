#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Simple script to read DESI catalogs and plot the histogram of a given quantity (see README.md for instructions) """

# In[]
""" Import necessary modules """
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Allow running from any working directory without installing the package.
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from desi_reader import *


""" Simple function to plot the histogram of a given quantity from DESI catalogs """

def plot_DESI_histogram(quantity, nonzero=True, finite=True, loghist=True, label=None, nbins=100):
    quantity = np.asarray(quantity)
    if finite:
        quantity = quantity[np.isfinite(quantity)]
    if nonzero:
        quantity = quantity[quantity > 0]
    if loghist:
        quantity = np.log10(quantity)
    plt.figure()
    plt.hist(quantity, bins=nbins, histtype="step", label=label)
    plt.xlabel(hist_field)
    plt.ylabel("Count")
    plt.xlim(8, 12.5)
    plt.legend()
    plt.tight_layout()
    plt.show()


# In[]
""" Set the file path and format """
# Update these paths to your local files.
file_name = 'File Name Here' # e.g. /data.hdf5
file_format = identify_file_type(file_name)  # 'hdf5', 'fits', or 'parquet'

hist_field = "MASS_CG"


# In[]
""" Load the catalog """
data = load_catalog(file_name)

if file_format == 'hdf5':
    quantity = data['catalog']['table'][hist_field]
elif file_format == 'fits':
    quantity = data['HDU1']['data'][hist_field]
elif file_format == 'parquet':
    quantity = pd.to_numeric(data[hist_field], errors="coerce")
else:
    raise SystemExit("Set file_format to 'hdf5', 'fits', or 'parquet'")

# In[]
""" Plot the mass histogram """
plot_DESI_histogram(quantity)
