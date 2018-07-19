
import os, os.path
import subprocess

from .io import *


def simulate(rotor, folder="./temp/", threshold=-15.0, max_freq=2000.0):
    __write_params(folder=folder, rotor=rotor, threshold=threshold, max_freq=max_freq)
    __run_simulation(folder=folder, rotor=rotor)
    return __read_lines(folder=folder, rotor=rotor)


def __make_filename(folder, extension, name):
    return os.path.join(folder, name + extension)


def __read_lines(rotor, folder="./temp/"):
    catfile = __make_filename(folder, '.cat', rotor.name)
    return load_cat(catfile)


def __run_simulation(rotor, folder="./temp/"):
    if os.name == 'nt':
        progname = "spcat.exe"
    else:
        progname = "spcat_linux"

    infilename = __make_filename(folder, '', rotor.name)
    spcatname = os.path.join(os.path.dirname(os.path.abspath(__file__)), progname)
    a = subprocess.Popen("%s %s" % (spcatname, infilename), stdout=subprocess.PIPE, shell=True)
    a.stdout.read()
    # a.stdout.read() seems to be best way to get SPCAT to finish


def __write_params(rotor, folder, threshold, max_freq):
    if not os.path.exists(folder):
        os.makedirs(folder)
    intfile = __make_filename(folder, '.int', rotor.name)
    varfile = __make_filename(folder, '.var', rotor.name)
    save_var(varfile, rotor)
    save_int(intfile, rotor, inten=threshold, max_freq=max_freq)
