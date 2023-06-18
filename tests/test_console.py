#!/usr/bin/python3
"""
Unittest for console interpreter
"""
import unittest
from io import StringIO
import os
import tests
import json
import console
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.review import Review
from models.engine.file_storage import FileStorage
from unittest.mock import patch


class TestConsole(unittest.TestCase):
    """Unittest for console"""

    def setUp(self):
        """used to setup the test"""
        pass

    def tearDown(self):
        """used to tear down the test"""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_doc(self):
        """tests the documentation in console"""
        self.assertIsNotNone(console.__doc__)

    def test_emptyline(self):
        """tests when there is no input"""
        inputs = console.HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("\n")
            self.assertIs(output.getvalue(), "")

    def test_create(self):
        """test the output for create"""
        inputs = console.HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("create")
            self.assertEqual(output.getvalue(), "** class name missing **\n")
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("create myModel")
            self.assertEqual(output.getvalue(), "** class doesn't exist **\n")
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("create Place name=Benin")
            self.assertTrue(isinstance(output.getvalue(), str))

    def test_show(self):
        """test the output for show"""
        inputs = console.HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("show")
            self.assertEqual(output.getvalue(), "** class name missing **\n")
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("show MyModel")
            self.assertEqual(output.getvalue(), "** class doesn't exist **\n")
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("show BaseModel")
            self.assertEqual(output.getvalue(), "** instance id missing **\n")
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("show BaseModel 121212")
            self.assertEqual(output.getvalue(), "** no instance found **\n")
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("BaseModel.show('Bar')")
            self.assertEqual(output.getvalue(), "** no instance found **\n")

    def test_destroy(self):
        """test the output for destroy"""
        inputs = console.HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("destroy")
            self.assertEqual(output.getvalue(), "** class name missing **\n")
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("destroy MyModel")
            self.assertEqual(output.getvalue(), "** class doesn't exist **\n")
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("destroy BaseModel")
            self.assertEqual(output.getvalue(), "** instance id missing **\n")
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("destroy BaseModel 4030222910")
            self.assertEqual(output.getvalue(), "** no instance found **\n")
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("BaseModel.destroy('4030222910')")
            self.assertEqual(output.getvalue(), "** no instance found **\n")

    def test_all(self):
        """test the output for all"""
        inputs = console.HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("all Mymodel")
            self.assertEqual(output.getvalue(), "** class doesn't exist **\n")
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("all BaseModel")
            self.assertEqual(output.getvalue()[:12], "[]\n")
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("create City")
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("City.all")
            self.assertEqual(output.getvalue()[:7], "[[City]")

    def test_update(self):
        """test the output for update"""
        inputs = console.HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("update")
            self.assertEqual(output.getvalue(), "** class name missing **\n")
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("update Mymodel")
            self.assertEqual(output.getvalue(), "** class doesn't exist **\n")
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("update Place")
            self.assertEqual(output.getvalue(), "** instance id missing **\n")
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("update Place 121212")
            self.assertEqual(output.getvalue(), "** no instance found **\n")
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("update")
            self.assertEqual(output.getvalue(), "** class name missing **\n")

    def test_count(self):
        """test the output for count"""
        inputs = console.HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("create User")
            inputs.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("count User")
            self.assertEqual(output.getvalue(), "2\n")
        with patch('sys.stdout', new=StringIO()) as output:
            inputs.onecmd("User.count()")
            self.assertEqual(output.getvalue(), "2\n")


if __name__ == "__main__":
    unittest.main()
