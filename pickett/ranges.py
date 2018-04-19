
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

            while trav[j] < len(datasets[j]) and datasets[j][trav[j], DIM.X] < x_i:
                trav[j] = trav[j] + 1

            if trav[j] == len(datasets[j]):
                continue # to next j

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

    out = np.column_stack((xvalues, ysumvalues / ynarrays))
    return out


class Ranges:

    def __init__(self, arrays=()):
        """'arrays': list of ndnumpy arrays
            where x axis is 1st column, y axis is last column (as above)"""

        if arrays:
            self.__arrs = self.__merge_overlaps(arrays)
        else:
            self.__arrs = []

    def spread(self):

        return max([np.max(a[:, DIM.Y]) - np.min(a[:, DIM.Y])
                    for a in self.__arrs])

    def add(self, arrays, merge_parameters = None):

        self.__arrs = self.__merge_overlaps(self.__arrs + arrays, merge_parameters)

    @staticmethod
    def __merge_overlaps(arrs, merge_parameters):

        if len(arrs) <= 1:
            return arrs

        result = []

        excluded = set()
        for i,ai in enumerate(arrs):

            if i in excluded:
                continue

            excluded.add(i)

            intersect = [(j,aj) for (j,aj) in enumerate(arrs)
                         if not j in excluded and aj[0, DIM.X] <= ai[-1, DIM.X]]

            if intersect:
                arrs_intersect = [aj for (j,aj) in intersect]
                j_intersect = [j for (j,aj) in intersect]

                result.append(avg_data([ai] + arrs_intersect))
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

    def print(self):

        print(self.export())

    def export(self):
        """convert Ranges to single array, filling gaps with zeros"""

        arrs = sorted(self.__arrs, key = lambda arr: arr[0, DIM.X])

        step = max([max(arr[1:, DIM.X] - arr[:-1, DIM.X]) for arr in arrs])

        if len(arrs) == 1:
            return arrs[0]
        
        result = None
        for i in range(1, len(arrs)):

            if result:
                result = np.vstack((result, arrs[i - 1]))
            else:
                result = arrs[i - 1]

            gap_l = arrs[i-1][-1, DIM.X]
            gap_r = arrs[i][0, DIM.X]

            insert_x = np.arange(gap_l + step, gap_r, step)
            insert_y = np.zeros(len(insert_x))

            insert = np.stack((insert_x, insert_y)).T

            result = np.vstack((result, insert))

        result = np.vstack((result, arrs[1]))

        return result



if __name__ == "__main__":
    """unit test"""

    x1 = np.linspace(1, 10, 10)
    x2 = np.linspace(10, 19, 10)
    x3 = np.linspace(25, 34, 10)
    x4 = np.linspace(5, 14, 10)

    y  = np.linspace(10, 100, 10)

    a1 = np.stack((x1, y)).T
    a2 = np.stack((x2, y)).T
    a3 = np.stack((x3, y)).T
    a4 = np.stack((x4, y)).T

    r = Ranges([a1, a2])
    r.add(a3)
    r.add(a4)

    r.print()
