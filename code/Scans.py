# load scanned images

import glob
import cv2

class Scans:
                          #"public" class attirubutes should go here.
                       ##the constructor, class-attribute instance variable unique to each instance
    def __init__(self):
        self.scans_list = self.read_document()

    @staticmethod
    def read_document():                                 #at the moment, this function only read all .jpg under C:/myProjects/OCR/rawImages/ d
        my_scans_list = []
        path_list = glob.glob('C:/myProjects/OCR/rawImages/*.jpg')  # returns a list of path names that matches the input directory
        # print(path_list)
        for i in range(len(path_list)):
            my_page = cv2.imread(path_list[i])
            my_scans_list.append(my_page)
        numPage = len(my_scans_list)

        print("read all pages from the initial folder- done, successfully read: " , numPage, " pages")
        return my_scans_list

