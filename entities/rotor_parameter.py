
class RotorParameter(object):
    """Rotor Hamiltonian expansion parameter (e.g. B, D) as in CDMS"""

    def __init__(self, name, value=1.0, error=None, flag_fit=True):
        self.name = name
        self.value = value
        self.error = error
        self.flag_fit = flag_fit
        self.flag_enabled = True
