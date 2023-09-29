import numpy as np
import h5py

data = 'DATA/sussing_000.z14.949.AHF_halos'

f = np.genfromtxt(data, dtype = None)
print(f)
