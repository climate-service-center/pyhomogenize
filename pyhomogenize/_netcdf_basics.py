import xarray as xr

from ._basics import basics


class netcdf_basics(basics):
    """Class for reading an writing netCDF files.

    The :class:`netcdf_basics` contains :class:`basics`.

    Parameters
    ----------
    files: str or list
        file on disk or xarray.Dataset or list of both
    """

    def __init__(self, files, **kwargs):
        basics.__init__(self, **kwargs)
        if isinstance(files, str):
            files = [files]
        self.files = self.files(files)
        self.ds = self.ds()
        self.name = self.name()

    def files(self, files):
        """List of input netCDF file(s) and/or xr.Dataset(s)."""
        return files

    def ds(self):
        """Input netCDF file(s) openend as xr.Dataset(s). See method open"""
        return self.open()

    def name(self):
        """CF variable name of `ds`. See method get_var_name"""
        return self.get_var_name()

    def _add_to_attrs(self, target, attr_name, value):
        """Adds or updates attribute

        Parameters
        ----------
        target: xr.Dataset or xr.DataArray
            target of adding or updating attribute
        attr_name: str
            Name of the attribute which will be added or updated
        value: str
            Name of the value to be added
        """
        if attr_name in target.attrs:
            value = target.attrs[attr_name] + ", " + value
        target.attrs[attr_name] = value

    def to_variable_attributes(self, indexes, attr_name):
        """Adds or updates variable attributes

        Parameters
        ----------
        indexes: str or list
            Attribute value to be added
        attr_name: str
            Name of the attribute which will be added or updated
        """
        var_name = self.name
        if isinstance(indexes, list):
            indexes = str(indexes)
        if indexes:
            for var in var_name:
                self._add_to_attrs(getattr(self.ds, var), attr_name, indexes)

    def to_global_attributes(self, indexes, attr_name):
        """Adds or updates gloabl attributes

        Parameters
        ----------
        indexes: str or list
            Attribute value to be added
        attr_name: str
            Name of the attribute which will be added or updated
        """
        if isinstance(indexes, list):
            indexes = str(indexes)
        if indexes:
            self._add_to_attrs(self.ds, attr_name, indexes)

    def get_var_name(self, ds=None):
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

        if not ds:
            ds = self.ds

        try:
            var_list = [
                var
                for var in self.ds.data_vars
                if condition(
                    self.ds,
                    var,
                )
            ]
            if var_list:
                return var_list
            return most_coords(ds)
        except Exception:
            return [self.ds.name]

    def _open_xrdataset(
        self,
        files,
        use_cftime=True,
        parallel=True,
        data_vars="minimal",
        chunks={"time": 1},
        coords="minimal",
        compat="override",
        drop=None,
        **kwargs
    ):
        """optimized function for opening large cf datasets.
        based on
        https://github.com/pydata/xarray/issues/1385#issuecomment-561920115
        decode_timedelta=False is added to leave variables and
        coordinates with time units in
        {“days”, “hours”, “minutes”, “seconds”, “milliseconds”, “microseconds”}
        encoded as numbers.

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
            **kwargs
        )

        return xr.decode_cf(ds, use_cftime=use_cftime, decode_timedelta=False)

    def open(self):
        """Opens file or list of files on disk.
        Result is automaticaly wrote to object's attributes.
        """
        if isinstance(self.files, xr.Dataset):
            return self.files
        elif isinstance(self.files, str):
            return self._open_xrdataset(self.files)
        elif isinstance(self.files, list):
            if all(isinstance(x, (xr.Dataset)) for x in self.files):
                return xr.concat(self.files, dim="time")
            elif all(isinstance(x, (str)) for x in self.files):
                return self._open_xrdataset(self.files)
        raise ValueError(
            "Input files are not xarray Datasets or files on disk."
            "You can not mix those two types."
        )

    def write(self, input=None, output=None):
        """Writes `self.ds` or user-given xr.Dataset as netCDF file on disk.

        Parameters
        ----------
        input: xr.Dataset, optional
            xr.Dataset to be written on disk
        output: str, optional
            Name of the output netCDF file

        Returns
        -------
        self
        """

        def is_dataset(input):
            if not isinstance(input, xr.Dataset):
                input = self.ds
            return input

        input = is_dataset(input)
        self.to_variable_attributes(
            self._convert_to_string(self.files), "associated_files"
        )
        if not output:
            print("No output selected.")
        else:
            input.to_netcdf(output)
        return self
