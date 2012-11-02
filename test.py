import unittest

###############################################################################
# DataSpec

from data_dictionary import DataSpec

class test_DataSpec(unittest.TestCase):
    def test_none_min(self):
        self.assertRaises(ValueError, DataSpec, 'ABC', 0, 10, 0, None)
    def test_none_max(self):
        self.assertRaises(ValueError, DataSpec, 'ABC', 0, 10, None, 0)
    def test_no_range(self):
        try:
            DataSpec('ABC', 0, 10)
        except ValueError:
            self.fail()
    def test_full_range(self):
        try:
            DataSpec('ABC', 0, 10, 0, 100)
        except ValueError:
            self.fail()
    def test_invalid_range(self):
        self.assertRaises(ValueError, DataSpec, 'ABC', 0, 10, 100, 0)
    def test_invalid_position(self):
        self.assertRaises(ValueError, DataSpec, 'ABC', 10, 0)

###############################################################################
# extract_range

from data_dictionary import extract_range

class test_extract_range(unittest.TestCase):
    def test_only_parens(self):
        self.assertEqual(extract_range('(a, b, c)'), ('a, b, c', ''))
    def test_multiple_parens(self):
        self.assertEqual(extract_range('(a, b, c)(d, e, f)'),
                         ('a, b, c', '(d, e, f)'))
    def test_raise_on_nested_parens(self):
        self.assertRaises(AssertionError, extract_range, '(())')
    def test_part_of_string_after(self):
        self.assertEqual(extract_range('a b c (1 2 3) d e f'),
                         ('1 2 3', 'a b c  d e f'))
    def test_no_parens(self):
        self.assertEqual(extract_range('a b c d e f'),
                         ('', 'a b c d e f'))
    def test_unclosed_left(self):
        self.assertEqual(extract_range('a b c ( d e f'),
                         ('', 'a b c ( d e f'))
    def test_start_on_paren(self):
        self.assertEqual(extract_range('(a b c d) e f g'),
                         ('a b c d', ' e f g'))

###############################################################################
# data_spec_line

from data_dictionary import data_spec_line
from data_dictionary import DataSpec

class test_data_spec_line(unittest.TestCase):
    def test_meta_test_equality_func(self):
        self.assertTrue(self.equality(DataSpec('FILLER', 58, 59),
                                      DataSpec('FILLER', 58, 59)))
    def test_simple_line(self):
        self.assertTrue(self.equality(data_spec_line('D FILLER 1 59'),
                                       DataSpec('FILLER', 58, 59)))
    def test_simple_range(self):
        self.assertTrue(self.equality(data_spec_line('D MIG_DSCP 1 328 (0:5)'),
                                      DataSpec('MIG_DSCP', 327, 328, 0, 5)))
    def test_auxiliaries(self):
        self.assertTrue(self.equality(data_spec_line('D MIG-ST 2 326 (00:56, 96)'),
                                      DataSpec('MIG-ST', 325, 327, 0, 56, [96])))
    def equality(self, ds1, ds2, msg=None):
        return (ds1.name == ds2.name and
            ds1.start == ds2.start and
            ds1.end == ds2.end and
            ds1.value_min == ds2.value_min and
            ds1.value_max == ds2.value_max and
            ds1.auxiliaries == ds2.auxiliaries)

if __name__ == '__main__':
    unittest.main()
