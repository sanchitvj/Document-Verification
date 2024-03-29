# -*- coding: utf-8 -*-
"""Face_Verification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1T-cMZ84gPxU50IE7iWC-bdBwW95p8te6
"""

!pip install deepface      #installing deepface(colab)

from deepface import DeepFace

import matplotlib.pyplot as plt
import os
import cv2

"""https://sefiks.com/2020/08/25/deep-face-detection-with-opencv-in-python/  
https://github.com/ageron/handson-ml
"""

#### Function to detect, align, and preprocess the image ####

def face_detect(img_path, output_name):

    img = DeepFace.functions.load_image(img_path)
    backends = ['opencv', 'ssd', 'dlib', 'mtcnn']
    backend = backends[3]
    detected_face = DeepFace.functions.detect_face(img = img, detector_backend = backend)
    aligned_face = DeepFace.functions.align_face(img = img, detector_backend = backend)
    processed_img = DeepFace.functions.detect_face(img = aligned_face, detector_backend = backend)
    
    #plt.imshow(processed_img)
    # Save output of the function.
    filename  =  output_name.format(os.getpid())
    cv2.imwrite(filename, processed_img)

# Check the output of face_detect function.
img_path = '/content/drive/My Drive/IMG_20201007_200043.jpg'
output_name = 'pan_img.jpg'
pan = face_detect(img_path, output_name)

# Check the output of face_detect function.
img_path = '/content/drive/My Drive/IMG20201010221637.jpg'
output_name = 'clicked_img.jpg'
orig = face_detect(img_path, output_name)

#### Resize the image because output of face_detect func will be scaled according
#### to original image but for verification size of both the images should be
#### same(PAN card image is little squeezed, resizing will solve that issue).
def resize_img(path, size):
    img = cv2.imread(path)
    img = cv2.resize(img, (size, size))
    return img

clicked_img = resize_img('/content/clicked_img.jpg', 512)
pan_img = resize_img('/content/pan_img.jpg', 512)

# Set enforce_detection False: Face could not be detected. Please confirm that the picture
# is a face photo or consider to set enforce_detection param to False.
result  = DeepFace.verify(clicked_img, pan_img, enforce_detection = False)

print("Is verified: ", result["verified"])
