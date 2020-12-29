Please refer to "Using Deep Learning Techniques to Improve OCR solutions - V1.pptx" for a description of the current state (results, proposal, etc.) and the background of this project.\
\
\
The relevant codes are included in two folders:\

customized_ocr: all codes related to customized page segmentation and OCR (Python). 
* batch_test.py: test ocr code on hundreds of pages.
* Horizontal.py, Vertical.py: page segmentation scripts. Detects horizontal and vertical table borders through morphological transformation and other techinques. 
* OCR.py: combine page segmentation scripts and connect segmented pages to Tesseract. 
* eval.py: evaluate the test results using the Character Error Rate metric.
* ETL.py : extract and prepare data from pdf. 
* Page.py: helper scripts for image redering. 

traning_tesseract: shell scripts that trains Tesseract-OCR in a Linux environment. 

