import unittest
from unittest.mock import Mock
from library.patron import Patron
from library import library
import json

class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.lib = library.Library()
        # self.books_data = [{'title': 'Learning Python', 'ebook_count': 3}, {'title': 'Learning Python (Learning)', 'ebook_count': 1}, {'title': 'Learning Python', 'ebook_count': 1}, {'title': 'Learn to Program Using Python', 'ebook_count': 1}, {'title': 'Aprendendo Python', 'ebook_count': 1}, {'title': 'Python Basics', 'ebook_count': 1}]
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())



    def test_is_ebook_true(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertTrue(self.lib.is_ebook('learning python'))
    
    def test_is_ebook_false(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertFalse(self.lib.is_ebook('Test Book'))

    def test_get_ebooks_count(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertEqual(self.lib.get_ebooks_count("learning python"), 8)
    
    def test_is_book_by_author_true(self):
        self.lib.api.books_by_author = Mock(return_value=['Book1', 'Book2'])
        self.assertTrue(self.lib.is_book_by_author("Ryan", "Book1"))
    
    def test_is_book_by_author_false(self):
        self.lib.api.books_by_author = Mock(return_value=['Book1', 'Book2'])
        self.assertFalse(self.lib.is_book_by_author("Ryan", "Book3"))
    
    def test_get_languages_for_book(self):
        self.lib.api.get_book_info = Mock(return_value=[{'title': 'Test Book', 'language': {'English', 'French'}}])
        self.assertEqual(self.lib.get_languages_for_book("Test Book"), {'English', 'French'})

    def test_register_patron_new(self):
        self.lib.db.insert_patron = Mock(return_value=20)
        self.assertEqual(self.lib.register_patron("Test", "User", 20, 20), 20)
    
    def test_is_patron_registered_true(self):
        patron = Patron("Big", "Bob", 20, 5)
        self.lib.db.retrieve_patron = Mock(return_value=patron)
        self.assertTrue(self.lib.is_patron_registered(patron))
    
    def test_register_patron_returns_id(self):
        patron_id = self.lib.register_patron("Bob", "Smith", 69, 21)
        # Check that the patron ID is not None
        self.assertIsNotNone(patron_id)
    
    def test_is_patron_registered_false(self):
        patron = Patron("Big", "Bob", 20, 5)
        self.lib.db.retrieve_patron = Mock(return_value=None)
        self.assertFalse(self.lib.is_patron_registered(patron))
    
    def test_borrow_book(self):
        patron = Patron("Big", "Bob", 20, 5)
        book = "TestBook"
        self.lib.db.update_patron = Mock()
        self.lib.borrow_book(book, patron)
        self.lib.db.update_patron.assert_called_with(patron)
        self.assertIn(book.lower(), patron.borrowed_books)
    
    def test_return_borrowed_book(self):
        patron = Patron("Big", "Bob", 20, 5)
        book = "TestBook"
        self.lib.db.update_patron = Mock()
        self.lib.return_borrowed_book(book, patron)
        self.lib.db.update_patron.assert_called_with(patron)
    
    def test_is_book_borrowed_true(self):
        patron = Patron("Big", "Bob", 20, 5)
        book = "TestBook"
        self.lib.db.update_patron = Mock()
        self.lib.borrow_book(book, patron)
        self.lib.db.update_patron.assert_called_with(patron)
        self.assertTrue(self.lib.is_book_borrowed(book, patron))
    
    def test_is_book_borrowed_false(self):
        patron = Patron("Big", "Bob", 20, 5)
        book = "TestBook"
        self.assertFalse(self.lib.is_book_borrowed(book, patron))



