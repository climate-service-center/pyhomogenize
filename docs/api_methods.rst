.. currentmodule:: pyhomogenize

Converting string to cftime.datetime object and vice versa
----------------------------------------------------------

.. automethod:: basics.str_to_date

.. automethod:: basics.date_to_str

Creating and manipulating time axis
-----------------------------------

.. automethod:: basics.date_range

.. automethod:: basics.date_range_to_frequency_limits

Reading, writing and manipulating netCDF file(s)
------------------------------------------------

.. automethod:: netcdf_basics.open

.. automethod:: netcdf_basics.write

.. automethod:: netcdf_basics.to_global_attributes

.. automethod:: netcdf_basics.to_variable_attributes

Checking self-created or netCDF file's time axis
------------------------------------------------

.. automethod:: basics.is_month_start

.. automethod:: basics.is_month_end

.. automethod:: time_control.get_duplicates

.. automethod:: time_control.get_missings

.. automethod:: time_control.get_redundants

.. automethod:: time_control.check_timestamps

.. automethod:: time_control.select_time_range

.. automethod:: time_control.select_limited_time_range

.. automethod:: time_control.within_time_range

Comparing time axes of several netCDF files and/or xr.Datasets
--------------------------------------------------------------

.. automethod:: time_compare.max_intersection

.. automethod:: time_compare.select_max_intersection
