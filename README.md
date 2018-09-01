# CV-Diffusion

Work in Progress

Introduction
----

This repository was independently developed as a data analysis pipeline for optically measuring radial drug diffusion in blood vessel gel analogs during Purdue's BME 306 "Biotransport Laboratory". Following a simple pixel-to-disance calibration step, it enables users to batch process an input folder of arbitrarily sized .jpg or .png files for diffusion 360˚ about a center point. This process is wholly replicable between users and is capable of processing on OSX or Linux with the pre-installed python 3.x and OpenCV dependencies. 

Getting Started
----

To get started, the first thing you will need to do is create a calibration file for your specific samples' geometry. Ideally you should take your input photos with a ruler in frame to validate your pixel-distance ratio. 

To get started, you will first need to install the necessary dependencies: 

```
pip3 install opencv-python numpy matplotlib pillow
```

Then you will need download or clone this repository and cd into the parent directory 

```
git clone https://github.com/barrettfdavis/CV-Diffusion.git
cd /CV-Diffusion
```

Next, transfer the image files you would like to analyze into the folder "Inputs" (NB: 

```
cp ~/[Insert Your Photos' Directory Here]/* ~/Inputs
```

And run the image pre-processing script. 

```
python3 diffusionCV.py
```

Processing a folder of around fifty 30kb JPEGs took about 1-2 minutes on my MBP, but the actual time will depend largely on your machine. Once this is finished, you will be ready to run the measurement script:  

```
python3 measure.py
```

Should everything have gone as expected, you should now see two new files in the "Outputs" folder called "gradFronts.txt" and "verboseOutput.txt". Congrats! You're data is now ready for analysis.


Reading from left to right across the gradFronts.txt file, you will find that for each line the comma seperated values correspond to a given sample's file name, the number of valid measurements taken on the sample, the diffusivity of the sample, and the standard deviation in diffusivity measurements: 

| Name | Number of Measurements | Mean Diffusivity (cm^2/s) | Diffusivity (cm^2/s) (STDev) |  |
|--------|------------------------|---------------------------|------------------------------|---|
| ABC123 | 100 | 1E-05 | 5E-06 |  |
| DEF345 | 100 | 2E-05 | 5E-06 |  |
| ... | ... | ... | ... |  |

Reading from right to left across the verboseOutput.txt file, you will find every recorded diffusivity value for a given sample on each individual line. The image file corresponding to each line is not shown, however the lines are organized alphabetically by filename. 


Methods
----

With respect to pixel-to-distance calibration, for the purposes of the lab, a random selection of 25 sample photos taken with rulers in the shot were analyzed to establish the number of pixels across one centimeter (1 cm) and the number of pixels across the major axis of a given gel's channel. The major axis was chosen as it was discovered that due to the variation in geometries of the implements used to create the gel channels during casting (i.e. drinking straws), each channel was slightly ellipsoidal in shape, but nearly identical in major axis length. Plotting these two data points (pixels per centimeter and pixels per major axis) a calibration curve to convert between the two was experimentally derived, as shown in figure below.

![Calibration Curve](https://github.com/barrettfdavis/CV-Diffusion/blob/master/illustrations/CalibrationCurve.png)

With an r<sup>2</sup>=0.985 it was assumed that a linear approximation could be reasonably applied when back-deriving a pixels/cm coefficient from the number of pixels across a gel's major axis by applying the equation

Cpx/cm = 0.679 * Cpx - Pixels Across Major Axis + 3.53

In practice, for a given calibration coefficient Cpx/cm, the physical length traveled by a drug/dye can be calculated via the equation  

Diffusion Length (cm) = Pixels Across Major Axis * Cpx/cm

![Gradient Finding](https://github.com/barrettfdavis/CV-Diffusion/blob/master/illustrations/gradientFinding.png)

![Processing Steps](https://github.com/barrettfdavis/CV-Diffusion/blob/master/illustrations/processDisplay.PNG)


Attributions
----

I would like to extend a huge thank you to the developers behind the OpenCV and PyAbel projects. This project would not have been possible without their hard work and support docs.
