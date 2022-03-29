.. currentmodule:: pyhomogenize

#############
API reference
#############

This page provides an auto-generated summary of the pyhomogenize API.

Pyhomogenize time creating and manipulating classes
===================================================

Basic functions for controlling netCDF CF standard time axis
------------------------------------------------------------

.. autoclass:: basics

   .. automethod:: basics.__init__

   .. rubric:: Methods

   .. autosummary::

      basics.str_to_date

      basics.date_to_str

      basics.is_month_start

      basics.is_month_end

      basics.date_range

      basics.date_range_to_frequency_limits

   .. rubric:: Attributes

   .. autosummary::

      basics.fmt

      basics.calendar
        
Basic functions to read an write netCDF files
---------------------------------------------

.. autoclass:: netcdf_basics

   .. automethod:: __init__

   .. rubric:: Methods

   .. autosummary::

      netcdf_basics.open

      netcdf_basics.write
      
      netcdf_basics.get_var_name

      netcdf_basics.to_global_attributes

      netcdf_basics.to_variable_attributes

   .. rubric:: Attributes

   .. autosummary::

      netcdf_basics.files

      netcdf_basics.ds

      netcdf_basics.name

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

Functions to get the intersection of multiple netCDF files's time axis
----------------------------------------------------------------------

.. autoclass:: time_compare

   .. automethod:: __init__

   .. rubric:: Methods

   .. autosummary::

      time_compare.max_intersection

      time_compare.select_max_intersection

   .. rubric:: Attributes

   .. autosummary::

      time_compare.compare_objects

      time_compare.time_control_objects

      time_compare.times

PageBreak      
      
Class methods
=============

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

.. automethod:: netcdf_basics.get_var_name

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

Class attributes
================

.. automethod:: basics.fmt

.. automethod:: basics.calendar

.. automethod:: netcdf_basics.files

.. automethod:: netcdf_basics.ds

.. automethod:: netcdf_basics.name

.. automethod:: time_control.time

.. automethod:: time_control.frequency

.. automethod:: time_control.time_fmt

.. automethod:: time_control.equalize

.. automethod:: time_control.calendar

.. automethod:: time_compare.compare_objects

.. automethod:: time_compare.time_control_objects

.. automethod:: time_compare.time		 
		

