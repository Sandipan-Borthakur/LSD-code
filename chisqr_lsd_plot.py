import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import Rbf,interp2d



def gaussian(x, y):
    return np.exp(-0.5 * ((x / 1)**2 + (y / 1)**2))

def interp_ticks_to_vel(vel_arr,num_points):
    ticks = np.arange(len(vel_arr))
    ticks_min,ticks_max = min(ticks),max(ticks)
    vel_arr_min,vel_arr_max = min(vel_arr),max(vel_arr)
    g = np.polyfit(ticks,vel_arr,1)
    f = np.poly1d(g)
    ticks_reduced = np.linspace(ticks_min,ticks_max,num_points)
    vel_arr_reduced = np.linspace(vel_arr_min,vel_arr_max,num_points)
    return ticks_reduced,vel_arr_reduced

fontsize = 16
ticks_length = 10
num_points = 5
path = 'zeeman_lsd/chi-sqr-table.npz'
data = np.load(path)
chisqr = data['chi_sqr']
vsini_arr = data['vsini_arr']
vmac_arr = data['vmac_arr']
vsini_arr = np.round(vsini_arr,1)
vmac_arr = np.round(vmac_arr,1)


rbf = interp2d(vsini_arr,vmac_arr,chisqr,kind='cubic')
vsini_arr_full = np.linspace(min(vsini_arr),max(vsini_arr),1000)
vmac_arr_full = np.linspace(min(vmac_arr),max(vmac_arr),1000)
# vsini_arr_full,vmac_arr_full = np.meshgrid(vsini_arr_full,vmac_arr_full)
chisqr_full = rbf(vsini_arr_full,vmac_arr_full)

# ind = chisqr_full>5
# chisqr_full[ind] = 50

fig = plt.figure(figsize=(8,8))
plt.imshow(chisqr_full,origin='lower',cmap='gray')

ticks_reduced,vsini_arr_reduced = interp_ticks_to_vel(vsini_arr,num_points)
plt.xticks(ticks_reduced,vsini_arr_reduced,fontsize=fontsize)
ticks_reduced,vmac_arr_reduced = interp_ticks_to_vel(vsini_arr,num_points)
plt.yticks(ticks_reduced,vmac_arr_reduced,fontsize=fontsize)

cbar = plt.colorbar(fraction=0.046,pad=0.04)
cbar.ax.tick_params(labelsize=fontsize,axis='both',direction='in',length=ticks_length)
cbar.set_label(label='$\chi_{\\nu}^2$', fontsize=fontsize)
plt.xlabel('vsini',fontsize=fontsize)
plt.ylabel('vmac',fontsize=fontsize)
plt.tick_params(axis='both', direction='in',length=ticks_length,right=True,top=True)
plt.tight_layout()
# fig.savefig('zeeman_lsd/chi-sqr_plot.png',dpi=300)
plt.show()