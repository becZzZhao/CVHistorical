# pip3 install opencv-python to install OpenCV
import cv2
from Page import Page
import matplotlib
import numpy as np

np.set_printoptions(linewidth=3000, threshold=3000)

# Step1. load raw page to view
a = Page.rawtobinary('test_Page_09.jpg')
# Page.display(a)

# crop 3 dots
top = 500 + 100 + 100  # crop the white edges
bottom = 600 + 100 + 50
left = 1750
right = 1800
loc = [top, bottom, left, right]

img = Page.rawtobinary('test_Page_09.jpg', locationRef=loc)
loc = [0, 4, 13, 13 + 20]
img = Page.cropImg(loc, img)


class Kernel():

    @staticmethod
    def img_to_kernel(display = False):
        knImg = img
        kn = []
        for i in range(0, len(knImg)):
            row = knImg[i]
            if list(row).count(255) >2:
                newRow = np.where(row == 255, 1, row)
                kn.append(list(newRow))

        kn = np.array(kn, np.uint8)
        if display == True:
            print(np.array(kn))

        return kn


    # pad 0s for empty spaces around the kernel
    # the unit for the size option is 1 kernel (max(vertical, horizontal))
    @staticmethod
    def padding(kernel,  size = 1, display = False,):
        kerSize = len(kernel)
        paddingSize = kerSize*size
        kernel = np.pad(kernel, pad_width=paddingSize)
        # kernel = kernel[:(len(kernel) - paddingSize)]


        return kernel



#
#
# mykn = img_to_kernel(display = False)
# paddedkn = padding(mykn)
