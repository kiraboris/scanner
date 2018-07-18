
import copy
from .state import State


class Line(object):
    """Spectroscopic transition as in CDMS;
        has an upper state and a lower state;
        properties follow CDMS convention:
        * E has the meaning of lower state energy
        * g has the meaing of upper state weight
    """

    def __init__(self):
        # states
        self.state_upper = State()
        self.state_lower = State()

        # Frequency of the line (usually in MHz)
        self.freq = None
        self.freq_err = None

        # base10 log of the integrated intensity:
        # * at 300 K in nm2MHz for theo lines
        # * arbitrary units for exp lines
        self.log_I = None
        self.Einstein_A = None

        # extended information
        self.extended = {}

        # pressure broadening dv=p*alpha*(T/296)^delta
        self.pressure_alpha = None
        self.pressure_delta = None

    def copy(self):
        return copy.deepcopy(self)

    def qid(self):
        """docstring"""

        return ((self.state_upper._quanta, self.state_lower._quanta))

    def _get_E(self):
        return self.state_lower.E

    def _set_E(self, x):
        self.state_lower.E = x

    def _get_g(self):
        return self.state_upper.g

    def _set_g(self, x):
        self.state_upper.g = x

    def _get_qu(self):
        return self.state_upper.q

    def _set_qu(self, x):
        self.state_upper.q = x

    def _get_ql(self):
        return self.state_lower.q

    def _set_ql(self, x):
        self.state_lower.q = x

    def _get_fmt(self):
        assert(self.state_upper.int_fmt == self.state_lower.int_fmt)
        return self.state_upper.int_fmt

    def _set_fmt(self, x):
        self.state_upper.int_fmt = x
        self.state_lower.int_fmt = x

    E = property(_get_E, _set_E)
    g = property(_get_g, _set_g)
    q_upper = property(_get_qu, _set_qu)
    q_lower = property(_get_ql, _set_ql)
    int_fmt = property(_get_fmt, _set_fmt)