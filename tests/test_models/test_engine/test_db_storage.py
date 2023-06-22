#!/usr/bin/python3
""" Testing the db_storage"""
import unittest
import sys
from models.engine.db_storage import DBStorage
from models import storage
from models.user import User
from models.state import State
from models.city import City
from os import getenv
from io import StringIO


database = getenv("HBNB_TYPE_STORAGE")


@unittest.skipIf(database != "db", "Test DBStorage")
class test_DBStorage(unittest.TestCase):
    """test for the DBStorage class"""
    def setUp(self):
        """set up for test"""
        self.dbstorage = DBStorage()
        self.output = StringIO()
        sys.stdout = self.output

    def tearDown(self):
        """delete elements"""
        del self.dbstorage
        del self.output

    def create(self):
        """testing the create method on dbstorage"""
        return HBNBCommand()

    def test_new(self):
        """testing the new method"""
        new_state = State(name="California")
        self.assertTrue(new_state.name == "California")
