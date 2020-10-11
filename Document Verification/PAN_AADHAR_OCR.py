
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re
import io
import json
import ftfy

image = cv2.imread('path/to/image.format')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray = cv2.threshold(gray, 0, 255,  cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
gray = cv2.GaussianBlur(gray, (5,5), 0)

# gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
# gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
# gray = cv2.bilateralFilter(gray, 9, 75, 75)

# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
filename  =  "pan_bw.png".format(os.getpid())
cv2.imwrite(filename, gray)

Image.MAX_IMAGE_PIXELS = 933120000
# load the image as a PIL/Pillow image, apply OCR, and then delete the temporary file

text = pytesseract.image_to_string(Image.open('/content/pan_bw.png'), lang = 'eng')
# add +hin after eng within the same argument to extract hindi specific text - change encoding to utf-8 while writing
print(text)

# writing extracted data into a text file
text_output = open('outputbase.txt', 'w', encoding='utf-8')
text_output.write(text)
text_output.close()

file = open('outputbase.txt', 'r', encoding='utf-8')
text = file.read()

# Cleaning all the gibberish text
text = ftfy.fix_text(text)
text = ftfy.fix_encoding(text)
print(text)

# Initializing data variable
name = None

text0 = []
text1 = []

# Searching for PAN
lines = text.split('\n')
print(lines)
for lin in lines:
    s = lin.strip()
    s = lin.replace('\n',' ')
    s = s.rstrip()
    s = s.lstrip()
    text1.append(s)

text1 = list(filter(None, text1))
print(text1)

# to remove any text read from the image file which lies before the line 'Income Tax Department'

lineno = 0  # to start from the first line of the text file.

for wordline in text1:
    xx = wordline.split('\n')
    if ([w for w in xx if re.search('(NAME|Name|Name|ame|AME|a|Name|ara|Name|-3y yw?|Number)$', w)]):
    #if ([w for w in xx if re.search('(Permanent Account Number Card)$', w)]):
        text1 = list(text1)
        lineno = text1.index(wordline)
        break

# text1 = list(text1)
text0 = text1[lineno+1:]
print('text0:  ', text0)  # Contains all the relevant extracted text in form of a list - uncomment to check


try:

    # Cleaning first names, better accuracy
    
    name = text0[0]
    name = name.rstrip([' '])
    name = name.lstrip()
    name = name.replace("8", "B")
    name = name.replace("0", "D")
    name = name.replace("6", "G")
    name = name.replace("1", "I")
    name = re.sub('[^a-zA-Z] +', ' ', name)
   # print('name: ', name)

except:
    pass

# Making tuples of data
data = {}

data['Name'] = name

print(data)
