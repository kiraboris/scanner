    #-----------------------------------------------------------------------
from task_myXCLASSFit import myXCLASSFit
import numpy as np
import shutil, os
import termcolor
import simplot

def fitplot(config):  
    # aliases    
    sp = config;
    iso_flag = (sp.iso_in != '');

    try:
        data = np.loadtxt(config.expdata);
        config.expdata = config.expdata + '.tmp';
    except:
        data = np.array([])
    
    if sum(data.shape) == 0:
        print(termcolor.critical("\%s empty or could not be loaded.\n" % config.expdata));
        return; 

    if(not config.freq_range is None):            
        nl = 0;
        nh = data.shape[0];
        for (i,fr) in enumerate(data[:,0]):
            if(nl == 0 and fr >= config.freq_range[0]):
                nl = i;
            if(nh == data.shape[0] and fr >= config.freq_range[1]):
                nh = i;
   
    if(config.expDataScaleFactor != 1.0):
        data[nl:nh, 1] = data[nl:nh, 1] * config.expDataScaleFactor;
        config.expDataScaleFactor = 1.0 
    if(config.expDataOffset != 0.0):
        data[nl:nh, 1] = data[nl:nh, 1] + config.expDataOffset;  
        config.expDataOffset = 0.0          
    if(config.freqInGHz == True):
        data[nl:nh, 0] = data[nl:nh, 0] * 1000;  
        config.freqInGHz = False
    
    np.savetxt(config.expdata, data[nl:nh, :]);
    
    # optimize from molfit_guess to molfit with myXCLASSFit task
    try:
        newmolfit, modeldata, JobDir =  myXCLASSFit(sp.numIterations, \
                sp.xml, sp.molfit, \
                sp.expdata, sp.TelescopeSize, \
                sp.Inter_Flag, sp.t_back_flag, sp.tBack, sp.tslope, \
                sp.nH_flag, sp.N_H, sp.beta_dust, sp.kappa_1300, \
                iso_flag, sp.iso_in, sp.RestFreq, sp.vLSR);
    except Exception as e:
        modeldata = np.array([])
        JobDir = ""
        print termcolor.critical(str(e))

    # copy new files and plot
    to_path = os.path.basename(os.path.normpath(JobDir))
    shutil.copytree(JobDir, to_path)
    
    xl = min(data[:, 0]);
    xh = max(data[:, 0]);
    simplot.plot(data, modeldata, config, [], xl, xh)
