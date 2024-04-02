#!/usr/bin/python3
"""BaseModel unit tests module
"""
import unittest
from datetime import datetime, timedelta
from uuid import UUID
import pycodestyle
import inspect
import models
from os import getenv

base_model = models.base_model

if getenv("HBNB_TYPE_STORAGE") != "db":
    class Test_base_model(unittest.TestCase):
        """
        Test class for base model
        All test cases writen in method like tests
        """

        @classmethod
        def setUpClass(cls) -> None:
            """Setup model instance to use in the test cases"""
            cls.b1 = base_model.BaseModel()
            cls.b2 = base_model.BaseModel()
            cls.out_dict = cls.b1.to_dict()
            cls.temp_dict = {
                "my_number": 89,
                "name": "My First Model",
                "__class__": "BaseModel",
                "updated_at": "2017-09-28T21:05:54.119572",
                "id": "b6a6e15c-c67d-4312-9a75-9d084935e579",
                "created_at": "2017-09-28T21:05:54.119427",
            }
            cls.b3 = base_model.BaseModel(**cls.out_dict)
            cls.b4 = base_model.BaseModel(**cls.temp_dict)
            functions = inspect.getmembers(base_model.
                                           BaseModel, inspect.ismethod)
            cls.fun_names = [name for name, _ in functions]

        def test_documentation(self) -> None:
            """Test if module, class and methods documentations exist"""
            self.assertGreater(len(self.b1.__doc__), 0)
            self.assertGreater(len(base_model.__doc__), 0)
            for func in self.fun_names:
                with self.subTest(func):
                    self.assertGreater(len(func.__doc__), 0,
                                       "Missing documentation \
                                        of {} method".format(func))

        def test_public_attrs(self) -> None:
            """
            Check if public attrs are accessible outside the class
            And have correct values
            """
            current_date = datetime.now()
            self.assertAlmostEqual(self.b1.created_at,
                                   current_date,
                                   delta=timedelta(seconds=1))
            self.assertAlmostEqual(self.b1.updated_at,
                                   current_date,
                                   delta=timedelta(seconds=1))
            self.assertIsNotNone(self.b2.id)

        def test_uuid(self) -> None:
            """Check if the generated id is a string and a UUID instance"""
            self.assertIsInstance(self.b2.id, str)
            self.assertIsInstance(UUID(self.b2.id), UUID)
            # test with dict passed as an arg unpon instantiation
            self.assertIsInstance(self.b4.id, str)
            self.assertIsInstance(UUID(self.b4.id), UUID)

        def test_inbuilt_str(self) -> None:
            """Check correct output of __str__ method"""
            output1 = "[{}] ({}) {}".format(self.b1.__class__.__name__,
                                            self.b1.id, self.b1.__dict__)
            output2 = "[{}] ({}) {}".format(self.b2.__class__.__name__,
                                            self.b2.id, self.b2.__dict__)
            output4 = "[{}] ({}) {}".format(self.b4.__class__.__name__,
                                            self.b4.id, self.b4.__dict__)
            self.assertEqual(str(self.b1), output1)
            self.assertEqual(str(self.b2), output2)
            # test with dict passed as an arg unpon instantiation
            self.assertEqual(str(self.b4), output4)

        def test_date_update_on_save(self) -> None:
            """Check if updated_at attr is updated upon save"""
            self.b1.save()
            self.b4.save()
            current_date = datetime.now()
            self.assertAlmostEqual(self.b1.updated_at,
                                   current_date,
                                   delta=timedelta(seconds=1))
            # test with dict passed as an arg unpon instantiation
            self.assertAlmostEqual(self.b4.updated_at,
                                   current_date,
                                   delta=timedelta(seconds=1))

        def test_to_dict_return_type(self) -> None:
            """check if the return type of to_dict method is a dictionary"""
            self.assertIsInstance(self.b2.to_dict(), dict)
            # test with dict passed as an arg unpon instantiation
            self.assertIsInstance(self.b4.to_dict(), dict)
            self.assertIsInstance(self.b3.to_dict(), dict)

        def test_to_dict_correct_values(self) -> None:
            """
            Check if correct values have been added to the dictionary
            returned by to_dict method
            """
            dict1 = self.b1.__dict__
            dict2 = self.b1.to_dict()
            self.assertTrue("__class__" in dict2.keys())
            self.assertTrue(dict2["__class__"] == self.b1.__class__.__name__)
            # check if all value in dict1 are in dict2
            self.assertTrue(all(key in dict2.keys() for key in dict1.keys()))

        def test_date_formats(self) -> None:
            """
            check if dates in the to_dict method returned dictionary
            are strings in format %Y-%m-%dT%H:%M:%S.%f
            """
            created = self.b1.to_dict()["created_at"]
            updated = self.b1.to_dict()["updated_at"]
            created2 = self.b4.to_dict()["created_at"]
            updated2 = self.b4.to_dict()["updated_at"]
            self.assertIsInstance(created, str)
            self.assertIsInstance(updated, str)
            self.assertEqual(created, self.b1.created_at.isoformat())
            self.assertEqual(updated, self.b1.updated_at.isoformat())
            # test with dict passed as an arg unpon instantiation
            self.assertIsInstance(created2, str)
            self.assertIsInstance(updated2, str)
            self.assertEqual(created2, self.b4.created_at.isoformat())
            self.assertEqual(updated2, self.b4.updated_at.isoformat())

        def test_object_creation_from_dict(self) -> None:
            """
            Check is an is correctly created
            when dict is passed as an arguments during instantiation
            """
            self.assertEqual(self.b3.created_at, datetime.
                             fromisoformat(self.out_dict["created_at"]))
            self.assertEqual(self.b3.updated_at, datetime.
                             fromisoformat(self.out_dict["updated_at"]))
            # check if self.b3 has not attribute __class__
            self.assertFalse("__class__" in self.b4.__dict__.keys())
            self.assertIsInstance(self.b4.id, str)
            self.assertFalse("__class__" in self.b3.__dict__.keys())
            self.assertIsInstance(self.b3.id, str)

        def test_pep8_complaince(self) -> None:
            """Check if module is complaint when you run pycodestyle on it"""
            style_checker = pycodestyle.StyleGuide()
            result = style_checker.check_files(['models/base_model.py'])
            self.assertEqual(result.total_errors, 0, "PEP 8 violations found")

    if __name__ == "__main__":
        unittest.main()
