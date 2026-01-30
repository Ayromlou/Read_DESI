"""Lightweight readers for DESI catalog files."""

from .io import (
    open_hdf5_dict,
    open_fits_dict,
    open_parquet_dict,
    fits_list,
    load_catalog,
    identify_file_type,
)

__all__ = [
    "open_hdf5_dict",
    "open_fits_dict",
    "open_parquet_dict",
    "fits_list",
    "load_catalog",
    "identify_file_type",
]