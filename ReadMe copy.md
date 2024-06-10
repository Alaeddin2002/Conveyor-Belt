Read Me

# To Run the Files first 
## Download the code files
### Note:
### The Default setting for the recording duration is 6 seconds, this can be changed if you open Data_Gen.py and change the argument for the labelling function

First open Terminal
Then insert the import command:
    
    pip install opencv-python

When the import command is done insert the command :

    python Data_Gen.py

A question will be popped up to ask about the folder name you want

Note that the laptop camera will open as soon as the command is entered. After three seconds the function will start taing pictures.

The function will not take pictures if a hand is present on camera 

After the camera window is closed, there will be a folder in the Connveyor-Belt folder, where pictures are saved and filtered for both their bluriness and hand detection. 

The Background Thread is imported to the Data_Gen.py, it is activated to detect bluriness in pictures at the same time while the function takes another picture.