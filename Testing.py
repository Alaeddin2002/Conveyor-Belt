import os
import cv2
def bluriness (folder_name,threshold):
    folder_path = folder_name
    blurred_images = []
    #take the images from the folder we saved
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(folder_path, filename)
            #read the images in the folder
            image = cv2.imread(image_path)
            
            #resize the image to make them smaller
            #As the bluriness is only in one area of the image
            resized_image = cv2.resize(image, (250, 250))  
            #Make the image grey as it is easier to detect bluriness
            gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)  
            #Apply Laplacian filter
            fm = cv2.Laplacian(blurred, cv2.CV_64F).var()
            #if fm is les sthan the threshold we decided, then image is
            #seen as blurry
            if fm < threshold:
                #if it is blurred then save to show laster
                blurred_images.append((filename, fm))
    print("For The Threshold of ",threshold, "these are the images filtered" )            
    if blurred_images:
        print("Blurred images found:")
        for image, fm in blurred_images:
            print(f"{image}: {fm}")
            #os.remove(folder_path + '/' + image)
        
    else:
        #if no blurred imags found
        print("No blurred images found.")
        
bluriness ("test_1",20)
#When threshold was 20, all pictures are blurry, but some blurry pictures
# make it through, such as Image 0.
        
bluriness ("test_1",25)
#When threshold was 25, one or two pictures that are clear are detected
# as blurry. While the rest are dtected correctly. 



bluriness ("test_1",30)
#When threshold was 30, most pictures detected were blurry, 
# but a lot were also clear.
#such as Image (1)


bluriness ("test_1",45)
#When threshold was 45,  more clear pictures with were
#detected. Thus they would be removed. 

