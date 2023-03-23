import unittest
from unittest.mock import Mock
from library import patron

class TestPatron(unittest.TestCase):

    def setUp(self):
        self.pat = patron.Patron("fname", "lname", "15", "1")
    
    def test_first_name_with_digit_raises_invalid_name_exception(self):
        with self.assertRaises(patron.InvalidNameException):
            patron.Patron("f1name", "lname", 15, 1)

    def test_last_name_with_digit_raises_invalid_name_exception(self):
        with self.assertRaises(patron.InvalidNameException):
            patron.Patron("fname", "l1name", 15, 1)
    
    def test_names_with_digit_raises_invalid_name_exception(self):
        with self.assertRaises(patron.InvalidNameException):
            patron.Patron("f2name", "l1name", 15, 1)
    
    def test_names_with_digit_raises_invalid_name_exception(self):
        with self.assertRaises(patron.InvalidNameException):
            patron.Patron("f2name", "l1name", 15, 1)
    
    def test_names_with_digit_raises_correct_exception(self):
        with self.assertRaises(patron.InvalidNameException) as cm:
            patron.Patron("f1name", "l2name", 15, 1)
        self.assertEqual(str(cm.exception), "Name should not contain numbers")
    
    def test_valid_name(self):
        pat = patron.Patron("fname", "lname", "15", "1")
        self.assertTrue(isinstance(pat, patron.Patron))

    def test_invalid_name(self):
        self.assertRaises(patron.InvalidNameException, patron.Patron, '1fname', '1lname', '20', '1234')
            
    def test_add_borrowed_book(self):
        test_patron = patron.Patron("fname", "lname", "15", "1")
        test_patron.add_borrowed_book("book1")
        self.assertEqual('book1', test_patron.get_borrowed_books()[0])

    def test_add_borrowed_book_twice(self):
        test_patron = patron.Patron("fname", "lname", "15", "1")
        test_patron.add_borrowed_book("Book")
        test_patron.add_borrowed_book("Book")
        self.assertEqual(1, len(test_patron.get_borrowed_books()))

    def test_return_borrowed_book(self):
        test_patron = patron.Patron("fname", "lname", "15", "1")
        book = "Book"
        test_patron.add_borrowed_book(book)
        test_patron.return_borrowed_book(book)
        self.assertEqual(0, len(test_patron.get_borrowed_books()))

    def test_return_not_borrowed_book(self):
        test_patron = patron.Patron("fname", "lname", "15", "1")
        test_patron.return_borrowed_book("No Book1")
        self.assertEqual(0, len(test_patron.get_borrowed_books()))

    def test_eq_equal(self):
        test_patron = patron.Patron("fname", "lname", "15", "1")
        equal_patron = patron.Patron("fname", "lname", "15", "1")
        result = test_patron.__eq__(equal_patron)
        self.assertEqual(True, result)

    def test_eq_not_equal(self):
        test_patron = patron.Patron("fname", "lname", "15", "1")
        not_equal_patron = patron.Patron("fnamedifferent", "lnamedifferent", "21", "1")
        result = test_patron.__eq__(not_equal_patron)
        self.assertEqual(False, result)

    def test_ne_equal(self):
        test_patron = patron.Patron("fname", "lname", "15", "1")
        test_equal = patron.Patron("fname", "lname", "15", "1")
        result = test_patron.__ne__(test_equal)
        self.assertEqual(False, result)

    def test_ne_not_equal(self):
        test_patron = patron.Patron("fname", "lname", "15", "1")
        test_not_equal = patron.Patron("fnamedifferent", "lnamedifferent", "15", "1")
        result = test_patron.__ne__(test_not_equal)
        self.assertEqual(True, result)

    def test_get_fname(self):
        test_patron = patron.Patron("fname", "lname", "15", "1")
        self.assertEqual("fname", test_patron.get_fname())

    def test_get_lname(self):
        test_patron = patron.Patron("fname", "lname", "15", "1")
        self.assertEqual("lname", test_patron.get_lname())

    def test_get_age(self):
        test_patron = patron.Patron("fname", "lname", "15", "1")
        self.assertEqual("15", test_patron.get_age())

    def test_get_memberID(self):
        test_patron = patron.Patron("fname", "lname", "15", "1")
        self.assertEqual("1", test_patron.get_memberID())
  