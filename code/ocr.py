# reference:http://answers.opencv.org/question/63847/how-to-extract-tables-from-an-image/



# General plan: detect the border of the table
# > get coordinates.
# > parse the texts
# also, detect capitalised State name, if there are two state in one page, try detect as well
# use open CV for detecting border, use tesseract to parse.
# for records with extra lines, put the same grid on,
# and search these columns by detecting empty columns later.


# details for detecting the border
# 1. detect table lines
# 2. detect the dotted lines for a couple of rows,
# get the height of them, then establish the grid accordinly
# note: the position of the row borders should be 0.5 mm bellow the dots (so that they do not overlap with the records.
# note: for the grid, detect the vertical lines directly, and make the rows perpendicular to them.

# train also with a dictionary of towns, person names, county names, and state names.


# more plans for detecting the state name.





# openCV installation
# > installation done through pycharm (-python-contri)

import cv2
import math
import numpy as np
import cv2
from matplotlib import pyplot as plt



# @@@@@@@@@@S0. load file & display       || see : http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_image_display/py_image_display.html
# find out how to load all pictures in the folder

myJpg = cv2.imread('test.jpg')

# the openCV way of displaying image:
# cv2.namedWindow('image', cv2.WINDOW_NORMAL)   # so that you can resize the window
# cv2.imshow('image',myJpg)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# display image with matplotlib  || see http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_image_display/py_image_display.html
# img = cv2.imread('test.jpg',0)
# plt.imshow
# (img, cmap = 'gray', interpolation = 'bicubic')
# plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
# plt.show()


# @@@@@@@@@@ S1.  detect the table lines

# s1.1 convert image to grey color
grayJpg = cv2.cvtColor(myJpg, cv2.COLOR_BGR2GRAY)  # change image to gray
binaryJpg = cv2.adaptiveThreshold(grayJpg, 255,  # change the gray image to binary
                                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY_INV, 15,
                                  18)  # the last variable: higher, less noise, but indents the letters, lower, more noise
# plt.imshow(binaryJpg, cmap = 'gray', interpolation = 'bicubic')             #display image
# plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
# plt.show()


# S1.2 detect the column borders.

 # .copy() return an equivalent object
vertical = binaryJpg.copy()
verticalSliderHeight = 60
verticalSliderWidth = 1
verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT,
                                              ksize=(verticalSliderWidth,
                                                     verticalSliderHeight))  # basically a vertical line scanning the image. If such line is detected, then pixe;s turned into 1, otherwise 0, such that everything else is deleted.
#print(len(verticalStructure))
myPoint = (-1,
           -1)  # there is no built-in point class in python, can either use a tuple (), or create a point class within the program. http://openbookproject.net/thinkcs/python/english3e/classes_and_objects_I.html
vertical = cv2.erode(vertical, verticalStructure, myPoint)  # single out vertical lines
vertical = cv2.dilate(vertical, verticalStructure, myPoint, iterations=1)

# s1.3 detect the dots to set up for rows
 ### use multiply structuring elementn

myJpg = cv2.imread('test.jpg')
blank = cv2.imread('blank.jpg')
blank2 = cv2.imread('blank.jpg')

horizontal = binaryJpg.copy()
#dotStructure = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(5,5))
oneDot = np.array    (  [
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],

                               [0,0,1,0,0],
                               [1,1,1,1,1],
                               [1,1,1,1,1],
                               [1,1,1,1,1],
                               [0,0,1,0,0],

                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],

                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                               ]                              ,np.uint8)
twoDots =np.array(            [[0,0,1,0,0, 0, 0,0,1,0,0],
                               [1,1,1,1,1, 0, 1,1,1,1,1],
                               [1,1,1,1,1, 0, 1,1,1,1,1],
                               [1,1,1,1,1, 0, 1,1,1,1,1],
                               [0,0,1,0,0, 0, 0,0,1,0,0]], np.uint8)
threeDots = np.array(         [[0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0],
                               [1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1],
                               [1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1],
                               [1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1],
                               [0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0]], np.uint8)
fourDots = np.array(          [[0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0],
                               [1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1],
                               [1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1],
                               [1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1],
                               [0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0]], np.uint8)
fiveDots = np.array(          [[0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0],
                               [1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1],
                               [1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1],
                               [1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1],
                               [0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0]], np.uint8)
sixDots = np.array(           [[0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0],
                               [1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 0,0,1,0,0, 0,0, 1,1,1,1,1],
                               [1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 0,0,1,0,0, 0,0, 1,1,1,1,1],
                               [1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 0,0,1,0,0, 0,0, 1,1,1,1,1],
                               [0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0]], np.uint8)
sevenDots = np.array(         [[0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0],
                               [1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 0,0,1,0,0, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1],
                               [1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 0,0,1,0,0, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1],
                               [1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 0,0,1,0,0, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1],
                               [0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0]], np.uint8)


myPoint = (-1,-1)
horizontal = cv2.erode(horizontal, oneDot , myPoint, iterations = 1)  # find all dots that have enough empty spaces around them
horizontal = cv2.dilate(horizontal, oneDot , myPoint, iterations = 3)
horizontal = cv2.erode(horizontal, sixDots , myPoint, iterations = 1)   #get rid of the noises that don't have 6 dots in a row
horizontal = cv2.dilate(horizontal,sixDots , myPoint, iterations= 1)

lines = cv2.HoughLinesP(horizontal,
                       2,       #rho, the fatness of the data, https://stackoverflow.com/questions/40531468/explanation-of-rho-and-theta-parameters-in-houghlines
                       np.pi/180   #theta
                       ,threshold= 1000   # the bigger this value is, the less lines in the result (which is good)
                        , minLineLength= 200
                        , maxLineGap= 700)
numLines = len(lines)
print("number of lines" , numLines)

# s1.4 filtering with angles, keep only lines that close to horizontal
# s1.5 draw horizontal lines on the vertical -> table structure.
for i in range(len(lines)):
    for x1, y1, x2, y2 in lines[i]:
         if y1 <3200:
            angle = np.real(np.arctan2(y2-y1,x2-x1)*180/np.pi)
            #print("angle: ", angle)
            if (angle < 182 and angle >178)  or (angle < 2 and angle >= 0):
                tableStructure = cv2.line(vertical, (x1, y1), (x2, y2)
                                 , 255   # tuple for color, scaler (225) for grey scale
                                 , 1)    # thickness
            else:
                continue
         else:
            continue


rectangleStructure = cv2.getStructuringElement(cv2.MORPH_RECT,(60,1))
#tableStructure = cv2.erode(tableStructure, rectangleStructure, myPoint, iterations = 1)  # find all dots that have enough empty spaces around them
#tableStructure = cv2.dilate(tableStructure, rectangleStructure , myPoint, iterations = 1)



#@@@S2 find the points where the lines cross, find within them pairs points with a vertical distancepf 35 (pix)
# s2.1 find all the corners where vertical and horizontal cross
#np.set_printoptions(threshold=np.nan)
tableStructure = cv2.imread('overlap.jpg')

tableCorners = cv2.cornerHarris(tableStructure,
                                1,   #neiborhood size
                                1,   # Aperture parameter for the Sobel() operator
                                k = 0.04)
goodCorners = cv2.goodFeaturesToTrack(tableCorners,                #https://docs.opencv.org/2.4/modules/imgproc/doc/feature_detection.html#void%20cornerHarris(InputArray%20src,%20OutputArray%20dst,%20int%20blockSize,%20int%20ksize,%20double%20k,%20int%20borderType)
                                      maxCorners=80,               #the max amount of corners to be returned, my guess is it ranks the qualities and return points with the highest quality
                                      qualityLevel= 0.01,         #the higher the quality level, the less the results
                                      minDistance= 20, )           # min Distance between corners.

for i in range(len(goodCorners)):    #this for loop displays the detected good corners by drawing.
    for x,y in goodCorners[i]:
        #print(x,y)
        myGoodCorners = cv2.circle(blank,(x,y),radius=2,color = (0,0,255),thickness=10)


plt.imshow(blank, cmap='gray', interpolation='bicubic')  # display image
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()


print("cv2.cornerHarris result: ", len(tableCorners))
print("cv2. goodFeaturesToTrack result, i.e. num goodcorners: ", len(goodCorners))


# s2.2 find pairs of corners that have a vertical distance of 35 pi, put append them to a list.

#look a x-axis value where there is >5 goodCorners (intersection) < if there are many goodCorners, then the reference point is likely not going to be noise
#> there might be exceptions where there is less then 5 lines on a page, but very unusual, can do something to capture the bug.
#-> look for two-three points with a vertical distance of about 35 pixels, start looking from the smaller xs.
#-> select either of the three as the reference point, then create a mask of horizontal lines covering the whole page (from 0, up to the height of the page)
#for vertical mask, find the likely position of the leftmost table intersections , then infer the rest of the vertical lines by addition.

#s2.2.1 I decide to find the left most corners first. To do that, first sort the points by x-values
goodCornersList = []
for i in range(len(goodCorners)):                #extract the (x,y) points from the comlicated result of goodCorners
    goodCornersList.append(goodCorners[i][0])
goodCornersList = sorted(goodCornersList, key = lambda k:[k[0],k[1]])           # this sorts x-values, then y-values #https://docs.python.org/2/library/functions.html#sorted

print("s2.2.1 sorted:",goodCornersList)


#S2.2.2 count points with similar (+-2) x-values, if count> 5, then I have find the leftmost corners ~ which is supposed to be between the first and the second column.
leftMostPointsList = []
referenceCornersImg= "empty"
count = 0
for i in range(len(goodCornersList)-1):

    x1 = goodCornersList[i][0]
    x2 = goodCornersList[i+1][0]

    y1 = goodCornersList[i][1]
    y2 = goodCornersList[i+1][1]
    numCornerDesired = 15       #minimun number of corner needed to determine the corners of a vertical line is found.

    #print("x1:", x1, "||||| x2:", x2)

    if (x1 < x2 + 2) and (x1 > x2 -2):
        count = count+1
        #print("count= " , count, "||i: ", i)
        if count == numCornerDesired:  # line A
            # count>5 means I found a couple of points that are aligned at the same x-value. I want to keep these into a list.
            #print("gotcha")
            for k in range(i-numCornerDesired+1,i):                                      #onece found n consecutive (given x are sorted) dots with the same x-value, extract all the previous 5 points to the list
                xVal = goodCornersList[k][0]                                 #also note -5+1 because python starts counting from 0
                yVal = goodCornersList[k][1]
                leftMostPointsList.append([xVal, yVal])
                referenceCornersImg = cv2.circle(blank2, (xVal, yVal), radius=2, color=(0, 0, 255), thickness=20) # draw these points on a blank page

            #print("I am breaking the loop here!!!!!!!!!!")
            print("enough (", numCornerDesired, ") points are found at x = ", x1)

            break                         #break the loop after 1 such vertical line is found.

        else:
            continue  # when we don't find n consecutive dots, we are supposed to return to the first line A of the for loop here, start a new count, and continue parsing the rest of the X-values
    else :

        print("did not find enough points at this x-value, you wanted:  ", numCornerDesired, " points at: ", x1, " reset count = 0, and continue to the next point")
        count = 0                               #reset count to 0 if find two different x

# plt.imshow(blank2, cmap='gray', interpolation='bicubic')  # display image
# plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
# plt.show()

if len(leftMostPointsList) == 0 :
    print ("s2.2.2 [BAD]It seems that your numCornerDesired is too large , sugestions: try values around 8~15 *************************") # warning, if cannot capture any group of n points with the same x.
    # Can also change the loop above, so that it adjust the numCornerDesired automatically.

# plt.imshow(referenceCornersImg, cmap='gray', interpolation='bicubic')  # display the image of points of selected at the same x
#
# plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
# plt.show()



#then go back to the good corners list, find a point at the same y.

print ("S2.2.3 now looking for a starting point for the horizontal masks within [leftMostPointsList]")
# S2.2.3 Find a pair of dots that has distance = aprox(35) pix in between
# S2.2.4 search from the goodCornersList (dots not at the same x), find another dot2 that has the same y, if not, move forgo the current dot for security concenrns.

leftMostPointsList = sorted(leftMostPointsList, key = lambda k:[k[1]]) #sort again by y
verticalDeviation = 40   #asummed vertical Deviance between two dots. > i.e. I want to find dot2 at the [same] y, but need to allow for some deviation because the scan was tilted to begin with.
for i in range(len(leftMostPointsList)-1):                 #loop thorugh the leftmost point,
    #print("point A")
    x1 = leftMostPointsList[i][0]                    # point A
    y1 = leftMostPointsList[i][1]
    y2 = leftMostPointsList[i+1][1]
    verticalDistance = np.abs(y1-y2)
    print("vertical Distance: ", verticalDistance)
    if (verticalDistance <= 36) and (verticalDistance >=34) :                #find two dots with vertical distance about = 35
        print("dot 1 is found *******************************************")
        for m in range(len(goodCornersList)):
            print("pointB, m: ", m)                          # point B
            x3 = goodCornersList[m][0]
            y3 = goodCornersList[m][1]
            print("y3: ", y3)
            if (y1< y3 + verticalDeviation/2 ) and (y1 > y3 - verticalDeviation/2):
                finalReferencePoints = [[x1,y1],[x3,y3]]
                print("My final reference poitns are : ", x1,y1, x3,y3)
                break             #(back to point A, because loop B is broken by [break]) found the final reference dot1 and a dot2 at the same y,  end the loop at point B , continue to a new iteration at point A
            else:

                continue                        # (back to point B), look for another dot2 from the [goodCornersList] which contain points with all Xs.
    else:
        print("cannot find y aprx. = ", y1, "from [good cornersList]")

        continue

for i in range(len(leftMostPointsList)):
    print("leftMostPointList-ys: ", leftMostPointsList[i][1])

print(len(leftMostPointsList))
print(goodCornersList)

    # if verticalDistance is around 35, and can find another point at aprox the same y :
    #     then draw line,
    #     according to this line, draw masks till the edges of the page.








# find the first point where two lines cross AND the distance to the second corss point is around 25 pixels.  (x1,y1)
# obtain y points to draw lines through. by using y1+25, til y= len(pic), and y1-25 till y=0.
# draw lines across the whole graph, passing through these y points > here is the horizontal borders.
#move the line down 2-3 pixels
#### it is better to let the line corss through y points, i.e. get the cross, get the other y that is associated with the line>>>>only need this later when there is a problem with the precision

#for vertical table lines, need more precise position than horizontal.
#detect where the lines cross, look for positions where there are 4 such detection of corsses
#draw lines that are perpendiuclar to the horizontal lines above, and crossing each of the four lines.

#