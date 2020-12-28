


import os
from Page import Page
from Vertical import Vertical
import cv2
from OCR import OCR
import pandas as pd
from Horizontal import Horizontal
from Vertical import Vertical
import pytesseract
from Page import Page
import cv2
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
import sys
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
from PIL import Image, ImageOps
from statistics import mode
from pytesseract import Output
from Post import Post
import regex
import os
from datetime import datetime

def save_test_page(path, img, fileName):
    outPath = os.path.join(path,fileName)
    cv2.imwrite(outPath, img)


def batch_test_horizontal(path):
    dirs = os.listdir(path)[0:]
    numPage_to_test = 420
    i = 0
    problem_count = 0
    few_lines_count = 0
    problem_pages_noLines = []
    problem_pages_fewLines = []

    dir1 = "OR1865_page8,OR1865_page10,OR1865_page12,OR1865_page14,OR1865_page21,OR1865_page27,OR1865_page30,OR1865_page33,OR1865_page34,OR1865_page35,OR1865_page36,OR1865_page37," \
           "OR1865_page38,OR1865_page39,OR1865_page42,OR1865_page44,OR1865_page53,OR1865_page77," \
           "OR1865_page78,OR1865_page79,OR1865_page80,OR1865_page88,OR1865_page91,OR1865_page92," \
           "OR1865_page93,OR1865_page94,OR1865_page96,OR1865_page98,OR1865_page99,OR1865_page103," \
           "OR1865_page104,OR1865_page107,OR1865_page110,OR1865_page114,OR1865_page115,OR1865_page124" \
           ",OR1865_page125,OR1865_page132,OR1865_page133,OR1865_page134,OR1865_page135,OR1865_page136," \
           "OR1865_page137,OR1865_page138,OR1865_page140,OR1865_page141,OR1865_page145,OR1865_page147," \
           "OR1865_page149,OR1865_page150,OR1865_page151,OR1865_page152,OR1865_page153,OR1865_page154," \
           "OR1865_page155,OR1865_page156,OR1865_page159,OR1865_page160,OR1865_page165,OR1865_page169," \
           "OR1865_page171,OR1865_page174,OR1865_page181,OR1865_page183,OR1865_page185,OR1865_page190," \
           "OR1865_page195,OR1865_page199,OR1865_page200,OR1865_page201,OR1865_page202,OR1865_page203," \
           "OR1865_page204,OR1865_page205,OR1865_page206,OR1865_page208,OR1865_page210,OR1865_page214," \
           "OR1865_page216,OR1865_page217,OR1865_page218,OR1865_page220,OR1865_page227,OR1865_page228," \
           "OR1865_page231,OR1865_page233,OR1865_page234,OR1865_page238,OR1865_page241,OR1865_page245," \
           "OR1865_page247,OR1865_page248,OR1865_page250,OR1865_page267,OR1865_page269,OR1865_page273," \
           "OR1865_page277,OR1865_page281,OR1865_page284,OR1865_page285,OR1865_page287,OR1865_page289," \
           "OR1865_page290,OR1865_page292,OR1865_page296,OR1865_page297,OR1865_page298,OR1865_page300," \
           "OR1865_page301,OR1865_page303,OR1865_page304,OR1865_page305,OR1865_page306,OR1865_page307," \
           "OR1865_page309,OR1865_page310,OR1865_page311,OR1865_page312,OR1865_page313,OR1865_page315," \
           "OR1865_page317,OR1865_page318,OR1865_page319,OR1865_page321,OR1865_page322,OR1865_page323," \
           "OR1865_page324,OR1865_page327,OR1865_page328,OR1865_page329,OR1865_page330,OR1865_page331,OR1865_page332,OR1865_page341,OR1865_page348,OR1865_page358,OR1865_page360,OR1865_page364,OR1865_page365,OR1865_page366,OR1865_page367,OR1865_page368,OR1865_page369,OR1865_page380,OR1865_page386,OR1865_page389,OR1865_page394,OR1865_page395,OR1865_page406,OR1865_page411,OR1865_page415,OR1865_page417,OR1865_page418,OR1865_page420"
    dir2 = "OR1865_page27,OR1865_page33,OR1865_page34,OR1865_page35,OR1865_page36,OR1865_page37,OR1865_page38,OR1865_page53,OR1865_page55,OR1865_page59,OR1865_page77,OR1865_page78,OR1865_page79,OR1865_page80,OR1865_page88,OR1865_page91,OR1865_page92,OR1865_page93,OR1865_page94,OR1865_page96,OR1865_page98,OR1865_page99,OR1865_page103,OR1865_page105,OR1865_page107,OR1865_page110,OR1865_page124,OR1865_page132,OR1865_page133,OR1865_page134,OR1865_page135,OR1865_page136,OR1865_page137,OR1865_page138,OR1865_page139,OR1865_page140,OR1865_page141,OR1865_page145,OR1865_page147,OR1865_page149,OR1865_page150,OR1865_page151,OR1865_page152,OR1865_page153,OR1865_page154,OR1865_page155,OR1865_page156,OR1865_page159,OR1865_page160,OR1865_page165,OR1865_page169,OR1865_page171,OR1865_page174,OR1865_page183,OR1865_page190,OR1865_page195,OR1865_page199,OR1865_page200,OR1865_page201,OR1865_page202,OR1865_page203,OR1865_page204,OR1865_page205,OR1865_page206,OR1865_page208,OR1865_page210,OR1865_page214,OR1865_page215,OR1865_page216,OR1865_page217,OR1865_page218,OR1865_page220,OR1865_page231,OR1865_page233,OR1865_page234,OR1865_page235,OR1865_page238,OR1865_page241,OR1865_page243,OR1865_page245,OR1865_page247,OR1865_page250,OR1865_page252,OR1865_page267,OR1865_page269,OR1865_page273,OR1865_page277,OR1865_page281,OR1865_page284,OR1865_page285,OR1865_page287,OR1865_page289,OR1865_page290,OR1865_page296,OR1865_page297,OR1865_page298,OR1865_page299,OR1865_page300,OR1865_page301,OR1865_page303,OR1865_page304,OR1865_page305,OR1865_page307,OR1865_page309,OR1865_page310,OR1865_page311,OR1865_page312,OR1865_page313,OR1865_page315,OR1865_page317,OR1865_page319,OR1865_page321,OR1865_page322,OR1865_page323,OR1865_page324,OR1865_page327,OR1865_page328,OR1865_page329,OR1865_page330,OR1865_page331,OR1865_page335,OR1865_page357,OR1865_page364,OR1865_page365,OR1865_page366,OR1865_page367,OR1865_page368,OR1865_page369,OR1865_page389,OR1865_page394,OR1865_page395,OR1865_page406"
    dir = dir1 + "," + dir2
    dir = list(dir.split(','))
    for i in range(0, len(dirs)):
        # image_dir = "OR1865_page%s"%(str(i))+".jpg"
        image_dir = dir[i] + ".jpg"
        # do not proceed if the dir does not point to an image
        if ".jpg" not in image_dir:
            continue
        fileName = image_dir.split(".")[0]
        image_dir = path + image_dir
        print("******************page %s******************" % str(i))
        print(fileName)

        binary = Page.rawtobinary(image_directory=image_dir)
        colored = Page.load_colored(image_directory=image_dir)
        colored = imutils.resize(colored, height=3663, width=2831)

        colored = OCR.two_dimensional_deskew(colored, display=False, log=True, fileName=fileName)
        binary = Page.colored_to_binary(colored)

        try:
            dots_img = Horizontal.find_all_dots(binary)
            horizontal_lines = Horizontal.dotted_to_lines(dots_img)

            if len(horizontal_lines) < 5:
                few_lines_count += 1
                problem_pages_fewLines.append(fileName)
            filtered_horizontal_lines = Horizontal.filter(horizontal_lines, len(binary))
            populated_horizontal_lines = Horizontal.populate_lines(filtered_horizontal_lines, page_height=len(dots_img),
                                                                   page_width=len(dots_img[0]))

        except:
            problem_count += 1
            problem_pages_noLines.append(fileName)
            print("cannot process page %s, moving on to next one" % (fileName))

            log_img = colored.copy()
            log1 = Page.draw_lines(horizontal_lines, log_img.copy(), thickness=3, color=(255, 0, 0))

            fileName = fileName + ".png"
            outPath = r"D:\MLProjects\CVHistorical\out\mask\test20201126\horizontalS1_dot_to_lines"
            outPath = os.path.join(outPath, fileName)
            cv2.imwrite(outPath, log1)

            continue

        log_img = colored.copy()
        log1 = Page.draw_lines(horizontal_lines, log_img.copy(), thickness=3, color=(255, 0, 0))
        log2 = Page.draw_lines(filtered_horizontal_lines, log1.copy(), thickness=2, color=(0, 255, 0))
        log3 = Page.draw_lines(populated_horizontal_lines, log2.copy(), thickness=1, color=(0, 0, 255))

        # Page.display(log_img)
        # Page.display(log1)
        # Page.display(log2)
        # Page.display(log3)

        outPath = r"D:\MLProjects\CVHistorical\out\mask\test20201126\horizontalS0_dots_img"
        fileName = fileName + ".png"
        outPath = os.path.join(outPath, fileName)
        cv2.imwrite(outPath, dots_img)

        outPath = r"D:\MLProjects\CVHistorical\out\mask\test20201126\horizontalS1_dot_to_lines"
        outPath = os.path.join(outPath, fileName)
        cv2.imwrite(outPath, log1)

        outPath = r"D:\MLProjects\CVHistorical\out\mask\test20201126\horizontalS2_filter"
        outPath = os.path.join(outPath, fileName)
        cv2.imwrite(outPath, log2)

        outPath = r"D:\MLProjects\CVHistorical\out\mask\test20201126\horizontalS3_populate"
        outPath = os.path.join(outPath, fileName)
        cv2.imwrite(outPath, log3)

    meta = []
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    msg0 = "Test: Horiztonal, Vertical, OCR.getMask at %s on %s pages. " % (now, numPage_to_test - 7)
    print("Test: Horiztonal, Vertical, OCR.getMask at %s on %s pages. " % (now, numPage_to_test))
    msg1 = "end of test, found %s problems, problematic files are: " % (problem_count)
    msg2 = ','.join(problem_pages_noLines)
    print(msg1)
    print(msg2)
    msg3 = "%s pages have very few initially detected lines" % (str(few_lines_count))
    msg4 = ','.join(problem_pages_fewLines)
    print(msg3)
    print(msg4)
    total = str(few_lines_count + problem_count)
    msg5 = "in total, there are %s pages that do not have good horizontal line detections." % (total)
    print(msg5)
    meta.append([msg0, msg1, msg2, msg3, msg4, msg5])
    meta = meta[0]

    with open("meta_data.txt", "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)

        # Append text at the end of file
        for line in meta:
            file_object.write("\n" + line)

        file_object.write("\n-------------------------------------------------------------------------")

    # takes a function and batch test it on all images under path.

def batch_test_vertical(path):

    dirs = os.listdir(path)[0:]
    numPage_to_test = 414
    i = 0
    problem_count = 0
    problem_ct_noHLine = 0
    problem_ct_tooManyLines = 0
    problem_ct_tooFewLines = 0

    problem_pages= []
    problem_pages_noHLine = []
    problem_pages_tooManyLines = []
    problem_pages_tooFewLines = []

    for i in range(105, numPage_to_test):
        image_dir = dirs[i]
        if ".jpg" not in image_dir:
            continue
        fileName =  image_dir.split(".")[0]
        image_dir = os.path.join(path, image_dir)
        print("******************page %s******************" % str(i))
        print(fileName)
        fileName = fileName + ".png"

        # preprocess
        binary = Page.rawtobinary(image_directory=image_dir)
        colored = Page.load_colored(image_directory=image_dir)
        colored = imutils.resize(colored, height=3663, width=2831)
        colored = OCR.two_dimensional_deskew(colored,display = False, log = False, fileName = None)
        binary = Page.colored_to_binary(colored)
        raw = binary

        contours = Vertical.lookfor_vertical_contours(raw)
        lines_vertical_0 = Vertical.determine_houghlines(contours, display=False)

        if (len(lines_vertical_0) == 0) :
            print("no hough lines detected.")
            problem_ct_noHLine +=1
            problem_pages_noHLine.append(fileName)
            problem_pages.append(fileName)
            problem_count +=1
            outPath = r"D:\git\Sites\CVHistorical\test_out\Vertical_20201205\error_pages\noHLine"
            contours  = Page.display_overlay(contours, colored)
            outPath = os.path.join(outPath, fileName)
            cv2.imwrite(outPath, contours)

            continue

        lines_vertical = Vertical.finalize_vertical_line(lines_vertical_0, page_height=len(raw))

        if len(lines_vertical) > 6:
            problem_pages.append(fileName)
            problem_pages_tooManyLines.append(fileName)
            problem_count +=1
            problem_ct_tooManyLines +=1

            outPath = r"D:\git\Sites\CVHistorical\test_out\Vertical_20201205\error_pages\tooManyFinal\HLines"
            lines = Page.draw_lines(lines_vertical_0,colored,thickness=2, color=(0,255,0) )
            outPath = os.path.join(outPath, fileName)
            cv2.imwrite(outPath, lines)

            outPath = r"D:\git\Sites\CVHistorical\test_out\Vertical_20201205\error_pages\tooManyFinal\finalLines"
            lines = Page.draw_lines(lines_vertical,colored,thickness=2, color=(0,255,0) )
            outPath = os.path.join(outPath, fileName)
            cv2.imwrite(outPath, lines)

            continue

        elif len(lines_vertical)<6:
            problem_pages.append(fileName)
            problem_pages_tooFewLines.append(fileName)
            problem_count += 1
            problem_ct_tooFewLines +=1


            outPath = r"D:\git\Sites\CVHistorical\test_out\Vertical_20201205\error_pages\tooFewFinal\HLines"
            lines = Page.draw_lines(lines_vertical_0,colored,thickness=2, color=(0,255,0) )
            outPath = os.path.join(outPath, fileName)
            cv2.imwrite(outPath, lines)

            outPath = r"D:\git\Sites\CVHistorical\test_out\Vertical_20201205\error_pages\tooFewFinal\finalLines"
            lines = Page.draw_lines(lines_vertical,colored,thickness=2, color=(0,255,0) )
            outPath = os.path.join(outPath, fileName)
            cv2.imwrite(outPath, lines)

            continue


        log_img = colored.copy()
        log1 = Page.display_overlay(contours, log_img, show = False)
        log2= Page.draw_lines(lines_vertical_0,log1.copy(), thickness=2, color=(0,255,0))
        log3 = Page.draw_lines(lines_vertical,log2.copy(), thickness=2, color=(255,0,0))


        outPath = os.path.join(r"D:\git\Sites\CVHistorical\test_out\Vertical_20201205\contours",fileName)
        cv2.imwrite(outPath, log1)

        outPath = os.path.join(r"D:\git\Sites\CVHistorical\test_out\Vertical_20201205\houghlines",fileName)
        cv2.imwrite(outPath, log2)

        outPath = os.path.join(r"D:\git\Sites\CVHistorical\test_out\Vertical_20201205\finalLines",fileName)
        cv2.imwrite(outPath, log3)


    meta = []
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    msg0 = "Test:  Vertical, at %s on %s pages. "%(now,numPage_to_test)
    print(msg0)
    msg1 = "end of test, found %s problems, problematic files are: "%(problem_count)
    msg2 = ','.join(problem_pages)
    print(msg1)
    print(msg2)

    msg3 = "%s pages have too many detected vertical lines, these files are:  "% (problem_ct_tooManyLines)
    msg4 = ','.join(problem_pages_tooManyLines)
    msg5 = "%s pages have too few detected vertical lines, these files are: " % (problem_ct_tooFewLines)
    msg6 = ','.join(problem_pages_tooFewLines)
    msg7 = "cannot detect hough lines on contours for %s pages, these pages are"%(problem_ct_noHLine)
    msg8 = ','.join(problem_pages_noHLine)

    meta.append([msg0, msg1, msg2, msg3, msg4,msg5, msg6, msg7, msg8])
    meta = meta[0]

    print(msg3)
    print(msg4)
    print(msg5)
    print(msg6)
    print(msg7)
    print(msg8)

    with open("meta_data.txt", "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)

        # Append text at the end of file
        for line in meta:
            file_object.write("\n" + line)

        file_object.write("\n-------------------------------------------------------------------------")

    # takes a function and batch test it on all images under path.

