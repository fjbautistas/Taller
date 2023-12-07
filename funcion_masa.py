import numpy as np
import matplotlib.pyplot as plt

#leer datos
path = "DATA/"
Mass = np.genfromtxt("DATA/sussing_125.z0.000.AHF_halos", usecols=[3])

#constantes e histograma 
n_bins         = 15; h = 0.7; cte = 1000*h      # Mpc/h ojo h=0.7
counts, edges  = np.histogram(np.log10(Mass), bins=n_bins)

#phi:
def phi(D_n, edges, constante):
    width = edges[1]-edges[0]                   # Anchos constantes?
    fi = (D_n/(width))/(constante**3)
    return fi

fi    = phi(counts, edges, cte)

exe_x = np.linspace(np.log10(min(Mass)), 
                    np.log10(max(Mass)), num=n_bins)

#datos:
csv_data = np.column_stack((exe_x, np.log10(fi)))
np.savetxt('out_data/datos_masa.csv', csv_data, delimiter=',', header='exe_x,log10(fi)', comments='')

#figura:
fig, ax = plt.subplots(1,1, figsize=(4, 4))

ax.plot(exe_x,np.log10(fi), color='C1', label="MDPL2")

ax.set_xlabel(r'$\log_{10}$(M$_{\mathrm{halo}}h^{-1}$[$\mathrm{M}_{\odot}$])')
ax.set_ylabel(r'$\log_{10}(\phi h^{3})$ [Mpc$^{-3}$dex$^{-1}$]')
plt.legend()

plt.tight_layout(); plt.savefig("masa.pdf")



