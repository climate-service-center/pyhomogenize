from . import merge  # noqa
from . import seltimerange  # noqa
from . import showdups  # noqa
from . import showmiss  # noqa
from . import showreds  # noqa
from . import showtimestamps  # noqa
from . import showvar  # noqa
from . import timecheck  # noqa

operators = """All available operators implemented:
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
