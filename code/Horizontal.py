import math
import numpy as np
import cv2
from Page import Page
from Vertical import Vertical
import Kernel

import math

class Horizontal():
    # s1.3 detect the dots to set up for rows
    ### use multiply structuring elements to refine the results.

    @staticmethod
    def find_all_dots(binary_page, display = False, customKernel = []):
        print(">Looking for all single dot patterns <")

        # these are hand-made kernels/ scanners. haha.
        # to detect 1-dot patterns, we need to confirm that there is enough white space in its surrounding
        #, otherwise we collect noise.

        # bug fix 2020-10-12: wrong kernel format in oneDot
        oneDot2 = np.array([

                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],



                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]



                        ], np.uint8)

        oneDot = np.array([

            [[0, 0, 255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 255, 255, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 255, 255, 255, 255,
              255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 255, 255, 255, 255,
              255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 255, 255, 255, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0]]

        ], np.uint8)
    
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


        page= binary_page.copy()
        # simple_dotStructure = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(5,5))
        # oneDot = simple_dotStructure
        myPoint = (-1, -1)


        if customKernel == [] :
            kernel = oneDot
        else:
            kernel = customKernel
        dots= cv2.erode(page, kernel, myPoint,
                               iterations=1)  # find all dots that have enough empty spaces around them

        dots= cv2.dilate(dots, kernel, myPoint, iterations=5)

        if display == True:
            print("second iter for dots")
            Page.display(dots)
        return dots
        #primitively define a horizontal by rows of dots

    # the detected dots are good references for the horizontal border of the table. 
    # convert detected dots to lines. 
    @staticmethod
    def dotted_to_lines(dots_img, display = False):
        print(">De-noise:  looking for consecutive dots that forms horizontal lines with custom filter<")
        sixDots = np.array(           [[0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0],
                                       [1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 0,0,1,0,0, 0,0, 1,1,1,1,1],
                                       [1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 0,0,1,0,0, 0,0, 1,1,1,1,1],
                                       [1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 1,1,1,1,1, 0,0, 0,0,1,0,0, 0,0, 1,1,1,1,1],
                                       [0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0, 0,0, 0,0,1,0,0]], np.uint8)

        horizontal_line = cv2.erode(dots_img, sixDots, (-1,-1),
                               iterations=1)  # get rid of the noises that don't have 6 dots in a row
        horizontal_line = cv2.dilate(horizontal_line, sixDots, (-1,-1), iterations=1)
        lines = cv2.HoughLinesP(horizontal_line,
                                2,
                                # rho, the fatness of the data, https://stackoverflow.com/questions/40531468/explanation-of-rho-and-theta-parameters-in-houghlines
                                np.pi / 180  # theta
                                , threshold=1000  # the bigger this value is, the less lines in the result (which is good)
                                , minLineLength=200
                                , maxLineGap=700)

        if display == True:
            # for x1, y1, x2, y2 in lines[0]:
            #     cv2.line(dots_img, (x1, y1), (x2, y2), (0, 255, 0), 3)
            #     Page.display(dots_img)
            Page.display(horizontal_line)
        numLines = len(lines)

        print("number of lines", numLines)

        return lines

    
    #get rid of two lines that are very close
    @staticmethod
    def filter(lines, page_length):                                      

        num_lines = len(lines)
        list = []

        for i in range(num_lines):
            x1 = lines[i][0][0]
            y1 = lines[i][0][1]
            x2 = lines[i][0][2]
            y2 = lines[i][0][3]

            list.append([x1,y1,x2,y2])

        sorted_list = sorted(list, key = lambda k :[k[1]])

        filtered_horizontals = []
        for i in range(len(sorted_list)-1):

            x1 = 0
            y1 = sorted_list[i][1]
            x2 = page_length
            y2 = sorted_list[i][3]
            y1_next = sorted_list[i+1][1]
            distance= y1_next- y1
            print(distance)

            if distance > 20:                                                           #get rid of two very close lines
                filtered_horizontals.append([x1,y1,x2,y2])


        print("number of lines after filtering: ", len(filtered_horizontals))
        print("filtered lines: " ,filtered_horizontals)

        return filtered_horizontals    #[[],[],[]]            # all lines that have distance > 20 between them



    @staticmethod
    #plan: just add lines to the list one by one, don't insert. 
    def populate_lines(filtered_horizontals, page_width, page_height):
        x1 = 0
        x2 = page_width

        horizontals_populated  = []

        for i in range(len(filtered_horizontals)-1):

            y_current = filtered_horizontals[i][1]
            y_next = filtered_horizontals[i+1][1]
            horizontals_populated.append([x1,y_current,x2, y_current])

            print("y_current: ", y_current)
            y_next = filtered_horizontals[i+1][1]
            line_distance = y_next-y_current
            num_lines_between= int(math.ceil(line_distance/33))-1
            print("real num lines between", line_distance/33, num_lines_between)
            if num_lines_between > 0:
                last_line_y = int(y_current)     ##################other wise address gets messed up
                for m in range(num_lines_between):
                    new_line_y = last_line_y + 33
                    print(last_line_y, new_line_y, "distance: " ,new_line_y-last_line_y)
                    if y_next-new_line_y >30:
                        horizontals_populated.append([x1, new_line_y, x2, new_line_y])
                        print("appended: ", new_line_y)
                    last_line_y = int(new_line_y)

        print("while loop 1")
        reached_the_bottom = False
        line_above = int(horizontals_populated[len(horizontals_populated)-1][1])
        while(reached_the_bottom == False):
            new_line_y = line_above + 33
            if new_line_y < page_height:
                horizontals_populated.append([x1, new_line_y, x2, new_line_y])
            print("appended: ", new_line_y)
            line_above = int(new_line_y)
            if page_height- new_line_y < 30:
                reached_the_bottom = True

        print("while loop 2")
        reached_the_top = False
        line_below = int(horizontals_populated[0][1])
        while (reached_the_top == False):
            new_line_y = line_below - 33
            if new_line_y >0:
                 horizontals_populated.append([x1, new_line_y, x2, new_line_y])
            print("appended: ", new_line_y)
            line_below = int(new_line_y)
            if new_line_y < 3:
                reached_the_top = True

        horizontals_populated = sorted(horizontals_populated, key=lambda k: [k[1]])
        print("final horizontal mask: ", horizontals_populated)


        return horizontals_populated

    
    # combine all methods above, draw results on a binary page. 
    @staticmethod
    def create_row_borders(page, draw = True):
        dots = Horizontal.find_all_dots(page)
        dotted_to_lines = Horizontal.dotted_to_lines(dots)
        filtered_horizontals = Horizontal.filter(dotted_to_lines,len(page))
        populated_lines = Horizontal.populate_lines(filtered_horizontals,len(page[0]),len(page))

        if draw == True:
            print("**drawing Horizontal borders on page")
            drawn_Horizontals = Page.draw_lines(populated_lines,page)
            return drawn_Horizontals
        if draw == False:
            return populated_lines


#test

# # testing the methods:
# p = Page.rawtobinary('test.jpg')
# blank = Page.create_blankpage(size_referece_page= p)
#
# contours= Vertical.lookfor_vertical_contours(p)
# lines_pts = Vertical.determine_houghlines(contours )
# final_verticals = Vertical.finalize_vertical_line(lines_pts, blank = blank.copy())
#
#
# p = Page.rawtobinary('test.jpg')
# dots = Horizontal.find_all_dots(p) #rerturns dots
# dotted_to_lines = Horizontal.dotted_to_lines(dots)
# filtered_horizontals = Horizontal.filter(dotted_to_lines,len(blank))
#
# populated_lines= Horizontal.populate_lines(filtered_horizontals,len(blank[0]),len(blank))
# print(populated_lines)

# p = Page.rawtobinary('test.jpg')
# Horizontal.create_row_borders(p)
