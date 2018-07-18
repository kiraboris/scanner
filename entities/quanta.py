
from werkzeug.datastructures import MultiDict

#
# Functions to operate on "quantum numbers" for optimization purposes
#


def qid(q1, q2=None):
    """
       create hashable quantum IDs used for dictionary lookup.
       q1, q2 are DICTS like also in other methods
    """
    if q2 is None:
        return frozenset(q1.items())
    else:
        return frozenset(q1.items()), frozenset(q2.items())


def qdict(entries):
    """
        Uses qid() to make a lookup dictionary
        entries is an iterable of Line of State instances
    """
    result = MultiDict()
    for e in entries:
        result.add(e.qid(), e)

    return result


def qtransform(self, entries, func_transform):
    """
        Executes func_transform on each entry in
        entries: an iterable of Line of State instances
    """
    for entry in entries:
        if hasattr(entry, "q"):
            entry.q = func_transform(entry.q)

        elif hasattr(entry, "q_upper") and hasattr(entry, "q_lower"):
            entry.q_upper = func_transform(entry.q_upper)
            entry.q_lower = func_transform(entry.q_lower)


