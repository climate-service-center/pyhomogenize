import xarray as xr
from iteration_utilities import duplicates

from . import _consts as consts
from ._netcdf_basics import netcdf_basics


class time_control(netcdf_basics):
    """Class for dealing with a netCDF file's time axis.

    The :class:`time_control` contains the :class:`ǹetcdf_basics`.
    """

    def __init__(self, *args, **kwargs):
        netcdf_basics.__init__(self, *args, **kwargs)
        self.time = self.time()
        del self.frequency
        self.frequency = self.frequency()
        self.time_fmt = self.time_fmt()
        self.equalize = self.equalize()
        del self.calendar
        self.calendar = self.calendar()

    def time(self):
        """netCDF file's time axis"""
        return self._convert_time(self.ds.time)

    def frequency(self):
        """netCDF file's frequency"""
        return self._get_frequency()

    def time_fmt(self):
        """predefined explicit format string derived from `frequency`"""
        return consts.format[self.ds.frequency]

    def equalize(self):
        """predefined list of ``datetime.datetime`` instance attributes
        to be ignored
        """
        return consts.equalize[self.ds.frequency]

    def calendar(self):
        """Calendar type read from netCDF file"""
        return self.time.calendar

    def _get_frequency(self):
        """Get frequency of xr.Dataset"""
        frequency = xr.infer_freq(self.ds.time)
        if not frequency:
            try:
                frequency = consts.frequencies[self.ds.frequency]
            except Exception:
                print("Could not determine any frequency")
                return
        return frequency

    def _duplicates(self):
        """Get duplicated time steps."""
        time = self._equalize_time(self.time, ignore=self.equalize)
        return sorted(list(duplicates(time)))

    def _missings(self):
        """Get missing time steps."""
        time = self._equalize_time(self.time, ignore=self.equalize)
        date_range = self._equalize_time(
            self.date_range(
                time[0], time[-1], self.frequency, calendar=self.time.calendar
            ),
            ignore=self.equalize,
        )
        return sorted(list(set(date_range).difference(time)))

    def _redundants(self):
        """Get redundant time steps."""
        time = self._equalize_time(self.time, ignore=self.equalize)
        date_range = self._equalize_time(
            self.date_range(
                time[0], time[-1], self.frequency, calendar=self.time.calendar
            ),
            ignore=self.equalize,
        )
        return sorted(list(set(time).difference(date_range)))

    def _write_timesteps(self, timesteps, naming):
        """Write timesteps to variable attributes."""
        timesteps = self._convert_to_string(timesteps)
        self._dictionary(naming, self.name, timesteps)
        self.to_variable_attributes(timesteps, naming)

    def get_duplicates(self):
        """Get string of duplicated time steps."""
        return self._convert_to_string(self._duplicates())

    def get_missings(self):
        """Get string of missing time steps."""
        return self._convert_to_string(self._missings())

    def get_redundants(self):
        """Get string of redundant time steps."""
        return self._convert_to_string(self._redundants())

    def check_timestamps(
        self,
        selection=["duplicates", "redundants", "missings"],
        output=None,
        correct=False,
    ):
        """Check netCDF file's time axis.

        Exist whether duplicated, missing and/or redundant time steps.

        Parameters
        ----------
        selection: str or list, default=['duplicates','redundants','missings']
            Check which kind of time steps exist.
        output: str, optional
            Write result on disk.
        correct: bool, default: False
            Delete located time steps from xr.Dataset.
            Automatically set True if output.

        Returns
        -------
        self

        Example
        -------
        To check netCDF file's time axis whether duplicated, missing and/or
        redundant time steps exist and result write on disk::

            from pyhomogenize import time_control

            time_control('input.nc').check_timestamps(output='output.nc')

        """
        if isinstance(selection, str):
            selection = [selection]
        deletes = []
        time = self._equalize_time(self.time, ignore=self.equalize)
        for select in selection:
            nmng = consts.naming[select]
            if not select.startswith("_"):
                select = "_" + select
            add = getattr(self, select)()

            for a in add:
                loc = [i for i, e in enumerate(time) if e == a][1:]
                deletes += loc
            self._write_timesteps(add, nmng)
        dlist = list(dict.fromkeys(deletes))
        timesteps = [n for n, t in enumerate(time) if n not in dlist]
        if output:
            correct = True
        if correct:
            self.ds = self.ds.isel(time=timesteps)
            self.time = self._convert_time(self.ds.time)
        if output:
            self.write(output=output)
        return self

    def select_time_range(self, time_range, output=None):
        """Select user-given time slice from xr.Dataset

        Parameters
        ----------
        time_range: list
            List of two strings or ``cftime.datatime`` object
            representing the left and right time bounds
        output: str, optional
            Write result on disk.

        Returns
        -------
        self

        Example
        -------
        To select time slice from netCDF file.::

            from pyhomogenize import time_control

            time_control('input.nc').select_time_range(
                                         ['2005-01-01','2005-12-31'],
                                         output='output.nc')
        """
        start_date, end_date = time_range
        if not isinstance(start_date, str):
            start_date = self.date_to_str(start_date)
        if not isinstance(end_date, str):
            end_date = self.date_to_str(end_date)
        self.ds = self.ds.sel(time=slice(start_date, end_date))
        self.time = self._convert_time(self.ds.time)
        if output:
            self.write(output=output)
        return self

    def select_limited_time_range(self, output=None, **kwargs):
        """Select time slice from xr.Dataset satisfying user-given conditions.
        See pyh.basics.date_range_to_frequency_limits.

        Parameters
        ----------
        output: str, optional
            Write result on disk.
        kwargs:
            Optional parameters transferred to function
            `date_range_to_frequency_limits`:
            smonth
            emonth
            is_month_start
            is_month_end

        Returns
        -------
        self

        Example
        -------
        To select time slice from netCDF file starts
        with the first month of any season and
        ends with the last month of any season.
        The time slice is then e.g. from 2005-03-16 to 2005-11-16::

            from pyhomogenize import time_control

            time_control('input.nc').select_limited_time_range(
                                               smonth=[3,6,9,12],
                                               emonth=[2,5,8,11],
                                               output='output.nc')

        """
        start, end = self.date_range_to_frequency_limits(
            self, date_range=self.time, frequency=self.frequency, **kwargs
        )
        start_date = self.date_to_str(start)
        end_date = self.date_to_str(end)
        self.ds = self.ds.sel(time=slice(start_date, end_date))
        self.time = self._convert_time(self.ds.time)
        if output:
            self.write(output=output)
        return self

    def within_time_range(self, requested_time_range, fmt=None):
        """
        Checks whether netCDF files time axis is within user-given borders.

        Parameters
        ----------
        requested_time_range: list
            List of two strings or ``cftime.datatime`` object representing
            the left and right time bounds
        fmt: str, default: '%Y-%m-%dT%H:%M:%S'
            Explicit format string for converting string into
            ``cftime.datetime`` object

        Returns
        -------
        bool

        Example
        -------

        To check whether netCDF files time axis is within user-given borders.::

            from pyhomogenize import time_control

            within = time_control('input.nc').within_time_range(['2005-01-02',
                                                                 '2005-12-31'])
        """
        avail_start = self.time[0]
        avail_end = self.time[-1]
        req_start = requested_time_range[0]
        req_end = requested_time_range[-1]
        if isinstance(req_start, str):
            req_start = self.str_to_date(
                req_start,
                fmt=fmt,
                calendar=self.calendar,
            )
        if isinstance(req_end, str):
            req_end = self.str_to_date(
                req_end, fmt=fmt, calendar=self.calendar, mode="end"
            )
        try:
            key = self.ds.frequency
        except Exception:
            key = self._get_key_to_value(consts.frequencies, self.frequency)
        for unit_of_time in consts.within[key]:
            astart = getattr(avail_start, unit_of_time)
            rstart = getattr(req_start, unit_of_time)
            if astart > rstart:
                return False
            if astart == rstart:
                continue
            break
        for unit_of_time in consts.within[key]:
            aend = getattr(avail_end, unit_of_time)
            rend = getattr(req_end, unit_of_time)
            if aend < rend:
                return False
            if aend == rend:
                continue
            break

        return True
