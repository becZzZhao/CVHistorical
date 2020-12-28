from Page import Page
from PIL import Image
import pytesseract
class to_text:



    @staticmethod
    def row_and_col(vertical_list, horizontal_list):    #get row and col position from the vertical& horitonzal lines list
        num_vertical = len(vertical_list)
        num_horizontal = len(horizontal_list)

        col_list = []
        row_list = []
        for i in range(num_vertical):
            col_list.append(vertical_list[i][0])

        for i in range(num_horizontal):
            row_list.append(horizontal_list[i][1])

        lists = [col_list, row_list]
        return lists

    @staticmethod
    def segment_cells(col_list, row_list, page_width, page_height):
        num_cols = len(col_list)
        num_rows = len(row_list)

        my_table= []
        for j in range(num_rows):
            my_row= []
            for i in range(num_cols):

                if j == 0:
                    my_cell_top = 0
                else:
                    my_cell_top = row_list[j-1]
                if j == num_rows:
                    my_cell_bottom = page_height
                else:
                    my_cell_bottom = row_list [j]


                if i == 0:
                    my_cell_left = 0
                else:
                    my_cell_left = col_list[i - 1]

                if i == num_cols:
                    my_cell_right = page_width
                else:
                    my_cell_right = col_list[i]


                my_cell = (my_cell_left, my_cell_top, my_cell_right, my_cell_bottom)
                print("col", i, "row", j, my_cell)

                my_row.append(my_cell)
                print("row",j, my_row )

            my_table.append(my_row)
            print(my_table)

        return my_table

    @staticmethod
    def segment_and_read(segmented_table_list, current_page):
        num_row = len(segmented_table_list)
        num_col = len(segmented_table_list[0])

        my_table = []
        for j in range(num_row):
            my_row = []
            for i in range(num_col):
                box = segmented_table_list[j][i]
                my_cell_img = current_page.crop(box)
                str1 = 'row'
                str2 = str(j)
                str3 = 'col'
                str4 = str(i)
                str5 = '.jpg'
                img_name = str1+str2+str3+str4+str5


                my_cell_img.save(img_name)




                cell_value = pytesseract.image_to_string(my_cell_img, lang = 'eng')
                my_row.append(cell_value)

            my_table.append(my_row)

        print(my_table)







vertical_list = [[431, 0, 431, 3275], [738, 0, 738, 3275], [1405, 0, 1405, 3275], [1610, 0, 1610, 3275]]
horizontal_list = [[0, 3, 1872, 3], [0, 36, 1872, 36], [0, 69, 1872, 69], [0, 102, 1872, 102], [0, 135, 1872, 135],
                   [0, 168, 1872, 168], [0, 201, 1872, 201], [0, 234, 1872, 234], [0, 267, 1872, 267], [0, 300, 1872, 300],
                   [0, 333, 1872, 333], [0, 366, 1872, 366], [0, 399, 1872, 399], [0, 432, 1872, 432], [0, 465, 1872, 465],
                   [0, 498, 1872, 498], [0, 531, 1872, 531], [0, 564, 1872, 564], [0, 597, 1872, 597], [0, 630, 1872, 630],
                   [0, 663, 1872, 663], [0, 696, 1872, 696], [0, 729, 1872, 729], [0, 762, 1872, 762], [0, 795, 1872, 795],
                   [0, 828, 1872, 828], [0, 861, 1872, 861], [0, 894, 1872, 894], [0, 927, 1872, 927], [0, 960, 1872, 960],
                   [0, 993, 1872, 993], [0, 1026, 1872, 1026], [0, 1059, 1872, 1059], [0, 1092, 1872, 1092], [0, 1125, 1872, 1125],
                   [0, 1158, 1872, 1158], [0, 1191, 1872, 1191], [0, 1224, 1872, 1224], [0, 1257, 1872, 1257], [0, 1290, 1872, 1290],
                   [0, 1323, 1872, 1323], [0, 1356, 1872, 1356], [0, 1389, 1872, 1389], [0, 1422, 1872, 1422], [0, 1457, 1872, 1457],
                   [0, 1489, 1872, 1489], [0, 1522, 1872, 1522], [0, 1555, 1872, 1555], [0, 1588, 1872, 1588], [0, 1621, 1872, 1621],
                   [0, 1654, 1872, 1654], [0, 1689, 1872, 1689], [0, 1720, 1872, 1720], [0, 1756, 1872, 1756], [0, 1789, 1872, 1789],
                   [0, 1821, 1872, 1821], [0, 1852, 1872, 1852], [0, 1885, 1872, 1885], [0, 1919, 1872, 1919], [0, 1952, 1872, 1952],
                   [0, 1985, 1872, 1985], [0, 2019, 1872, 2019], [0, 2052, 1872, 2052], [0, 2085, 1872, 2085], [0, 2118, 1872, 2118],
                   [0, 2151, 1872, 2151], [0, 2184, 1872, 2184], [0, 2215, 1872, 2215], [0, 2253, 1872, 2253], [0, 2283, 1872, 2283],
                   [0, 2316, 1872, 2316], [0, 2349, 1872, 2349], [0, 2385, 1872, 2385], [0, 2416, 1872, 2416], [0, 2449, 1872, 2449],
                   [0, 2482, 1872, 2482], [0, 2515, 1872, 2515], [0, 2548, 1872, 2548], [0, 2584, 1872, 2584], [0, 2616, 1872, 2616],
                   [0, 2649, 1872, 2649], [0, 2682, 1872, 2682], [0, 2715, 1872, 2715], [0, 2748, 1872, 2748], [0, 2781, 1872, 2781],
                   [0, 2814, 1872, 2814], [0, 2847, 1872, 2847], [0, 2879, 1872, 2879], [0, 2912, 1872, 2912], [0, 2945, 1872, 2945],
                   [0, 2979, 1872, 2979], [0, 3011, 1872, 3011], [0, 3044, 1872, 3044], [0, 3077, 1872, 3077], [0, 3110, 1872, 3110],
                   [0, 3143, 1872, 3143], [0, 3176, 1872, 3176], [0, 3209, 1872, 3209], [0, 3242, 1872, 3242]]

a = Page.rawtobinary('test.jpg')
page_height = len(a)
page_width = len(a[1])

img = Image.fromarray(a)
row_and_col = to_text.row_and_col(vertical_list, horizontal_list)
col_list = row_and_col[0]
row_list = row_and_col[1]
print(col_list)
print(row_list)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
segmented_table_list = to_text.segment_cells(col_list, row_list, page_width,page_height )
segmentedimgs_totable = to_text.segment_and_read(segmented_table_list,img)