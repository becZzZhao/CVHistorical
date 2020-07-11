import numpy as np
import cv2
from Page import Page

class Vertical(Page):
    #some more primitive methods relating to line detection
    @staticmethod
    def lookfor_vertical_contours(binary_nparr):
        jpg_tolook = binary_nparr.copy()
        line_Height = 60
        line_Width = 1
        verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, # this structuring element acts like a "sliding scanner"
                                                      ksize=(line_Width,
                                                             line_Height))  # basically a vertical line scanning the image. If such line is detected, then pixe;s turned into 1, otherwise 0, such that everything else is deleted.
        # print(len(verticalStructure))
        somePoint = (-1,-1)
        vertical_contours = cv2.erode(jpg_tolook, verticalStructure, somePoint)  # single out vertical lines
        # vertical_contours = cv2.dilate(vertical, verticalStructure, myPoint, iterations=1)
        # Vertical.display(vertical_contours)
        return vertical_contours

    @staticmethod
    def determine_houghlines(somecontours_binary_nparr, display = False):            #takes any binary array that contains potential lines, use cv2.houghline to detect lines, and store the x1,y1,x2,y2 values to a list
        threshold = 500
        minLineLength = 600
        maxLineGap = 300
        lines = cv2.HoughLinesP(somecontours_binary_nparr, 1, np.pi/180, threshold, minLineLength, maxLineGap)

        numlines = int(len(lines))                             # ************ error: QAQ the input was not iterable beccause this value was not set to an int. I think.
        print("number of [lines of min length = ", minLineLength, "from HoughineLine: ", numlines,
              " |||e.g. the first line [x1,y1,x2,y2]: ", lines[0])

        if display == True:
            p = Page.create_blankpage(somecontours_binary_nparr)
            for i in range(numlines):
                for x1, y1, x2, y2 in lines[i]:
                    p = cv2.line(p, (x1, y1), (x2, y2), 255, 2)
            Page.display(p)
        return lines # a list obj [[[]],[[]]]

    @staticmethod
    def draw_line(any_image, point1, point2, color = 255 , thickness = 2, display = False):      #input are tuples: point 1 = (0,0)
        lines = cv2.line(any_image, point1, point2, color, thickness)
        if(display == True):
            Page.display(lines)

        return lines

    @staticmethod
    def finalize_vertical_line(houghlines_pts,page_height, monitor = False, display = False):

        print("vvvvvvStart to finalize all lines with finalize_vertical_line() method  ***********************************")
        # extract houghlines points from [[[]],[[]]] structure to [[],[]] structure.
        lines_list = []
        for i in range(len(houghlines_pts)):
            lines_list.append(houghlines_pts[i][0])
            if monitor == True:
                print("extract the point: ", houghlines_pts[i][0])
        # sort the lines by their x1 value.
        lines_sortedbyx1 = sorted(lines_list, key = lambda k:[k[0],k[1]])
        print(lines_sortedbyx1)

        #create a new list [[],[],[],[]] for categozing the lines into 4 vertical lines (each is one line_part)
         
        num_line_parts = len(lines_sortedbyx1)

        line_1_line_parts = []
        line_2_line_parts = []
        line_3_line_parts = []
        line_4_line_parts = []
        line_parts = [line_1_line_parts,line_2_line_parts,line_3_line_parts,line_4_line_parts]      # this is the final data structure to be populated by the following loop.


        j = 0
        for i in range(num_line_parts-1):
            if monitor == True:
                print("*********************************")
                print("The process of  finalize_vertical_line() is being monitored.")
                print("j: " , j )

            current_line = lines_sortedbyx1[i]
            x1 = current_line[0]
            nextline = lines_sortedbyx1[i+1]
            x1_nextline = nextline[0]

            distance = x1_nextline - x1

            if monitor == True:
                print("distance, " , distance)
            line_parts[j].append(current_line)

            if distance > 180 and distance < 700:
                print(len(line_parts[j]), " lines found for line ", j, "move on to line ", j+1)
                j = j+1

        if display == True:
            print("results for finalize_vertical_lines[] : ")
            for i in range (4):
                print("vertical: ", i)
                for m in range (len(line_parts[i])):
                    x1 = line_parts[i][m][0]
                    y1 = line_parts[i][m][1]
                    x2 = line_parts[i][m][2]
                    y2 = line_parts[i][m][3]

                    print ("x1: ", x1, "|y1: ", y1, "x2: ", x2, "|y2: ", y2 )


        print(str(line_parts[0])[1:-1])     #print the result of the for loop above no matter monitor= True or not.
        #take the avg of all x1 candidates from line_parts


        final_four_verticals = []
        for i in range(4):                                                                 #loop through each group of candidates for the final verticals, take the sum for each vertical, divide by the number of candiates. i.e. avrerage x1 for each line.
            sum_ofx1 = 0
            for m in range(len(line_parts[i])):
                line_part = line_parts[i][m]
                x1 = line_part[0]
                #print(x1)
                sum_ofx1 = sum_ofx1 + x1

            num_line_parts = len(line_parts[i])
            avgx1_line = int(sum_ofx1/num_line_parts)
            print("avg x1 for line " , i , ": ",avgx1_line)

            final_four_verticals.append(avgx1_line)
        print("^^^^^^^^Finalized Vertical Vertical, final x for each vertical: ", final_four_verticals, " ************************************************************")


        x_vertical_1 = final_four_verticals[0]
        x_vertical_2 = final_four_verticals[1]
        x_vertical_3 = final_four_verticals[2]
        x_vertical_4 = final_four_verticals[3]

        y1 = 0
        y2 = page_height
        final_four_verticals_lines = [[x_vertical_1,y1,x_vertical_1,y2],
                                      [x_vertical_2,y1,x_vertical_2,y2],
                                      [x_vertical_3,y1,x_vertical_3,y2],
                                      [x_vertical_4,y1,x_vertical_4,y2]]

        return final_four_verticals_lines   # a []

    @staticmethod
    def create_column_borders(page,draw = True ):
        contours = Vertical.lookfor_vertical_contours(page)
        houghlines = Vertical.determine_houghlines(contours,display = False )
        finalized_borders_list = Vertical.finalize_vertical_line(houghlines,len(page))

        if draw == False:
            return finalized_borders_list

        if draw == True:
            print("**drawing vertical borders on page")
            drawn_page = Page.draw_lines(finalized_borders_list, page)
            return drawn_page



# # # testing the methods:
# p = Page.rawtobinary('test.jpg')
# blank = Page.create_blankpage(size_referece_page= p)
# contours= Vertical.lookfor_vertical_contours(p)
# lines_pts = Vertical.determine_houghlines(contours,display = False )
# #Vertical.draw_line(blank,(0,599),(100,599),color =255, thickness = 4,display = False)
# finals = Vertical.finalize_vertical_line(lines_pts,len(blank))
# Page.display_lines(finals,p)

p = Page.rawtobinary('test.jpg')
Vertical.create_column_borders(p,draw=True)


#******next: locate the four lines, draw the four lines.