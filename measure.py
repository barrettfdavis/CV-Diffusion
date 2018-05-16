"""
Barrett Davis
BME 306 Module 1
Diffusion Check
"""
#Import Libraries

import cv2
import polar as pc
import numpy as np
import glob
from matplotlib import pyplot as plt

def px2diff(l,cal,t=50*60):
    #this converts pixels to diffusivity
    return [((i/(2*cal))**2)/t for i in l]

def px2dist(l,cal):
    #this converts pixels to distance
    return [i/cal for i in l]

#this just readies files for outputing results
outF = open('YOUR OUTPUT.TXT GOES HERE','w')
verboseF = open('YOUR VERBOSEOUTPUT.TXT GOES HERE','w')

sstv = 10 #defines the sensitivity of check
trim = 0 #defines percentages trimmed from each end
verbose,stats = [],[] # defines output arrays

#these are px-cm calibration values for input photos
calFile =[] # YOUR CSVs go here

numF = -1
#iterates through pre-processed photos
for filename in sorted(glob.glob('YOUR FOLDER GOES HERE')):
    numF+=1

    #this handles exceptions from dye cross contamination
    #(e.g. when blue dye splashed on red dye test samples)
    #if filename[18:] in('MSR13.png'):grad=1
    #else:grad=2

    print('Parsing ', filename[18:], '...') # status output

    im = cv2.imread(filename); shape = im.shape #read in image
    vR = shape[0]; vTheta = shape[1] # get image dimensions

    centers = np.unique(im); sorted(centers); # define colors in image and sort

    storage = [[None for x in range(0,2)] for y in range(0,vTheta)]

    for theta in range(0,vTheta-1):
        for count,r in enumerate(range(sstv,vR)): #check for start of gradient
            if all(im[(r-sstv):r,theta,0] == centers[grad]):
                storage[theta][0] = r-sstv
        for f in range((count-sstv),vR): #check for end of gradient
            if not any(im[(f-sstv):f,theta,0] == centers[grad]):
                storage[theta][1] = f
                continue # move onto next column

    temp = []
    for theta in range(0,vTheta):
        #remove any columns that did not have the dye diffusion
        if not(None in storage[theta]):
            #find length of diffusion length
            temp.extend([storage[theta][1]-storage[theta][0]])

    #convert pixel length to diffusivity and trim upper and lower 10% of values
    verbose.append(sorted(px2diff(temp,calFile[numF])))
    #verbose.append(sorted(px2dist(temp,calFile[numF])))
    del verbose[numF][:int(len(verbose[numF])*trim)] #remove last %trim
    del verbose[numF][0:int(len(verbose[numF])*trim)] #reomve first %trim

    #take the mean and standard deviation of the counted pixels
    stats.append([len(verbose[numF]),np.mean(verbose[numF]),np.std(verbose[numF])])

    #Output to high level and verbose .txt files
    print(filename[18:23]+',',' %d, %0.4e, %0.4e'%(len(verbose[numF]),stats[numF][1],stats[numF][2]),file=outF)
    print(str(verbose[numF]).strip('[]'),file=verboseF)
