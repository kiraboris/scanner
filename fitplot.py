#-----------------------------------------------------------------------
from task_myXCLASSFit import myXCLASSFit;
from time import gmtime, strftime 
from simplot import simplot;
from shutil import copyfile;
import numpy as np;
import termcolor;
import glob
import os;

def fitplot(config):  
    # aliases
    sp = config;
    iso_flag = (sp.iso_in != '');

    # select range if needed
    if(not config.freq_range is None):
        try:
            data = np.loadtxt(config.expdata);
        except:
            data = np.array([])
        
        if sum(data.shape) == 0:
            print(termcolor.critical("\%s empty or could not be loaded.\n" % config.expdata));
            return; 
            
        nl = 0;
        nh = data.shape[0];
        for (i,fr) in enumerate(data[:,0]):
            if(nl == 0 and fr >= config.freq_range[0]):
                nl = i;
            if(nh == data.shape[0] and fr >= config.freq_range[1]):
                nh = i;
               
        config.expdata = config.expdata + '.tmp';
        if(config.expDataScaleFactor != 1.0):
            data[nl:nh, 1] = data[nl:nh, 1] * config.expDataScaleFactor;
        if(config.expDataOffset != 0.0):
            data[nl:nh, 1] = data[nl:nh, 1] + config.expDataOffset;  
            config.expDataOffset = 0.0            
        
        np.savetxt(config.expdata, data[nl:nh, :]);
    
    # optimize from molfit_guess to molfit with myXCLASSFit task
    try:
        newmolfit, modeldata, JobDir =  myXCLASSFit(sp.numIterations, \
                sp.xml, sp.molfit, \
                sp.expdata, sp.TelescopeSize, \
                sp.Inter_Flag, sp.t_back_flag, sp.tBack, sp.tslope, \
                sp.nH_flag, sp.N_H, sp.beta_dust, sp.kappa_1300, \
                iso_flag, sp.iso_in, sp.RestFreq, sp.vLSR);
    except:
        modeldata = np.array([])
        JobDir = ""

    # new molfit and iso
    mlst = glob.glob(JobDir + '*.out.molfit')
    ilst = glob.glob(JobDir + '*isoratios*.out.input')

    if(not mlst or (iso_flag and not ilst)):
        print(termcolor.critical("\nNo fitting result. I am sorry...\n"));
        return;   
    else:
        config.molfit_out = mlst[0]
        config.iso_out = ilst[0]
        
    # copy new files
    cwd = os.getcwd();
    timestamp = "_" + strftime("%Y-%m-%d-%Hh%Mm", gmtime()) if config.outFilesUnique else "";
    
    config.molfit = cwd + '/fitted' + timestamp + '.molfit'
    copyfile(config.molfit_out, config.molfit);
    
    if(iso_flag):
        config.iso_in = cwd + '/fitted_iso' + timestamp + '.txt'
        copyfile(config.iso_out, config.iso_in);    
        
    # simple simulated plot
    simplot(config);
