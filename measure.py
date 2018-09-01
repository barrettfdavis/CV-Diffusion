"""
Barrett Davis
CV-Diffusion
2018-08-31
"""
# --------------------------- IMPORT LIBRARIES --------------------------------

import cv2
import glob
import polar as pc
import numpy as np
from matplotlib import pyplot as plt

# --------------------------- USER PARAMETERS ---------------------------------
""" defines system sensitivity to gradient boundaries -- the higher the number
the more pixels needed to constitute a gradient band -- generally the higher
this number the fewer valid end-point measurements there will be """
sstv = 10

"""defines the percentage of data trimmed from upper and lower extremes after
processing -- generally 0.05 to 0.01 is sufficient to remove outliers/noise
without removing valid data points """
trim = 0.05

""" these are px-cm calibration values for your input photos -- currently these
should be included as a comma seperated list. With a minor rewrite one should
be able to automate this given a calibration curve from 5-10 pictures """
calFile = [421.96,517.71,576.63,657.64,657.64,637.02,430.8,486.77,430.8,526.55,535.38,442.59,748.96,782.84,498.56,536.86,588.41,517.71,921.3,489.72,1015.57,887.42,790.21,1056.81,1149.61,1024.41,946.34,1193.8,1050.92,843.23,978.75,410.18,370.41,520.65,1030.3,622.29,654.69,479.41,427.86,466.15,719.5,1245.35,1128.99,738.65,831.45,893.31,519.18,604.61,351.26,497.09,463.21,391.03,312.96,270.25,395.45,449.95,401.34,461.73,455.84,405.76,391.03,439.64,441.11,467.63,408.71,368.94,447]  # YOUR CSVs go here

# ----------------------------- FUNCTIONS--------------------------------------


def px2diff(l, cal, t=50*60):
    # this converts pixels to diffusivity (cm^2/s)
    # the runtime t must be defined in seconds (s)
    return [((i/(2*cal))**2)/t for i in l]


def px2dist(l, cal):
    # this converts pixels to distance
    return [i/cal for i in l]


# ----------------------------- BODY ------------------------------------------

# this just readies files for outputing results
verbose, stats = [], []  # defines output arrays

outF = open('output/gradFronts.txt', 'w')
verboseF = open('output/verboseOutput.txt', 'w')

numF = -1
# iterates through pre-processed photos
for filename in sorted(glob.glob('processed/polars/*')):
    numF += 1

    # this handles exceptions from dye cross contamination
    # (e.g. when blue dye splashed on red dye test samples)
    # if filename[18:] in('MSR13.png'):grad=1
    # else:grad=2

    print('Parsing ', filename[18:], '...')  # status output

    im = cv2.imread(filename); shape = im.shape  # read in image
    vR = shape[0]; vTheta = shape[1]  # get image dimensions

    centers = np.unique(im); sorted(centers);  # define colors in image and sort

    storage = [[None for x in range(0, 2)] for y in range(0, vTheta)]

    for theta in range(0, vTheta-1):
        for count, r in enumerate(range(sstv, vR)):  # look for start of grad.
            if all(im[(r-sstv):r, theta, 0] == centers[grad]):
                storage[theta][0] = r-sstv
        for f in range((count-sstv), vR):  # look for end of grad.
            if not any(im[(f-sstv):f, theta, 0] == centers[grad]):
                storage[theta][1] = f
                continue  # move onto next column

    temp = []
    for theta in range(0, vTheta):
        # remove any columns that did not have the dye diffusion
        if not(None in storage[theta]):
            # find length of diffusion length
            temp.extend([storage[theta][1]-storage[theta][0]])

    # cvt pixel length to diffusivity and trim upper and lower trim% of values
    verbose.append(sorted(px2diff(temp, calFile[numF])))
    # verbose.append(sorted(px2dist(temp,calFile[numF])))
    del verbose[numF][:int(len(verbose[numF])*trim)]  # remove last %trim
    del verbose[numF][0:int(len(verbose[numF])*trim)]  # reomve first %trim

    # take the mean and standard deviation of the counted pixels
    stats.append([len(verbose[numF]), np.mean(verbose[numF]), np.std(verbose[numF])])

    # Output to high level and verbose .txt files
    print(filename[18:23]+',',' %d, %0.4e, %0.4e'%(len(verbose[numF]), stats[numF][1], stats[numF][2]), file=outF)
    print(str(verbose[numF]).strip('[]'), file=verboseF)
