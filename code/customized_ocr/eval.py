# https://github.com/kahne/fastwer
# install vs build tools before installation https://visualstudio.microsoft.com/visual-cpp-build-tools/
import cv2
import pytesseract
from Page import Page
from pytesseract import Output
import pandas
import sys
import os
import fastwer
import pandas as pd
import shutil
from OCR import OCR
import imutils

# -*- coding: utf-8 -*-

outPath = "test/output/test_results"
# shutil.rmtree(outPath)
# os.makedirs(outPath)

img_dirs = os.listdir("test/jpg")
inPath = "test/jpg"
gtPath = "test/gt"

def test_psm(dirs = None):
    if dirs == None:
        dirs = os.listdir(r'C:\Users\Mengyue Zhao\PycharmProjects\cv3\venv\test_pages\full_1865_post')[0:]

    for mydir in dirs:

        pagedir = r'C:\Users\Mengyue Zhao\PycharmProjects\cv3\venv\test_pages\full_1865_post' +  "\\"+ mydir
        page = Page.load_colored(pagedir)
        d = pytesseract.image_to_data(page, lang='eng',config='--psm 6', output_type=Output.DICT)
        n_boxes = len(d['left'])
        p = page.copy()

        color = (0, 0, 0)
        print(d)

        for i in range(n_boxes):
            if color == (0, 0, 0):
                color = (0, 255, 0)
            else:
                color = (0, 0, 0)
            if d['level'][i] != 1:
                continue
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            cv2.rectangle(p, (x, y), (x + w, y + h), color, 2)


        outPath = r"../test/output/psm/first"
        fileName =   mydir.split(".")[0] + ".png"
        outPath = os.path.join(outPath, fileName)

        cv2.imwrite(outPath,p)

def get_xer(ocrOutput_corpus, gt_corpus):
    hypo = [ocrOutput_corpus]
    ref = [gt_corpus]

    WER = fastwer.score_sent(hypo[0], ref[0])/100
    CER = fastwer.score_sent(hypo[0], ref[0], char_level=True)/100

    XER_dict = {"WER": WER, "CER": CER}

    return XER_dict


def gen_gt_corpus():
    global gtPath
    gt_dirs = [f for f in os.listdir(gtPath) if f.endswith('.' + "txt")]

    corpus_dir = os.path.join(gtPath,'gt_corpus.txt')
    with open(corpus_dir, 'w', encoding='utf8') as outfile:
        for fname in gt_dirs:
            fdir = os.path.join(gtPath, fname)
            with open(fdir, encoding='utf8') as infile:
                outfile.write(infile.read().rstrip() + '\n')

    gt_corpus_file = open(corpus_dir, 'r', encoding='utf8')
    gt_corpus = gt_corpus_file.read()
    return gt_corpus




def gen_results_corpus(img_dir = None):
    global img_dirs
    global outPath
    global inPath

    img_dirs = [f for f in img_dirs if f.endswith('1.jpg')]
    for img_dir in img_dirs:
        inFile = os.path.join(inPath,img_dir)
        fileName = img_dir.split(".")[0] + ".txt"
        outFile= os.path.join(outPath, fileName)
        page = Page.load_colored(inFile)
        output = pytesseract.image_to_string(page, lang='eng',config='--psm 6', output_type= Output.STRING)
        print(fileName)
        print(output)
        with open(outFile, mode = 'w', encoding='utf-8') as f:
            f.write(output)

        del inFile, outFile

    filenames = os.listdir(outPath)
    corpus_dir = os.path.join(outPath,'out_corpus.txt')
    with open(corpus_dir, 'w', encoding='utf8') as outfile:
        for fname in filenames:
            fdir = os.path.join(outPath, fname)
            with open(fdir, encoding='utf8') as infile:
                outfile.write(infile.read().rstrip() + '\n')

    output_corpus_file = open(corpus_dir, 'r', encoding='utf8')
    output_corpus =  output_corpus_file.read()

    return output_corpus


def gen_eval_metrics(verbose = False):
    global img_dirs
    global outPath
    global inPath

    img_dirs = [f for f in img_dirs if f.endswith('1.jpg')]
    avg_metrics = {'WER_corpus': 0, 'WER_sentence': 0, 'CER_corpus': 0, 'CER_sentence': 0}
    n = 0

    num_error_global = 0
    num_char_global = 0

    for img_dir in img_dirs:
        fileName = img_dir.split(".")[0]

        gt_dir = os.path.join(gtPath, fileName + ".txt")
        out_corpus_dir = os.path.join(outPath, fileName +".txt")

        gt = open(gt_dir, 'r', encoding='utf8').readlines()
        out_corpus = open(out_corpus_dir, 'r', encoding='utf8').readlines()

        num_error = 0
        num_char = 0
        for gt, out in zip(gt,out_corpus):
            num_char += len(gt)
            metrics = get_xer(ocrOutput_corpus=out, gt_corpus=gt)

            num_char += len(gt)
            num_error += len(gt) * metrics["CER"]


            if verbose == True:
                print("_________________________________________________")
                print("ground truth: ", gt)
                print("OCR output: ", out)
                print(metrics)
                print("%s errors found in %s chars"% (len(gt) * metrics["CER"], len(gt)))


        page_CER = num_error/ num_char

        num_error_global += num_error
        num_char_global += num_char

        if verbose == True:
            print("*****************************************************")
            print("CER of page: %s, total number of error: %s, total number of chars: %s"%(page_CER, num_error, num_char))
            print("====================================================================================================")

    test_CER  = num_error_global/num_char_global
    print("test CER: %s" % test_CER)
    return test_CER

def OCR_test_pages():
    global img_dirs
    img_dirs = [f for f in img_dirs if f.endswith('1.jpg')]
    out_dir = os.path.join(outPath , "test_results_ocr")
    for img_dir in img_dirs[2:]:
        inFile = os.path.join(inPath, img_dir)
        fileName = img_dir.split(".")[0] + ".txt"
        page_co = Page.load_colored(inFile)
        page_bi = Page.rawtobinary(inFile)

        page_co = imutils.resize(page_co, height=3663, width=2831)
        page_bi = imutils.resize(page_bi, height=3663, width=2831)

        df = OCR.section_to_df(page_bi, page_co)

        file_dir = os.path.join(out_dir, fileName)
        df.to_csv(file_dir, sep= '|')

OCR_test_pages()
# set eval.outpath to desired subdir.



# gen_results_corpus(img_dirs)
# gen_eval_metrics(verbose = False)


#
# for img_dir in img_dirs:
#     inFile = os.path.join(inPath,img_dir)
#     img = Page.load_colored(inFile)
#     Page.display(img)


# page = Page.load_colored(intputPath)
        # output = pytesseract.image_to_string(page, lang='eng',config='--psm 6', output_type= Output.STRING)
        #
        # print(img_dir)
    # fileName = imgdir.split(".")[0]
    # outPath = os.path.join(outPath, fileName)

    # # img_dir = os."../test/jpg"
    # # def get_XER(gt = None, ocr_output = None, metric = 'CER')`
    # # C:\Users\Mengyue Zhao\PycharmProjects\cv3\venv\test_pages\full_1865_post
    # page = Page.load_colored(r"../test/jpg/OR1857_page1.jpg")
    # output = pytesseract.image_to_string(page, lang='eng',config='--psm 1', output_type= Output.STRING)
    #
    # with open('../test/output/test2.txt', mode = 'w', encoding='utf-8') as f:
    #     f.write(output)



# gen_test_results()

# test_psm()
    # print(n_boxes)
    # for level in range(1,6):
    #     p = page.copy()
    #     for i in range(n_boxes):
    #         if d['level'][i] != level:
    #             continue
    #         (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    #         cv2.rectangle(p, (x, y), (x + w, y + h), (255, 255, 255), 2)
    #     Page.display(p)



# from tesserocr import PyTessBaseAPI
#
# images = ['sample.jpg', 'sample2.jpg', 'sample3.jpg']

# with PyTessBaseAPI() as api:
#     for img in images:
#         api.SetImageFile(img)
#         print(api.GetUTF8Text())
#         print(api.AllWordConfidences())
