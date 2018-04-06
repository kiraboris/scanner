
import numpy as np


class DIM:
    """ndarray dimensions"""
    X = 0
    Y = -1

def interpolate(x1, y1, x2, y2, x):
    assert (x2 >= x >= x1 and x2 > x1)
    y = y1 + (y2 - y1) / (x2 - x1) * (x - x1)
    return y

def match_data(data):
    """data must be a list of ndarrays
       matched by 1st column (x), averaged by last column (y) (as above)"""

    datasets = [a[a[:, DIM.X].argsort()] for a in data]

    xl = max([a[0, DIM.X] for a in datasets])
    xh = min([a[-1, DIM.X] for a in datasets])
    assert (xh >= xl)  # ensure common range is found

    set_xvalues = set()
    for a in datasets:
        for x in a[:, DIM.X]:
            if xh >= x >= xl:
                set_xvalues.add(x)

    xvalues = sorted(list(set_xvalues))
    yvalues = np.empty((len(xvalues), len(datasets)))

    trav = [0] * len(datasets)
    for (i, x_i) in enumerate(xvalues):
        for j in range(len(trav)):

            while datasets[j][trav[j], DIM.X] < x_i:
                trav[j] = trav[j] + 1

            x_t_j = datasets[j][trav[j], DIM.X]
            y_t_j = datasets[j][trav[j], DIM.Y]

            if x_t_j == x_i:
                yvalues[i, j] = y_t_j
            else:  # only x_t_j > x with trav[j] > 0
                x_t_j_minus = datasets[j][trav[j] - 1, DIM.X]
                y_t_j_minus = datasets[j][trav[j] - 1, DIM.Y]

                yvalues[i, j] = interpolate(x_t_j_minus, y_t_j_minus, x_t_j, y_t_j, x_i)

    out = np.column_stack((xvalues, yvalues))
    return out


class Ranges:

    def __init__(self, arrays=()):
        """'arrays': list of ndnumpy arrays
            where x axis is 1st column, y axis is last column (as above)"""

        self.__arrs = list(arrays)

    def spread(self):

        return max([np.max(a[:, DIM.Y]) - np.min(a[:, DIM.Y])
                    for a in self.__arrs])

    def add(self, arr):

        self.__arrs.append(arr)
        self.__merge_overlaps()

    def __merge_overlaps(self):




    def nslices(self, step, span, nmipmap=0, dim=None):

        nbins = 0
        for a in self.__arrs:
            left = 0
            right = 0

            if dim is None:
                xa = a
            else:
                xa = a[:, DIM.Y]

            nbins += (((xa[-1] - span / 2) - (xa[0] + span / 2)) / step) * (nmipmap + 1)

        return int(nbins)

    def slices(self, step, span, nmipmap=0, dim=None):
        """'span': size of slice,
           'step': offset of each next slice from begin of previous one"""

        for a in self.__arrs:
            left = 0
            right = 0

            if dim is None:
                xa = a
            else:
                xa = a[:, dim]

            bins = np.arange(xa[0] + span / 2, xa[-1] - span / 2, step)

            for x in bins:
                while xa[left] <= x - span / 2.0: left = left + 1
                while xa[right] < x + span / 2.0: right = right + 1

                mleft = left
                mright = right
                for n in range(0, nmipmap + 1):

                    if dim is None:
                        yield a[mleft:mright]
                    else:
                        yield a[mleft:mright, :]

                    mleft += int((mright - mleft) / 4)
                    mright -= int((mright - mleft) / 4)
