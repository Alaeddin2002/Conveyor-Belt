from inference_sdk import InferenceHTTPClient
import cv2
import mediapipe as mp
import time
import os
from datetime import datetime
from Background_thread import DetectBlurriness

from flask import Flask

capture = True
app = Flask(__name__)


def detect_hand(frame):
    # Initialize MediaPipe Hands model
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(frame_rgb)

    # Check if a hand is detected
    if results.multi_hand_landmarks:
        return True
    else:
        return False

    
    
def labelling (sku):
    global capture
    
    print('Camera will start capturing')
    print("To stop Capturing, enter http://127.0.0.1:5000/stop_capture")
    #seconds = int(second)
    #Importing Object Detection model to infer live video from it
    CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="Hzoy0ZJOqJZGo8xqaqhG"
    )
    # add sku number to name your file
    #sku = input("What is the folder name/sku number?")

    #file will be saved to downloads folder
    path = sku

    if os.path.exists(path) == False:
        print(os.path.exists(path))
        os.mkdir(path)

    #specify that the laptop camera will be used
    camera = cv2.VideoCapture(0)
    
    print("Pictures will be taken in")
    print("3")
    time.sleep(1)
    print("2") 
    time.sleep(1)
    print("1")   
    time.sleep(1)

    #adding time to make sure pictures are taken in one second
    start_time = time.time()
    elapsed_time = 0
    overall_time = [0]
    final = [0]
    hand_timer = 0
    i = 0
    
    #while loop to keep camera open until 6 seconds of pictures are taken
    #This is calcaluated by suming the time of every loop until it reaches 
    #the number of seconds we need 
    while capture == True:
        #Activating the Background Thread to detect bluriness in pictures 
        #while the function atkes another picture
        Detect_blurriness = DetectBlurriness(path)
        Detect_blurriness.start()
        
        
        return_value,image = camera.read()
        
        #show user the camera recording
        #cv2.imshow('image',image)
        cv2.waitKey(1)
        
        
        if return_value:
            # Detect hand in the captured frame
            hand_detected = detect_hand(image)
            
            #Detect Objects in captured frame
            result = CLIENT.infer(image, model_id="groceries-9vwuo/3")
        
            #if statement for if hand is detected  is true
            if hand_detected is True or len(result['predictions']) == 0:
                #start time from 0 again
                start_time = time.time()
            else:
                # name the picture as the sku number plus the time it was taken
                name = 'Image_'+str(i)+'_'+str(datetime.now()) +'.jpg'
                cv2.imwrite(os.path.join(path , name),image) 
                cv2.waitKey(1)
                return_value,image = camera.read()
                i+=1
 
                #for each loop time taken is recorded and saved in a list
                elapsed_time = time.time() - start_time
                if elapsed_time < overall_time[-1]:
                    final.append(overall_time[-1])
                overall_time.append(elapsed_time)
                
        #stoping the background thread after a loop is done
        Detect_blurriness.stop()

    #Remove the video recording tab after function is done          
    camera.release()
    cv2.destroyAllWindows()
    

@app.route('/')
def intro():
    messages = ['To start capturing, go to http://127.0.0.1:5000/start/sku, replace sku with the sku name you want', 'To stop capturing, go to http://127.0.0.1:5000/stop_capture, images will be saved in a downloads folder with the sku number on it']
    
    return messages

@app.route('/start/<sku>')
def start_capture(sku):
    global capture
    capture = True
    labelling(sku)
    return 'images are in a folder in downloads, your sku is the name of it'
    
    


@app.route('/stop_capture')
def stop_capture():
    global capture

    # Stop image capture
    capture = False

    return ('Image capture stopped.')



if __name__ == '__main__':
    app.run(debug=True)