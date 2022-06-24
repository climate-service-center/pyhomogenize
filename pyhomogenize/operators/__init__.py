from . import (merge, seltimerange, showdups, showmiss, showreds,
               showtimestamps, showvar, timecheck)

operators = """

All available operators implemented:
Arguments in brackets are optional.
"""

operators += merge.help
operators += showvar.help
operators += seltimerange.help
operators += showtimestamps.help
operators += showdups.help
operators += showmiss.help
operators += showreds.help
operators += timecheck.help
