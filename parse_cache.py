import matplotlib.pyplot as plt
import numpy as np
import sys

cache_lines = 32768
line_bytes = 64

filename = sys.argv[1]

with open(filename, 'rb') as f:
    data = np.fromfile(f, dtype='<u8', count=line_bytes*cache_lines)
    array = np.reshape(data, [cache_lines, line_bytes])
    array = np.vsplit(array, 16) # Split into 16 arrays for easier viewing

    # get our minimum and maximum values for the colourmap
    min_val = np.amin(array)
    max_val = np.amax(array)
    # print('{} {}'.format(min_val, max_val))

    # create the subplots from the data
    fig, axes = plt.subplots(ncols=16, sharey=True)
    for i in range(len(array)):
        axes[i].imshow(array[i], cmap='viridis', interpolation='none', aspect='auto', vmin=min_val, vmax=max_val)
        # add a heatmap for each cache division
        im = axes[i].imshow(array[i], cmap='viridis', interpolation='none', aspect='auto', vmin=min_val, vmax=max_val)
        # modify the x-ticks
        if i == 0:
            axes[i].set_xticks([0,32,64])
        else:
            axes[i].set_xticks([32,64])
        # remove ticks for all plots except the first one
        if i != 0:
            axes[i].yaxis.set_ticks_position('none')

    # add an axe for the colourbar and put it to the right of the plot
    colour_bar_axe = fig.add_axes([0.92,0.15,0.01,0.7])

    # show colourbar
    fig.colorbar(im, cax=colour_bar_axe)

    # adjust subplot margins
    plt.subplots_adjust(left=0.075, bottom=None, right=None, top=None, wspace=0.05, hspace=None)

    plt.show()