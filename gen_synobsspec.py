import os
import matplotlib.pyplot as plt
import numpy as np
from zeeman_python import  run

def gensynspec(configfile,synspecfilename):
    run(configfile=configfile)
    os.system(f'cp /export/borthaku/Codes/ZEEMAN1/plotff1i {synspecfilename}')

def addnoisetospec(flux,snr):
    sig = 1/snr
    gaussian_noise = np.random.normal(1, sig, len(flux))
    flux_noise = flux/gaussian_noise
    return flux_noise

def gensynobsspec(configfile,specfilename,snr,plot=False):
    # gensynspec(configfile,specfilename)
    os.system('./zuc')
    data = np.loadtxt(specfilename)
    wave,flux = data[:,0],data[:,1]
    flux = addnoisetospec(flux,snr)
    wave = wave/10
    np.savetxt(specfilename,np.c_[wave,flux],delimiter=' ',fmt=['%.4f','%.4e'])
    os.system(f'python3 add-errs-convert.py {specfilename}')
    synobsspecfile = specfilename+'.err'
    if plot:
        wave,flux,fluxerr = np.loadtxt(synobsspecfile,unpack=True)
        plt.errorbar(wave,flux,yerr=fluxerr)
        plt.show()
    return synobsspecfile

path = 'plot1'
configfile = 'zeeman_lsd/zeeman_lsd_config'
for snr in [300]:
    synobsspecfile = gensynobsspec(configfile=configfile,specfilename=path,snr=snr,plot=False)

    data = np.loadtxt(synobsspecfile)
    wave,flux,fluxerr = data[:,0]*10,data[:,1],data[:,2]
    w1000filename = synobsspecfile.replace('.err','_w1000.err')
    np.savetxt(w1000filename,np.c_[wave,flux,fluxerr],delimiter=' ',fmt=["%.4f","%.4e","%.4e"])

    os.system(f'cp {synobsspecfile} zeeman_lsd/t9000g40_snr-{snr}.synobsspec.err')
    os.system(f'cp {w1000filename} zeeman_lsd/t9000g40_snr-{snr}_w1000.synobsspec.err')
