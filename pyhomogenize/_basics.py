import copy
from datetime import datetime as dt
from datetime import timedelta as td

import cftime
import pandas as pd
import xarray as xr

from . import _consts as consts


class basics:
    """Class for controlling netCDF CF standard time axis.

    The :class:`basics` contains some basics functions.

    Parameters
    ----------
    fmt: str, default: '%Y-%m-%dT%H:%M:%S'
        Time format for converting strings into ``cftime.datetime`` object
    calendar: str, default: 'standard'
        Calendar type for the datetimes.
    """

    def __init__(
        self,
        fmt="%Y-%m-%dT%H:%M:%S",
        calendar="standard",
        frequency="D",
    ):
        self.fmt = fmt
        self.calendar = calendar
        self.frequency = frequency

    def fmt(self, fmt):
        """Time format for converting strings into
        ``cftime.datetime`` object.
        """
        return fmt

    def calendar(self, calendar):
        """Calendar type for the datetimes.
        Will be overwritten by netCDF file's inherent calendar.
        """
        return calendar

    def frequency(self, frequency):
        """Frequency strings or list of strings can have multiples.
        Will be overwritten by netCDF file's inherent frequency.
        """
        return frequency

    def _flatten_list(self, lst):
        """Flatten a list containing strings and lists
        of arbitrarily nested lists

        Parameters
        ----------
        lst: list
            List containing strings and lists of arbitrarily nested lists

        Returns
        -------
        list
        """
        rt = []
        for i in lst:
            if isinstance(i, list):
                rt.extend(self._flatten_list(i))
            else:
                rt.append(i)
        return rt

    def _convert_to_string(self, values, delim=",", fmt=None):
        """Converts list of strings and ``cftime.datetime`` or
        ``datetime.datetime`` objects to string.

        Parameters
        ----------
        values: list
            List of strings and ``cftime.datetime`` or
            ``datetime.datetime`` objects
        delim: str, default: ','
            Output string delimiter between input list entries
        fmt: str, default: '%Y-%m-%dT%H:%M:%S'
            Explicit format string for converting string into
            ``cftime.datetime`` object
            Consider only if list element is ``cftime.datetime`` object

        Returns
        -------
        str
        """
        if not fmt:
            fmt = self.fmt
        converted = ""
        for v in values:
            try:
                v = self.date_to_str(v, fmt=fmt)
            except Exception:
                pass
            converted += str(v) + delim
        return converted[:-1]

    def _dictionary(self, attr, keys, value):
        """Write or update attribute using key-value pairs

        Parameters
        ----------
        attr: str
            Attribute name
        keys: str
            Key names
        values: any type
            Key values
        """
        for key in keys:
            if attr in self.__dict__:
                getattr(self, attr)[key] = value
            else:
                setattr(self, attr, {key: value})

    def _get_key_to_value(self, dict, value):
        """Get key of key-value pair using value

        Parameters
        ----------
        dict: dict
            Dictionary containing key-value pair
        value: any type
            Value of key-value pair

        Returns
        -------
        key: str
            Key of key-value pair
        """
        key_list = list(dict.keys())
        val_list = list(dict.values())
        position = val_list.index(value)
        return key_list[position]

    def _get_date_attr(self, frequencies):
        """Get ``cftime.datetime`` instance attribute from CF frequency

        Parameters
        ----------
        frequencies: str or list
            CF frequency or list of CF frequencies

        Returns
        -------
        attribute: str
            ``cftime.datetime`` instance attribute
        """
        f = self._get_key_to_value(consts.frequencies, frequencies)
        return consts.translator[f]

    def str_to_date(self, str, fmt=None, mode="start", calendar=None):
        """Converts string to ``cftime.datetime`` object

        Parameters
        ----------
        str: str
            string representing the time
        fmt: str, default: '%Y-%m-%dT%H:%M:%S'
            Explicit format string
        calendar: str, default: 'standard'
            Calendar type for the datetimes
        mode: {'start', 'end'}, default: 'start'
            `start`: Set ``cftime.datetime`` instance attributes
            not represented by `fmt` to 0.
            `end`: Set ``cftime.datetime`` instance attributes
            not represented by `fmt` to last possible values
            considering `str`.

        Returns
        -------
        ``cftime.datetime`` object
        """
        i = 1
        if not fmt:
            fmt = self.fmt
        if not calendar:
            calendar = self.calendar
        if mode not in ["start", "end"]:
            return
        while True:
            try:
                date = dt.strptime(str, fmt[:i])
                break
            except Exception:
                i += 1
        cfdate = cftime.datetime(
            date.year,
            date.month,
            date.day,
            calendar=calendar,
        )
        if mode == "start":
            return cfdate
        if mode == "end":
            return cfdate + td(days=1) - td(seconds=1)

    def date_to_str(self, date, fmt=None):
        """Converts ``cftime.datetime`` or ``datetime.datetime`` object
        to string

        Parameters
        ----------
        date: ``cftime.datetime`` or ``datetime.datetime`` object
            time to be converted
        fmt: str, default: '%Y-%m-%dT%H:%M:%S'
            Explicit format string

        Returns
        -------
        str: str
            string representing the time
        """
        if not fmt:
            fmt = self.fmt
        return date.strftime(fmt)

    def _convert_time(self, time, calendar="standard"):
        """Converts time object to ``datetime.datetime`` object"""

        def cftimeindex(time_index, calendar):
            cf_datetime = [
                cftime.datetime(
                    t.year,
                    t.month,
                    t.day,
                    calendar=calendar,
                )
                for t in time_index
            ]
            return xr.CFTimeIndex(cf_datetime)

        if hasattr(self, "calendar"):
            calendar = self.calendar
        if "calendar" not in time.attrs:
            calendar = calendar
        if calendar == "proleptic_gregorian":
            calendar = "standard"
        try:
            if "units" in time.attrs:
                time_index = pd.to_datetime(
                    time.indexes["time"].astype("str"),
                    format=time.units.split(" ")[-1],
                )
            else:
                time_index = pd.to_datetime(
                    time.indexes["time"],
                )
            return cftimeindex(
                time_index,
                calendar=calendar,
            )
        except Exception:
            if "time" in time.indexes:
                return time.indexes["time"]
            else:
                t = time.values[()]
                return cftimeindex(t, calendar=calendar)

    def _equalize_time(
        self,
        time,
        ignore=["second", "microsecond", "nanosecond"],
    ):
        """Ignore ``datetime.datetime`` instance attributes and set them to 0

        Parameters
        ----------
        time: CFTimeIndex
            CFTimeIndex containing cftime.datetime objects
        ignore: list, default: ['second','microsecond','nanosecond']
            list of datetime.datetime instance attributes to be ignored

        Returns
        -------
        time: CFTimeIndex
            ``CFTimeIndex`` containing ``cftime.datetime`` objects
            with ignored instance attributes
        """
        n = 0
        while n < len(ignore):
            etime = time.tolist()
            query = {ignr: 1 for ignr in ignore[::-1][n:]}
            try:
                i = 0
                while i < len(etime):
                    etime[i] = etime[i].replace(**query)
                    i += 1
                return etime
            except Exception:
                n += 1
        return time.tolist()

    def _interpret_frequency(self, freq):
        if isinstance(freq, str):
            if freq in consts.frequencies.keys():
                freq = consts.frequencies[freq]
        return freq

    def _mid_timestep(self, freq, st, end, calendar=None, **kwargs):
        """Build ``CFTimeIndex``
        Set elements between user-given frequencies

        Parameters
        ----------
        freq: list
            list of two frequency strings for use with ``cftime`` calendars
            https://xarray.pydata.org/en/stable/generated/xarray.cftime_range.html
        st: cftime.datetime or datetime.datetime
            Left bound for generating dates
        end: cftime.datetime or datetime.datetime
            Right bound for generating dates
        calendar: str, default: 'standard'
            Calendar type for the datetimes

        Returns
        -------
        CFTimeIndex
        """

        if not calendar:
            calendar = self.calendar
        t1 = xr.cftime_range(
            st,
            end,
            freq=freq[0],
            calendar=calendar,
            **kwargs,
        )
        t2 = xr.cftime_range(
            st,
            periods=len(t1),
            freq=freq[1],
            calendar=calendar,
            **kwargs,
        )
        return t1 + (t2 - t1) / 2

    def _point_timestep(self, freq, st, end, calendar=None, **kwargs):
        """Build ``CFTimeIndex``
        Set elements to user-given frequency

        Parameters
        ----------
        freq: str
            frequency string for use with ``cftime`` calendars
            https://xarray.pydata.org/en/stable/generated/xarray.cftime_range.html
        st: cftime.datetime or datetime.datetime
            Left bound for generating dates
        end: cftime.datetime or datetime.datetime
            Right bound for generating dates
        calendar: str, default: 'standard'
            Calendar type for the datetimes

        Returns
        -------
        CFTimeIndex
        """
        if not calendar:
            calendar = self.calendar
        return xr.cftime_range(st, end, freq=freq, calendar=calendar, **kwargs)

    def date_range(self, start, end, frequency="D", calendar=None, **kwargs):
        """Build ``CFTimeIndex``

        Parameters
        ----------
        start: cftime.datetime or datetime.datetime or str
            Left bound for generating dates
        end: cftime.datetime or datetime.datetime or str
            Right bound for generating dates
        frequency: str ot list
            frequency string or list of frequency strings
            for use with ``cftime`` calendars
            https://xarray.pydata.org/en/stable/generated/xarray.cftime_range.html
            Set elements to user-given frequency if type of frequency is str
            Set elements between user-given frequencies if type
        calendar: str, default: 'standard'

        Returns
        -------
        CFTimeIndex
        """
        if not calendar:
            calendar = self.calendar
        frequency = self._interpret_frequency(frequency)
        if isinstance(frequency, str):
            return self._point_timestep(
                frequency,
                start,
                end,
                calendar=calendar,
                **kwargs,
            )
        if isinstance(frequency, list):
            return self._mid_timestep(
                frequency,
                start,
                end,
                calendar=calendar,
                **kwargs,
            )

    def is_month_start(self, cftime_range):
        """Check whether each element of ``CFTimeIndex``
        is first day of the month

        Parameters
        ----------
        cftime_range: CFTimeIndex
            CFTimeIndex containing cftime.datetime objects

        Returns
        -------
        list
            list of boolean values
        """
        array = []
        for cftr in cftime_range:
            prev = cftr - td(days=1)
            if prev.month != cftr.month:
                array += [True]
                continue
            array += [False]
        return array

    def is_month_end(self, cftime_range):
        """Check whether each element of ``CFTimeIndex``
        is last day of the month

        Parameters
        ----------
        cftime_range: CFTimeIndex
            CFTimeIndex containing cftime.datetime objects

        Returns
        -------
        list
            list of boolean values
        """

        array = []
        for cftr in cftime_range:
            next = cftr + td(days=1)
            if next.month != cftr.month:
                array += [True]
                continue
            array += [False]
        return array

    def date_range_to_frequency_limits(
        self,
        start=None,
        end=None,
        date_range=None,
        frequency=None,
        calendar=None,
        smonth=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        emonth=[12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        is_month_start=None,
        is_month_end=None,
        get_range=False,
        **kwargs,
    ):
        """Get bounds of CFTimeIndex which satisfy user-given conditions.

        Parameters
        ----------
        start: str or datetime.datetime or cftime.cftime, optional
            Left bound for generating dates
        end: str or datetime.datetime or cftime.cftime, optional
            Right bound for generating dates
        date_range: CFTimeIndex, optional
            CFTimeIndex containing cftime.datetime objects
        frequency: str ot list
            CF frequency string or list of CF frequency strings
            or frequency string or list of frequency strings
            for use with ``cftime`` calendars
            https://xarray.pydata.org/en/stable/generated/xarray.cftime_range.html
        calendar: str, default: 'standard'
            Calendar type for the datetimes
        smonth: list, default: [1,2,3,4,5,6,7,8,9,10,11,12]
            One of the allowed values of left bound's
            ``datetime.datetime`` instance attribute month
        emonth: list, default: [12,11,10,9,8,7,6,5,4,3,2,1]
            One of the allowed values of right bound's
            ``datetime.datetime`` instance attribute month
        is_month_start: bool, optional
            Value of left bound's ``datetime.datetime`` instance attribute day
            must be equal to first day of the month
            Automatically set to True for sub_monthly frequencies
        is_month_end: bool, optional
            Value of right bound's ``datetime.datetime`` instance attribute day
            must be equal to last day of the month
            Automatically set to True for sub_monthly frequencies
        get_range: bool, default:False
            If False returns left and right bounds
            If True returns CFTimeIndex

        Returns
        -------
        tuple
            Tuple of start and end dates satisfying all conditions

        Example
        -------
        To get bounds of CFTimeIndex which satisfy user-given conditions.
        Monthly frequency values with a 360-day calendar have to start with
        the first month of any season and have to end with the last month
        of any season.
        It returns the tuple (2005-03-16 00:00:00 2005-11-16 00:00:00)::

            from pyhomogenize import basics

            basics = basics()

            start, end = basics.date_range_to_frequency_limits(
                     start='2005-01-01',
                     end='2005-12-30',
                     smonth=[3,6,9,12],
                     emonth=[2,5,8,11],
                     calendar='360_day',
            )

        """
        if date_range is None:
            if not frequency:
                frequency = self.frequency
            if not calendar:
                calendar = self.calendar
            frequency = self._interpret_frequency(frequency)
            if start is None or end is None:
                return None, None
            date_range = self.date_range(
                start,
                end,
                frequency=frequency,
                calendar=calendar,
                **kwargs,
            )
        start = date_range[0]
        end = date_range[-1]
        sdate_range = copy.copy(date_range)
        edate_range = copy.copy(date_range)
        if is_month_start is None:
            is_month_start = consts.is_month[self._get_date_attr(frequency)]
        if is_month_end is None:
            is_month_end = consts.is_month[self._get_date_attr(frequency)]
        if is_month_start:
            sdate_range = date_range[self.is_month_start(date_range)]
        if is_month_end:
            edate_range = date_range[self.is_month_end(date_range)]

        if sdate_range.empty:
            return None, None
        if edate_range.empty:
            return None, None
        for sdate in sdate_range:
            if sdate < start:
                continue
            if sdate.month in smonth:
                break
            sdate = None
        if not sdate:
            return None, None
        for edate in reversed(edate_range):
            if edate > end:
                continue
            if edate.month in emonth:
                break
            edate = None
        if not edate:
            return None, None
        if get_range:
            return xr.CFTimeIndex(
                [cft for cft in date_range if cft >= sdate and cft <= edate]
            )
        else:
            return sdate, edate

    def get_time_bounds(
        self,
        start=None,
        end=None,
        date_range=None,
        frequency=None,
        calendar=None,
        l_freq=None,
        u_freq=None,
        tdelta=None,
        dims={},
        coords={},
        **kwargs,
    ):
        """Get time bounds of CFTimeIndex.

        Parameters
        ----------
        start: str or datetime.datetime or cftime.cftime, optional
            Left bound for generating dates
        end: str or datetime.datetime or cftime.cftime, optional
            Right bound for generating dates
        date_range: CFTimeIndex, optional
            CFTimeIndex containing cftime.datetime objects
        frequency: str or list
            CF frequency string or list of CF frequency strings
            or frequency string or list of frequency strings
            for use with ``cftime`` calendars
            https://xarray.pydata.org/en/stable/generated/xarray.cftime_range.html
        calendar: str, default: 'standard'
            Calendar type for the datetimes
        l_freq: str, optional
            CF frequency string for left bounds
            If None take time frequency-dependent string
        u_freq: str, optional
            CF frequency string for right bounds
            If None take time frequency-dependent string
        tdelta: int, optional
            Number of hours to substract from left bounds
            and add to right bounds
            If None take time frequency-dependent integer
        dims: dict
            Time dimensions.
        coords: dict
            Time coordinates.

        Returns
        -------
        xr.DataArray

        """
        if start is None:
            if date_range is None:
                raise ValueError("Choose one of: start or date_range")
            start = date_range[0]
            end = date_range[-1]
            frequency = date_range.freq
        if frequency is None:
            frequency = self.frequency
        frequency = self._interpret_frequency(frequency)
        if calendar is None:
            calendar = self.calendar
        f = self._get_key_to_value(consts.frequencies, frequency)
        if l_freq is None:
            l_freq = consts.tbounds[f][0]
        if u_freq is None:
            u_freq = consts.tbounds[f][1]
        if tdelta is None:
            tdelta = consts.tbounds[f][2]
        if isinstance(start, str):
            start = self.str_to_date(start)
        if isinstance(end, str):
            end = self.str_to_date(end)
        ll = self.date_range(
            start=start,
            end=end,
            frequency=l_freq,
            **kwargs,
        )
        ul = self.date_range(
            start=start,
            end=end,
            frequency=u_freq,
            **kwargs,
        )
        if end is None:
            end = start
            ll = ll[:-1]
            ul = ul[1:]

        while True:
            if ll[0] > start:
                shift_l = ll.shift(-1, freq=l_freq)
                ll = self.date_range(
                    start=shift_l[0],
                    end=ll[-1],
                    frequency=l_freq,
                )
                if ll[0] > start:
                    shift_u = ul.shift(-1, freq=u_freq)
                    ul = self.date_range(
                        start=shift_u[0],
                        end=ul[-1],
                        frequency=u_freq,
                    )
            else:
                break
        while True:
            if ul[-1] < end:
                shift_u = ul.shift(1, freq=u_freq)
                ul = self.date_range(
                    start=ul[0],
                    end=shift_u[-1],
                    frequency=u_freq,
                )
                if ul[-1] < end:
                    shift_l = ll.shift(1, freq=l_freq)
                    ll = self.date_range(
                        start=ll[0],
                        end=shift_l[-1],
                        frequency=l_freq,
                    )
            else:
                break

        if start == end and len(ll) > 1:
            ll = ll[:-1]

        ll_ = ll - td(hours=tdelta)
        if ll.equals(ul):
            bounds = xr.DataArray(ll_, coords=coords, dims="bnds")
        else:
            ul_ = ul + td(hours=tdelta)
            lower = xr.DataArray(ll_, coords=coords, dims=dims)
            upper = xr.DataArray(ul_, coords=coords, dims=dims)
            bounds = xr.concat([lower, upper], dim="bnds")
        # first = (bounds.isel({"time": 0}) - td(days=1)).assign_coords(
        #    {"time": start}
        # )
        # result = xr.concat([first, bounds], dim="time")
        result = bounds
        return result.transpose(..., "bnds")
