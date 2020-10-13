# pip3 install opencv-python to install OpenCV
import cv2
from Page import Page
import matplotlib
from Horizontal import Horizontal
from Kernel import Kernel


# temporary changes:
# under page, raw to img, removed cropping temporarily.

# tool1. display to display an cv image object (?)
# Page.display(a)

import numpy as np
import sys
#

np.set_printoptions(linewidth=3000, threshold = 3000)

# Step1. load raw page to view
a = Page.rawtobinary('test_Page_03.jpg')

m = Horizontal.find_all_dots(a, display = False)
n = Horizontal.dotted_to_lines(m, display = False)
k = Horizontal.filter(n, len(m))

Page.draw_lines(k, a,display = True)

# m = Horizontal.find_all_dots(a, display = True, customKernel = )
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
