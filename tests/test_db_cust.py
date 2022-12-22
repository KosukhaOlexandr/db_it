from unittest import TestCase
from db_cust import Row, Column, Table

class TestTable(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c_int = Column('c_int', 'int')
        cls.c_str = Column('c_str', 'str')
        cls.c_float = Column('c_float', 'float')
        cls.c_complex = Column('c_complex', "complex")
        cls.c_char = Column('c_char', 'char')

    def test_delete_duplicates(self):
        table = Table('Table1')
        table.add_column(self.c_str)
        table.add_column(self.c_char)
        not_distinct = Row({self.c_str: '123', self.c_char: '2'})
        table.add_row(not_distinct)
        table.add_row(Row(not_distinct.col_val))
        distnct = Row({self.c_str: '12', self.c_char: '2'})
        table.add_row(distnct)

        table.delete_duplicates()

        self.assertEqual([ro.col_val for ro in table.rows], [not_distinct.col_val, distnct.col_val,])



