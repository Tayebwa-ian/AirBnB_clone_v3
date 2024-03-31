#!/usr/bin/python3
"""Test file storage module"""
import json
import unittest
import pycodestyle
import inspect
from models import storage, file_storage, User
from os import getenv

if getenv("HBNB_TYPE_STORAGE") != "db":
    class Test_file_storage(unittest.TestCase):
        """
        Test class for file storage
        All test cases writen in method like tests
        """

        @classmethod
        def setUpClass(cls) -> None:
            """Setup model instance to use in the test cases"""
            cls.fun_names = [name for name, _ in
                            inspect.getmembers(file_storage.FileStorage,
                                                inspect.ismethod)]
            cls.file_path = "file.json"
            cls.user = User()
            cls.user2 = User(first_name="Denash")

        def test_return_value_of_all_function(self) -> None:
            """Test the return value of all function"""
            with open(self.file_path, "r") as file:
                data = json.load(file)
            self.user.save()
            key = self.user.__class__.__name__ + ".{}".format(self.user.id)
            data[key] = self.user.to_dict()
            all_dict = {key: storage.all()[key].to_dict()
                        for key in storage.all().keys()}
            self.assertEqual(data, all_dict, "stored data differing")

        def test_file_update(self) -> None:
            """Check if the json file is updated with new obj
            Upon creation of a new obj
            """
            with open(self.file_path, "r") as file:
                data = json.load(file)
            self.user.save()
            self.assertEqual(len(data) + 1, len(storage.all()),
                            "")

        def test_documentation(self) -> None:
            """Test if module, class and methods documentations exist"""
            self.assertGreater(len(storage.__doc__), 0)
            self.assertGreater(len(file_storage.__doc__), 0)
            for func in self.fun_names:
                with self.subTest(func):
                    self.assertGreater(len(func.__doc__), 0,
                                    f"Missing documentation of {func} method")

        def test_pep8_complaince(self) -> None:
            """Check if module is complaint when you run pycodestyle on it"""
            style_checker = pycodestyle.StyleGuide()
            result = style_checker.check_files(['models/engine/file_storage.py'])
            self.assertEqual(result.total_errors, 0, "PEP 8 violations found")

        def test_get_function(self) -> None:
            """test retrieving of a single object"""
            obj = self.user2
            obj.save()
            result = storage.get(User, self.user2.id)
            self.assertEqual(obj.id, result.id,
                            "A single object can not be retrieved")

        def test_count_function(self) -> None:
            """Check if the correct number of all object in storage is returned"""
            with open(self.file_path, "r") as file:
                data = json.load(file)
            self.assertEqual(len(data), len(storage.all()),
                            "Incorrect count for the number \
                                of objects in file storage")


    if __name__ == "__main__":
        unittest.main()
