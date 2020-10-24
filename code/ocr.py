

from Horizontal import Horizontal
from Vertical import Vertical
import pytesseract
from Page import Page
import cv2
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
import sys
from Kernel import Kernel
from imutils.perspective import four_point_transform
from imutils import contours
import imutils


class OCR(Vertical, Horizontal):
    @staticmethod
    def get_mask(path_to_raw_page, display = False):
        raw = Page.rawtobinary(path_to_raw_page)

        # detect horizontal borders
        dots = Horizontal.find_all_dots(raw, display = False)
        lines = Horizontal.dotted_to_lines(dots, display=False)
        lines_filtered = Horizontal.filter(lines, len(raw))
        lines_horizontal = Horizontal.populate_lines(lines_filtered, len(raw[0]), len(raw))

        vertical_pic = Page.draw_lines(lines_horizontal, raw, display=False, thickness=5)

        # detect vertical lines
        contours = Vertical.lookfor_vertical_contours(raw)
        lines_vertical = Vertical.determine_houghlines(contours, display=False)
        lines_vertical = Vertical.finalize_vertical_line(lines_vertical, page_height=len(raw))

        mask_pic =  Vertical.draw_line(vertical_pic, lines_vertical, display=False, thickness=7)

        if display == True: Page.display(mask_pic)

        return lines_horizontal,lines_vertical, mask_pic

    @staticmethod
    def remove_trailing_dots(myCell):
        np.set_printoptions(threshold=sys.maxsize)
        # myCell = Page.cropImg([27, 35, 272, 400], myCell)
        image = myCell
        #resizing is necessary for better performance. I don't know why
        image = imutils.resize(image, height=100)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # remove salt-and-pepper noise on the page.
        thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)[1]
        # blurring makes the dots more elliptical-like
        blurred = cv2.blur(thresh, (6, 6), 0)
        # prepare for contouring
        edged = cv2.Canny(blurred, 120, 255, 1)
        # dilation connects the edges
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
        edged_dilated = cv2.dilate(edged, kernel)


        # print(np.unique(image.reshape(-1, image.shape[2]), axis=0))

        # find the outmost contour
        cnts = cv2.findContours(edged_dilated, cv2.RETR_CCOMP ,
                                 cv2.CHAIN_APPROX_NONE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        # p = Page.create_blankpage(edged)
        p = image

        circles = []
        for i in range(0, len(cnts)):
           (x, y), radius = cv2.minEnclosingCircle(cnts[i])
           area = cv2.contourArea(cnts[i])
           circles.append([(x, y), radius, area])

        circles.sort(key = lambda x: x[0][0], reverse = True)
        print(circles[:14])

        # remove the outliers of the rightmost 3 points.

        for i in range(1, len(circles)):
            (x0, y0), radius0, area0 = circles[i-1]
            (x, y), radius, area = circles[i]

            dist_x = abs(x-x0)
            dist_y = abs(y-y0)
            dist_euc = (dist_x**2 + dist_y**2)**(1/2)
            # or (dist_euc > 50)
            # or (dist_y > 10)
            if not ((dist_x > 60) ) :
                # if i > 10:break
                #
                if (500> area > 50):
                # problem: not secure enough to break it, would better off just use houghline
                    cv2.circle(p, (int(x),int(y)), int(radius), (0, 0, 255), 2)
                    if (i == 1) & (500 >area0 >50):
                        cv2.circle(p, (int(x0), int(y0)), int(radius0), (0, 0, 255), 2)

        return p








        Page.display(p)












#https://levelup.gitconnected.com/text-extraction-from-a-table-image-using-pytesseract-and-opencv-3342870691ae
#https://www.pyimagesearch.com/2018/08/20/opencv-text-detection-east-text-detector/
    @staticmethod
    def preprocess_img(myCell):
        np.set_printoptions(threshold=sys.maxsize)
        #input is RGB

        # local denoise + binarization
        myCell = cv2.threshold(myCell, 127, 255, cv2.THRESH_BINARY_INV)[1]


        # get unique color to replace
        # print(np.unique(myCell.reshape(-1, myCell.shape[2]), axis=0))

        # # red & yellow color to white
        myCell[np.where((myCell == [255, 255, 0]).all(axis=2))] = [255, 255, 255]
        myCell[np.where((myCell == [255, 0, 0]).all(axis=2))] = [255, 255, 255]

        # convert to binary gray scale (easier to print)
        myCell = cv2.cvtColor(myCell, cv2.COLOR_RGB2GRAY)

        # initial cropping
        alph0 = Page.cropImg([8, 31, 100, 135], myCell)
        dots0 = Page.cropImg([27,35,272,400], myCell)


        # erode and dilate
        kernel = np.array(np.ones((3,4),dtype=np.uint8))  # when erode() takes an empty kernel, it automatically generates a 3*3 rectangular structuring element.
        kernel = Kernel.padding(kernel)
        # kernel =  cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(4,4))
        dots= cv2.erode(dots0, kernel,iterations=1)  # find all dots that have enough empty spaces around them
        alph = cv2.erode(alph0, kernel, iterations=1)
        myCell = cv2.erode(myCell, kernel, iterations=1)

        dots1 = dots.copy()

        kernel2 = np.array(np.ones((2,3),dtype=np.uint8))  # when erode() takes an empty kernel, it automatically generates a 3*3 rectangular structuring element.
        kernel2 = Kernel.padding(kernel2)

        dots= cv2.dilate(dots, kernel2,iterations=1)  # find all dots that have enough empty spaces around them
        alph = cv2.dilate(alph, kernel2, iterations=1)
        myCell = cv2.dilate(myCell, kernel2, iterations=1)


        # # erode and dilate
        # kernel = np.array(np.ones((2,4),dtype=np.uint8))  # when erode() takes an empty kernel, it automatically generates a 3*3 rectangular structuring element.
        # kernel = Kernel.padding(kernel,size = 2)
        # # kernel =  cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(4,4))
        # dots= cv2.erode(dots0, kernel,iterations=1)  # find all dots that have enough empty spaces around them
        # alph = cv2.erode(alph0, kernel, iterations=1)
        # myCell = cv2.erode(myCell, kernel, iterations=1)


        # Page.display(myCell)
        print(dots0)
        print("<><><><><><><><><><><><><")
        print(dots1)
        print("<><><><><><><><><><><><><")
        print(dots)
        print("<><><><><><><><><><><><><")
        print(alph)

        Page.display(myCell)



        return dots
        # Page.display(dots)
        # dots= cv2.dilate(dots, kernel, myPoint, iterations=5)

        # myCell = Horizontal.dotted_to_lines(myCell)




    @staticmethod
    def split_cells(img, lines_horizontal, lines_vertical, topRowIdx = 50, bottomRowIdx = 80, leftColIdx = 0, rightColIdx = 5):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cells = []
        for i in range(topRowIdx,bottomRowIdx):
            myRow= []
            for j in range(leftColIdx,rightColIdx):
                offset = 10
                top = int(lines_horizontal[i][1])
                bottom = int(lines_horizontal[i + 1][1]) + offset
                left = int(lines_vertical[j][0])
                right = int(lines_vertical[j + 1][0])

                myCell = Page.cropImg([top, bottom, left, right], img)
                myRow.append(myCell)

                if (bottomRowIdx - topRowIdx == 1) and (rightColIdx - leftColIdx == 1 ):
                    return myCell

            cells.append(myRow)


        return cells






    @staticmethod
    def draw_text(img, text):
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (0, len(img))
        fontScale = 1
        fontColor = (255, 255, 255)
        lineType = 2

        labeled_img = cv2.putText(img, text,
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    lineType)
        return labeled_img


