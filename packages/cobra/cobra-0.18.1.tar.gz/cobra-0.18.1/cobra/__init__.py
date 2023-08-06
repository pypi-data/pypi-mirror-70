# -*- coding: utf-8 -*-

from __future__ import absolute_import

# set the warning format to be on a single line
import warnings as _warnings
from os import name as _name
from os.path import abspath as _abspath
from os.path import dirname as _dirname

# set the warning format to be prettier and fit on one line
_cobra_path = _dirname(_abspath(__file__))
if _name == "posix":
    _warning_base = "%s:%s \x1b[1;31m%s\x1b[0m: %s\n"  # colors
else:
    _warning_base = "%s:%s %s: %s\n"


def _warn_format(message, category, filename, lineno, file=None, line=None):
    shortname = filename.replace(_cobra_path, "cobra", 1)
    return _warning_base % (shortname, lineno, category.__name__, message)

_warnings.formatwarning = _warn_format

import sys

if sys.version_info[0] == 2:
    _warnings.warn(
        "Python 2 is reaching end of life (see "
        "https://www.python.org/dev/peps/pep-0373/) and many cobra "
        "dependencies have already dropped support. At the moment it *should* "
        "still work but we will no longer actively maintain Python 2 support.",
        FutureWarning
    )

from cobra.core import (
    Configuration, DictList, Gene, Metabolite, Model, Object, Reaction,
    Solution, Species)
from cobra import flux_analysis
from cobra import io
from cobra import sampling
from cobra.util import show_versions

__version__ = "0.18.1"
