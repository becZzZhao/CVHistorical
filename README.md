Please refer to "Using Deep Learning Techniques to Improve OCR solutions - V1.pptx" for a description of the current state (results, proposal, etc.) and the background of this project.\
\
\
relevant codes are include in two folders:\

customized_ocr: all codes related to customized page segmentation and ocr scripts in Python. \ 
*** batch_test.py: test ocr code on hundreds of pages.
*** Horizontal.py, Vertical.py: page segmentation scriptons. Detects horizontal and vertical table borders through morphological transformation and other techinques. 
*** OCR.py: combine page segmentation scripts and connect segmented pages to Tesseract. 
*** eval.py: evaluate the test results using the Character Error Rate metric.
*** ETL.py : extract and prepare data from pdf. 
*** Page.py: helper scripts for image redering. 
traning_tesseract: shell scripts that trains ocr for one font in linux. \

