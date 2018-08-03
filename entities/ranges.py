
import numpy as np


class DIM:
    """ndarray dimensions"""
    X = 0
    Y = -1


def interpolate(x1, y1, x2, y2, x):
    assert (x2 >= x >= x1 and x2 > x1)
    y = y1 + (y2 - y1) / (x2 - x1) * (x - x1)
    return y


def _make_xvalues(datasets, flag_fill_gaps=False):
    # datasets must be already sorted here
    default_step = max([max(arr[1:, DIM.X] - arr[:-1, DIM.X]) for arr in datasets])
    xvalues_arrs = []
    prev_a = None
    for a in datasets:
        if flag_fill_gaps and prev_a is not None:
            gap_l = prev_a[-1, DIM.X]
            gap_r = a[0, DIM.X]

            if gap_r > gap_l:
                insert_x = np.arange(gap_l + default_step, gap_r, default_step)
                xvalues_arrs.append(insert_x.reshape((1, -1)))

            prev_a = a

        xvalues_arrs.append(a[:, DIM.X])

    xvalues = np.unique(np.hstack(xvalues_arrs))
    return xvalues


def _special_increase(x):
    if x < 0:
        return 1
    else:
        return x + 1


def _special_initvalue():
    return -1


def avg_data(data, flag_fill_gaps=False):
    """data must be a list of ndarrays
       matched by 1st column (x), averaged by last column (y) (as above)"""

    datasets = [a[a[:, DIM.X].argsort()] for a in data]

    xvalues = _make_xvalues(datasets, flag_fill_gaps)
    ysumvalues = np.zeros(len(xvalues))
    ynarrays = np.zeros(len(xvalues))

    trav = [0] * len(datasets)  # traversion index for each input array
    for (i, x_i) in enumerate(xvalues):
        ynarrays[i] = _special_initvalue()
        ysumvalues[i] = 0
        for j in range(len(trav)):

            while trav[j] < len(datasets[j]) and datasets[j][trav[j], DIM.X] < x_i:
                trav[j] = trav[j] + 1

            if trav[j] == len(datasets[j]):
                continue  # to next j

            x_trav_j = datasets[j][trav[j], DIM.X]
            y_trav_j = datasets[j][trav[j], DIM.Y]

            if x_trav_j == x_i:
                ynarrays[i] = _special_increase(ynarrays[i])
                ysumvalues[i] += y_trav_j

            elif x_trav_j > x_i and trav[j] > 0:
                x_trav_j_minus = datasets[j][trav[j] - 1, DIM.X]
                y_trav_j_minus = datasets[j][trav[j] - 1, DIM.Y]

                ynarrays[i] = _special_increase(ynarrays[i])
                ysumvalues[i] += interpolate(x_trav_j_minus, y_trav_j_minus,
                                             x_trav_j, y_trav_j, x_i)

    out = np.column_stack((xvalues, ysumvalues / ynarrays))
    return out


class Ranges:

    def __init__(self, arrays=()):
        """'arrays': list of ndnumpy arrays
            where x axis is 1st column, y axis is last column (as above)"""

        if arrays:
            self.__arrs = arrays
        else:
            self.__arrs = []

        self.__invisible_indexes = set()

    def spread_y(self):

        return max([np.max(a[:, DIM.Y]) - np.min(a[:, DIM.Y])
                    for a in self.__arrs])

    def add(self, arrays):

        self.__arrs = self.__arrs + arrays

    def slices(self, step, span, nmipmap=0):
        """'span': size of slice,
           'step': offset of each next slice from begin of previous one"""

        a = self.export()

        left = 0
        right = 0

        xa = a[:, DIM.X]

        nbins = (((xa[-1] - span / 2) - (xa[0] + span / 2)) / step) * (nmipmap + 1)
        bins = np.arange(xa[0] + span / 2, xa[-1] - span / 2, step)

        for i, x in enumerate(bins):
            while xa[left] <= x - span / 2.0 and left < len(xa)-1: left = left + 1
            while xa[right] < x + span / 2.0 and right < len(xa)-1: right = right + 1

            mleft = left
            mright = right
            for n in range(0, nmipmap + 1):

                yield a[mleft:mright, :], float(i) / nbins

                mleft += int((mright - mleft) / 8)
                mright -= int((mright - mleft) / 8)

    def print(self):
        print(self.export())

    def visible_arrs(self):
        arrs = []
        for i, arr in self.__arrs:
            if i not in self.__invisible_indexes:
                arrs.append(arr)
        return arrs

    def export(self):
        """convert Ranges to single array, filling gaps with zeros"""
        arrs = self.visible_arrs()
        if not arrs:
            return None
        elif len(arrs) == 1:
           return arrs[0]
        else:
            return avg_data(arrs, flag_fill_gaps=True)

    def add_data_files(self, names):
        newNames = []
        arrs = []
        for name in names:
            try:
                arr = np.loadtxt(name)
                arrs.append(arr)
                newNames.append(name)
            except:
                # who the heck would care?
                pass
        if arrs:
            self.add(arrs)
        return newNames

    def deserialize(self, stream):
        return True

    def remove(self, index):
        if index < len(self.__arrs):
            del self.__arrs[index]
            self.__invisible_indexes.remove(index)
            return True
        else:
            return False

    def set_visibility(self, index, flag):
        if flag:
            self.__invisible_indexes.add(index)
        else:
            self.__invisible_indexes.remove(index)


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
    r.add([a3])
    r.add([a4])

    r.print()
