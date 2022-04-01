.. currentmodule:: pyhomogenize

============================================
Use pyhomogenize as a command-line interface
============================================

All available operators. Arguments in brackets are optional.

merge : Merge given input files
    usage: pyhomogenize merge -i ifile1 [ifile2 [ifileN]] -o ofile

showvar : Print variable names.
    usage: pyhomogenize showvar -i ifile1 [ifile2 [ifileN]]

seltimerange : Select user-given time range.
    usage: pyhomogenize seltimerange,<timestamp1>,<timestamp2> -i ifile1 [ifile2 [ifileN]] -o ofile
    timeformat: %y%m%d[T:%H:%M:%S]

showtimestamps : Show available timestamps.
    usage: pyhomogenize showtimestamps -i ifile1 [ifile2 [ifileN]]

showdups : Print duplicated timestamps.
    usage: pyhomogenize showdups -i ifile1 [ifile2 [ifileN]]

showmiss : Print missing timestamps.
    usage: pyhomogenize showmiss ifile1 [ifile2 [ifileN]]

showreds : Print redundant timestamps.
    usage: netcdf_time_control showreds ifile1 [ifile2 [ifileN]]

timecheck : By default, delete duplicated and redundant time stamps from input files and write duplicated, redundant and missing timestamps to netcdf variable attributes. The selection is changeable.
    usage: pyhomogenize timecheck[,duplicates,redundants,missings] -i ifile1 [ifile2 [ifileN]] -o ofile\n'
