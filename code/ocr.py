
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





class OCR(Vertical, Horizontal):
    @staticmethod
    def two_dimensional_deskew(raw_colored, display = False):
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
        dilate = cv2.dilate(thresh, kernel, iterations=5)
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

        # rotate image, given angle.
        (h, w) = raw_colored.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        deskewed_image = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        print("Deskew Correction Angle: ", rotation_angle)

        # to look at result, maybe overlay the two images.
        # Page.display_overlay(raw_colored, newImage)

        return deskewed_image

    @staticmethod
    def get_mask(binary_image, colored, display = False):
        # takes binary  and detect vertical& horizontal lines
        # colored = Page.load_colored("test_Page_10.jpg")
        # colored = imutils.resize(colored, 3663, 2831)
        #
        # colored = Page.load_colored("test_Page_10.jpg")
        raw = binary_image.copy()
        # detect horizontal borders
        dots = Horizontal.find_all_dots(binary_image, display = False)
        lines, lines_dilated = Horizontal.dotted_to_lines(dots)
        lines_filtered = Horizontal.filter(lines, len(raw))
        lines_horizontal = Horizontal.populate_lines(lines_filtered, len(raw[0]), len(raw) )

        mask_pic = Page.draw_lines(lines_horizontal, binary_image, display=False, thickness=3, color = (255, 255, 255))

        # detect vertical lines
        contours = Vertical.lookfor_vertical_contours(raw)
        lines_vertical = Vertical.determine_houghlines(contours, display= False)
        lines_vertical = Vertical.finalize_vertical_line(lines_vertical, page_height=len(raw))

        mask_pic =  Page.draw_lines(lines_vertical, mask_pic,display=False, thickness=7)

        if display == True:
            display_pic = colored.copy()
            Page.draw_lines(lines_vertical, display_pic)
            Page.draw_lines(lines_horizontal, display_pic)
            # cv2.imwrite(r"logs/20201119_page_segmentation.png", display_pic)
            Page.display(display_pic)
            Page.display(mask_pic)

        return lines_horizontal,lines_vertical, mask_pic

    @staticmethod
    def split_cells(raw_colored_image, lines_horizontal, lines_vertical, display = False,  topRowIdx = 50, bottomRowIdx = 60, leftColIdx = 0, rightColIdx = 5):
        # takes raw image (colored) return cropped image of cells/ ROI
        # output is unprocessed cells.

        print("vertical lines")
        print(lines_vertical)
        img = cv2.cvtColor(raw_colored_image, cv2.COLOR_BGR2RGB)
        cells = []
        for i in range(topRowIdx,bottomRowIdx):
            myRow= []
            for j in range(leftColIdx,rightColIdx):
                offset = 10
                top = int(lines_horizontal[i][1])
                bottom = int(lines_horizontal[i + 1][1]) + offset
                left = int(lines_vertical[j][0])
                right = int(lines_vertical[j + 1][0])

                myCell = Page.cropImg([top, bottom, left, right], img)
                myRow.append(myCell)

                if (bottomRowIdx - topRowIdx == 1) and (rightColIdx - leftColIdx == 1 ):
                    return myCell

            cells.append(myRow)

        if display == True: Page.show_cell_in_table(cells)

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


        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # cv2.rectangle(all_recognized_regions_demo, (x, y), (x + w, y + h), (0, 255, 0), 3)

            # bound the images
            if w > 16 and h > 30:
                # first char is 95, thinner char 25, normal char 50.
                # if it is the first char, w>100 considered >2 char.
                # if it is not the first char, w> 75 considered > 2char.
                cv2.rectangle(cnt_rect, (x, y), (x + w, y + h), (0, 255,0), 3)
                cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), -1)

                if  (y ==0) and (h <=70):
                    deletion_target.append(cnt)
            else:
                deletion_target.append(cnt)

        # Page.display(all_recognized_regions_demo)
        myCell = OCR.delete_noise(myCell, deletion_target)
        myCell = np.invert(myCell)   # it seems that tesseract only works well with white back ground and black text, not binaries with black background.

        # Bitwise-and to isolate characters
        # https: // stackoverflow.com / questions / 60066481 / recognize - single - characters - on - a - page -
        # with-tesseract

        result = cv2.bitwise_and(myCell, mask)
        result[mask == 0] = 255

        # OCR
        if col in [0, 1, 2, 3]:
            config = '--psm 6 -c tessedit_debug_fonts=1 -c tessedit_char_blacklist=0123456789 -c preserve_interword_spaces=1'
            data = pytesseract.image_to_string(result, lang='eng', config= config)

        elif col == 4:
            config = '--psm 6 outputbase digits -c tessedit_debug_fonts=1 -c preserve_interword_spaces=1 -c tessedit_char_blacklist=.'
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
    def Page_to_DF(colored, binary_page, display = False, inspect = False):
        # this function assembles split_cells, ROI to text, returns a df

        lines_horizontal, lines_vertical, mask_pic = OCR.get_mask(binary_page, colored, display= False)
        cells = OCR.split_cells(colored, lines_horizontal, lines_vertical, display=False, topRowIdx=50, bottomRowIdx=60,
                                leftColIdx=0, rightColIdx=5)
        table = cells.copy()
        out = []
        out_pic = []
        for row in table:
            myRowOut = []
            myRowOut_pic = []
            col = 0
            for cell in row:
                data, img = OCR.ROI_to_text(cell, col = col, inspect = inspect)
                myRowOut.append(data)
                myRowOut_pic.append(img)
                col += 1

            out.append(myRowOut)
            out_pic.append(myRowOut_pic)

        out = pd.DataFrame(out)

        if display == True:
            Page.show_cell_in_table(out_pic)

        return out

    @staticmethod
    def get_general_ROIs(raw_colored, binary_page, display = True):
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


        if display == True: Page.display(out_illustrate)
        # cv2.imwrite(r"logs/20201119_psm_header_detection_OTD16_cmp_nodenoise.png", out_illustrate)

        return ROI_rect_list

    @staticmethod
    def OCR_general_ROIs(colored ,ROIs_rect,display = False):
        ROIs_rect.sort(key = lambda x: x[1])
        out_pics = []
        header_list = []
        for [x,y,w,h] in ROIs_rect:
            padding = 10
            cv2.rectangle(colored, (x, y), (x + w, y + h + padding), (255, 0, 0), 3)
            ROI_pic = Page.cropImg([y, y + h , x, x+w], colored)
            data, img = OCR.ROI_to_text(ROI_pic, col= "header", inspect = 'TESS') # means that it will be recognized

            out_pics.append(img)
            if data != '':
                header_list.append([data, (x,y,w,h)])

        # look for 'department' or 'state names' in string.

        if display == True: Page.show_images(out_pics, numCol =1)

        return header_list

    @staticmethod
    def classify_general_ROIs(OCR_out):
        print(OCR_out)

    @staticmethod
    def get_header_ROIs_old(colored_nparray, binary_page, display = True):
        colored_nparray = cv2.cvtColor(colored_nparray, cv2.COLOR_BGR2RGB) # turn it blue, basically, to integrate with the ROI_to_text method
        # binary_page = Page.colored_to_binary(colored_nparray)
        # takes a binary pate, crops out the top 1/5 of it.  
        # methodology, dilate and blurr text regions into rectangle-like objects
        # then detect these objects as ROI
        # problem: horizontal lines become noises, at the moment, only used area as a filtering mechanism. This could be improved by Houghline > remove.
        
        # binary_page = Page.cropImg([0, int(len(binary_page)/5), 0, len(binary_page[0])], binary_page)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
        eroded= cv2.erode(binary_page, kernel)
    
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilated = cv2.dilate(eroded, kernel2)
        kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (50,5))
        dilated = cv2.dilate(dilated, kernel3)
        kernel4 = cv2.getStructuringElement(cv2.MORPH_RECT, (6,30))
        dilated = cv2.dilate(dilated, kernel4)
    
        blurred = cv2.blur(dilated, (50, 50), 30)

    
        dilated = dilated.astype('uint8')
        contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
        ROIs = []

        out_illustrate = binary_page.copy()



        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if (cv2.contourArea(cnt) > 15000) and ( 1000>w > 500):
                cv2.rectangle(out_illustrate, (x, y), (x + w, y + h), (255, 0, 0), 3)
                top, bottom, left, right = y, y+h, x, x+w

                image= Page.cropImg([top,bottom, left, right], colored_nparray)
                ROIs.append((image,y))

        # sort ROI so that the list stores titles top-down. Need this for parsing.
        ROIs.sort(key = lambda k: k[1])
        ROIs = [tup[0] for tup in ROIs]

        header_info = []
        out_pic = []

        for ROI in ROIs:
            data, img = OCR.ROI_to_text(ROI, col= 1) # means that it will be recognized 
            header_info.append(data)
            out_pic.append(img)

        header_df = pd.DataFrame(header_info)

        if display == True:
            Page.show_images(out_pic)
            Page.display(out_illustrate)

        return header_df

    @staticmethod
    def page_to_df_and_header(path, display = True):
        # resize page so vertical, horizontal detections, and OCR codes will work
        colored = Page.load_colored(path)
        binary_page = Page.colored_to_binary(colored)
        colored = imutils.resize(colored, height = 3663, width = 2831)
        binary_page = imutils.resize(binary_page, height = 3663, width = 2831)

        colored = OCR.two_dimensional_deskew(colored)
        binary_page = OCR.two_dimensional_deskew(raw_page)
        header_df = OCR.get_header_ROIs(colored, binary_page, display = display)
        df = OCR.Page_to_DF(colored, binary_page, display = display)

        df.to_csv("test.csv", index = False)
        header_df.to_csv("header.csv", index = False)

        print(header_df)
        print(df)
        
        return header_df, df
