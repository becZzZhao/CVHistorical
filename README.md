# CVHistorical, reading historical documents with computer vision techniques in an OOP environment. 
Reading historical documents with computer vision techniques. Written in an OOP environment.<br />

&nbsp;
This is a side project of my undergraduate research work in the field of economic history. My work involves digitizing millions of historical economic indicators from scanned historical documents. The intention of this project is to allow the digitization to be conducted in a time-saving and cost-saving manner. This project is an example of my interest in machine vision, ability and motivation to explore all possible solutions for my problem. <br />
&nbsp;
&nbsp;

The main challenge that I have encountered is that, due perhaps to the limitation of Nineteenth-Century and Twentieth-Century printing techniques, the tables are not properly aligned for detection by modern OCR software.  The solution is, there fore to make use of the computer vision capabilities of OpenCV and open source OCR packages such as Tesseract and Tensorflow OCR.   <br />

&nbsp;
&nbsp;
&nbsp;

The next step of the project is to connect to open-source OCR libraries and tesseract to extract the content of the table. <br />
At the time that I worked with this project, I have not learned deep learning techniques such as CNN. After learning about the capability of these new techniques, I realized that some of the steps, such as creating the kernel and scanning the picture with it, could be replaced by deep learning techniques. This would potentially increase the accuracy a lot if combined with some hard-coded rules. <br />
Transfer learning might also be another area to explore, since local patterns (dots) and global patterns (tables) could be handled simultaneously by different layers.  <br />

