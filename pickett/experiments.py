
from .entities import Line
from .ranges import Ranges
from .peakfinder import AdvancedPeakfinder

class Experiment:

    def __init__(self, ranges, settings, lines):
        self.ranges = ranges
        self.settings = settings
        self.lines = lines

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class Experiments:

    def __init__(self):
        self.__exp = []

    def merge_data_to_experiment(self, number_of_experiment, arrays):

        with self.__exp[number_of_experiment] as exp:
            exp.ranges.add(arrays)
            exp.lines = AdvancedPeakfinder(exp.ranges, exp.settings).find()

    def add_experiment(self, arrays):

        self.__ranges.append(Ranges(arrays))

    def merge_experiments(self, numbers):

        new_arrays = [self.__ranges[i].export() for i in numbers]

        new_ranges = [r for i, r in enumerate(self.__ranges) if not i in numbers]

        new_ranges.append(Ranges(new_arrays))

        self.__ranges = new_ranges

    @staticmethod
    def __extract_lines():
