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
        self.path = path; self.file = file; self.read()
        
    def read(self):
        if self.file == "*.hdf5":
            print("No se ha hecho esta parte")
        else:
            self.data = np.genfromtxt(str(self.path+self.file), usecols = self.cols)#, names=True)   
            #self.data = np.array([list(row) for row in data])#para poder hacer slicing
            
    def halo_info(self, index, info=False): 
        self.hinfo = self.data[index]
        return(self.hinfo)

#cinematica entre DOS halos
class kinetic:                                   
    
    def __init__(self, halo1, halo2):                       #halo1 y halo22 son objetos de read_file (halo_info)  
        self.halo1 = halo1; self.halo2 = halo2     

    def distance(self): 
        posA = self.halo1[4:]; posB = self.halo2[4:]
        return(np.linalg.norm(posA-posB))
    
    #def velocity(self, , halo2): 
        #return(np.linalg.norm(halo1-halo2))
    

#=======================================================================================================
#if __name__ == '__main__':
    path = 'DATA/'; file ='sussing_125.z0.000.AHF_halos'
    sussing_125 = read_file(path, file)

    #histograma 2D del N. estructuras vs la masa:
    datos = sussing_125.data[sussing_125.data[:,0] == 0] 

    ejeX = datos[:,2]; ejeY = datos[:,1]   #Solo datos positivos
    nz = (ejeX>0)&(ejeY>0)

    H, xedges, yedges = np.histogram2d(np.log10(ejeX[nz]), 
                                       ejeY[nz], bins=100)
    
    #enmascara el histograma (centra cada bin)
    H = np.ma.masked_where(H<=0, H)
    x = (xedges[1:]+xedges[:-1])/2
    y = (yedges[1:]+yedges[:-1])/2

    #Escritura de archivo, primero H y luego los edges: 
    np.savetxt('out_data/H_data.csv', H.flatten(), delimiter=',', fmt='%f', header='H')
    np.savetxt('out_data/edges_data.csv', np.column_stack((xedges, yedges)), delimiter=',', fmt='%f', header='xedges,yedges')

    # Grafico con bines: 
    fig, ax = plt.subplots(1,1, figsize=(4, 4))
    X,Y = np.meshgrid(x,y)
    hist2D = H.T/(xedges[1]-xedges[0])/(yedges[1]-yedges[0])
    
    cs = ax.imshow(H.T, origin="lower", cmap=cm.viridis, 
                   norm=colors.LogNorm(vmin=1),
                   extent=[xedges[0], xedges[-1], yedges[0],yedges[-1]], 
                   aspect='auto', interpolation='nearest') 

    plt.yscale('log'); 
    ax.set_xlabel(r'log$_{10}$(M$_{halo}$[$M_{0}h^{-1}$])')
    ax.set_ylabel("Number of subsetructures")
    plt.tight_layout()
    plt.savefig("plot/hist2D.pdf")


