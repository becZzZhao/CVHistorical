# pip3 install opencv-python to install OpenCV
import cv2
from Page import Page
import matplotlib
import numpy as np
# from Horizontal import Horizontal




# class Kernel():
#     @staticmethod
#     def createKernelFromImg(dotPattern):
#
np.set_printoptions(linewidth=3000, threshold = 3000)

# Step1. load raw page to view
a = Page.rawtobinary('test_Page_09.jpg')
# Page.display(a)

# crop 3 dots
top = 500 + 100 + 100  # crop the white edges
bottom = 600 + 100 + 50
left = 1750
right = 1800
loc = [top, bottom, left, right]
# myimg = Page.cropImg(loc, a)
# Page.display(myimg)


# change img to function nput
img = Page.rawtobinary('test_Page_09.jpg', locationRef = loc)
# Page.display(b)

def img_to_kernel(display = False):

    kn = []
    for i in range(0, len(img)):
        row = img[i]
        if list(row).count(255) >2:
            newRow = np.where(row == 255, 1, row)
            kn.append(list(newRow))
    kn = np.array(kn, np.uint8)
    if display == True:
        print(np.array(kn))

    return kn


# pad 0s for empty spaces around the kernel
# the unit for the size option is 1 kernel (max(vertical, horizontal))
def padding(kernel, where = 'all', size = 1):

    kerSize = len(kernel)

    paddingSize = kerSize*size

    kernel = np.pad(kernel, pad_width=paddingSize )
    # myRows = [0]*len(kernel[0])
    # print(myRows)
    # npzero = np.zeros(shape = 1, dtype = np.int8)[0]
    # for i in range(0, paddingSize):
    #     kernel = np.insert(kernel,0, 0,axis = 0)
    #     kernel = np.insert(kernel, -1, 0, axis=0)
        # kernel.insert(0, myRows)
        # kernel.append(myRows)

    print(kernel)
    return kernel
    # print(np.array(kernel))
    # if where == 'all':




mykn = img_to_kernel(display = False)
paddedkn = padding(mykn)
# get only one kernel add padding.


# m = Horizontal.find_all_dots(a, display = True)





# Step2. turn raw page to binary image, cuts the white edges too.
# need to fix white edge cutting.
# p = Page.rawtobinary('test_Page_09.jpg')
# Page.display(p)
# print(len(p))
# to draw a line
# Page.draw_lines([[100,1000, 100, 0]], a,display = True)

# detect all single dot patterns with blank surroudings
# m = Horizontal.find_all_dots(p, display = True)
# Page.display(m)


# detect horizontal lines with surroundings.
# Horizontal.dotted_to_lines(m, display = True)
# Page.draw_lines(lines, a, display = True)
