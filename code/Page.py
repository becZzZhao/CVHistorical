import cv2
from matplotlib import pyplot as plt
import numpy as np
from numpy import zeros
from PIL import Image

class Page:

    def __init__(self, image_directory):  ##the constructor, class-attribute instance variable unique to each instance, default index value is set to 0.
        self.binary_page = Page.rawtobinary(image_directory)                          #in the initializer, rawtobinary() take self.raw_page input, but rawtobinary() can be used indeendently as well when called from Pages.rawtoBinary
        #can add grey_page, etc later.



    @staticmethod
    def rawtobinary(image_directory):                                          # turn jpg>nparray> binary_nparray. this method combines the rawtogrey() and greytobinary, and converts a raw page to a binary directly.
        my_raw_page = Image.open(image_directory)

        top = 100              #crop the white edges
        bottom = 3375
        left = 360
        right = 2232
        cropped_page = my_raw_page.crop((left,top,right,bottom))


        to_nparray = np.array(cropped_page)        #cv2 only read np.array.
        my_grey_page = cv2.cvtColor(to_nparray, cv2.COLOR_BGR2GRAY)
        my_binary_page = cv2.adaptiveThreshold(
                                          my_grey_page, 255,  # change the gray image to binary
                                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY_INV, 15,
                                          18)
        return my_binary_page
    @staticmethod
    def display(any_page):
        plt.imshow(any_page, cmap='gray', interpolation='bicubic')  # display image
        plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
        plt.show()

    @staticmethod
    def create_blankpage(size_referece_page):                   #create a blank (in black) page of the same size as self.
        page_height = len(size_referece_page)                  # no. rows of pixels
        page_width = len(size_referece_page[0])
        blank_page = zeros([page_height,page_width])
        return blank_page


    @staticmethod
    def load_colored (image_directory):
        my_raw_page = Image.open(image_directory)

        top = 100  # crop the white edges
        bottom = 3375
        left = 360
        right = 2232
        cropped_page = my_raw_page.crop((left, top, right, bottom))

        to_nparray = np.array(cropped_page)

        return to_nparray


    @staticmethod
    def draw_lines(lines_list,page, display = False):

        for i in range(len(lines_list)):
            x1 = lines_list[i][0]
            y1 = lines_list[i][1]
            x2 = lines_list[i][2]
            y2 = lines_list[i][3]

            if display == False:
                lines = cv2.line(page, (x1,y1),(x2,y2),255,1)
            else:
                lines = cv2.line(page, (x1, y1), (x2, y2), 255, 3)

        Page.display(lines)
        return lines






