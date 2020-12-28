# import OCR
# import numpy as np
# from Page import Page
# import cv2
# from PIL import ImageFont, ImageDraw, Image
# import imutils


# https://github.com/Belval/TextRecognitionDataGenerator

# class OCRAug():
#     @staticmethod
#     def gen_original_chars():
#         #https://github.com/pholls/patent_bot/tree/48aec4c0ce1dc5756009e8fb495979dfcfee44e7/assets/fonts/Times_New_Roman
#         w,h = 60, 60
#         img = Image.new(mode='RGB', size=(h, w), color=(0,0,0))
#         draw = ImageDraw.Draw(img)
#         # font = ImageFont.load("Times_New_Roman.ttf")
#         font = ImageFont.truetype("Times_New_Roman.ttf", size = 50)
#         size = font.getsize("A")
#
#         draw.text((10,0), "A", font=font, size = size) # when it's 100 it reached some maximum size
#         img.show()

import OCR
import numpy as np
from Page import Page
import cv2
from PIL import ImageFont, ImageDraw, Image, ImageOps
import imutils

class OCRAug():
    @staticmethod
    def draw_save_chars(char_list, labels, font_path):
        w,h = 60, 60
        img = Image.new(mode='RGB', size=(h, w), color=(0,0,0))
        for char in char_list:
            charImg = img.copy()
            draw = ImageDraw.Draw(charImg)
            font = ImageFont.truetype(font_path, size=50) # this number exceeds the maximum size.
            size = font.getsize(char)
            draw.text((15, 0), char, font=font, size=size)

            charImg = ImageOps.invert(charImg)
            outPath = "chars\\original\\" + char + labels + ".png"
            charImg.save(outPath, "PNG")

    @staticmethod
    def gen_original_chars():
        #https://github.com/pholls/patent_bot/tree/48aec4c0ce1dc5756009e8fb495979dfcfee44e7/assets/fonts/Times_New_Roman
        char_list_upper = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        char_list_lower = list("abcdefghijklmnopqrstuvwxyz")
        char_list_digits = list("$0123456789")

        OCRAug.draw_save_chars(char_list_upper, labels= '_upper', font_path = "Times_New_Roman.ttf")
        OCRAug.draw_save_chars(char_list_upper, labels='_upper_italic', font_path="Times_New_Roman_Italic.ttf")

        OCRAug.draw_save_chars(char_list_lower, labels='_lower', font_path="Times_New_Roman.ttf")
        OCRAug.draw_save_chars(char_list_lower, labels='_lower_italic', font_path="Times_New_Roman_Italic.ttf")

        OCRAug.draw_save_chars(char_list_digits, labels='_digits', font_path="Times_New_Roman.ttf")
        OCRAug.draw_save_chars(char_list_digits, labels='_digits_italic', font_path="Times_New_Roman_Italic.ttf")


from trdg.generators import (
    GeneratorFromDict,
    GeneratorFromRandom,
    GeneratorFromStrings,
    GeneratorFromWikipedia,
)

fontPaths = ['Times_New_Roman.ttf',
             'Times_New_Roman_Italic.ttf']
# The generators use the same arguments as the CLI, only as parameters
generator = GeneratorFromStrings(
    ['Test1', 'Test2', 'Test3'],
    fonts = fontPaths,
    blur=2,
    random_blur=True

)



i = 0
for img, lbl in generator:
    i+=1
    img.save(r"chars\train\testttttttttttttttttttttttt%s.png" %i, "PNG")
    # Do something with the pillow images here.





