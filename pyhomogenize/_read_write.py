# flake8: noqa: E501

import numpy as np
import xarray as xr
from scipy.interpolate import griddata


def open_xrdataset(
    files,
    use_cftime=True,
    decode_times=False,
    parallel=False,
    preprocess=None,
    data_vars="minimal",
    chunks={"time": 1},
    coords="minimal",
    compat="override",
    combine="by_coords",
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
    preprocess: func, optional
        See [open_mfdataset_]
        If None preprocc is ds.reset_coords(drop=True)
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
    xr.Dataset

    References
    ----------
    .. [open_xrdataset] https://github.com/pydata/xarray/issues/1385#issuecomment-561920115
    .. [open_mfdataset] https://docs.xarray.dev/en/stable/generated/xarray.open_mfdataset.html
    .. [decode_cf] https://docs.xarray.dev/en/stable/generated/xarray.decode_cf.html

    """

    def drop_all_coords(ds):
        return ds.reset_coords(drop=True)

    if preprocess is None:
        preprocess = drop_all_coords

    ds = xr.open_mfdataset(
        files,
        parallel=parallel,
        decode_times=decode_times,
        combine=combine,
        preprocess=preprocess,
        decode_cf=False,
        chunks=chunks,
        data_vars=data_vars,
        coords=coords,
        compat=compat,
        **kwargs,
    )
    if isinstance(files, list):
        files = ",  ".join(map(str, files))
    data_vars = get_var_name(ds)
    for var in data_vars:
        ds[var].attrs["associated_files"] = files
    ds.attrs["CF_variables"] = data_vars
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
        Tuple of block lengths for this DataArray’s data
    """
    chunk_dict = {}
    if not chunk_var in da.coords:
        return tuple(chunk_dict.values())
    if da.coords[chunk_var].size == 1:
        return tuple(chunk_dict.values())
    chunks = da.chunks
    if chunks is None:
        chunks = da.chunk().chunks
    dims = da.dims
    size = 1
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
    encoding={},
    MISSVAL=1e20,
    chunk_dict={},
):
    """Get encoding for each CF variable in dataset.

    Parameters
    ----------
    ds: xr.Dataset
        Dataset containing CF variables.
    encoding: dict
        Encoding dictionary
    MISSVAL: float, optional
        Missing value.
    chunk_dict: dict or None, optional
        Dictionary with parameters for `get_chunksizes`.
        If None do not chunk dimension.
        If empty call `get_chunksizes` with default values.

    Returns
    -------
    dict
        Encoding dictionary
    """
    for var in get_var_name(ds):
        if not var in encoding.keys():
            encoding[var] = {}
        encoding[var]["_FillValue"] = MISSVAL
        encoding[var]["missing_value"] = MISSVAL
        if isinstance(chunk_dict, dict):
            chunk_tpl = get_chunksizes(
                ds[var],
                **chunk_dict,
            )
            if chunk_tpl == ():
                continue
            encoding[var]["chunksizes"] = chunk_tpl
    return encoding


def save_xrdataset(
    ds,
    name=None,
    encoding_dict={},
    format="NETCDF4",
    unlimited_dims={"time": True},
    compute=True,
):
    """Save dataset as netCDF file.

    Parameters
    ----------
    ds: xr.Dataset
        Dataset to save on disk.
    name: str, optional
        name of the netcdf output file
    encoding_dict: dict or None, optional
        Encoding dictionary for `get_encoding`.
        If dict call `get_encoding` with dict values as parameters.
        If empty call `get_encoding` with default values.
        If None encoding = {}.
    format: str, optional
        File format for the resulting netCDF file
    unlimited_dims: dict
        Dimension(s) that should be serialized as unlimited dimensions.
        By default, no dimensions are treated as unlimited dimensions.
    compute: bool, optional
        If true compute immediately, otherwise return a
        `dask.delayed.Delayed` object that can be computed later.

    Returns
    -------
        * ``bytes`` if name is None
        * ``dask.delayed.Delayed`` if compute is False
        * None otherwise
    """
    if encoding_dict is None:
        encoding_dict = {}
    encoding = get_encoding(
        ds,
        **encoding_dict,
    )
    return ds.to_netcdf(
        name,
        encoding=encoding,
        format=format,
        unlimited_dims=unlimited_dims,
        compute=compute,
    )


def get_var_name(ds):
    """List of CF variables in xr.Dataset.

    Parameters
    ----------
    ds: xr.Dataset

    Returns
    -------
    list
        List of CF variables
    """

    def drop_bnds(var_list):
        return [var for var in var_list if "_bnds" not in var and "_bounds" not in var]

    def condition(ds, var):
        return len(ds[var].dims) == len(ds.dims)

    def most_dims(ds):
        dims = 0
        name = []
        for var in ds.data_vars:
            ndims = len(ds[var].dims)
            if ndims > dims:
                dims = ndims
                name = [var]
            elif dims == ndims:
                name += [var]
        return drop_bnds(name)

    try:
        var_list = [var for var in ds.data_vars if condition(ds, var)]
        if var_list:
            return drop_bnds(var_list)
        return most_dims(ds)
    except Exception:
        if hasattr(ds, "name"):
            return [ds.name]
        raise ValueError("Could not find any CF variables.")


def era5_to_regular_grid(
    inp,
    lat="latitude",
    lon="longitude",
    method="linear",
    fill_value=None,
):
    """Convert ERA5 reduced gaussian grid to regular lat/lon grid.

    Parameters
    ----------
    inp: xr.Dataset, xr.DataArray
        ERA5 input as xr.Dataset or xr.DataArray.
    lat: str
        Name of the latitude dimension in `inp`.
    lon: str
        Name of the longitude dimension in `inp`.
    method: {"linear", "nearest", "cubic"}
        Method of interpolation
    fill_value: float, optional
        Value used to fill in for requested points outside
        of the convex hull of the input points.

    Returns
    -------
    xr.Dataset or xr.DataArray
        xr.Dataset or xr.DataArray of interpolated values

    Notes
    -----
    The idea is taken from https://gis.stackexchange.com/questions/455149/interpolate-irregularly-sampled-data-to-a-regular-grid.
    For more information about the input parameter see: https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html
    """

    def interp_to_grid(u, xc, yc, new_lats, new_lons, method, fill_value):
        new_points = np.stack(np.meshgrid(new_lats, new_lons), axis=2).reshape(
            (new_lats.size * new_lons.size, 2)
        )
        z = griddata(
            (xc, yc),
            u,
            (new_points[:, 1], new_points[:, 0]),
            method=method,
            fill_value=fill_value,
        )
        return z.reshape((new_lats.size, new_lons.size), order="F")

    lats = inp[lat].values
    lons = inp[lon].values
    lat_attrs = inp[lat].attrs
    lon_attrs = inp[lon].attrs

    _new_lats = np.unique(lats)
    _new_lons = np.unique(lons)
    _new_lats = np.sort(_new_lats)[::-1]
    lat_attrs["stored_direction"] = "decreasing"
    _new_lons = np.arange(
        _new_lons[0],
        _new_lons[-1] + _new_lons[1] - _new_lons[0],
        _new_lons[1] - _new_lons[0],
    )

    new_lons = xr.DataArray(
        _new_lons,
        dims=lon,
        coords={lon: _new_lons},
        attrs=lon_attrs,
    )
    new_lats = xr.DataArray(
        _new_lats,
        dims=lat,
        coords={lat: _new_lats},
        attrs=lat_attrs,
    )
    if fill_value is None:
        fill_value = np.nan

    # Vectorize the `interp_to_grid` function.
    out = xr.apply_ufunc(
        interp_to_grid,
        inp,
        lons,
        lats,
        new_lats,
        new_lons,
        method,
        fill_value,
        vectorize=True,
        dask="parallelized",
        input_core_dims=[["values"], ["values"], ["values"], [lat], [lon], [], []],
        output_core_dims=[[lat, lon]],
        output_dtypes=[float],
        keep_attrs=True,
    )
    out[lat] = new_lats
    out[lon] = new_lons
    return out


def era5_combine_time_step(
    inp,
):
    """Combine coordinates `time` and `step` to new time coordinate.

    Parameters
    ----------
    inp: xr.Dataset or xr.DataArray
        ERA5 input as xr.Dataset or xr.DataArray.

    Returns
    -------
    xr.Dataset or xr.DataArray
        xr.Dataset or xr.DataArray with combined time coordinate.
    """

    def convert_step(step):
        from datetime import timedelta

        if "units" in step.attrs:
            units = step.units
            return [timedelta(**{units: s}) for s in step.values]
        return step

    ds = inp.copy()
    ds["step"] = convert_step(ds["step"])
    ds = ds.stack(new_time=["time", "step"])
    time = [t + s for t, s in ds["new_time"].values]
    ds = ds.reset_index(["time", "step"])
    ds["new_time"] = time
    for coord in ["time", "step", "valid_time"]:
        if coord in ds.coords:
            del ds[coord]
    return ds.rename({"new_time": "time"})
