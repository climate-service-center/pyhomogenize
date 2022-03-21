
from . import merge
from . import showvar
from . import seltimerange
from . import showtimerange
from . import showdups
from . import showmiss
from . import showreds
from . import timecheck

operators = """

All available operators implemented:
Arguments in brackets are optional.
"""

operators += merge.help
operators += showvar.help
operators += seltimerange.help
operators += showtimerange.help
operators += showdups.help
operators += showmiss.help
operators += showreds.help
operators += timecheck.help
