
import os.path

from entities.rotor import Rotor
import pickett


class Species:
    def __init__(self, filename):
        basepath, extension = os.path.splitext(filename)
        if pickett.is_valid_extension(extension):
            self.worker = pickett

        self.rotor = Rotor()
        self.basepath = basepath
        self.worker.load_rotor(self.rotor, self.basepath)
