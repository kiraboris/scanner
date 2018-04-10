
import numpy as np


class DIM:
    """ndarray dimensions"""
    X = 0
    Y = -1

def interpolate(x1, y1, x2, y2, x):
    assert (x2 >= x >= x1 and x2 > x1)
    y = y1 + (y2 - y1) / (x2 - x1) * (x - x1)
    return y

def avg_data(data):
    """data must be a list of ndarrays
       matched by 1st column (x), averaged by last column (y) (as above)"""

    datasets = [a[a[:, DIM.X].argsort()] for a in data]

    set_xvalues = set()  # uniqueness needed here
    for a in datasets:
        for x in a[:, DIM.X]:
            set_xvalues.add(x)

    xvalues = sorted(list(set_xvalues))
    ysumvalues = np.zeros(len(xvalues))
    ynarrays   = np.zeros(len(xvalues))

    trav = [0] * len(datasets)  # traversion index for each input array
    for (i, x_i) in enumerate(xvalues):
        for j in range(len(trav)):

            while datasets[j][trav[j], DIM.X] < x_i:
                trav[j] = trav[j] + 1

            x_trav_j = datasets[j][trav[j], DIM.X]
            y_trav_j = datasets[j][trav[j], DIM.Y]

            if x_trav_j == x_i:
                ysumvalues[i] += y_trav_j
                ynarrays[i] += 1
            elif x_trav_j > x_i and trav[j] > 0:
                x_trav_j_minus = datasets[j][trav[j] - 1, DIM.X]
                y_trav_j_minus = datasets[j][trav[j] - 1, DIM.Y]

                ynarrays[i] +=1
                ysumvalues[i] += interpolate(x_trav_j_minus, y_trav_j_minus,
                                             x_trav_j, y_trav_j, x_i)
            else:
                pass

    out = np.column_stack((xvalues, ysumvalues / ynarrays))
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

        self.__arrs = self.__merge_overlaps(self.__arrs + arr)

    @staticmethod
    def __merge_overlaps(arrs):

        result = []

        excluded = set()
        for i,ai in enumerate(arrs):

            if i in excluded:
                continue

            excluded.add(i)

            intersect = [(aj,j) for (aj,j) in enumerate(arrs)
                         if not j in excluded and aj[0, DIM.X] >= ai[-1, DIM.X]]

            if intersect:
                arrs_intersect = [aj for (aj,j) in intersect]
                j_intersect = [j for (aj, j) in intersect]

                result.append(avg_data(arrs_intersect))
                excluded.update(j_intersect)
            else:
                result.append(ai)

        return result

    def nslices(self, step, span, nmipmap=0):

        nbins = 0
        for a in self.__arrs:
            left = 0
            right = 0

            xa = a[:, DIM.X]

            nbins += (((xa[-1] - span / 2) - (xa[0] + span / 2)) / step) * (nmipmap + 1)

        return int(nbins)

    def slices(self, step, span, nmipmap=0):
        """'span': size of slice,
           'step': offset of each next slice from begin of previous one"""

        for a in self.__arrs:
            left = 0
            right = 0

            xa = a[:, DIM.X]

            bins = np.arange(xa[0] + span / 2, xa[-1] - span / 2, step)

            for x in bins:
                while xa[left] <= x - span / 2.0: left = left + 1
                while xa[right] < x + span / 2.0: right = right + 1

                mleft = left
                mright = right
                for n in range(0, nmipmap + 1):

                    yield a[mleft:mright, :]  # yield spectrum, both DIM.X and DIM.Y

                    mleft += int((mright - mleft) / 4)
                    mright -= int((mright - mleft) / 4)
