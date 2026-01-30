# DESI public readers

Helpers for reading DESI catalogs in HDF5, FITS, and Parquet

Written by M. Reza Ayromlou (ayromlou@gmail.com; ayromlou@uni-bonn.de) and Max Warkentin (mwarken@MPA-Garching.MPG.DE).

## Contents
- `desi_reader/io.py`: `open_hdf5_dict`, `open_fits_dict`, `open_parquet_dict`, `load_catalog`
- `examples/plot_mass_cg.py`: quick histogram sanity check

## Install deps
```
pip install -r requirements.txt
```

## Usage
```python
from desi_reader import *

hdf5 = open_hdf5_dict("data_path.h5") # or .hdf5 -> This loads the HDF5 file as a dictionary
fits = open_fits_dict("data_path.fits") # -> This loads the FITS file as a dictionary
parq = open_parquet_dict("data_path.parquet") # -> This loads the Parquet file as a dictionary
data = load_catalog("data_path.h5")  # or .hdf5, .fits, .parquet, .pq -> This auto-detects the format and loads the catalog
```

## Example
Edit `examples/plot_mass_cg.py` and set:
- `file_name` to your local catalog path
- `file_format` to `hdf5`, `fits`, `parquet`

Then run:
```
python examples/plot_mass_cg.py
```
or simply use ipython.
