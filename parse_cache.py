import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import sys

#the following fixes an overflow error when saving figure 3
mpl.rcParams['agg.path.chunksize'] = 10000

cache_lines = 32768
line_bytes = 64
colour_map = 'plasma'
path = sys.argv[1]
section_min = 20400
section_max = 20600
filename = path.split('/')[-1]

show_plots = False
save_plots = True

with open(path, 'rb') as f:
    data = np.fromfile(f, dtype='<u8', count=line_bytes*cache_lines)
    orig_array = np.reshape(data, [cache_lines, line_bytes])
    split_array = np.vsplit(orig_array, 16) # Split into 16 arrays for easier viewing
    section_array = orig_array[section_min:section_max][:] # Get rows 0 through 200 and all of the colums

    # get our minimum and maximum values for the colourmap
    min_val = np.amin(orig_array)
    max_val = np.amax(orig_array)
    # max_val = 100000
    print('{} {}'.format(min_val, max_val))

    # print the entire cache
    # create the subplots from the data
    fig_0, axes_0 = plt.subplots(ncols=16, sharey=True, figsize=(10,5))
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
        # set the title for each cache chunk
        axes_0[i].set_title('+{}'.format(len(split_array[i])*i), fontsize=5)
    # add an axe for the colourbar and put it to the right of the plot
    colour_bar_axe_0 = fig_0.add_axes([0.92,0.15,0.01,0.7])
    # show colourbar
    fig_0.colorbar(im_0, cax=colour_bar_axe_0)
    # adjust subplot margins
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.05, hspace=None)
    # add titles to axes
    fig_0.suptitle('Bit Flip Frequency Heat Map\n' + filename)
    fig_0.text(0.5, 0.04, 'Line Byte', ha='center')
    fig_0.text(0.04, 0.5, 'Cache Line', va='center', rotation='vertical')
    # show the plot
    if show_plots:
        fig_0.show()
    if save_plots:
        fig_0.savefig(filename + '_heat.png', dpi=300)

    # show an interesting section of the cache
    fig_1 = plt.figure(figsize=(10,5))
    # add the interesting section array
    im_1 = fig_1.gca().imshow(section_array, cmap=colour_map, interpolation='none', aspect='auto', vmin=min_val, vmax=max_val)
    # modify the x-ticks
    fig_1.gca().set_xticks(np.arange(0, 64+1, 4))
    fig_1.gca().set_xlim(-0.5, 63.5)
    # modify the y-ticks
    fig_1.gca().set_yticks(np.arange(0, len(section_array), (section_max-section_min) / 10))
    # add titles to axes
    fig_1.gca().set_title('Close-Up of Cache Lines {} to {}\n'.format(section_min, section_max) + filename)
    fig_1.gca().set_ylabel('Offset from {}'.format(section_min))
    fig_1.gca().set_xlabel('Cache Line Byte')
    # add an axe for the colourbar and put it to the right of the plot
    colour_bar_axe_1 = fig_1.add_axes([0.92,0.15,0.01,0.7])
    # show colourbar
    fig_1.colorbar(im_1, cax=colour_bar_axe_1)
    # adjust subplot margins
    plt.subplots_adjust(left=0.075, bottom=0.075, right=None, top=None, wspace=0.05, hspace=None)
    fig_1.show()
    # show the plot
    if show_plots:
        fig_1.show()
    if save_plots:
        fig_1.savefig(filename + '_closeup.png', dpi=300)

    # show a histogram of the byte bit flips
    fig_2 = plt.figure(figsize=(7,5))
    fig_2.gca().hist(data, bins=500)
    fig_2.gca().set_title('Distribution of Byte Bit Flip Frequency\n' + filename)
    fig_2.gca().set_ylabel('Frequency')
    fig_2.gca().set_xlabel('Bit Flips per Cache Bytes')
    fig_2.show()
    # show the plot
    if show_plots:
        fig_2.show()
    if save_plots:
        fig_2.savefig(filename + '_hist.png', dpi=300)

    # show a 2D plot of the cache byte bit flips
    fig_3 = plt.figure(figsize=(7,5))
    fig_3.gca().plot(data)
    fig_3.gca().set_title('Bit Flips per Cache Byte\n' + filename)
    fig_3.gca().set_ylabel('Number of Bit Flips')
    fig_3.gca().set_xlabel('Cache Byte')
    fig_3.show()
    # show the plot
    if show_plots:
        fig_3.show()
    if save_plots:
        fig_3.savefig(filename + '_scatter.png', dpi=300)

    # wait for user input
    if show_plots:
        input()