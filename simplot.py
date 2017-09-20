#-----------------------------------------------------------------------
from task_LoadASCIIFile import LoadASCIIFile;
from task_myXCLASS import myXCLASS;
from task_myXCLASSPlot import myXCLASSPlot;
from datetime import datetime;
import termcolor;
import shutil, os

def plot(expdata, modeldata, config, TransEnergies, xl, xh):
    if(config.PlotTitle == ""):
        config.PlotTitle = default_title();
    
    if(not modeldata is None and not expdata is None):
        ymin = min(min(expdata[:, 1]), min(modeldata[:, 1]))
        ymax = max(max(expdata[:, 1]), max(modeldata[:, 1]))
        yh = ymax + (ymax - ymin) * 0.2
        yl = ymin # if abs(ymin / ymax) < 0.1 else ymin - (ymax - ymin) * 0.2
    elif(not expdata is None):
        yl = min(expdata[:, 1]) * 1.2;
        yh = max(expdata[:, 1]) * 1.2;
    elif(not modeldata is None):
        yl = min(modeldata[:, 1]) * 1.2;
        yh = max(modeldata[:, 1]) * 1.2;  
        expdata = []
    else:
        return;
        
    LegendFlag = True;
    SaveFigureFile = "";
    myXCLASSPlot(expdata, modeldata, TransEnergies, config.RestFreq, \
                config.vLSR, config.MinIntensity, xl, xh, yl, yh, \
                config.PlotTitle, LegendFlag, SaveFigureFile);

def simplot(config):

    expdata = None
    if (config.expdata != ''):      # load expdata
        try:
            expdata = LoadASCIIFile(config.expdata, config.numHeaderLines, config.RestFreq, config.vLSR);
        except:
            expdata = None
            
    if(not expdata is None):            # scale and trim expdata
        indices = (expdata[:,1] < 0);
        if(config.flagExpDataNotLessZero):
            expdata[indices, 1] = 0; 
        if(config.expDataScaleFactor != 1.0):
            expdata[:, 1] = expdata[:, 1] * config.expDataScaleFactor;
        if(config.expDataOffset != 0.0):
            expdata[:, 1] = expdata[:, 1] + config.expDataOffset;        

    if config.freq_range is None:   # get range
        if expdata is None:
            print(termcolor.critical("\nIf no expdata supplied, please set config.freq_range!\n"));
            return
        else:
            xl = min(expdata[:, 0]);
            xh = max(expdata[:, 0]);
    else:
        xl = config.freq_range[0];
        xh = config.freq_range[1];

    if config.stepOverride is None: # get step
        if expdata is None:
            print(termcolor.critical("\nIf no expdata supplied, please set config.stepOverride!\n"));
            return
        else:
            step = max(abs(expdata[1:-1, 0] - expdata[0:-2, 0]))
    else:
        step = config.stepOverride
            
    
    modeldata = [];
    TransEnergies = [];
    try:                            # simulate overlay   
        (modeldata, TransEnergies) = simulate(config, xl, xh, step);
    except:
        modeldata = []
        TransEnergies = []
        
    if(modeldata == []):  
        print(termcolor.warning("\nNo simulation results.\n"));
        
    plot(expdata, modeldata, config, TransEnergies, xl, xh)    

    
def simulate(sp, FreqMin, FreqMax, FreqStep):
    # create a synthetic spectra with myXCLASS task
    iso_flag = (sp.iso_in != '')
    modeldata, log, TransEnergies, IntOptical, JobDir = myXCLASS(
                                        FreqMin, FreqMax, FreqStep, \
                                        sp.TelescopeSize, sp.Inter_Flag, \
                                        sp.t_back_flag, sp.tBack, \
                                        sp.tslope, sp.nH_flag, sp.N_H, \
                                        sp.beta_dust, sp.kappa_1300, \
                                        sp.molfit, \
                                        iso_flag, sp.iso_in, \
                                        sp.RestFreq, sp.vLSR);
     # copy new files 
    to_path = os.path.basename(os.path.normpath(JobDir))
    shutil.copytree(JobDir, to_path)
 
    return (modeldata, TransEnergies);

def default_title():
    return 'Spectrum at ' + datetime.now().strftime('%Y-%m-%d %H:%M');

    
    
