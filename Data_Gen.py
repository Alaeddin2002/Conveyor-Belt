import cv2
import mediapipe as mp
import time
import os
from datetime import datetime
from Background_thread import DetectBlurriness



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
    
    

def labelling (seconds):
    # add sku number to name your file
    sku = input("What is the folder name/sku number?")

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
    while sum(final) + elapsed_time< seconds:
        #Activating the Background Thread to detect bluriness in pictures 
        #while the function atkes another picture
        Detect_blurriness = DetectBlurriness(path)
        Detect_blurriness.start()
        
        
        return_value,image = camera.read()
        
        #show user the camera recording
        cv2.imshow('image',image)
        cv2.waitKey(1)
        
        
        if return_value:
            # Detect hand in the captured frame
            hand_detected = detect_hand(image)
        
            #if statement for if hand is detected  is true
            if hand_detected is True:
                #start time from 0 again
                start_time = time.time()
            else:
                # name the picture as the sku number plus the time it was taken
                sku = sku[0:-1] + str(seconds - i)
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
labelling(6)


