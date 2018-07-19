
from enum import Enum


class RotorType(Enum):
    lin = 1
    sym = 2
    asym = 3


class RotorParameter(object):
    """Rotor Hamiltonian expansion parameter (e.g. B, D) as in CDMS"""

    def __init__(self, name, value=1.0, error=None, flag_fit=True):
        self.name = name
        self.value = value
        self.error = error
        self.flag_fit = flag_fit
        self.flag_enabled = True


class Rotor(object):

    def __init__(self, name="noname"):

        self.type = RotorType.asym
        self.name = name
        self.params = {}
        self.flag_wavenumbers = False

        self.extended = {}

        self.mu_A = None
        self.mu_B = None
        self.mu_C = None

    def param(self, name):

        return self.params[name]

    def add_param(self, name, **kwargs):

        self.params[name] = RotorParameter(name, **kwargs)

    def Q(self, T):
        if self.type == RotorType.asym:
            Q_rot_base = (self.param('A').value *
                          self.param('B').value *
                          self.param('C').value) ** (-0.5)
        elif self.type == RotorType.sym:
            Q_rot_base = (self.param('A').value *
                          self.param('B').value ** 2) ** (-0.5)
        else:
            Q_rot_base = 0

        Q_rot = ((5.3311 * 10 ** (6)) * (T ** (1.5)) * Q_rot_base)
        return Q_rot