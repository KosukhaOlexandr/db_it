from unittest import TestCase
from db_cust import Row, Column
import copy


class TestRow(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c_int = Column('c_int', 'int')
        cls.c_str = Column('c_str', 'str')
        cls.c_float = Column('c_float', 'float')
        cls.c_complex = Column('c_complex', "complex")
        cls.c_char = Column('c_char', 'char')
        cls.success_dict = {cls.c_int: 1,
                        cls.c_str: 'abc',
                        cls.c_float: 5.7,
                        cls.c_complex: complex('1+1j'),
                        cls.c_char: 'x'}

    def test_add_col_val_success(self):
        r_col_val = Row(self.success_dict).col_val
        self.assertEqual(self.success_dict, r_col_val)

    def test_add_col_val_fail(self):
        fail_dict = {self.c_int: 'a'}
        with self.assertRaises(TypeError):
            r = Row(fail_dict)

    def test_remove_col_success(self):
        success_remove_complx = copy.deepcopy(self.success_dict)
        success_remove_complx.pop(self.c_complex)

        test_row = Row(self.success_dict)
        test_row.remove_col(self.c_complex)
        self.assertEqual(success_remove_complx, test_row.col_val)

    def test_remove_col_fail(self):
        row = Row(self.success_dict)
        with self.assertRaises(ValueError):
            row.remove_col('c_not_exist')

    def test_edit_success(self):
        row = Row(self.success_dict)
        edit_str = copy.deepcopy(self.success_dict)
        edit_str[self.c_str] = 'change'
        row.edit(self.c_str.name, 'change')
        self.assertEqual(edit_str, row.col_val)

    def test_edit_fail(self):
        row = Row(self.success_dict)
        with self.assertRaises(ValueError):
            row.edit(self.c_char, 'nice_val')

