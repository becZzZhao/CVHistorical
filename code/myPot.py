import cv2
import numpy as np
from Page import Page
from Vertical import Vertical


img= cv2.imread('overlap.jpg')
img= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

good = cv2.goodFeaturesToTrack(img, maxCorners= 60, minDistance=30, qualityLevel=0.1)
print(good)


sorted = sorted(good, key = lambda k:[k[0][0],k[0][1]])
print(sorted)