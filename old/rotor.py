
import os, os.path
import subprocess

from pickett_old import pickett
from pickett_old import entities

# *** quantum rotor model ***


class RotorSymmetry:

    def __init__(self):
        # sample defaults
        self.type = "asym"
        self.group = 'C1'
        self.representation = 'prolate'
        self.reduction = 's'
        self.Qdegree = 3   # used in Q() calculation
        self.spin_degeneracy = 1  # for all spins, in Pickett format





class Rotor(object):

    def __init__(self, name="noname"):

        self.name = name
        self.params = {}
        self.symmetry = RotorSymmetry()
        self.sim_lines = []
        self.simulation_method = "pickett"
        self.flag_wavenumbers = False
        self.mu_A = None
        self.mu_B = None
        self.mu_C = None





