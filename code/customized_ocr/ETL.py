import os
from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader
import re
import tempfile
from pdf2image import convert_from_path, convert_from_bytes, pdfinfo_from_path
import sqlite3

#visualize pk and fk



def split_pdf_pages():
    p = re.compile('OR[0-9]{4}.+.pdf')
    l1 = os.listdir()
    l2 = [ s for s in l1 if p.match(s) ]
    numPage =len(l2)
    year = str(1865)
    docuName = "OR" + year
    inputpdf = PdfFileReader(open(docuName+ ".pdf", "rb"))

    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        outPageName = docuName + "_" + "%s.pdf" % i
        with open(outPageName, "wb") as outputStream:
            print(outPageName)
            output.write(outputStream)
        if i == 5:
            break


def PDF_to_JPG_pages():
# download poppler binary from https://github.com/oschwartz10612/poppler-windows/releases/ then get the bin directory

    os.chdir(r"C:\Users\Mengyue Zhao\PycharmProjects\cv3\venv\test_pages\full_1865_post")

    poppler_path = r"C:\Users\Mengyue Zhao\PycharmProjects\cv3\venv\Lib\site-packages\poppler-20.11.0\bin"
    pdf_path= "OR1865_PO.pdf"
    # print("converting")
    # pages = convert_from_path(pdf_path,  poppler_path = poppler_path)

    info = pdfinfo_from_path(pdf_path, userpw=None, poppler_path=poppler_path)
    maxPages = info["Pages"]

    counter = 7
    for i in range(1, maxPages+1, 30) :
        pages = convert_from_path(pdf_path,  first_page=i, last_page = min(i+30-1,maxPages),poppler_path=poppler_path)

        for page in pages:
            # page.close()
            outFileDir = 'OR1865_page%s.jpg'%counter
            print("saved: %s"%outFileDir)
            page.save(outFileDir, 'JPEG')
            counter +=1

    os.chdir(r"C:\Users\Mengyue Zhao\PycharmProjects\cv3\venv")



############### parts of the code removed for protecting my work efforts. This script is for demonstration purpose only.
############### if you would like to learn more about the project, you are welcome to email beczhaozmy@gmail.com

# def df_to_db(df):
#
