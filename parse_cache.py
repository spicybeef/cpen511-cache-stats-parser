import matplotlib.pyplot as plt
import numpy as np

# filename = 'nvmCacheRaw_blackscholes_4K.dat'
filename = 'nvmCacheRaw_blackscholes_16K.dat'
# filename = 'nvmCacheRaw_blackscholes_64K.dat'
# filename = 'nvmCacheRaw_blackscholes_10M.dat'

cache_lines = 32768
line_bytes = 64

with open(filename, 'rb') as f:
    data = np.fromfile(f, dtype='<u8', count=line_bytes*cache_lines)
    array = np.reshape(data, [cache_lines, line_bytes])
    array = np.vsplit(array, 16) # Split into 16 arrays for easier viewing

    fig = plt.figure()
    for i in range(len(array)):
        ax = fig.add_subplot(1, 16, i+1)
        im = ax.imshow(array[i], cmap='viridis', interpolation='none', aspect='auto')
        ax.set_xlim(-0.5, 63.5)
        ax.margins(0, 0)
        ax.axis('off')
    fig.colorbar(im)
    plt.show()