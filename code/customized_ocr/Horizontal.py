import math
import numpy as np
import cv2
from Page import Page
from Vertical import Vertical
import math


class Horizontal():
    # s1.3 detect the dots to set up for rows
    ### use multiply structuring elements to refine the results.

    @staticmethod
    def find_all_dots(binary_page, display=False, customKernel=[]):
        print(">Looking for all single dot patterns <")

        # these are hand-made kernels/ scanners. haha.
        # to detect 1-dot patterns, we need to confirm that there is enough white space in its surrounding
        # , otherwise we collect noise.

        page = binary_page.copy()
        # simple_dotStructure = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(5,5))
        # oneDot = simple_dotStructure
        myPoint = (-1, -1)

        kernel = np.array(
            [])  # when erode() takes an empty kernel, it automatically generates a 3*3 rectangular structuring element.

        dots = cv2.erode(page, kernel, myPoint,
                         iterations=1)  # find all dots that have enough empty spaces around them

        dots = cv2.dilate(dots, kernel, myPoint, iterations=5)

        if display == True:
            print("second iter for dots")
            Page.display(dots)
        return dots
        # primitively define a horizontal by rows of dots

    # the detected dots are good references for the horizontal border of the table.
    # convert detected dots to lines.
    @staticmethod
    def dotted_to_lines(dots_img):
        print(">De-noise:  looking for consecutive dots that forms horizontal lines with custom filter<")
        sixDots = np.array([[0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                             1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                            [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                             1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                             1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                             1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                            [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                             1, 0, 0, 0, 0, 0, 0, 1, 0, 0]], np.uint8)

        lines_eroded = cv2.erode(dots_img, sixDots, (-1, -1),
                                    iterations=1)  # get rid of the noises that don't have 6 dots in a row
        lines_dilated = cv2.dilate(lines_eroded, sixDots, (-1, -1), iterations=1)
        lines = cv2.HoughLinesP(lines_dilated,
                                2,
                                # rho, the fatness of the data, https://stackoverflow.com/questions/40531468/explanation-of-rho-and-theta-parameters-in-houghlines
                                np.pi / 180  # theta
                                , threshold=1000
                                # the bigger this value is, the less lines in the result (which is good)
                                , minLineLength=200
                                , maxLineGap=700)

        numLines = len(lines)
        print("number of lines after houghline detection. ", numLines)

        return lines, lines_dilated

    # get rid of two lines that are very close
 
############### code below removed for protecting my work efforts. This script is for demonstration purpose only.
############### if you would like to learn more about the project, you are welcome to email beczhaozmy@gmail.com
