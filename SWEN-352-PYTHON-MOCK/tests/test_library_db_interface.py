import unittest
from unittest.mock import Mock, call
from library import library_db_interface
from library.patron import Patron

class TestLibbraryDBInterface(unittest.TestCase):

    def setUp(self):
        self.db_interface = library_db_interface.Library_DB()
    
    def test_database_file(self):
        db = library_db_interface.Library_DB()
        self.assertEqual(db.DATABASE_FILE, 'db.json')

    def test_insert_patron_not_in_db(self):
        patron_mock = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=None)
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        self.db_interface.db.insert = Mock(return_value=10)
        self.assertEqual(self.db_interface.insert_patron(patron_mock), 10)

    def test_update_patron(self):
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        db_update_mock = Mock()
        self.db_interface.db.update = db_update_mock
        self.db_interface.update_patron(Mock())
        db_update_mock.assert_called()

    def test_convert_patron_to_db_format(self):
        patron_mock = Mock()

        patron_mock.get_fname = Mock(return_value=1)
        patron_mock.get_lname = Mock(return_value=2)
        patron_mock.get_age = Mock(return_value=3)
        patron_mock.get_memberID = Mock(return_value=4)
        patron_mock.get_borrowed_books = Mock(return_value=5)
        self.assertEqual(self.db_interface.convert_patron_to_db_format(patron_mock),
                         {'fname': 1, 'lname': 2, 'age': 3, 'memberID': 4,
                          'borrowed_books': 5})

    def test_insert_patron_already_in_db(self):
        patron_mock = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=patron_mock)
        self.assertEqual(self.db_interface.insert_patron(patron_mock), None)

    def test_update_patron_not_in_db(self):
        patron_mock = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=None)
        self.assertEqual(self.db_interface.update_patron(patron_mock), None)
    
    def test_update_patron(self):
        # Create a new patron
        fname = "John"
        lname = "Doe"
        age = 30
        memberID = 123
        patron = Patron(fname, lname, age, memberID)
        self.db_interface.insert_patron(patron)
        new_fname = "Jane"
        new_lname = "Doe"
        new_age = 35
        new_patron = Patron(new_fname, new_lname, new_age, memberID)
        self.db_interface.update_patron(new_patron)
        updated_patron = self.db_interface.retrieve_patron(memberID)
        # Check that the patron's data has been updated correctly
        self.assertEqual(updated_patron.get_fname(), new_fname)
        self.assertEqual(updated_patron.get_lname(), new_lname)
        self.assertEqual(updated_patron.get_age(), new_age)

    def test_retrieve_patron_not_in_db(self):
        self.db_interface.db.purge_tables()
        result = self.db_interface.retrieve_patron('nonexistent_memberID')
        self.assertEqual(result, None)

    def test_retrieve_patron_in_db(self):
        self.db_interface.db.purge_tables()
        patron_mock = Patron('John', 'Doe', 25, '123')
        self.db_interface.insert_patron(patron_mock)
        result = self.db_interface.retrieve_patron('123')
        self.assertEqual(result.get_memberID(), patron_mock.get_memberID())
        self.assertEqual(result.get_fname(), patron_mock.get_fname())
        self.assertEqual(result.get_lname(), patron_mock.get_lname())
        self.assertEqual(result.get_age(), patron_mock.get_age())
        self.assertEqual(result.get_borrowed_books(), patron_mock.get_borrowed_books())
    
    def test_insert_patron_is_none(self):
        self.assertIsNone(self.db_interface.insert_patron(None))
    
    def test_update_patron_is_none(self):
        self.assertIsNone(self.db_interface.update_patron(None))

    def test_close_db(self):
        db_close_mock = Mock()
        self.db_interface.db.close = db_close_mock
        self.db_interface.close_db()
        db_close_mock.assert_called_once()

    def test_get_patron_count_returns_zero_for_empty_db(self):
        self.assertEqual(self.db_interface.get_patron_count(), 0)

    def test_get_patron_count_returns_correct_count_for_single_patron(self):
        patron_mock = Mock()
        self.db_interface.db.insert = Mock(return_value=1)
        self.db_interface.db.all = Mock(return_value=[patron_mock])
        self.db_interface.insert_patron(patron_mock)
        self.assertEqual(self.db_interface.get_patron_count(), 1)

    def test_get_patron_count_returns_correct_count_for_multiple_patrons(self):
        patron_mock1 = Mock()
        patron_mock2 = Mock()
        self.db_interface.db.insert = Mock(return_value=1)
        self.db_interface.insert_patron(patron_mock1)
        self.db_interface.db.insert = Mock(return_value=2)
        self.db_interface.insert_patron(patron_mock2)
        self.db_interface.db.all = Mock(return_value=[patron_mock1, patron_mock2])
        self.assertEqual(self.db_interface.get_patron_count(), 2)

    def test_get_all_patrons_returns_empty_list_if_db_is_empty(self):
        self.db_interface.db.purge() # remove all patrons from the db
        self.assertEqual(self.db_interface.get_all_patrons(), [])

    def test_get_all_patrons_returns_correct_list_of_patrons(self):
        # create some test patrons and add them to the db
        patron1 = Patron('John', 'Doe', 30, 'JD123')
        patron2 = Patron('Jane', 'Doe', 25, 'JD456')
        self.db_interface.insert_patron(patron1)
        self.db_interface.insert_patron(patron2)

        # retrieve all patrons from the db and compare to expected list
        expected_patrons = [patron1, patron2]
        self.db_interface.db.all = Mock(return_value=[patron1, patron2])
        actual_patrons = self.db_interface.get_all_patrons()
        self.assertEqual(len(actual_patrons), len(expected_patrons))
        for actual, expected in zip(actual_patrons, expected_patrons):
            self.assertEqual(actual.get_fname(), expected.get_fname())
            self.assertEqual(actual.get_lname(), expected.get_lname())
            self.assertEqual(actual.get_age(), expected.get_age())
            self.assertEqual(actual.get_memberID(), expected.get_memberID())
            self.assertEqual(actual.get_borrowed_books(), expected.get_borrowed_books())
