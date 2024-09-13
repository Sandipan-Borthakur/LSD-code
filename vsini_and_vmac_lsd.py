import os
import matplotlib.pyplot as plt
import numpy as np
import LSDpy
import time
from zeeman_python import run

def gen_chisqr_2D(vsini_min,vsini_max,n_vsini,vmac_min,vmac_max,n_vmac,configfile,Mask_file_name,obsspec):
    vsini_arr = np.linspace(vsini_min, vsini_max, n_vsini)
    vmac_arr = np.linspace(vmac_min, vmac_max, n_vmac)

    obsprof = LSDpy.lsd(observation=obsspec, mask=Mask_file_name,
                        outName="", velStart=-200., velEnd=+200.,
                        velPixel=2.2, normDepth=0.2, normLande=1.2, normWave=500., fLSDPlotImg=0)

    obsvel, obsflux, obsfluxerr = obsprof[0], obsprof[1], obsprof[2]
    obsfluxflipped = 1 - obsflux

    chi_sqr = np.zeros((vsini_arr.shape[0], vmac_arr.shape[0]))

    for ivsini, vsini in enumerate(vsini_arr):
        for ivmac, vmac in enumerate(vmac_arr):
            run(configfile=configfile, vsini=vsini, vmac=vmac)
            synthetic_spectrum_file = "/export/borthaku/Codes/ZEEMAN1/plotff1i"

            data = np.loadtxt('plotff1i')
            synwave,synflux = data[:,0]/10,data[:,1]
            np.savetxt('plotff1i',np.c_[synwave,synflux],delimiter=' ',fmt=['%.4f','%.4e'])
            os.system('python3 add-errs-convert.py plotff1i')

            synprof = LSDpy.lsd(observation=synthetic_spectrum_file+".err", mask=Mask_file_name,
                                outName="", velStart=-200., velEnd=+200.,
                                velPixel=2.2, normDepth=0.2, normLande=1.2, normWave=500., fLSDPlotImg=0)


            synvel,synflux = synprof[0],synprof[1]
            synflux = synflux * np.median(obsflux) / np.median(synflux)
            synflux = 1-synflux

            synflux = synflux*max(obsfluxflipped)/max(synflux)
            chi_sqr[ivsini][ivmac] = np.sum((synflux - obsfluxflipped) ** 2 / obsfluxerr**2)/(len(synflux)-1)

            plt.plot(synvel, synflux, 'b')
            plt.plot(obsvel,obsfluxflipped,'r')
            plt.show()

    return vsini_arr,vmac_arr,chi_sqr

vsini_min,vsini_max,n_vsini = 0,20,20
vmac_min,vmac_max,n_vmac = 0,20,20
configfile = 'zeeman_lsd/zeeman_lsd_config'
Mask_file_name = 'zeeman_lsd/t9000g40_depth0.02_480.0-800.0_clean.mask'
obsspec = 'zeeman_lsd/t9000g40_snr-300.synobsspec.err'

starttime = time.time()
vsini_arr,vmac_arr,chi_sqr = gen_chisqr_2D(vsini_min,vsini_max,n_vsini,vmac_min,vmac_max,n_vmac,configfile,Mask_file_name,obsspec)
endtime = time.time()
print(endtime-starttime)
np.savez('zeeman_lsd/chi-sqr-table.npz',chi_sqr=chi_sqr,vsini_arr=vsini_arr,vmac_arr=vmac_arr)

fontsize = 16
fig = plt.figure(figsize=(8,8))
vsini_arr = np.round(vsini_arr,1)
vmac_arr = np.round(vmac_arr,1)
ind = chi_sqr>5
chi_sqr[ind] = 50
plt.imshow(chi_sqr,cmap='gray',origin='lower')
plt.xticks(np.arange(len(vsini_arr)),vsini_arr,fontsize=fontsize)
plt.yticks(np.arange(len(vmac_arr)),vmac_arr,fontsize=fontsize)
cbar = plt.colorbar(fraction=0.046,pad=0.04)
cbar.ax.tick_params(labelsize=fontsize)
cbar.set_label(label='$\chi_{\\nu}^2$', fontsize=16)
plt.xlabel('vsini',fontsize=fontsize)
plt.ylabel('vmac',fontsize=fontsize)
plt.tight_layout()
fig.savefig('zeeman_lsd/chi-sqr_plot.png',dpi=300)
plt.show()

# import LSDpy
# import matplotlib.pyplot as plt
# import numpy as np
# import os
#
# print(os.getcwd())
# obs_observation = 'zeeman_lsd/t9000g40_snr-300.synobsspec.err'
# mask = 'zeeman_lsd/t9000g40_depth0.02.mask'
# obsprof = LSDpy.lsd(observation=obs_observation,mask=mask,outName="",velStart=-100.,velEnd=+100.,
#                  velPixel=2.2,normDepth=0.2,normLande=1.2,normWave=450., fLSDPlotImg=0)
#
# fig,axs = plt.subplots(2,1)
# obsvel,obsflux = obsprof[0],obsprof[1]
#
# syn_observation = 'plot1.err'
# synprof = LSDpy.lsd(observation=syn_observation,mask=mask,outName="",velStart=-100.,velEnd=+100.,
#                  velPixel=2.2,normDepth=0.2,normLande=1.2,normWave=450., fLSDPlotImg=0)
#
# synvel,synflux = synprof[0],synprof[1]
# synflux = synflux*np.median(obsflux)/np.median(synflux)
# synflux = 1-synflux
# obsflux = 1-obsflux
#
# synflux = synflux*max(obsflux)/max(synflux)
# axs[0].plot(obsvel,obsflux,'b')
# axs[0].plot(synvel,synflux,'r')
#
#
# obsdata = np.loadtxt(obs_observation)
# obswave,obsflux = obsdata[:,0],obsdata[:,1]
#
# syndata = np.loadtxt(syn_observation)
# synwave,synflux = syndata[:,0],syndata[:,1]
#
# axs[1].plot(obswave,obsflux,'b')
# axs[1].plot(synwave,synflux,'r')
# plt.show()