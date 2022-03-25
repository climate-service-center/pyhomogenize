
from ._time_control import time_control

class time_compare(time_control):
    
    def __init__(self, *compare_objects, **kwargs):
        self.compare_objects = self._flatten_list(compare_objects)
        self.time_control_objects = [self._to_time_control_object(cpo, **kwargs) for cpo in self.compare_objects]
        self.times = [tco.time for tco in self.time_control_objects]

    def _to_time_control_object(self, identity, **kwargs):
        if isinstance(identity, time_control):
            return identity
        else:
            return time_control(identity, **kwargs)

    def max_intersection(self):
        start, end = None, None
        for time in self.times:
            if not start: start = time[0]
            if not end: end = time[-1]
            if time[0]  > start: start = time[0]
            if time[-1] < end: end = time[-1]
            if start > end:
                start, end = None, None
        return start, end

    def select_max_intersection(self, **kwargs):
        max_intersection = self.max_intersection()
        if max_intersection == (None, None): return
        return [tco.select_range(max_intersection, **kwargs) for tco in self.time_control_objects]
