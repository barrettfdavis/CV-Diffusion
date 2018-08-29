# CV-Diffusion

This repository was independently developed as a data analysis tool for measuring drug diffusion in blood vessel gel analogues during Purdue's BME 306 "Biotransport Laboratory". 

This tool allows for batch processing images of circumferentially sliced vessels 360˚ about the vessle's center point, and outputting relevant statistics on drug diffusion and diffusivity in an output.txt file for further analysis. 

To accomplish this, all images within the user's input folder are subjected to a three-step process of Gaussian blurring, k-means color clustering, cartesian to polar mapping and diffusion boundary detection. 

This process is wholly replicable between users and capable of processing on any machine with the pre-installed python 3.x and OpenCV dependencies.  
