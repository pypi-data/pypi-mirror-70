#!python

from PyFoam.Applications.ChangePython import changePython

changePython("pvpython","PVSnapshot",options=["--mesa-swr"])
