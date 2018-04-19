
from glob import glob

from . import pickett


def glob_file(catID, folder, extension):

    return None


class Rotor(object):

    def __init__(self):

        self.params = {}
        self.symmetry = RotorSymmetry()

    def param(self, name):

        return self.params[name]

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

        Q_rot = ((5.3311 * 10 ** (6)) * (T ** (1.5)) * Q_rot_base)

        return Q_rot

    def update_params(self, catID, folder):

        varfile = glob_file(catID, folder, '.var'):
        if varfile:
            pickett.load_var(self)

        parfile = glob_file(catID, folder, '.var'):
        if parfile:
            pickett.load_par(self)

