import matplotlib.pyplot as plt
import numpy as np
import sys

cache_lines = 32768
line_bytes = 64
colour_map = 'inferno'
filename = sys.argv[1]
section_min = 0
section_max = 500

with open(filename, 'rb') as f:
    data = np.fromfile(f, dtype='<u8', count=line_bytes*cache_lines)
    orig_array = np.reshape(data, [cache_lines, line_bytes])
    split_array = np.vsplit(orig_array, 16) # Split into 16 arrays for easier viewing
    section_array = orig_array[section_min:section_max][:] # Get rows 0 through 200 and all of the colums

    # get our minimum and maximum values for the colourmap
    min_val = np.amin(orig_array)
    max_val = np.amax(orig_array)
    # print('{} {}'.format(min_val, max_val))

    # print the entire cache
    # create the subplots from the data
    fig_0, axes_0 = plt.subplots(ncols=16, sharey=True)
    for i in range(len(split_array)):
        axes_0[i].imshow(split_array[i], cmap=colour_map, interpolation='none', aspect='auto', vmin=min_val, vmax=max_val)
        # add a heatmap for each cache division
        im_0 = axes_0[i].imshow(split_array[i], cmap=colour_map, interpolation='none', aspect='auto', vmin=min_val, vmax=max_val)
        # modify the x-ticks
        if i == 0:
            axes_0[i].set_xticks([0,32,64])
        else:
            axes_0[i].set_xticks([32,64])
        # modify the y-ticks
        axes_0[i].set_yticks(np.arange(0, len(split_array[0]), 200))
        # remove ticks for all plots except the first one
        if i != 0:
            axes_0[i].yaxis.set_ticks_position('none')
    # add an axe for the colourbar and put it to the right of the plot
    colour_bar_axe_0 = fig_0.add_axes([0.92,0.15,0.01,0.7])
    # show colourbar
    fig_0.colorbar(im_0, cax=colour_bar_axe_0)
    # adjust subplot margins
    plt.subplots_adjust(left=0.075, bottom=0.075, right=None, top=None, wspace=0.025, hspace=None)
    # show the plot
    fig_0.show()

    # show an interesting section of the cache
    fig_1 = plt.figure()
    # add the interesting section array
    im_1 = fig_1.gca().imshow(section_array, cmap=colour_map, interpolation='none', aspect='auto', vmin=min_val, vmax=max_val)
    # modify the x-ticks
    fig_1.gca().set_xticks(np.arange(0, 64+1, 4))
    # modify the y-ticks
    fig_1.gca().set_yticks(np.arange(0, len(section_array), 50))
    # add an axe for the colourbar and put it to the right of the plot
    colour_bar_axe_1 = fig_1.add_axes([0.92,0.15,0.01,0.7])
    # show colourbar
    fig_1.colorbar(im_1, cax=colour_bar_axe_1)
    # adjust subplot margins
    plt.subplots_adjust(left=0.075, bottom=0.075, right=None, top=None, wspace=0.05, hspace=None)
    fig_1.show()

    # wait for user input
    input()