import cv2
import threading
import time
import os

class DetectBlurriness(threading.Thread):
    #start running the thread
    def __init__(self, sku):
        threading.Thread.__init__(self)
        self.sku = sku

    
    #bluriness function
    def run(self):
        threshold = 30
        #where blurred images are saved
        blurred_images = []
        for filename in os.listdir(self.sku):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(self.sku, filename)
                #read the images in the folder
                full_image = cv2.imread(image_path)
        
                resized_image = cv2.resize(full_image, (250, 250))  # Resize the image
                #Change picture to gray to detect bluriness 
                gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Apply Gaussian blur
                fm = cv2.Laplacian(blurred, cv2.CV_64F).var()
                if fm < threshold:
                    blurred_images.append((filename, fm))
                     
        if blurred_images !=0:
            for image, fm in blurred_images:
                os.remove(self.sku + '/' + image)
        
    #stop running the thread
    def stop(self):
        self.running = False
