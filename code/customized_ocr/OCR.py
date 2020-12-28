
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






class OCR(Vertical, Horizontal):
    @staticmethod
    def two_dimensional_deskew(raw_colored, display = False, log = False, fileName = None):
        # https://becominghuman.ai/how-to-automatically-deskew-straighten-a-text-image-using-opencv-a0c30aed83df
        # Calculate skew angle of an image
        # Prep image, copy, convert to gray scale, blur, and threshold
        newImage = raw_colored.copy()
        gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
        thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY_INV)[1]

        # Apply dilate to merge text into meaningful lines/paragraphs.
        # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
        # But use smaller kernel on Y axis to separate between different blocks of text
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 3))
        dilate = cv2.dilate(thresh, kernel, iterations=10)


        # Find all contours
        contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)


        # Find largest contour and surround in min area box
        largestContour = contours[0]
        minAreaRect = cv2.minAreaRect(largestContour)

        if display == True:
            box = cv2.boxPoints(minAreaRect)
            box = np.int0(box)
            minAreaRect_box = raw_colored.copy()
            cv2.drawContours(minAreaRect_box, [box], 0, (0, 0, 255), 2)
            Page.display(minAreaRect_box)

        # Determine the angle. Convert it to the value that was originally used to obtain skewed image
        angle = minAreaRect[-1]
        if angle < -45:
            angle = 90 + angle

        rotation_angle =  -1.0 * angle

        # deskew is likely erroneous if the rotation angle is too big (>1)
        if abs(rotation_angle) > 0.55:
            angle  = 0
            print("deskew angle too big (%s), reverted to 0"%rotation_angle)

        # rotate image, given angle.
        (h, w) = raw_colored.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        deskewed_image = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        print("Deskew Correction Angle: ", rotation_angle)

        # to look at result, maybe overlay the two images.
        # Page.display_overlay(raw_colored, newImage)

        if log == True:
            showLargestCnt = raw_colored.copy()
            cv2.drawContours(showLargestCnt, [largestContour], 0, (255), -1)

            outPath = r"D:\MLProjects\CVHistorical\out\deskew\test20201125\cnt"
            fileName = fileName + ".png"
            outPath = os.path.join(outPath, fileName)
            cv2.imwrite(outPath, showLargestCnt)

            box = cv2.boxPoints(minAreaRect)
            box = np.int0(box)
            minAreaRect_box = raw_colored.copy()
            cv2.drawContours(minAreaRect_box, [box], 0, (0, 0, 255), 2)

            outPath = r"D:\MLProjects\CVHistorical\out\deskew\test20201125\rect"
            fileName = fileName + ".png"
            outPath = os.path.join(outPath, fileName)
            cv2.imwrite(outPath, minAreaRect_box)

            outPath = r"D:\MLProjects\CVHistorical\out\deskew\test20201125\out"
            fileName = fileName + ".png"
            outPath = os.path.join(outPath, fileName)
            cv2.imwrite(outPath, deskewed_image)

        return deskewed_image

    @staticmethod
    def get_mask(binary_image, colored, display = False, fileName = None):
        # takes binary  and detect vertical& horizontal lines
        raw = binary_image.copy()
        # detect horizontal borders
        dots = Horizontal.find_all_dots(binary_image, display = False)

        lines = Horizontal.dotted_to_lines(dots)
        Page.draw_lines(lines, binary_image, display= True)
        lines_filtered = Horizontal.filter(lines, len(raw))
        lines_horizontal = Horizontal.populate_lines(lines_filtered, len(raw[0]), len(raw) )
        mask_pic = Page.draw_lines(lines_horizontal, binary_image, display=False, thickness=3, color = (255, 255, 255))
        # detect vertical lines
        contours = Vertical.lookfor_vertical_contours(raw)
        lines_vertical_0 = Vertical.determine_houghlines(contours, display= False)
        lines_vertical = Vertical.finalize_vertical_line(lines_vertical_0, page_height=len(raw))

        mask_pic =  Page.draw_lines(lines_vertical, mask_pic,display=True, thickness=7)

        if display == True:
            display_pic = colored.copy()
            Page.draw_lines(lines_vertical, display_pic)
            Page.draw_lines(lines_horizontal, display_pic)
            Page.display(display_pic)
            Page.display(mask_pic)

        if fileName!= None:
            outPath = r"D:\MLProjects\CVHistorical\out\mask"
            fileName =  fileName + ".png"
            outPath = os.path.join(outPath, fileName)
            print("mask realted  file saved to : %s" % outPath)
            cv2.imwrite(outPath,mask_pic)

            outPath = r"D:\MLProjects\CVHistorical\out\mask\test20201125\horizontal_S1"
            outPath = os.path.join(outPath, fileName)

            a = Page.draw_lines(lines, colored.copy(), thickness=3)
            cv2.imwrite(outPath, a)

            outPath = r"D:\MLProjects\CVHistorical\out\mask\test20201125\horizontal_S2"
            outPath = os.path.join(outPath, fileName)
            b = Page.draw_lines(lines_filtered, colored.copy(), thickness=3)
            cv2.imwrite(outPath, b)


            outPath = r"D:\MLProjects\CVHistorical\out\mask\test20201125\horizontal_S3"
            outPath = os.path.join(outPath, fileName)
            c =  Page.draw_lines(lines_horizontal, colored.copy(), thickness=3)
            cv2.imwrite(outPath, c)

        return lines_horizontal,lines_vertical, mask_pic

    @staticmethod
    def split_cells(raw_colored_image, lines_horizontal, lines_vertical, display = False,  topRowIdx = 50, bottomRowIdx = 55, leftColIdx = 0, rightColIdx = 5, fileName = None):
        # takes raw image (colored) return cropped image of cells/ ROI
        # output is unprocessed cells.

        img = cv2.cvtColor(raw_colored_image, cv2.COLOR_BGR2RGB)
        cells = []

        for i in range(topRowIdx,bottomRowIdx):
            myRow= []
            for j in range(leftColIdx,rightColIdx):
                offset = 10
                # top = max(int(lines_horizontal[i][1])-offset/2,0)
                top = int(lines_horizontal[i][1])
                bottom = int(lines_horizontal[i + 1][1]) + offset
                left = int(lines_vertical[j][0])
                right = int(lines_vertical[j + 1][0])

                myCell = Page.cropImg([top, bottom, left, right], img)
                myRow.append(myCell)

                # if it is just a single picture, then directly return 1 pciture.
                if (bottomRowIdx - topRowIdx == 1) and (rightColIdx - leftColIdx == 1 ):
                    return myCell

            cells.append(myRow)

        if display == True:
            Page.show_cell_in_table(cells)
        if fileName != None:
            outPath = r"D:\MLProjects\CVHistorical\out\cell_roi"
            fileName =  fileName + ".png"
            outPath = os.path.join(outPath, fileName)
            print("roi and output  file saved to : %s" % outPath)
            Page.show_cell_in_table(cells, fileName = outPath)


        return cells

    @staticmethod
    def inspect_pytesseract_ROI_recognition(cell, demo_picture, config, col = None, display = False):
        # this method investigates what pytesseract recognizes as ROI
        # it takes one segmented cell pictures and returns a demostration of the OCR results.
        # combined with Page_to_df()

        d = pytesseract.image_to_data(cell, output_type=Output.DICT, config = config)
        n_boxes = len(d['level'])
        for i in range(n_boxes):
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            cv2.rectangle(demo_picture, (x, y), (x + w, y + h), (255, 0, 0), 2)

        if display == True: Page.display(demo_picture)
        return demo_picture

    @staticmethod
    def delete_noise(cell, target_cnts, isMask = False):
        #https://stackoverflow.com/questions/54485543/removing-contours-from-an-image
        #delete a set of target contours from a image
        # Page.display(cell)
        if isMask == False:
            mask = np.zeros(cell.shape[:2], dtype=cell.dtype)

            # loop over the contours
            for cnt in target_cnts:
                # if the contour is bad, draw it on the mask
                cv2.drawContours(mask, [cnt], 0, (255), -1)

        elif isMask == True:
            mask = target_cnts.copy()
        mask = cv2.bitwise_not(mask)
        # Page.display(mask)
        # remove the contours from the image and show the resulting images
        cleaned_cell = cv2.bitwise_and(cell, cell, mask=mask)
        # Page.display(cleaned_cell)
        return cleaned_cell

    @staticmethod
    def ROI_to_text(image, col, inspect = False):

        # https://github.com/lavanya-m-k/character-detection-and-crop-from-an-image-using-opencv-python
        # tesseract only correctly recognize if the image is resized.
        image = imutils.resize(image, height=100)

        # local denoise + binarization
        myCell = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)[1]

        # get unique color to replace
        # print("unique colors on picture: ")
        # print(np.unique(myCell.reshape(-1, myCell.shape[2]), axis=0))

        # # red & yellow color to white
        myCell[np.where((myCell == [255, 255, 0]).all(axis=2))] = [255, 255, 255]
        myCell[np.where((myCell == [255, 0, 0]).all(axis=2))] = [255, 255, 255]

        # convert to binary gray scale (easier to print)
        gray = cv2.cvtColor(myCell, cv2.COLOR_RGB2GRAY)

        # dilate
        kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2,5))
        kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3,1))
        dilated = cv2.dilate(gray, kernel1)
        dilated = cv2.dilate(dilated, kernel2)
        dilated = cv2.dilate(dilated, kernel3)



        # blurring makes the dots more elliptical-like
        ret, thresh1 = cv2.threshold(dilated, 127, 255, cv2.THRESH_BINARY)
        # https://github.com/lavanya-m-k/character-detection-and-crop-from-an-image-using-opencv-python

        contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # create a mask that to draw ROI rectangles on. tesseract works better with pre-determined mask for segmentation.
        mask = np.zeros(myCell.shape, dtype=np.uint8)
        cnt_rect = image.copy()    #stores the boxes recognized by contour detection.
        # all_recognized_regions_demo = image.copy()
        deletion_target = []

        # cnt_vi = Page.create_blankpage(image)
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # cv2.rectangle(all_recognized_regions_demo, (x, y), (x + w, y + h), (0, 255, 0), 3)

            # bound the images
            if w > 16 and h > 30:
                # first char is 95, thinner char 25, normal char 50.
                # if it is the first char, w>100 considered >2 char.
                # if it is not the first char, w> 75 considered > 2char.
                # cv2.drawContours(cnt_vi, [cnt],0, (255, 255, 255), 2)
                cv2.rectangle(cnt_rect, (x, y), (x + w, y + h), (0, 255,0), 3)
                cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), -1)

                if  (y ==0) and (h <=70):
                    deletion_target.append(cnt)
            else:
                deletion_target.append(cnt)

        # Page.display(cnt_vi)
        # Page.display(all_recognized_regions_demo)
        myCell = OCR.delete_noise(myCell, deletion_target)
        myCell = np.invert(myCell)   # it seems that tesseract only works well with white back ground and black text, not binaries with black background.

        # Bitwise-and to isolate characters
        # https: // stackoverflow.com / questions / 60066481 / recognize - single - characters - on - a - page -
        # with-tesseract

        result = cv2.bitwise_and(myCell, mask)
        result[mask == 0] = 255

        # OCR
        if col in [0, 1, 2]:
            config = '--psm 6 -c tessedit_debug_fonts=1 -c tessedit_char_whitelist=" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ()" -c preserve_interword_spaces=1'
            data = pytesseract.image_to_string(result, lang='eng', config= config)

        elif col in [3,4]:
            config = '--psm 6 outputbase digits -c tessedit_debug_fonts=1 -c preserve_interword_spaces=1 -c tessedit_char_whitelist=1234567890\s$ -c tessedit_char_blacklist=.|'
            data = pytesseract.image_to_string(result, lang='eng', config= config)

        elif col == "header":
            config = '--psm 6 -c tessedit_char_blacklist=.|! '

            # config = '--psm 7 outputbase digits -c tessedit_char_blacklist=.| '
            data = pytesseract.image_to_string(result, lang='eng', config=config)


        if inspect == 'TESS':
            demo_inspect = OCR.inspect_pytesseract_ROI_recognition(result, cnt_rect, config=config, col=col)
            result = demo_inspect
        elif inspect == 'CNT_RECT':
            result = cnt_rect



        data = data[:-2]
        # print(data)
        # if "\n" in data:
        #     Page.display(myCell)
        out = OCR.draw_text(result, data)

        # Page.show_images([image, result, myCell, thresh01, thresh02])
        return data, out

    @staticmethod
    def draw_text(img, text):
        # add padding at bottom
        top = 0
        bottom = 0 + len(img)
        left = 0
        right = 0
        img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value = (255,255,255))

        font = cv2.FONT_HERSHEY_COMPLEX
        bottomLeftCornerOfText = (3, len(img)-3)
        fontScale = 3
        fontColor = (0, 0, 255)
        lineType = 2

        labeled_img = cv2.putText(img, text,
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    lineType)
        return labeled_img

    @staticmethod
    def get_general_ROIs(raw_colored, binary_page, display = False):
        raw_colored = cv2.cvtColor(raw_colored, cv2.COLOR_BGR2RGB) # turn it blue, basically, to integrate with the ROI_to_text method
        newImage = raw_colored.copy()
        newImage = OCR.two_dimensional_deskew(newImage)
        # Page.display(newImage)
        gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
        # blur = cv2.GaussianBlur(gray, (9, 9), 255)

        thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)[1]
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
        detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=5)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (300, 2))
        detect_horizontal = cv2.dilate(detect_horizontal,kernel, iterations = 3)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1000, 4))
        detect_horizontal = cv2.dilate(detect_horizontal,kernel, iterations = 2)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 20))
        detect_horizontal = cv2.dilate(detect_horizontal,kernel, iterations = 2)

        gray_denosied = OCR.delete_noise(thresh, detect_horizontal, isMask = True)
        # displayovl = Page.display_overlay(detect_horizontal, newImage)
        # cv2.imwrite(r"logs/20201119_psm_header_detection_noise_OTD16_2.png",  displayovl)

        # transform binary page again for header detection, now without the noises of horizontal lines.
        blur = cv2.GaussianBlur(gray_denosied, (9, 9), 0)
        thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)[1]

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 3))
        dilate = cv2.dilate(thresh, kernel, iterations=5)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 3))
        dilate = cv2.dilate( dilate , kernel, iterations=5)

        # Find all contours
        contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        if display == True:
            out_illustrate = raw_colored.copy()

        ROI_rect_list = []
        for cnt in contours:
            #area = cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            rect = [x, y, w, h]
            if h > 30:
                ROI_rect_list.append(rect)
                if display == True:
                    cv2.rectangle(out_illustrate, (x, y), (x + w, y + h), (255, 0, 0), 3)
                    cv2.drawContours(out_illustrate, [cnt], 0, (0, 0, 255), 2)


        if display == True:
            Page.display(out_illustrate)





        # cv2.imwrite(r"logs/20201119_psm_header_detection_OTD16_cmp_nodenoise.png", out_illustrate)
        return ROI_rect_list

    @staticmethod
    def OCR_general_ROIs(colored ,ROIs_rect,display = False, fileName = None):

        colored = cv2.cvtColor(colored, cv2.COLOR_RGB2BGR)

        ROIs_rect.sort(key = lambda x: x[1])
        out_pics = []
        header_list = []

        for [x,y,w,h] in ROIs_rect:

            padding = 10
            if display == True:
                cv2.rectangle(colored, (x, y), (x + w, y + h + padding), (255, 0, 0), 3)
            ROI_pic = Page.cropImg([y, y + h , x, x+w], colored)
            data, img = OCR.ROI_to_text(ROI_pic, col= "header", inspect = 'TESS') # means that it will be recognized

            out_pics.append(img)
            if data != '':
                header_list.append([data, (x,y,w,h)])
            elif h>100:
                header_list.append(["potential text body", (x,y,w,h)])

        # look for 'department' or 'state names' in string.

        if display == True:
            Page.display(colored)
            Page.show_images(out_pics, numCol=1)

        # if fileName != None:
        #     outPath = r"D:\MLProjects\CVHistorical\out\pre_sec_roi"
        #     fileName = fileName + ".png"
        #     outPath = os.path.join(outPath, fileName)
        #     print("pre-General ROI detection file saved to : %s" % outPath)
        #     Page.show_images(out_pics, outPath = outPath)


        return header_list

    @staticmethod
    def classify_general_ROIs(header_list, img = None, display = False, fileName = None):
        sorted_section_dict = Post.analyze_page_sections(header_list)

        if (display == True) or (fileName!=None):
            for item in sorted_section_dict.items():
                section_content_label = item[0]
                (x,y,w,h) = item[1][1]

                font = cv2.FONT_HERSHEY_COMPLEX
                bottomLeftCornerOfText = (x+w, y+h - 3)
                fontScale = 2
                fontColor = (0, 0, 255)
                lineType = 2

                labeled_img = cv2.putText(img, "<-"+ section_content_label,
                                          bottomLeftCornerOfText,
                                          font,
                                          fontScale,
                                          fontColor,
                                          lineType)

                if regex.match("^office_header", item[0]) != None:
                    state_label = "state: " + item[1][0]
                    bottomLeftCornerOfText = (x + w, y + h - 3 + 50)
                    labeled_img = cv2.putText(img,  state_label,
                                              bottomLeftCornerOfText,
                                              font,
                                              fontScale,
                                              fontColor,
                                              lineType)

                cv2.rectangle( labeled_img, (x, y), (x + w, y + h), (255, 0, 0), 2)

            if display == True:
                Page.display(labeled_img)

            if fileName != None:
                outPath = r"D:\MLProjects\CVHistorical\out\sec_roi"
                fileName = fileName + ".png"
                outPath = os.path.join(outPath, fileName)
                print("General ROI detection file saved to : %s" % outPath)
                cv2.imwrite(outPath, labeled_img)

        return sorted_section_dict

    @staticmethod
    def section_to_df(ROI_table_bi, ROI_table_co, display= False, fileName = None):
        lines_horizontal, lines_vertical, mask_pic = OCR.get_mask(ROI_table_bi, ROI_table_co, display=False, fileName = fileName)
        cells = OCR.split_cells(ROI_table_co, lines_horizontal, lines_vertical, display=True, topRowIdx=0,
                                bottomRowIdx= len(lines_horizontal)-1 ,
                                leftColIdx=0, rightColIdx=5)


        table = cells.copy()
        out = []
        out_pic = []
        for row in table:
            myRowOut = []
            myRowOut_pic = []
            col = 0
            for cell in row:
                # data, img = OCR.ROI_to_text(cell, col=col)
                data, img = OCR.ROI_to_text(cell, col=col, inspect='TESS')
                myRowOut.append(data)
                myRowOut_pic.append(img)
                col += 1

            out.append(myRowOut)
            out_pic.append(myRowOut_pic)

        df_new = pd.DataFrame(out)

        if display == True:
            Page.show_cell_in_table(out_pic)

        if fileName!= None:
            outPath = r"D:\MLProjects\CVHistorical\out\cell_roi"
            fileName =  fileName + ".png"
            outPath = os.path.join(outPath, fileName)
            print("roi and output  file saved to : %s" % outPath)
            Page.show_cell_in_table(out_pic, fileName = outPath)



        return df_new

    @staticmethod
    def page_to_DF(colored, binary, display=False, inspect=False, fileName = None):

        colored = imutils.resize(colored, height=3663, width=2831)
        colored =  OCR.two_dimensional_deskew(colored)
        binary = Page.colored_to_binary(colored)


        # this function assembles split_cells, ROI to text, returns a df
        ROI_rect = OCR.get_general_ROIs(colored, binary, display=False)
        header_list = OCR.OCR_general_ROIs(colored, ROI_rect, display=False, fileName = fileName)

        sections_dict = OCR.classify_general_ROIs(header_list, img=colored, display=False, fileName = fileName)

        department = [item[1] for item in sections_dict.items() if regex.match("^department", item[0]) != None]
        headers = [item[1] for item in sections_dict.items() if regex.match("^office_header", item[0]) != None]
        tables = [item[1] for item in sections_dict.items() if regex.match("^table_body", item[0]) != None]

        df = pd.DataFrame()
        for i in range(0, len(tables)):
            try:
                state = headers[i][0]
            except:
                print(">>>>>>>>>>>>>>>>Error: cannot parse state name.<<<<<<<<<<<<<<<<<<")
            (x,y,w,h) = tables[i][1]

            ROI_table_bi = Page.cropImg([y, y+h, 0,len(binary[0])], binary)
            ROI_table_co = Page.cropImg([y, y+h, 0,len(binary[0])], colored)

            if len(tables) > 1:
                fileName = fileName + "_sec%s"%i
            df_new = OCR.section_to_df(ROI_table_bi, ROI_table_co, display = False, fileName = fileName )

            try:
                df_new['state'] = state
            except:
                print("con")

            df = pd.concat([df, df_new], ignore_index= True)

        return df

    @staticmethod
    def dir_to_df(path):
        dirs = os.listdir(path)[0:]
        numPage_to_gen = 100
        i = 0
        for image_dir in dirs:

            # do not proceed if the dir does not point to an image
            if ".jpg" not in image_dir:
                continue

            fileName =  image_dir.split(".")[0]
            image_dir = path + image_dir
            print("******************page %s******************" % str(i))
            colored = Page.load_colored(image_directory=image_dir)
            colored = imutils.resize(colored, height=3663, width=2831)
            colored = OCR.two_dimensional_deskew(colored)
            binary = Page.colored_to_binary(colored)



            i+=1

            if i>= numPage_to_gen:
                break

    @staticmethod
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
        dir = dir1  + "," + dir2
        dir = list(dir.split(','))
        for i in range(0, len(dirs)):
            # image_dir = "OR1865_page%s"%(str(i))+".jpg"
            image_dir = dir[i] + ".jpg"
            # do not proceed if the dir does not point to an image
            if ".jpg" not in image_dir:
                continue
            fileName =  image_dir.split(".")[0]
            image_dir = path + image_dir
            print("******************page %s******************" % str(i))
            print(fileName)

            binary = Page.rawtobinary(image_directory=image_dir)
            colored = Page.load_colored(image_directory=image_dir)
            colored = imutils.resize(colored, height=3663, width=2831)

            colored = OCR.two_dimensional_deskew(colored,display = False, log = True, fileName = fileName)
            binary = Page.colored_to_binary(colored)

            try:
                dots_img = Horizontal.find_all_dots(binary)
                horizontal_lines = Horizontal.dotted_to_lines(dots_img)

                if len(horizontal_lines) <5:
                    few_lines_count +=1
                    problem_pages_fewLines.append(fileName)
                filtered_horizontal_lines = Horizontal.filter(horizontal_lines, len(binary))
                populated_horizontal_lines = Horizontal.populate_lines(filtered_horizontal_lines, page_height= len(dots_img), page_width=len(dots_img[0]))

            except:
                problem_count +=1
                problem_pages_noLines.append(fileName)
                print("cannot process page %s, moving on to next one"%(fileName))

                log_img = colored.copy()
                log1 = Page.draw_lines(horizontal_lines, log_img.copy(), thickness=3, color=(255, 0, 0))

                fileName = fileName + ".png"
                outPath = r"D:\MLProjects\CVHistorical\out\mask\test20201126\horizontalS1_dot_to_lines"
                outPath = os.path.join(outPath, fileName)
                cv2.imwrite(outPath, log1)

                continue



            log_img = colored.copy()
            log1 = Page.draw_lines(horizontal_lines,log_img.copy(), thickness=3, color= (255,0,0))
            log2= Page.draw_lines(filtered_horizontal_lines,log1.copy(), thickness=2, color=(0,255,0))
            log3 = Page.draw_lines(populated_horizontal_lines,log2.copy(), thickness=1, color=(0,0,255))

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
        msg0 = "Test: Horiztonal, Vertical, OCR.getMask at %s on %s pages. "%(now,numPage_to_test-7)
        print("Test: Horiztonal, Vertical, OCR.getMask at %s on %s pages. "%(now,numPage_to_test))
        msg1 = "end of test, found %s problems, problematic files are: "%(problem_count)
        msg2 = ','.join(problem_pages_noLines)
        print(msg1)
        print(msg2)
        msg3 = "%s pages have very few initially detected lines"%(str(few_lines_count))
        msg4 = ','.join(problem_pages_fewLines)
        print(msg3)
        print(msg4)
        total = str(few_lines_count + problem_count)
        msg5 = "in total, there are %s pages that do not have good horizontal line detections."%(total)
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

    @staticmethod
    def batch_test_vertical(path):

        dirs = os.listdir(path)[0:]
        numPage_to_test = 414
        i = 0
        problem_count = 0
        problem_pages= []

        for i in range(0, numPage_to_test):
            image_dir = dir[i] + ".jpg"
            if ".jpg" not in image_dir:
                continue
            fileName =  image_dir.split(".")[0]
            image_dir = path + image_dir
            print("******************page %s******************" % str(i))
            print(fileName)
            fileName = fileName + ".png"

            # preprocess
            binary = Page.rawtobinary(image_directory=image_dir)
            colored = Page.load_colored(image_directory=image_dir)
            colored = imutils.resize(colored, height=3663, width=2831)
            colored = OCR.two_dimensional_deskew(colored,display = False, log = False, fileName = None)
            binary = Page.colored_to_binary(colored)

            try:
                contours = Vertical.lookfor_vertical_contours(raw)
                lines_vertical_0 = Vertical.determine_houghlines(contours, display=False)
                lines_vertical = Vertical.finalize_vertical_line(lines_vertical_0, page_height=len(raw))

            except:
                problem_count +=1
                problem_pages.append(fileName)
                print("cannot process page %s, moving on to next one"%(fileName))

                log_img = colored.copy()
                log0 = contours
                log00 = Page.draw_lines(lines_vertical_0 , log_img.copy(), thickness=3, color=(255, 0, 0))


                outPath0 = os.makedirs( r"D:\git\Sites\CVHistorical\test_out\Vertical_20201205\error_pages\contours", exist_ok=True)
                outPath0 = os.path.join(outPath0, fileName)
                cv2.imwrite(outPath0, log0)

                outPath00= os.makedirs( r"D:\git\Sites\CVHistorical\test_out\Vertical_20201205\error_pages\houghlines", exist_ok=True)
                outPath00 = os.path.join(outPath00, fileName)
                cv2.imwrite(outPath00, log00)


                continue



            log_img = colored.copy()
            log1 = Page.display_overlay(contours, log_img)
            Page.display(log1)
            log2= Page.draw_lines(lines_vertical_0,log1.copy(), thickness=2, color=(0,255,0))
            log3 = Page.draw_lines(lines_vertical,log2.copy(), thickness=1, color=(0,0,255))


            outPath = os.makedirs(r"D:\git\Sites\CVHistorical\test_out\Vertical_20201205\contours",exist_ok=True)
            outPath = os.path.join(outPath, fileName)
            cv2.imwrite(outPath, log1)

            outPath = os.makedirs(r"D:\git\Sites\CVHistorical\test_out\Vertical_20201205\houghlines",exist_ok=True)
            outPath = os.path.join(outPath, fileName)
            cv2.imwrite(outPath, log2)

            outPath = os.makedirs(r"D:\git\Sites\CVHistorical\test_out\Vertical_20201205\houghlines",exist_ok=True)
            outPath = os.path.join(outPath, fileName)
            cv2.imwrite(outPath, log3)


        meta = []
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        msg0 = "Test:  Vertical, at %s on %s pages. "%(now,numPage_to_test)
        print(msg0)
        msg1 = "end of test, found %s problems, problematic files are: "%(problem_count)
        msg2 = ','.join(problem_pages)
        print(msg1)
        print(msg2)

        meta.append([msg0, msg1, msg2])
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


