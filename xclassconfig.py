#-----------------------------------------------------------------------
# My common XClass/Magix configurations
#  setup flags include {'Alvaro', 'Nadine', 'isofile', 'algofile', 'overwrite'}

class XClassConfig:
    def __init__(self, flags=[]):
        self.RestFreq=0;
        self.vLSR=0;
        self.expDataScaleFactor = 1.0
        self.expDataOffset = 0.0
        self.flagExpDataNotLessZero = True
        self.PlotTitle = ""
        self.freq_range = None
        self.expdata = ""
        self.molfit = "tofit.molfit"
        self.numHeaderLines = 0
        self.MinIntensity = 0.0; 
        self.numIterations = 100 # LM only
        self.xml = ""  # activates LM
        self.outFilesUnique = True
        self.stepOverride = None
        self.iso_in = ""      

        if('Nadine' in flags):
            self.t_back_flag = True
            self.tBack = 0;
            self.tslope = 0;
            self.nH_flag = True;
            self.N_H = 0.0;
            self.beta_dust = 0.0;
            self.kappa_1300 = 0.0;
            self.Inter_Flag = True;
            self.TelescopeSize = 1; #just a small number

        if('Alvaro' in flags):
            self.t_back_flag = True;
            self.tBack = 0;
            self.tslope = 0;
            self.nH_flag = True;
            self.N_H =  3.2E+24;
            self.beta_dust = 0.0;
            self.kappa_1300 = 0.0;
            self.Inter_Flag = True;
            self.TelescopeSize =  0.7; #arcseconds
