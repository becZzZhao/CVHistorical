
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




class OCR(Vertical, Horizontal):
    @staticmethod
    def get_mask(binary_image, display = False):
        # takes binary  and detect vertical& horizontal lines

        
        raw = binary_image.copy()
        # detect horizontal borders
        dots = Horizontal.find_all_dots(binary_image, display = False)
        lines = Horizontal.dotted_to_lines(dots, display=False)
        lines_filtered = Horizontal.filter(lines, len(raw))
        lines_horizontal = Horizontal.populate_lines(lines_filtered, len(raw[0]), len(raw))

        vertical_pic = Page.draw_lines(lines_horizontal, raw, display=False, thickness=5)

        # detect vertical lines
        contours = Vertical.lookfor_vertical_contours(raw)
        lines_vertical = Vertical.determine_houghlines(contours, display=False)
        lines_vertical = Vertical.finalize_vertical_line(lines_vertical, page_height=len(raw))

        mask_pic =  Vertical.draw_line(vertical_pic, lines_vertical, display=False, thickness=7)

        if display == True: Page.display(mask_pic)

        return lines_horizontal,lines_vertical, mask_pic

    @staticmethod
    def split_cells(raw_colored_image, lines_horizontal, lines_vertical, display = False,  topRowIdx = 50, bottomRowIdx = 80, leftColIdx = 0, rightColIdx = 5):
        # takes raw image (colored) return cropped image of cells/ ROI
        # output is unprocessed cells. 
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
    def ROI_to_text(image, col):
    
        # use MP
        # https://github.com/lavanya-m-k/character-detection-and-crop-from-an-image-using-opencv-python
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

        kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2,10))
        dilated = cv2.dilate(gray, kernel1)
        # Page.display(dilated)
        dilated = cv2.dilate(dilated , kernel2)
        # Page.display(dilated)
        # blurring makes the dots more elliptical-like
        ret, thresh1 = cv2.threshold(dilated, 127, 255, cv2.THRESH_BINARY)

        # https://github.com/lavanya-m-k/character-detection-and-crop-from-an-image-using-opencv-python
        contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # cnt = sorted(cnt, key=lambda x: (x[0][0], x[0][1]))

        word = []

        i  = 0
        # myCell = myCell[:, :, 0]
        myCell = np.invert(myCell)  # pytesseract take black word & white paper?
        mask = np.zeros(myCell.shape, dtype=np.uint8)

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)

            # bound the images
            if w > 16 and h > 30:
                # first char is 95, thinner char 25, normal char 50.
                # if it is the first char, w>100 considered >2 char.
                # if it is not the first char, w> 75 considered > 2char.
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255,0), 2)
                cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), -1)

                # ROI = Page.cropImg([y,y+h,x,x+w],myCell)


        # Bitwise-and to isolate characters
        # https: // stackoverflow.com / questions / 60066481 / recognize - single - characters - on - a - page -
        # with-tesseract
        result = cv2.bitwise_and(myCell, mask)
        result[mask == 0] = 255


        # OCR
        if col in [0, 1, 2, 3]:
            data = pytesseract.image_to_string(result, lang='eng', config='--psm 6 -c tessedit_char_blacklist=0123456789')
        else:
            data = pytesseract.image_to_string(result, lang='eng', config='--psm 6 outputbase digits')

        data = data[:-2]
        out = OCR.draw_text(result, data)

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
    def Page_to_DF(colored, binary_page, display = False):
        # this function assembles split_cells, ROI to text, returns a df

        lines_horizontal, lines_vertical, mask_pic = OCR.get_mask(binary_page, display=False)
        cells = OCR.split_cells(colored, lines_horizontal, lines_vertical, display=False, topRowIdx=50, bottomRowIdx=55,
                                leftColIdx=0, rightColIdx=5)


        table = cells.copy()
        out = []
        out_pic = []
        for row in table:
            myRowOut = []
            myRowOut_pic = []
            col = 0
            for cell in row:
                data, img = OCR.ROI_to_text(cell, col = col)
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
    def get_header_ROIs(colored_nparray, binary_page, display = True):
        colored_nparray = cv2.cvtColor(colored_nparray, cv2.COLOR_BGR2RGB) # turn it blue, basically, to integrate with the ROI_to_text method
        # binary_page = Page.colored_to_binary(colored_nparray)
        # takes a binary pate, crops out the top 1/5 of it.  
        # methodology, dilate and blurr text regions into rectangle-like objects
        # then detect these objects as ROI
        # problem: horizontal lines become noises, at the moment, only used area as a filtering mechanism. This could be improved by Houghline > remove.
        
        binary_page = Page.cropImg([0, int(len(binary_page)/5), 0, len(binary_page[0])], binary_page)

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
        # out_illustrate = binary_page.copy()
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if (cv2.contourArea(cnt) > 15000) and ( 1000>w > 500):
                # cv2.rectangle(out_illustrate, (x, y), (x + w, y + h), (255, 0, 0), 3)
                top, bottom, left, right = y, y+h, x, x+w
                image = Page.cropImg([top,bottom, left, right], colored_nparray)
                ROIs.append(image)

        header_info = []
        out_pic = []
        for ROI in ROIs:
            data, img = OCR.ROI_to_text(ROI, col= 1) # means that it will be recognized 
            header_info.append(data)
            out_pic.append(img)

        print(header_info)
        if display == True: Page.show_images(out_pic)

        return header_info
        

    @staticmethod
    def page_to_df_and_header(path, display = False):
        colored = Page.load_colored(path)
        binary_page = Page.colored_to_binary(colored)
        header_info = OCR.get_header_ROIs(colored, binary_page, display = display)
        df = OCR.Page_to_DF(colored, binary_page, display = display)
        
        print(header_info)
        print(df)
        
        return header_info, df
