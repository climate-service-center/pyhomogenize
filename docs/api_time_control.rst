.. currentmodule:: pyhomogenize

Functions for dealing with a netCDF file's time axis
----------------------------------------------------

.. autoclass:: time_control

   .. automethod:: __init__

   .. rubric:: Methods

   .. autosummary::

      time_control.get_duplicates

      time_control.get_missings

      time_control.get_redundants

      time_control.check_timestamps

      time_control.select_time_range

      time_control.select_limited_time_range

      time_control.within_time_range

   .. rubric:: Attributes

   .. autosummary::

      time_control.time

      time_control.frequency

      time_control.time_fmt

      time_control.equalize

      time_control.calendar
