import cv2
import numpy as np
from matplotlib import pyplot as plt

def histprint(l,c,lbl,verbose):

    #define upper and lower bound for bins based on max and min
    #values of diffusivity found in verbose output
    bins = np.linspace(min(min(verbose)),max(max(verbose)),50)

    #overlay the given sample outputs onto same axes
    for i in range(0,len(l)):
        #alpha sets transparency
        #color define the colors of the histogram bars
        #label gives legend information
        plt.hist(l[i],bins,alpha=0.5,color=c[i],label=lbl[i])

    plt.legend(loc='upper right')
    plt.xlabel('Diffusivity (cm^2/s)'); plt.ylabel('Frequency')
    plt.show()

with open('YOUR FOLDER HERE') as f:
    #read verbose output text file back in as a list
    verbose = [[float(x.strip(',')) for x in line.split()] for line in f]

blues = ['#0000ff','#4c4cff','#7f7fff'] #arbitrary color values
reds  = ['#b20000','#ff0000','#ff4c4c'] #arbitrary color values

#defining inputs for different histograms
#Lablels (lbl1 and lbl2) based on personal naming conventions of samples
l1,c1,lbl1 = verbose[0:3],blues,['ACB11','ACB12','ACB13']
l2,c2,lbl2 = verbose[9:12],reds,['ACR11','ACR12','ACR13']

#defining input for six different samples
l3 = verbose[9:12]+verbose[49:52]
c3,lbl3 = reds + blues, ['ACR11','ACR12','ACR13','MSB11','MSB12','MSB13']

#print three example histograms on different figures
histprint(l1,c1,lbl1,verbose)
histprint(l2,c2,lbl2,verbose)
histprint(l3,c3,lbl3,verbose)
