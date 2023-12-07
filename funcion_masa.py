import numpy as np
import matplotlib.pyplot as plt

#leer datos
path = "/data/repository/MDGalaxies/MDPL2"
Mass = np.genfromtxt("/data/repository/MDGalaxies/MDPL2/sussing_125.z0.000.AHF_halos", usecols=[3])

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

#guardar los datos:

with open(phi_masa, 'w') as archivo:
    for d1, d2 in zip(exe_x, fi):
        archivo.write(f'{d1}\t{d2}\n')

#figura:
fig, ax = plt.subplots(1,1, figsize=(4, 4))

ax.plot(exe_x,np.log10(fi), color='C1', label="MDPL2")

ax.set_xlabel(r'$\log_{10}$(M$_{\mathrm{halo}}h^{-1}$[$\mathrm{M}_{\odot}$])')
ax.set_ylabel(r'$\log_{10}(\phi h^{3})$ [Mpc$^{-3}$dex$^{-1}$]')
plt.legend()

plt.tight_layout(); plt.savefig("masa.pdf")



