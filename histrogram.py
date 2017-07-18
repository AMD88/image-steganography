import cv2
import numpy as np
from matplotlib import pyplot as plt

imagename = 'coverimage3.jpg'


imagepath = 'images/'+imagename

print imagepath
img = cv2.imread(imagepath, -1)

img2= cv2.imread('images/coverimage3_shifted.png', -1)
img3= cv2.imread('shifted (copy).png', -1)
# cv2.imshow('GoldenGate',img)

def his(img):
    color = ('b','g','r')
    for channel,col in enumerate(color):
        histr = cv2.calcHist([img],[channel],None,[256],[0,256])
        plt.plot(histr,color = col)
        plt.plot(histr,color = col)
        plt.xlim([0,256])
    plt.title('Histogram for color scale picture')
    plt.show()

    while True:
        k = cv2.waitKey(0) & 0xFF
        if k == 27: break             # ESC key to exit
    # cv2.destroyAllWindows()

his(img2)

# image = raw_input('enter image name: ')
# print image

