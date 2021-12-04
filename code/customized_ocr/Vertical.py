import numpy as np
import cv2
from Page import Page

class Vertical(Page):


    #some more primitive methods relating to line detection

    @staticmethod
    def determine_houghlines(somecontours_binary_nparr, display = False):
        #takes any binary array that contains potential lines, use cv2.houghline to detect lines, and store the x1,y1,x2,y2 values to a list

        threshold = 50
        minLineLength = 50
        maxLineGap = 300
        lines = cv2.HoughLinesP(somecontours_binary_nparr,
                                1,
                                np.pi/180,
                                threshold,
                                minLineLength,
                                maxLineGap)

        numlines = int(len(lines))                             # ************ error: QAQ the input was not iterable beccause this value was not set to an int. I think.
        print("number of [vertical lines of min length = ", minLineLength, "from HoughineLine: ", numlines,
              " |||e.g. the first line [x1,y1,x2,y2]: ", lines[0])

        if display == True:
            p = Page.create_blankpage(somecontours_binary_nparr)
            for i in range(numlines):
                for x1, y1, x2, y2 in lines[i]:
                    p = cv2.line(p, (x1, y1), (x2, y2), 255, 2)

        return lines # a list obj [[[]],[[]]]

    @staticmethod
    def draw_line(any_image, pt_list, color = 255 , thickness = 2, display = False):      #input are tuples: point 1 = (0,0)

        print(pt_list[0])
        if len(pt_list[0] )== 2:
            for [(x1,y1),(x2,y2)] in pt_list:
                if color == "rand":
                    color = random.randrange(0,255), random.randrange(0,255)
                lines = cv2.line(any_image, (x1,y1), (x2,y2), color, thickness)
        elif len(pt_list[0]) ==1:
            for [[x1,y1,x2,y2]] in pt_list:
                if color == "rand":
                    color = random.randrange(0,255), random.randrange(0,255)
                lines = cv2.line(any_image, (x1,y1), (x2,y2), color, thickness)
        else:
            for [x1,y1,x2,y2] in pt_list:
                if color == "rand":
                    color = random.randrange(0,255), random.randrange(0,255)
                lines = cv2.line(any_image, (x1,y1), (x2,y2), color, thickness)




        if(display == True):
            Page.display(lines)

        return lines
    
############### code below removed for protecting my work efforts. This script is for demonstration purpose only.
############### if you would like to learn more about the project, you are welcome to email beczhaozmy@gmail.com
