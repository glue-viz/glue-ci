from __future__ import print_function

import sys

print("Python  :", sys.version.split()[0])

import numpy

print("Numpy   :", numpy.__version__)

import scipy

print("Scipy   :", scipy.__version__)

import matplotlib
import matplotlib.pyplot

print("MPL     :", matplotlib.__version__)

import IPython

print("IPython :", IPython.__version__)

import pyfits

print("PyFITS  :", pyfits.__version__)

from PyQt4.QtCore import QT_VERSION_STR
from PyQt4.pyqtconfig import Configuration
cfg = Configuration()

print("Qt      :", QT_VERSION_STR)
print("SIP     :", cfg.sip_version_str)
print("PyQt    :", cfg.pyqt_version_str)
