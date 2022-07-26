## WEHC Audience:
## Please visit this website instead
## https://beczzzhao.github.io/CVHistorical/



I significantly enhanced the output of Optical Character Recognition tools for historical documents by a few simple changes. And the glued-together (:)) project outperforms most commercial OCR software or Open-source Deep Learning OCR engines.  This is a continuation of a personal project that I did in the past to create big data for modern historians.


Checkout my paper for results, comparisons and some discussions:
https://www.linkedin.com/posts/mengyue-rebecca-zhao-a15bb8111_machine-vision-tools-enhancement-for-ocr-activity-6893647253307736064-dONL




\
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

