# pip3 install opencv-python to install OpenCV
import cv2
from Page import Page
import matplotlib
from Horizontal import Horizontal
from Vertical import Vertical
import numpy as np
import sys
import pytesseract
from OCR import OCR
from collections import Counter
import imutils
from PIL import Image
import pandas as pd
import os
from Post import Post
from Post import Name
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
a = pytesseract.get_tesseract_version()
print(a)

pd.set_option("display.max_columns", 10)
pd.set_option("display.max_rows", 200)
np.set_printoptions(linewidth=5000, threshold=5000)

binary = Page.rawtobinary(image_directory = "test_Page_11.jpg")
colored = Page.load_colored("test_Page_11.jpg")
colored = imutils.resize(colored, height=3663, width=2831)
binary = imutils.resize(binary, height=3663, width=2831)

OCR.Page_to_DF(colored, binary, display = True, inspect = True)

# **********************clean df using chunk processing and then reload.
# inpath = r"D:\MLProjects\CVHistorical\external_data\1850_to_1880_names_only.csv"
# # df = pd.read_csv("1850_to_1880_unique_first_names.csv")
# outpath = r"D:\MLProjects\CVHistorical\external_data\1850_to_1880_unique_last_names.csv"
# Name.chunk_process(write_meta= True,  func = Name.map_process_names, inpath= inpath, outpath = outpath, col_name = "NAMEFRST" )
# df = pd.read_csv(outpath)
# print(df)
#
# outpath = r"D:\MLProjects\CVHistorical\external_data\1850_to_1880_unique_first_names.csv"
# Name.chunk_process(write_meta= True,  func = Name.map_process_names, inpath= inpath, outpath = outpath , col_name = "NAMELAST")
# df = pd.read_csv(outpath)
# print(df)














# df = pd.read_csv("test.csv")
# header = pd.read_csv("header.csv")
# # a = Post.clean_header(header)
#
# # a = Name.load_census_feature(r"D:\MLProjects\CVHistorical\external_data\1850_to_1880_names_only.csv")
# #
#
# a = Name.chunk_process(func = Name.map_process_NAMEFRST, filepath = r"D:\MLProjects\CVHistorical\external_data\1850_to_1880_names_only.csv")
#




# header, out = OCR.page_to_df_and_header("OR_test_0.jpg", display= True)
# print(header)



# a = pd.read_csv("test2.csv")
# print(a)

# "OR_test_departs_11.jpg"
# cannot detect the leftmost border for this sample.

# colored = Page.load_colored("test_Page_10.jpg")
# binary = Page.rawtobinary("test_Page_10.jpg")
# header, out = OCR.page_to_df_and_header("OR_test_0.jpg", display= True)
# print(header, out)
# fix detect vertical
# then use the ETL loop

# ETL loop:
#
# dir = r"C:\Users\Mengyue Zhao\PycharmProjects\cv3\venv\OR_pages"
# pageNames = os.listdir(dir)
#
#
# for pageName in pageNames:
#     path = dir +  "/"+ pageName
#     # colored = Page.load_colored(path)
#     # binary_page = Page.colored_to_binary(colored)
#     OCR.page_to_df_and_header(path)



# for i in range(1, 12):
#     pageNum = str(i) if i >=10 else str(0) + str(i)
#     path = "test_Page_" + pageNum + ".jpg"
#     binary = Page.rawtobinary(path)
#     OCR.get_header_ROIs(binary)

# out = OCR.Page_to_DF("test_Page_11.jpg", display = False)




# OCR.get_header_ROIs(colored,binary_page , display = True)



# OCR.get_header_text(binary)

# a= OCR.preprocess("test_Page_11.jpg")
# # b = OCR.get_header_ROIs(a)



# c = OCR.Page_to_DF("test_Page_11.jpg")



# print(out)
# horizontal, vertical, pic, raw= OCR.get_mask('test_Page_11.jpg', display = False)
# raw = Page.load_colored('test_Page_11.jpg')
# img = raw.copy()
# input = img.copy()
# cell = OCR.split_cells(img, horizontal, vertical,17,27,0,5)
#
# # cell = OCR.remove_trailing_dots_deprec(cell)

#
# table = cell.copy()
# out = []
# out_pic = []
# for row in table:
#     myRowOut = []
#     myRowOut_pic = []
#     col = 0
#     for cell in row:
#         data, img = OCR.ROI_to_text(cell, col = col, display = True)
#         myRowOut.append(data)
#         myRowOut_pic.append(img)
#         col += 1
#
#     out.append(myRowOut)
#     out_pic.append(myRowOut_pic)
#
# out = pd.DataFrame(out)
# print(out)
#
# # Page.display(input)
# Page.show_cell_in_table(out_pic)




#

# assemble
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
# print("heer")
# # temporary changes:
# # under page, raw to img, removed cropping temporarily.
#
# # tool1. display to display an cv image object (?)
# # Page.display(a)
#
#
# #
# print("d")
# np.set_printoptions(linewidth=3000, threshold = 3000)
#
# # Step1. load raw page to view
# a = Page.rawtobinary('test_Page_11.jpg')
# # a= Page.cropImg([1000, 1000+ 600, 500, 1500], a)
# Page.display(a)
# #
# m = Horizontal.find_all_dots(a, display = False)
# n = Horizontavenv2/cv1.py:64l.dotted_to_lines(m, display = False)
# k = Horizontal.filter(n, len(m))
# k= Horizontal.populate_lines(k, len(a[0]), len(a))
# a = Page.draw_lines(k, a,display = False,thickness = 5)
#
# #
# contours= Vertical.lookfor_vertical_contours(a)
# lines_pts = Vertical.determine_houghlines(contours,display = False)
# final_vertical = Vertical.finalize_vertical_line(lines_pts, page_height = len(a))
# print("height," , len(a))
# a = Vertical.draw_line(a,final_vertical , display = False, thickness = 7)
# # a = Page.cropImg([650, 800,500, 500+100],a)






#*****************************************************************88
# intro
# a = cv2.cvtColor(a, cv2.COLOR_GRAY2RGB)
# a = Page.cropImg([500, 800,500, 500+100], a)


#
# Page.display(a)
# print("B")
# # print(pytesseract.image_to_boxes(a))
# print("C")



#Vertical.draw_line(blank,(0,599),(100,599),color =255, thickness = 4,display = False)
# finals = Vertical.finalize_vertical_line(lines_pts,len(a), monitor = True)


# cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB)

# p = Page.rawtobinary('eg1.jpg')
# Vertical.create_column_borders(p,draw=False)

# m = Horizontal.find_all_dots(a, display = True, customKernel = )
# m = Horizontal.find_all_dots(a, display = True)


# Step2. turn raw page to binary image, cuts the white edges too.
# need to fix white edge cutting.
# p = Page.rawtobinary('test_Page_09.jpg')
# Page.display(p)
# print(len(p))
# to draw a line
# Page.draw_lines([[100,1000, 100, 0]], a,display = True)

# detect all single dot patterns with blank surroudings
# m = Horizontal.find_all_dots(p, display = True)
# Page.display(m)


# detect horizontal lines with surroundings.
# Horizontal.dotted_to_lines(m, display = True)
# Page.draw_lines(lines, a, display = True)
