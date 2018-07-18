
import copy


class State(object):
    """Quantum state as in CDMS"""

    def __init__(self):
        object.__init__(self)

        # energy and weight
        self.E = None
        self.E_err = None
        self.g = None

        # extended information
        self.extended = {}

        # quantum numbers
        self._quanta = frozenset()
        self.int_fmt = None

    def copy(self):
        return copy.deepcopy(self)

    def qid(self):
        """docstring"""

        return self._quanta

    def has_quanta(self, quanta_subset):
        """Checks if state has these quanta as a subset"""

        return all(x in self.q.items()
                   for x in quanta_subset.items())

    def _get_q(self):
        return dict(self._quanta)

    def _set_q(self, dict_x):
        self._quanta = frozenset(dict_x.items())

    q = property(_get_q, _set_q)
