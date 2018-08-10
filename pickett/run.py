
import os, os.path
import subprocess

from .io import *


def make_lines(rotor, folder="./temp/", threshold=-15.0, max_freq=2000.0):
    write_rotor(folder=folder, rotor=rotor, threshold=threshold, max_freq=max_freq)
    __run_spcat(folder=folder, rotor=rotor)
    return __read_lines(folder=folder, rotor=rotor)


def fit_lines():
    pass


def __read_lines(rotor, folder="./temp/"):
    catfile = make_filename(folder, '.cat', rotor.name)
    return load_cat(catfile)


def __run_spcat(rotor, folder="./temp/"):
    if os.name == 'nt':
        progname = "spcat.exe"
    else:
        progname = "spcat_linux"

    infilename = make_filename(folder, '', rotor.name)
    spcatname = os.path.join(os.path.dirname(os.path.abspath(__file__)), progname)
    a = subprocess.Popen("%s %s" % (spcatname, infilename), stdout=subprocess.PIPE, shell=True)
    a.stdout.read()
    # seems to be best way to get SPCAT to finish



