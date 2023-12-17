import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams, colors, ticker, cm

#leer archivo:
class read_file: 

    def __init__(self, path, file, columns=None):
        if columns is not None:
            self.cols = columns
        else:
            #self.cols     = [0, 1, 2, 3, 5, 6, 7]        #ID, hosthalo, substruc, masa y posiciones xyz
            self.cols      = [1, 2, 3]                    #solo N. de sub y masa para el plot 2D.
        self.path = path; self.file = file; 
        self.read()

    def read(self):
        data = []
        if self.file == "*.hdf5":
            print("No se ha hecho esta parte")
        else:
            with open(self.path + self.file, 'r') as file:
                for line in file:
                    split_line = line.split()  # Asumiendo que los datos están separados por espacios
                    try:
                        # Seleccionar solo las columnas deseadas y convertirlas a float
                        selected_data = [float(split_line[i]) for i in self.cols]
                        data.append(selected_data)
                    except (ValueError, IndexError):
                        # Manejar posibles errores de conversión o índices incorrectos
                        continue
        self.data = np.array(data)
        #return np.array(self.data)
                
    def halo_info(self, index, info=False): 
        self.hinfo = self.data[index]
        return(self.hinfo)

#cinematica entre DOS halos
'''class kinetic:                                   
    
    def __init__(self, halo1, halo2):                       #halo1 y halo22 son objetos de read_file (halo_info)  
        self.halo1 = halo1; self.halo2 = halo2     

    def distance(self): 
        posA = self.halo1[4:]; posB = self.halo2[4:]
        return(np.linalg.norm(posA-posB))
'''    
    #def velocity(self, , halo2): 
        #return(np.linalg.norm(halo1-halo2))
    

#=======================================================================================================
if __name__ == '__main__':
    path = 'DATA/'; file = 'sussing_125.z0.000.AHF_halos'
    sussing_125 = read_file(path, file)

    # Histograma 2D del N. estructuras vs la masa:
    datos = sussing_125.data[sussing_125.data[:, 0] == 0]

    ejeX = datos[:, 2]  # Solo datos positivos
    ejeY = datos[:, 1]
    nz = (ejeX > 0) & (ejeY > 0)

    # Convertir a escala logarítmica
    ejeY_log = np.log10(ejeY[nz])
    ejeX_log = np.log10(ejeX[nz])

    # Crear histograma 2D
    H, xedges, yedges = np.histogram2d(ejeX_log, ejeY_log, bins=100)

    # Gráfico con bines:
    fig, ax = plt.subplots(1, 1, figsize=(5, 4))

    X, Y = np.meshgrid(xedges, yedges)
    H_masked = np.ma.masked_where(H == 0, H)  # Mascarar los valores cero

    pc = ax.pcolormesh(X, Y, H_masked.T, norm=colors.LogNorm(vmin=H_masked.min()+1, vmax=H_masked.max()), cmap=cm.viridis)

    cbar = plt.colorbar(pc, ax=ax, pad=0.02)
    cbar.set_label('Frequency')

    ax.set_xlabel(r'log$_{10}$(M$_{halo}$[$M_{0}h^{-1}$])')
    ax.set_ylabel("log(Number of substructures)")
    plt.tight_layout()
    plt.savefig("plot/hist2Db_log.pdf")

    print('finalicé y todo bien')
