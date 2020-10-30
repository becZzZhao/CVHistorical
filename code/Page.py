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
    def rawtobinary(image_directory, locationRef = None):                                          # turn jpg>nparray> binary_nparray. this method combines the rawtogrey() and greytobinary, and converts a raw page to a binary directly.
        my_raw_page = Image.open(image_directory)

        to_nparray = np.array(my_raw_page)        #cv2 only read np.array.
        my_grey_page = cv2.cvtColor(to_nparray, cv2.COLOR_BGR2GRAY)
        my_binary_page = cv2.adaptiveThreshold(
                                          my_grey_page, 255,  # change the gray image to binary
                                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY_INV, 15,
                                          18)

        if locationRef == None:
            return my_binary_page
        else:
            return Page.cropImg(locationRef,my_binary_page)

    @staticmethod
    def cropImg(locationRef, binaryPage):
        top, bottom, left, right = locationRef
        crop_img = binaryPage[top:bottom, left:right]

        return crop_img


    @staticmethod
    def display(any_page):
        plt.imshow(any_page, cmap='gray', interpolation='bicubic')  # display image
        plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
        plt.show()
    @staticmethod
    def show_images(images, numCol=3) -> None:
        n: int = len(images)
        f = plt.figure()
        for i in range(n):
            f.add_subplot(n, numCol, i + 1)  # (total # of img, num col, index in list)
            plt.xticks([]), plt.yticks([])
            plt.imshow(images[i], cmap='gray', interpolation='bicubic')
        plt.show(block=True)


    def show_cell_in_table(cell_images) -> None:
        nCol = len(cell_images[0])
        nrow = len(cell_images)


        cell_images_extract = [cell for row in cell_images for cell in row]
        f = plt.figure(figsize=(30, 80))
        for i in range(nrow*nCol):
            f.add_subplot(nrow, nCol, i + 1)  # (total # of img, num col, index in list)
            plt.xticks([]), plt.yticks([])
            plt.imshow(cell_images_extract[i], cmap='gray', interpolation='bicubic')


        plt.show(block=True)


        # expressed as a fraction of the average axis height


    @staticmethod
    def create_blankpage(size_referece_page):                   #create a blank (in black) page of the same size as self.
        page_height = len(size_referece_page)                  # no. rows of pixels
        page_width = len(size_referece_page[0])
        blank_page = zeros([page_height,page_width])
        return blank_page



    # load a raw page to nd.array, can use Page.display() to display the raw material.
    @staticmethod
    def load_colored (image_directory):
        my_raw_page = Image.open(image_directory)

        # top = 100  # crop the white edges
        # bottom = 2700
        # left = 360
        # right = 2232
        # cropped_page = my_raw_page.crop((left, top, right, bottom))

        to_nparray = np.array(my_raw_page)

        return to_nparray


    @staticmethod
    # one straight line
    # given a list of lines in the format of [x1, y1, x2, y2], draw lines on the page.
    # if want to display, draw very thick lines.

    def draw_lines(lines_list, page,thickness = 1, display = False):

        for i in range(len(lines_list)):
            x1 = lines_list[i][0]
            y1 = lines_list[i][1]
            x2 = lines_list[i][2]
            y2 = lines_list[i][3]

            lines = cv2.line(page, (x1,y1),(x2,y2),255,thickness)

        if display == True: Page.display(lines)

        return lines






