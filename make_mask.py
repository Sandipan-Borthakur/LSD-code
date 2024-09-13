import specpolFlow as pol


LineList_file_name = 'data/t9000g40.dat'
wlStart,wlEnd = 480.,800.
Mask_file_name = f't9000g40_depth0.02_{wlStart}-{wlEnd}.mask'
Clean_Mask_file_name = f't9000g40_depth0.02_{wlStart}-{wlEnd}_clean.mask'
# mask_clean = pol.make_mask(LineList_file_name, outMaskName=Mask_file_name,
#                            depthCutoff = 0.02, atomsOnly = True,wlStart=wlStart,wlEnd=wlEnd)

pol.cleanMaskUI(Mask_file_name,'zeeman_lsd/t9000g40_snr-300.synobsspec.err',Clean_Mask_file_name)