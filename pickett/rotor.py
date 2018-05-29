
import os, os.path
import subprocess

from . import pickett
from . import entities

# *** quantum rotor model ***


class RotorSymmetry:

    def __init__(self):
        # sample defaults
        self.type = "asym"
        self.group = 'C1'
        self.representation = 'prolate'
        self.reduction = 's'
        self.Qdegree = 3   # used in Q() calculation
        self.spin_degeneracy = 1  # for all spins, in Pickett format


class RotorParameter(object):

    def __init__(self, name, value=1.0, error=None, flag_fit=True):
        self.name = name
        self.value = value
        self.error = error if error else value / 2
        self.flag_fit = flag_fit
        self.flag_enabled = True


class Rotor(object):

    def __init__(self, name="noname"):

        self.name = name
        self.params = {}
        self.symmetry = RotorSymmetry()
        self.sim_lines = []
        self.simulation_method = "pickett"
        self.flag_wavenumbers = False
        self.mu_A = None
        self.mu_B = None
        self.mu_C = None

    def param(self, name):

        return self.params[name]

    def add_param(self, name, **kwargs):

        self.params[name] = RotorParameter(name, **kwargs)

    def Q(self, T):

        if self.symmetry.type == "asym":
            Q_rot_base = (self.param('A').value *
                          self.param('B').value *
                          self.param('C').value) ** (-0.5)
        elif self.symmetry.type == "sym":
            Q_rot_base = (self.param('A').value *
                          self.param('B').value ** 2) ** (-0.5)
        else:
            Q_rot_base = 0

        Q_rot = ((5.3311 * 10 ** (6)) * (T ** (1.5)) * Q_rot_base * self.symmetry.Qdegree)

        return Q_rot

    def make_filename(self, folder, extension):
        return os.path.join(folder, self.name + extension)

    def read_lines(self, folder="./temp/"):
        if self.simulation_method == "pickett":
            catfile = self.make_filename(folder, '.cat')
            self.sim_lines = pickett.load_cat(catfile)

    def run_simulation(self, folder="./temp/"):
        if self.simulation_method == "pickett":
            infilename = self.make_filename(folder, '')
            spcatname = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spcat")
            a = subprocess.Popen("%s %s" % (spcatname, infilename), stdout=subprocess.PIPE, shell=True)
            a.wait()  # a.stdout.read() seems to be best way to get SPCAT to finish. I tried .wait(), but it outputted everything to screen

    def simulate(self, folder="./temp/", threshold=-15.0):
        self.write_params(folder, threshold)
        self.run_simulation(folder)
        self.read_lines(folder)

    def write_params(self, folder="./temp/", threshold=-15.0):
        if self.simulation_method == "pickett":
            if not os.path.exists(folder):
                os.makedirs(folder)
            intfile = self.make_filename(folder, '.int')
            varfile = self.make_filename(folder, '.var')
            pickett.save_var(varfile, self)
            pickett.save_int(intfile, self, inten=threshold)

    def read_params(self, catID, folder="./temp/"):

        if self.simulation_method == "pickett":
            varfile = self.make_filename(folder, '.var')
            if varfile:
                pickett.load_var(varfile, self)

            parfile = self.make_filename(folder, '.par')
            if parfile:
                pickett.load_par(parfile, self)

