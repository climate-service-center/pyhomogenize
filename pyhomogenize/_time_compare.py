from ._time_control import time_control


class time_compare(time_control):
    """Class for getting the intersection of two time axis.

    The :class:`time_compare` contains the class `time_control`.

    Parameters
    ----------
    compare_objects: str or list or nested list
        List of all objects to compare their time axes
    """

    def __init__(self, *compare_objects, **kwargs):
        self.compare_objects = self.compare_objects(compare_objects)
        self.time_control_objects = self.time_control_objects(**kwargs)
        self.times = self.times()

    def compare_objects(self, compare_objects):
        """List of all objects to compare their time axes."""
        return self._flatten_list(compare_objects)

    def time_control_objects(self, **kwargs):
        """List of all `compare_objects` set to time_control objects."""
        return [
            self._to_time_control_object(
                cpo,
                **kwargs,
            )
            for cpo in self.compare_objects
        ]

    def times(self):
        """List of all time axes read from ``time_control_objects``."""
        return [tco.time for tco in self.time_control_objects]

    def _to_time_control_object(self, identity, **kwargs):
        """Open identity as ``time_control`` object."""
        if isinstance(identity, time_control):
            return identity
        else:
            return time_control(identity, **kwargs)

    def max_intersection(self):
        """Get the maximum intersection of all time axes.

        Intersection of user-given netCDF files on disk
        and/or ``time_control`` objects.

        Returns
        -------
        tuple
            Left and right border of maximum time intersection

        Example
        -------
        To get left and right border of maximum time intersection
        of two netCDF files.::

            from pyhomogenize import time_compare

            sinter, einter = time_compare('input1.nc',
                                          'input2.nc').max_intersection()


        """
        start, end = None, None
        for time in self.times:
            if not start:
                start = time[0]
            if not end:
                end = time[-1]
            if time[0] > start:
                start = time[0]
            if time[-1] < end:
                end = time[-1]
            if start > end:
                start, end = None, None
        return start, end

    def select_max_intersection(self, **kwargs):
        """Select maximum intersection time slice.

        Intersection of user-given netCDF files on disk
        and/or ``time_control`` objects.

        Parameters
        ----------
        kwargs
            Optional parameters transferred to function `select_time_range`
            output

        Returns
        -------
        list
            List of user-given netCDF files on disk
            and/or ``time_control`` objects
            cropped to maximum time intersection.

        Example
        -------
        To crop time axes of two netCDF files to maximum time intersection.::

            from pyhomogenize import time_compare

            time_compare('input1.nc',
                         'input2.nc').select_max_intersection(output='output.nc')


        """
        max_intersection = self.max_intersection()
        if max_intersection == (None, None):
            return
        return [
            tco.select_time_range(max_intersection, **kwargs)
            for tco in self.time_control_objects
        ]
