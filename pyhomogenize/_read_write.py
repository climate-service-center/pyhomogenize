# flake8: noqa: E501

import xarray as xr


def open_xrdataset(
    files,
    use_cftime=True,
    parallel=True,
    data_vars="minimal",
    chunks={"time": 1},
    coords="minimal",
    compat="override",
    **kwargs,
):
    """Optimized function for opening large cf datasets.

    based on [open_xrdataset]_.
    decode_timedelta=False is added to leave variables and
    coordinates with time units in
    {“days”, “hours”, “minutes”, “seconds”, “milliseconds”, “microseconds”}
    encoded as numbers.

    Parameters
    ----------
    files: str or list
        See [open_mfdataset]_
    use_cftime: bool, optional
        See [decode_cf]_
    parallel: bool, optional
        See [open_mfdataset]_
    data_vars: {"minimal", "different", "all"} or list of str, optional
        See [open_mfdataset]
    chunks: int or dict, optional
        See [open_mfdataset]
    coords: {"minimal", "different", "all"} or list of str, optional
        See [open_mfdataset]
    compat: str (see `coords`), optional
        See [open_mfdataset]

    Returns
    -------
    xarray.Dataset

    References
    ----------
    .. [open_xrdataset] https://github.com/pydata/xarray/issues/1385#issuecomment-561920115
    .. [open_mfdataset] https://docs.xarray.dev/en/stable/generated/xarray.open_mfdataset.html
    .. [decode_cf] https://docs.xarray.dev/en/stable/generated/xarray.decode_cf.html

    """

    def drop_all_coords(ds):
        return ds.reset_coords(drop=True)

    ds = xr.open_mfdataset(
        files,
        parallel=parallel,
        decode_times=False,
        combine="by_coords",
        preprocess=drop_all_coords,
        decode_cf=False,
        chunks=chunks,
        data_vars=data_vars,
        coords=coords,
        compat=compat,
        **kwargs,
    )
    return xr.decode_cf(ds, use_cftime=use_cftime, decode_timedelta=False)


def get_chunksizes(
    da,
    chunk_var="time",
    size_opt=128,
    bit_precision=32,
):
    """Get optimum chunk size.

    Get chunk size for each dimension and calculate chunk size for
    dimension `chunk_var` to get `size_opt` per chunk.

    Parameters
    ----------
    da: xr.DataArray
        DataArray of CF variable.
    chunk_var: str, optional
        Calculate chunk size for dimension name.
    size_opt: int, optional
        Optiumum size per chunk in MB.
    bit_precision: int
        floating-point format
        32: single precision, 64: double precision

    Returns
    -------
    tuple
        Tuple of block lengths for this dataarray’s data
    """
    chunks = da.chunks
    dims = da.dims
    size = 1
    chunk_dict = {}
    for dim, chunk in dict(zip(dims, chunks)).items():
        if isinstance(chunk, tuple):
            chunk_size = sum(chunk)
        else:
            chunk_size = chunk
        if dim != chunk_var:
            size *= chunk_size
        chunk_dict[dim] = chunk_size
    size_act = size * bit_precision / 8 / 1024**2
    chunk_dict[chunk_var] = min(
        chunk_dict[chunk_var],
        int(size_opt / size_act),
    )
    return tuple(chunk_dict.values())


def get_encoding(
    ds,
    MISSVAL=1e20,
    chunking=True,
    chunk_dict={},
):
    """Get encoding for each CF variable in dataset.

    Parameters
    ----------
    ds: xr.Dataset
        Dataset containing CF variables.
    MISSVAL: float, optional
        Missing value.
    chunking: bool, optional
        If true call `get_chunksizes`.
    chunk_dict: dict, optional
        Dictionary with parameters for `get_chunksizes`.

    Returns
    -------
    dict
        Encoding dictionary
    """
    encoding = {}
    for var in get_var_name(ds):
        encoding[var] = {
            "_FillValue": MISSVAL,
            "missing_value": MISSVAL,
        }
        if chunking:
            encoding[var]["chunksizes"] = get_chunksizes(
                ds[var],
                **chunk_dict,
            )
    return encoding


def save_to_netcdf(
    ds,
    name,
    encoding={},
    compute=True,
):
    """Save dataset as netCDF file.

    Parameters
    ----------
    ds: xr.Dataset
        Dataset to save on disk.
    name: str
        name of the netcdf output file
    encoding: dict or None, optional
        Encoding dictionary for `get_encoding`.
    compute: bool, optional
        If true compute immediately, otherwise return a
        `dask.delayed.Delayed` object that can be computed later.

    Returns
    -------
        * ``bytes`` if path is None
        * ``dask.delayed.Delayed`` if compute is False
        * None otherwise
    """
    if isinstance(encoding, dict):
        encoding = get_encoding(
            ds,
            **encoding,
        )
    elif encoding is None:
        encoding = {}
    return ds.to_netcdf(
        name,
        encoding=encoding,
        format="NETCDF4",
        unlimited_dims={"time": True},
        compute=compute,
    )


def get_var_name(ds):
    """List of CF variables in xr.Dataset

    Parameters
    ----------
    ds: xr.Dataset
        xarray Dataset
    Returns
    -------
    list
        List of CF variables
    """

    def condition(ds, var):
        return len(ds[var].coords) == len(ds.coords)

    def most_coords(ds):
        coords = 0
        name = []
        for var in ds.data_vars:
            ncoords = len(ds[var].coords)
            if ncoords > coords:
                coords = ncoords
                name += [var]
        return name

    try:
        var_list = [var for var in ds.data_vars if condition(ds, var)]
        if var_list:
            return var_list
        return most_coords(ds)
    except Exception:
        if hasattr(ds, "name"):
            return [ds.name]
        raise ValueError("Coul not find any CF variables.")
