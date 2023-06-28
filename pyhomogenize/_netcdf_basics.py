import xarray as xr

from ._basics import basics
from ._read_write import get_var_name, open_xrdataset, save_xrdataset


class netcdf_basics(basics):
    """Class for reading an writing netCDF files.

    The `netcdf_basics` class contains `basics` class.

    Parameters
    ----------
    files: str or list
        file on disk or xarray.Dataset or list of both
    """

    def __init__(self, files, **kwargs):
        """Read and write netCDF files."""
        basics.__init__(self, **kwargs)
        if isinstance(files, str):
            files = [files]
        self.files = self.files(files)
        self.ds = self.ds()
        self.name = self.name()
        self._encoding_coordinates()

    def files(self, files):
        """List of input netCDF file(s) and/or xr.Dataset(s)."""
        return files

    def ds(self):
        """Input netCDF file(s) openend as xr.Dataset(s). See method open."""
        return self.open()

    def name(self):
        """CF variable name of `ds`. See method get_var_name."""
        return get_var_name(self.ds)

    def _encoding_coordinates(self):
        for data_var in self.ds.data_vars:
            if data_var not in self.name:
                self.ds[data_var].encoding["coordinates"] = None
                self.ds[data_var].encoding["_FillValue"] = None

    def _add_to_attrs(self, target, attr_name, value):
        """Add or update attribute.

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
        """Add or update variable attributes.

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
        """Add or update global attributes.

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

    def open(self):
        """Open file or list of files on disk.

        Result will be automaticaly written to object's attributes.
        """
        if isinstance(self.files, xr.Dataset):
            return self.files.copy()
        elif isinstance(self.files, str):
            return open_xrdataset(self.files)
        elif isinstance(self.files, list):
            if all(isinstance(x, (xr.Dataset)) for x in self.files):
                return xr.concat(self.files, dim="time")
            elif all(isinstance(x, (str)) for x in self.files):
                return open_xrdataset(self.files)
        raise ValueError(
            "Input files are not xarray Datasets or files on disk."
            "You can not mix those two types."
        )

    def write(self, output=None, **kwargs):
        """Write `self.ds` or user-given xr.Dataset as netCDF file on disk.

        Parameters
        ----------
        output: str, optional
            Name of the output netCDF file

        Returns
        -------
        self
        """
        self.to_variable_attributes(
            self._convert_to_string(self.files), "associated_files"
        )
        if not output:
            print("No output selected.")
        else:
            save_xrdataset(self.ds, output, **kwargs)
        return self
