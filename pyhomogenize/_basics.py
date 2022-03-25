import xarray as xr
import datetime
from datetime import timedelta as td
from datetime import datetime as dt
import pandas as pd
import copy

from . import _consts as consts

class basics():

    def __init__(self, fmt=None):
        if not fmt: fmt = '%Y-%m-%dT%H:%M:%S'
        self.fmt = fmt
        
    def _flatten_list(self, lst):
        rt = []
        for i in lst:
            if isinstance(i,list): rt.extend(self._flatten_list(i))
            else: rt.append(i)
        return rt

    def _convert_to_string(self, values, delim=',',fmt=None):
        converted = ''
        for v in values:
            try:
                v = self._date_to_str(v, fmt=fmt)
            except:
                pass
            converted += str(v) + delim
        return converted[:-1]

    def _dictionary(self, attr, keys, value):
        for key in keys:
            if attr in self.__dict__:
                getattr(self, attr)[key] = value
            else:
                setattr(self, attr, {key : value})

    def _get_key_to_value(self, dict, value):
        key_list = list(dict.keys())
        val_list = list(dict.values())
        position = val_list.index(value)
        return key_list[position]

    def _get_date_attr(self, frequencies):
        f = self._get_key_to_value(consts.frequencies, frequencies)
        return consts.translator[f]

    def _str_to_date(self, str, fmt=None, mode='start'):
        i=1
        if not fmt: fmt=self.fmt
        if mode not in ['start', 'end']: return
        while True:
            try:
                if mode == 'start': return dt.strptime(str, fmt[:i])
                if mode == 'end'  : return dt.strptime(str, fmt[:i]) + td(days=1) - td(seconds=1)
            except:
                i+=1

    def _date_to_str(self, date, fmt=None):
        if not fmt: fmt=self.fmt
        return date.strftime(fmt)

    def _convert_time(self, time):
        try:
            return pd.to_datetime(time.indexes['time'].astype('str'), format=time.units.split(' ')[-1])
        except:
            return time.indexes['time']

    def _equalize_time(self, time, ignore=['second','microsecond','nanosecond']):
        n = 0
        while n < len(ignore):
            etime = time.tolist()
            query = {ignr:1 for ignr in ignore[::-1][n:]}
            try:
                i = 0
                while i < len(etime):
                    etime[i] = etime[i].replace(**query)
                    i += 1
                return etime
            except:
                n += 1
        return time.tolist()

    def _end_of(self, date, attr):
        while True:
            m  = getattr(date, attr)
            nm = getattr((date + td(hours=1)), attr)
            if nm != m:
                return date
            date += td(hours=1)

    def _begin_of(self, date, attr):
        while True:
            m  = getattr(date, attr)
            pm = getattr((date - td(hours=1)), attr)
            if pm !=m:
                return date
            date -= td(hours=1)

    def _mid_timestep(self, freq, st, end, calendar):
        attr = self._get_date_attr(freq)
        st  = self._date_to_str(self._begin_of(st, attr))
        end = self._date_to_str(self._end_of(end, attr))
        t1  = xr.cftime_range(st, end, freq=freq[0], calendar=calendar)
        t2 = xr.cftime_range(st, periods=len(t1), freq=freq[1], calendar=calendar)
        return t1 + (t2 - t1 + td(days=1)) / 2

    def _point_timestep(self, freq, st, end, calendar):
        if not isinstance(st, str): st = self._date_to_str(st)
        if not isinstance(end, str): end = self._date_to_str(end)
        return xr.cftime_range(st, end, freq=freq, calendar=calendar)

    def _date_range(self, start, end, frequency, calendar='standard'):
        function = xr.cftime_range
        if isinstance(frequency, str):
            return self._point_timestep(frequency, start, end, calendar=calendar)
        if isinstance(frequency, list):
            return self._mid_timestep(frequency, start, end, calendar=calendar)

    def _is_month_start(self, cftime_range):
        array = []
        for cftime in cftime_range:
            prev = cftime - td(days=1)
            if prev.month != cftime.month:
                array += [True]
                continue
            array += [False]
        return array

    def _is_month_end(self, cftime_range):
        array = []
        for cftime in cftime_range:
            next = cftime + td(days=1)
            if next.month != cftime.month:
                array += [True]
                continue
            array += [False]
        return array

    def date_range_to_frequency_limits(self, start=None,
                                       end=None,
                                       date_range=None,
                                       frequency='mon',
                                       smonth=[1,2,3,4,5,6,7,8,9,10,11,12],
                                       emonth=[12,11,10,9,8,7,6,5,4,3,2,1],
                                       is_month_start=None,
                                       is_month_end=None):
        if isinstance(frequency, str):
            if frequency in consts.frequencies.keys():
                frequency = consts.frequencies[frequency]
        if date_range is None:
            if not start or not end: return None, None
            if isinstance(start, str): start = self._str_to_date(start)
            if isinstance(end, str): end   = self._str_to_date(end, mode='end')
            date_range = self._date_range(start, end, frequency)
        else:
            start = date_range[0]
            end   = date_range[-1]
        sdate_range = copy.copy(date_range)
        edate_range = copy.copy(date_range)
        if is_month_start is None: is_month_start = consts.is_month[self._get_date_attr(frequency)]
        if is_month_end is None: is_month_start = consts.is_month[self._get_date_attr(frequency)]
        if is_month_start: sdate_range=date_range[self._is_month_start(date_range)]
        if is_month_end: edate_range=date_range[self._is_month_end(date_range)]
        if sdate_range.empty: return None, None
        if edate_range.empty: return None, None
        for sdate in sdate_range:
            if sdate < start: continue
            if sdate.month in smonth: break
            sdate = None
        if not sdate: return None, None
        for edate in reversed(edate_range):
            if edate > end: continue
            if edate.month in emonth: break
            edate=None
        if not edate: return None, None
        return sdate, edate
