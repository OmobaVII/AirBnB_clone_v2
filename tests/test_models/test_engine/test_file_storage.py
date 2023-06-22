#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models import storage
import os
from models.engine.file_storage import FileStorage
from models.state import State
import json
from os import getenv


@unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == "db",
                 "Wont test for DBStorage")
class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """
        self.storage = FileStorage()
        self.my_model = BaseModel()

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_new(self):
        """ New object is correctly added to __objects """
        self.storage.new(self.my_model)
        key = str(self.my_model.__class__.__name__ + "." + self.my_model.id)
        self.assertTrue(key in self.storage._FileStorage__objects)

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        try:
            self.storage.reload()
            self.assertTrue(True)
        except Exception as e:
            self.assertTrue(False)

    def test_reload_empty(self):
        """ Load from an empty file """
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        _id = new.to_dict()['id']
        for key in storage.all().keys():
            temp = key
        self.assertEqual(temp[9:10], ".")

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.file_storage import FileStorage
        print(type(storage))
        self.assertEqual(type(storage), FileStorage)

    def test_delete(self):
        """ test the delete method"""
        fs = FileStorage()
        new_state = State()
        fs.new(new_state)
        fs.save()
        fs.delete(new_state)
        with open("file.json") as myFile:
            for k, v in json.load(myFile).items():
                self.assertFalse(new_state.id == k.split("."[0]))

    def test_delete_none(self):
        """test the deleted method with None"""
        fs = FileStorage()
        new_state = State()
        new_state.name = "California"
        fs.new(new_state)
        fs.save()
        another_state = State()
        another_state.name = "Nevada"
        fs.new(another_state)
        fs.save()
        fs.delete(new_state)
        with open("file.json") as myFile:
            for k, v in json.load(myFile).items():
                self.assertEqual(len(fs.all(State)), 3)
