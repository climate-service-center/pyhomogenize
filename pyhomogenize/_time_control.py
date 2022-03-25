import xarray as xr
import numpy as np

from ._netcdf_basics import netcdf_basics
from . import _consts as consts

class time_control(netcdf_basics):

    def __init__(self, files, **kwargs):
        netcdf_basics.__init__(self, files, **kwargs)
        self.time        = self._convert_time(self.ds.time)
        self.frequency   = self._get_frequency()
        self.time_fmt    = consts.format[self.ds.frequency]
        self.equalize    = consts.equalize[self.ds.frequency]

    def _get_frequency(self):
        frequency = xr.infer_freq(self.ds.time)
        if not frequency:
            try:
                frequency = consts.frequencies[self.ds.frequency]
            except:
                print('Could not determine any frequency')
                return
        return frequency

    def _duplicates(self):
        time =  self._equalize_time(self.time, ignore=self.equalize)
        return sorted(list(duplicates(time)))

    def _missings(self):
        time       = self._equalize_time(self.time, ignore=self.equalize)
        date_range = self._equalize_time(self._date_range(time[0], time[-1], self.frequency, calendar=self.time.calendar), ignore=self.equalize)
        return sorted(list(set(date_range).difference(time)))

    def _redundants(self):
        time       = self._equalize_time(self.time, ignore=self.equalize)
        date_range = self._equalize_time(self._date_range(time[0], time[-1], self.frequency, calendar=self.time.calendar), ignore=self.equalize)
        return sorted(list(set(time).difference(date_range)))

    def _write_timesteps(self, timesteps, naming):
        timesteps = self._convert_to_string(timesteps)
        self._dictionary(naming, self.name, timesteps)
        self._to_variable_attributes(timesteps, naming)

    def get_duplicates(self):
        return self._convert_to_string(self._duplicates())

    def get_missings(self):
        return self._convert_to_string(self._missings())

    def get_redundants(self):
        return self._convert_to_string(self._redundants())

    def check_timestamps(self, selection=['duplicates','redundants','missings'], output=None, correct = False):
        if isinstance(selection, str): selection = [selection]
        deletes = []
        time    = self._equalize_time(self.time, ignore=self.equalize)
        for select in selection:
            nmng = consts.naming[select]
            if not select.startswith('_'): select = '_' + select
            add = getattr(self, select)()
            range = np.arange(len(time))
            for a in add:
                loc = [index for index, element in enumerate(time) if element == a][1:]
                deletes += loc
            self._write_timesteps(add, nmng)
        timesteps = [n for n,t in enumerate(time) if n not in list(dict.fromkeys(deletes))]
        if correct: self.ds = self.ds.isel(time=timesteps)
        if output: self.write(input=self.ds, output=output)
        return self

    def select_range(self, time_range, output=None):
        start_date, end_date =time_range
        if not isinstance(start_date, str):
            start_date = self._date_to_str(start_date)
        if not isinstance(end_date, str):
            end_date = self._date_to_str(end_date)
        self.ds   = self.ds.sel(time=slice(start_date, end_date))
        self.time = self._convert_time(self.ds.time)
        if output: self.write(input=self.ds, output=output)
        return self

    def select_limited_time_range(self, output=None, **kwargs):
        start, end = self.date_range_to_frequency_limits(self, date_range=self.time,
                                                         frequency=self.frequency, **kwargs)
        start_date = self._date_to_str(start)
        end_date = self._date_to_str(end)
        self.ds   = self.ds.sel(time=slice(start_date, end_date))
        self.time = self._convert_time(self.ds.time)
        if output: self.write(input=self.ds, output=output)
        return self

    def within_time_range(self, requested_time_range, fmt=None):
        avail_start = self.time[0]
        avail_end   = self.time[-1]
        req_start   = requested_time_range[0]
        req_end     = requested_time_range[-1]
        if isinstance(req_start, str):
            req_start   = self._str_to_date(req_start, fmt=fmt)
        if isinstance(req_end, str):
            req_end     = self._str_to_date(req_end, fmt=fmt, mode='end')
        try:
            key = self.ds.frequency
        except:
            key = self._get_key_to_value(consts.frequencies, self.frequency)
        for unit_of_time in consts.within[key]:
            if getattr(avail_start, unit_of_time) > getattr(req_start, unit_of_time):
                return False
            if getattr(avail_start, unit_of_time) == getattr(req_start, unit_of_time):
                continue
            break
        for unit_of_time in consts.within[key]:
            if getattr(avail_end, unit_of_time) < getattr(req_end, unit_of_time):
                return False
            if getattr(avail_end, unit_of_time) == getattr(req_end, unit_of_time):
                continue
            break

        return True
