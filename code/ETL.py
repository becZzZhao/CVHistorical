import os
from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader
import re
import tempfile
from pdf2image import convert_from_path, convert_from_bytes
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


def PDF_to_JPG_pages(pdf_path):
# download poppler binary from https://github.com/oschwartz10612/poppler-windows/releases/ then get the bin directory
    poppler_path = r"C:\Users\Mengyue Zhao\PycharmProjects\cv3\venv\Lib\site-packages\poppler-20.11.0\bin"
    pdf_path= "OR_test.pdf"
    pages = convert_from_path(pdf_path,  poppler_path = poppler_path)
    # pages[0].close()
    counter = 0


    os.chdir(r"C:\Users\Mengyue Zhao\PycharmProjects\cv3\venv\OR_pages")

    while counter <=5:
        for page in pages:
            # page.close()
            outFileDir = 'OR_test_departs_%s.jpg'%counter
            page.save(outFileDir, 'JPEG')
            counter +=1

    os.chdir(r"C:\Users\Mengyue Zhao\PycharmProjects\cv3\venv")

# def df_to_db(df):
#