
# To Run the Files first 
## Download the code files
### Note:
### The Default setting for the recording duration is 6 seconds, this can be changed if you open Data_Gen.py and change the argument for the labelling function

First open Terminal
Go to folder directory that you just installed

    cd downloads/Conveyor-Belt/

Then insert the import commands:
    
    pip install opencv-python
    pip install flask

When the import command is done insert the command :

    python Data_Gen.py

To use the API, and start the camera to take pictures  go to 
 http://127.0.0.1:5000/start/sku 
replace sku with the sku name you want.

To stop capturing, go to 
 http://127.0.0.1:5000/stop_capture 

Images will be saved in a folder where your directory is  with the sku number on it.
Pictures are saved and filtered for both their bluriness, hand detection, and object detection.

The function will not take pictures if a hand is present on camera 

The Background Thread is imported to the Data_Gen.py, it is activated to detect bluriness in pictures at the same time while the function takes another picture.


If you want to see the test folder

insert the command 

    python3 Testing.py

It will show the images filtered based on the bluriness, and why the threshold of 25 was selected.
