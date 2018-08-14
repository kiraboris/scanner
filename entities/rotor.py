

class RotorType:
    lin = 1
    sym = 2
    asym = 3


class RotorParameter(object):
    """Rotor Hamiltonian expansion parameter (e.g. B, D) as in CDMS"""
    def __init__(self, code=None, value=None, error=None, flag_fit=True):
        self.code = code
        self.value = value
        self.error = error
        self.flag_fit = flag_fit
        self.flag_enabled = True


class Rotor(object):
    def __init__(self, name=None):
        self.type = RotorType.asym
        self.name = name
        self.params = {}
        self.flag_wavenumbers = False

        self.extended = {} # additional information

        self.mu_A = None
        self.mu_B = None
        self.mu_C = None

        self.exp_lines = []  # assignment
        self.sim_lines = []  # passed from quantum simulation to plot simulation
        self.flag_changed = False

    def param(self, name):
        try:
            return self.params[name]
        except KeyError:
            return self.add_param(name)

    def add_param(self, name, **kwargs):
        new_par = RotorParameter(**kwargs)
        self.params[name] = new_par
        return new_par

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