import numpy as np
import cv2
from Page import Page

class Vertical(Page):


    #some more primitive methods relating to line detection
    @staticmethod
    def lookfor_vertical_contours(binary_nparr):
        jpg_tolook = binary_nparr.copy()
        kernel  = cv2.getStructuringElement(cv2.MORPH_RECT, # this structuring element acts like a "sliding scanner"
                                                      ksize=(1,250))  # basically a vertical line scanning the image. If such line is detected, then pixe;s turned into 1, otherwise 0, such that everything else is deleted.

        somePoint = (-1,-1)

        vertical_contours = cv2.erode(jpg_tolook,kernel, somePoint)  # single out vertical lines
        # Page.display(vertical_contours)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,1500))
        vertical_contours = cv2.dilate(vertical_contours, kernel, somePoint, iterations=2)
        # Page.display(vertical_contours)


        return vertical_contours

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

        if display == True:
            p = Page.create_blankpage(somecontours_binary_nparr)
            for i in range(len(lines)):
                for x1, y1, x2, y2 in lines[i]:
                    p = cv2.line(p, (x1, y1), (x2, y2), 255, 2)
        if lines is None:
            return []
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

    @staticmethod
    def finalize_vertical_line(houghlines_pts, page_height = 0, display = False):
        ptList = [[(x1,y1), (x2,y2)] for [[x1,y1, x2,y2]] in houghlines_pts]
        ptList.sort(key = lambda k: k[1][0]) # sorting on x2
        final_lines = []

        xAvg = ptList[0][0][0]
        for i in range(1, len(ptList)):

            currentLine = ptList[i]
            lastLine = ptList[i-1]

            x1_current = currentLine[0][0]
            x1_previous = lastLine[0][0]

            xDist = x1_current- x1_previous

            if xDist < 10:
                xAvg = (x1_current + xAvg)/2

            elif xDist > 50:
                (x1,y1), (x2,y2) = lastLine
                finalLine = [int(xAvg),0, x2,page_height]
                final_lines.append(finalLine)
                xAvg = x1_current

            if i == len(ptList) -1:
                (x1, y1), (x2, y2) = currentLine
                finalLine = [int(xAvg),0, x2,page_height]
                final_lines.append(finalLine)

        final_lines.sort(key = lambda x: x[0])

        # [[991, 0, 992, 2690], [1301, 0, 1302, 2690], [1967, 0, 1968, 2690], [2177, 0, 2179, 2690]]
        if len(final_lines) <=5:
            if len(final_lines) == 5:
                if final_lines[0][0]>300:
                    final_lines.insert(0,[ max(final_lines[0][0]-500,0), final_lines[0][1], max(final_lines[0][2]-500,0), final_lines[0][3]])
                elif final_lines[3][0] <= 2300:
                        final_lines.insert(-1, [min(final_lines[0][0] + 300, 2831), final_lines[0][1],
                                                min(final_lines[0][2] + 300, 2831),
                                                final_lines[0][3]])
            elif len(final_lines)==4:
                if final_lines[0][0] > 300:
                    final_lines.insert(0, [max(final_lines[0][0] - 500,0), final_lines[0][1], max(final_lines[0][2] - 500,0),
                                           final_lines[0][3]])

                if final_lines[3][0] <= 2300:
                    final_lines.insert(-1, [min(final_lines[3][0] + 450,2831), final_lines[0][1], min(final_lines[3][2] + 450,2831),
                                           final_lines[0][3]])

        final_lines.sort(key = lambda x: x[0])

        print("we found %s vertical lines: " % (len(final_lines)) )
        print(final_lines)


        # if len(final_lines) ==5 :
        #     if final_lines[0][0]>300:
        #         x1,y1,x2,y2 = final_lines[0]
        #         final_lines.append([0, y1, 0,y2])
        #     else:
        #         x1, y1, x2, y2 = final_lines[-1]
        #         final_lines.append([x1+300,y1,0,y2, x2+300])
        # elif len(final_lines) == 4:
        #     x1, y1, x2, y2 = final_lines[0]
        #     final_lines.append([1, y1, 1, y2])
        #     x1, y1, x2, y2 = final_lines[-1]
        #     final_lines.append([x1 + 300, y1, 0, y2, x2 + 300])
        #
        # print("we found %s vertical lines: " % (len(final_lines)) )
        # print(final_lines)

        return final_lines

    @staticmethod
    def create_column_borders(page,draw = False ):
        contours = Vertical.lookfor_vertical_contours(page)
        houghlines = Vertical.determine_houghlines(contours,display = False )
        finalized_borders_list = Vertical.finalize_vertical_line(houghlines,len(page))

        if draw == False:
            return finalized_borders_list

        if draw == True:
            print("**drawing vertical borders on page")
            drawn_page = Page.draw_lines(finalized_borders_list, page)
            return drawn_page, finalized_borders_list



# # # testing the methods:
# p = Page.rawtobinary('test.jpg')
# blank = Page.create_blankpage(size_referece_page= p)
# contours= Vertical.lookfor_vertical_contours(p)
# lines_pts = Vertical.determine_houghlines(contours,display = False )
# #Vertical.draw_line(blank,(0,599),(100,599),color =255, thickness = 4,display = False)
# finals = Vertical.finalize_vertical_line(lines_pts,len(blank))
# Page.display_lines(finals,p)

# p = Page.rawtobinary('eg1.jpg')
# Vertical.create_column_borders(p,draw=False)


#******next: locate the four lines, draw the four lines.
