"""Standalone I/O helpers for HDF5, FITS, and Parquet catalogs.

Written by M. Reza Ayromlou (ayromlou@gmail.com).
"""

from typing import Any, Dict, Optional, Sequence

import os

import h5py
import numpy as np
import pandas as pd
from astropy.io import fits


def hdf5_to_dict(hdf5_group, fields = None, print_header = False, print_keys = False):
    result = {}
    keys = fields if fields is not None else hdf5_group.keys()
    for key in keys:
        if key not in hdf5_group:
            raise KeyError(f"Field '{key}' not found in group {hdf5_group.name}")
        if print_keys:
            print(f"Processing key: {key}")
        item = hdf5_group[key]
        if isinstance(item, h5py.Dataset):
            result[key] = item[()]
        elif isinstance(item, h5py.Group):
            # Recurse, but do not pass the same fields list deeper.
            result[key] = hdf5_to_dict(item, None, print_header)
        if print_header and key == "Header":
            print("Header:")
            for attr_name, attr_value in item.attrs.items():
                print(f"  {attr_name}: {attr_value}")
    return result


def open_hdf5_dict(file_path, fields = None, print_header = False):
    with h5py.File(file_path, "r") as hdf:
        data = hdf5_to_dict(hdf, fields, print_header)
    return data


def open_fits_dict(file_path, fields = None, print_header = False):
    with fits.open(file_path, memmap=False) as hdul:
        hdu_map = {}
        for idx, hdu in enumerate(hdul):
            base = hdu.name if hdu.name else f"HDU{idx}"
            key = base if base not in hdu_map else f"{base}_{idx}"
            hdu_map[key] = hdu

        data = {}
        keys = fields if fields is not None else hdu_map.keys()
        for key in keys:
            if key not in hdu_map:
                raise KeyError(f"HDU '{key}' not found in FITS file")
            hdu = hdu_map[key]
            if print_header:
                print(f"Header [{key}]:")
                print(hdu.header)
            data[key] = {"data": hdu.data, "header": hdu.header}

    return data


def fits_list(file_path):
    """Print a summary of the FITS HDUs, similar to `h5ls -r`."""
    with fits.open(file_path, memmap=False) as hdul:
        print(f"Filename: {file_path}")
        for idx, hdu in enumerate(hdul):
            name = hdu.name if hdu.name else f"HDU{idx}"
            hdu_type = type(hdu).__name__
            shape = getattr(hdu.data, "shape", None)
            shape_str = str(shape) if shape is not None else "None"
            if getattr(hdu, "columns", None) is not None:
                col_count = len(hdu.columns)
                print(f"[{idx}] {name}: {hdu_type}, shape={shape_str}, cols={col_count}")
            else:
                print(f"[{idx}] {name}: {hdu_type}, shape={shape_str}")


def open_parquet_dict(file_path, columns = None):
    try:
        import pyarrow.parquet as pq

        table = pq.read_table(file_path, columns=columns)
        return table.to_pydict()
    except Exception:
        df = pd.read_parquet(file_path, columns=columns)
        return df.to_dict(orient="list")

def identify_file_type(file_path):
    """Identify the file type based on its extension."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext in {".hdf5", ".h5"}:
        return "hdf5"
    elif ext in {".fits", ".fit", ".fts"}:
        return "fits"
    elif ext in {".parquet", ".pq"}:
        return "parquet"
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

def load_catalog(file_path, fields = None, columns = None, print_header = False):
    file_type = identify_file_type(file_path)
    if file_type == "hdf5":
        return open_hdf5_dict(file_path, fields=fields, print_header=print_header)
    elif file_type == "fits":
        return open_fits_dict(file_path, fields=fields, print_header=print_header)
    elif file_type == "parquet":
        return open_parquet_dict(file_path, columns=columns)
    else:
        raise ValueError(f"Unsupported file extension: {file_path}")
