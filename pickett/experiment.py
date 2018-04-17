
from .entities import Line
from .ranges import Ranges


class Experiments:

    def __init__(self):
        self.__ranges = []
        self.__lines = []

    def add_data_to(self, number_of_experiment, arrays):

        self.__ranges[number_of_experiment].add(arrays)

    def add_experiment(self, arrays):

        self.__ranges.append(Ranges(arrays))