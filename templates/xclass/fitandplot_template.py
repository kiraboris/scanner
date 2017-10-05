#-----------------------------------------------------------------------
from fitplot import fitplot

class Config: pass 
config = Config()

# input settings
config.freq_range = [330000, 331100]
config.expdata = "data_mean.txt"
config.molfit = "tofit.molfit"
config.iso_in = "isonames_tofit.txt"
config.expDataScaleFactor = (292.0-70.0)/(293.0-77.0)
config.expDataOffset = 0.0
config.numHeaderLines = 0
config.freqInGHz = False

# plot settings
config.flagExpDataNotLessZero = True
config.PlotTitle = ""          # empty value for datetime title 
config.MinIntensity = 1000.0;  # label threshold, big value for no labels
config.stepOverride = None     # uses exp step if None set

# algorighm settings
config.numIterations = 150     # LM only
config.xml = ""                # empty value activates LM

# observation settings
config.t_back_flag = True
config.tBack = 0;
config.tslope = 0;
config.nH_flag = True;
config.N_H = 0.0;
config.beta_dust = 0.0;
config.kappa_1300 = 0.0;
config.Inter_Flag = True;
config.TelescopeSize = 1; #just a small number
config.RestFreq=0;
config.vLSR=0;

# ===
fitplot(config)

