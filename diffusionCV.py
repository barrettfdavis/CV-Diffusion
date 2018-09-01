"""
Barrett Davis
CV-Diffusion
2018-08-31
"""
#Import Libraries
import matplotlib.pyplot as plt
from PIL import Image
import polar as pc
import numpy as np
import glob, cv2, os

#Define Containers for Imported and Altered Images

norms,images,blurs,colors = [],[],[],[]
segments, gauss = 4, 7

def segmentCV(img,K):
    #img = cv2.imread(img)
    Z = img.reshape((-1,1)); Z = np.float32(Z) # convert to np.float32

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret,label,center=cv2.kmeans(Z,K,None,criteria,7,cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))

    return(res2)

#Image Pre-Processing
for filename in sorted(glob.glob('inputs/*')):

    print('Processing',filename[9:],'...')

    im1 = cv2.imread(filename)
    norms.append([im1, filename[9:len(filename)-4]])

    nix = cv2.GaussianBlur(im1,(gauss,gauss),0) # Apply guassian blur
    nix1 = cv2.cvtColor(nix, cv2.COLOR_BGR2GRAY) # Convert to grayscale
    nix2 = segmentCV(nix1,segments) # K-Means Clustering w/ k segs

    data = np.array(nix2)
    polarGrid,r,theta = pc.reproject_image_into_polar2D(data, origin=None)

    blurPolar = np.flipud(segmentCV(polarGrid,segments)) # repeat segmentation

    # Add pre-processed image to indexed arrays

    blurs.append([nix1, filename[9:len(filename)-4]])
    colors.append([nix2, filename[9:len(filename)-4]])
    images.append([blurPolar, filename[9:len(filename)-4]])

#Saving Images to Folder
cwd = os.getcwd()
for i in range(0,len(images)):

    #Store pre-processed images in indv. folders
    blurF = cwd + "/processed/blurs/%s.png"%images[i][1]
    segmentF = cwd + "/processed/segments/%s.png"%images[i][1]
    polarF = cwd + "/processed/polars/%s.png"%images[i][1]

    cv2.imwrite(blurF,blurs[i][0])
    cv2.imwrite(segmentF,colors[i][0])
    cv2.imwrite(polarF,images[i][0])

    #Combine pre-processed image steps for display photos

    filename = cwd + "/processed/displays/%s.png"%images[i][1]

    f, axarr = plt.subplots(1,4)

    axarr[0].imshow(cv2.cvtColor(norms[i][0],cv2.COLOR_BGR2RGB),aspect='auto')
    axarr[0].set_title("1. Input"); axarr[0].axis('off')

    axarr[1].imshow(blurs[i][0],'gray', aspect = 'auto')
    axarr[1].set_title("2. Gaussian Blur"); axarr[1].axis('off')

    axarr[2].imshow(colors[i][0],aspect = 'auto')
    axarr[2].set_title("3. K-Means Segmenting"); axarr[2].axis('off')

    axarr[3].imshow(images[i][0], aspect = 'auto')
    axarr[3].set_title("4. Polar Output"); axarr[3].axis('off')

    plt.savefig(filename)
    plt.close()
