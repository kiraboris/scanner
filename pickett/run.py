
import os, os.path
import subprocess

from .io import *


def make_lines(rotor, folder="./temp/", basename="temp", **kwargs):
    write_rotor(folder=folder, rotor=rotor, basename=basename, **kwargs)
    __run_spcat(folder=folder, rotor=rotor, basename=basename)
    lines = __read_lines(folder=folder, rotor=rotor, basename=basename)
    return lines


def fit_lines():
    pass


def __read_lines(rotor, basename, folder="./temp/"):
    catfile = make_filename(folder, '.cat', basename)
    return load_cat(catfile)


def __run_spcat(rotor, basename, folder="./temp/"):
    if os.name == 'nt':
        progname = "spcat.exe"
    else:
        progname = "spcat_linux"

    infilename = make_filename(os.path.abspath(folder), '', basename)
    spcatname = os.path.join(os.path.dirname(os.path.abspath(__file__)), progname)
    a = subprocess.Popen("%s %s" % (spcatname, infilename), stdout=subprocess.PIPE, shell=True)
    a.stdout.read()
    # seems to be best way to get SPCAT to finish



