
from entities.rotor import RotorType


class SimulationParams:
    def __init__(self, sigma=None, resolution=None, min_freq=None, max_freq=None, threshold=None, intensity_factor=None):
        self.intensity_factor = intensity_factor
        self.resolution = resolution
        self.threshold = threshold  # minumum intensity in Pickett units
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.x_unit_name = 'MHz'
        self.sigma = sigma
        self.flag_Atype = True
        self.flag_Btype = True
        self.flag_Ctype = True
        self.J_min = 0
        self.J_max = 50
        self.Ka_min = 0
        self.Ka_max = 50
        self.Kc_min = 0
        self.Kc_max = 50

    def set(self, sigma=None, resolution=None, min_freq=None, max_freq=None, threshold=None, intensity_factor=None,
                  flag_Atype=None, flag_Btype=None, flag_Ctype=None, J_min=None, J_max=None,
                  Ka_min=None, Ka_max=None, Kc_min=None, Kc_max=None):
        if intensity_factor:
            self.intensity_factor = intensity_factor
        if resolution:
            self.resolution = resolution
        if threshold:
            self.threshold = threshold   # minumum intensity in Pickett units
        if min_freq:
            self.min_freq = min_freq
        if max_freq:
            self.max_freq = max_freq
        if sigma:
            self.sigma = sigma
        if flag_Atype:
            self.flag_Atype = flag_Atype
        if flag_Btype:
            self.flag_Btype = flag_Btype
        if flag_Ctype:
            self.flag_Ctype = flag_Ctype
        if J_min:
            self.J_min = J_min
        if J_max:
            self.J_max = J_max
        if Ka_min:
            self.Ka_min = Ka_min
        if Ka_max:
            self.Ka_max = Ka_max
        if Kc_min:
            self.Kc_min = Kc_min
        if Kc_max:
            self.Kc_max = Kc_max

    def set_from_ui_dict(self, info):
        try:
            self.intensity_factor = float(info['Y Factor'].strip().split()[0])
        except:
            pass
        try:
            self.threshold = float(info['Y Threshold'].strip().split()[0])
        except:
            pass
        try:
            self.sigma = float(info['Sigma'].strip().split()[0])
        except:
            pass
        try:
            self.flag_Atype = info['A-type']
        except:
            pass
        try:
            self.flag_Btype = info['B-type']
        except:
            pass
        try:
            self.flag_Ctype = info['C-type']
        except:
            pass
        try:
            self.J_min = int(info['J min'].strip().split()[0])
        except:
            pass
        try:
            self.J_max = int(info['J max'].strip().split()[0])
        except:
            pass
        try:
            self.Ka_min = int(info['Ka min'].strip().split()[0])
        except:
            pass
        try:
            self.Ka_max = int(info['Ka max'].strip().split()[0])
        except:
            pass
        try:
            self.Kc_min = int(info['Kc min'].strip().split()[0])
        except:
            pass
        try:
            self.Kc_max = int(info['Kc max'].strip().split()[0])
        except:
            pass


    def make_ui_dict(self, rotor):
        info = {}
        info['Y Factor'] = str(self.intensity_factor)
        info['Y Threshold'] = str(self.threshold) + " PU"
        info['Sigma'] = str(self.sigma) + " " + str(self.x_unit_name)
        if rotor.mu_A:
            info['A-type'] = self.flag_Atype
        if rotor.mu_B:
            info['B-type'] = self.flag_Btype
        if rotor.mu_C:
            info['C-type'] = self.flag_Ctype
        #info['J min'] = str(self.J_min)
        info['J max'] = str(self.J_max)
        if rotor.type == RotorType.asym:
            #info['Ka min'] = str(self.Ka_min)
            info['Ka max'] = str(self.Ka_max)
            #info['Kc min'] = str(self.Kc_min)
            info['Kc max'] = str(self.Kc_max)
        return info
