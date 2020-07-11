### Try directly image to text first, then get box, etc.

from Page import Page
from Vertical import Vertical
from Horizontal import Horizontal

class Mask:
    @staticmethod
    def create_table_onpage(page):
        p = Vertical.create_column_borders(page)
        table = Horizontal.create_row_borders(p)

        return table




page= Page.rawtobinary('test.jpg')
Mask.create_table_onpage(page)