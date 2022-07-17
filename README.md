# Blender Multi-Camera Simultaneous Video Capture Plugin

## Introduction
The Addon is a Multi cameara simultaneous video capture addon which spawns in 5 cameras and recodes the animations from 5 points of views simultaneous between the specified frames.

## Contents
This Repository contains:
- A sample animation in a blend file.
- A .py file that is the addon which can be installed in blender.
- A results folder where the rendered animations are saved.

## To see the demo of the addon
- Clone the repo to your local machine.
- Open the blend file in blender.
- Go to Edit->Preferences->import and select the multiCamRec.py file and import.
- Once the import is successful you can enable the addon by ticking the right mark.
- Then go to the scene properties in Properties panel and you sould find a panel named "MultiCam Recording".
- Click on "Setup Cameras" and set the start frame and end frame of the animation and click "Record Animation" button.
- This might take some time depending on the number of frames to be rendered and the samples (set to 2 by default).
- Once the "Record Animation" button becomes gray color again the render is done you can now go and see the final videos in the results folder in the same location where the blend file is.