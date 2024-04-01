#!/usr/bin/python3
"""Test Amenity Module"""

import unittest
from datetime import datetime, timedelta
from uuid import UUID
import pycodestyle
import inspect
import models

amenity = models.amenity


class Test_amenity(unittest.TestCase):
    """
    Test class for Amenity Model
    All test cases writen in method like tests
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Setup model instance to use in the test cases"""
        cls.a1 = amenity.Amenity(name="TV")
        cls.a2 = amenity.Amenity(name="wifi")
        cls.out_dict = cls.a1.to_dict()
        cls.temp_dict = {
            "name": "Swimming Pool",
            "__class__": "Amenity",
            "updated_at": "2017-09-28T21:05:54.119572",
            "id": "b6a6e15c-c67d-4312-9a75-9d084935e579",
            "created_at": "2017-09-28T21:05:54.119427",
            "name": "Kitchen"
        }
        cls.a3 = amenity.Amenity(**cls.out_dict)
        cls.a4 = amenity.Amenity(**cls.temp_dict)
        cls.fun_names = [name for name, _ in
                         inspect.getmembers(amenity.Amenity,
                                            inspect.ismethod)]

    def test_documentation(self) -> None:
        """Test if module, class and methods documentations exist"""
        self.assertGreater(len(self.a1.__doc__), 0)
        self.assertGreater(len(amenity.__doc__), 0)
        for func in self.fun_names:
            with self.subTest(func):
                self.assertGreater(len(func.__doc__), 0,
                                   f"Missing documentation of {func} method")

    def test_public_attrs(self) -> None:
        """
        Check if public attrs are accessible outside the class
        And have correct values
        """
        current_date = datetime.now()
        self.assertAlmostEqual(self.a1.created_at,
                               current_date,
                               delta=timedelta(seconds=1))
        self.assertAlmostEqual(self.a1.updated_at,
                               current_date,
                               delta=timedelta(seconds=1))
        self.assertIsNotNone(self.a2.id)

    def test_uuid(self) -> None:
        """Check if the generated id is a string and a UUID instance"""
        self.assertIsInstance(self.a2.id, str)
        self.assertIsInstance(UUID(self.a2.id), UUID)
        # test with dict passed as an arg unpon instantiation
        self.assertIsInstance(self.a4.id, str)
        self.assertIsInstance(UUID(self.a4.id), UUID)

    def test_inbuilt_str(self) -> None:
        """Check correct output of __str__ method"""
        output1 = "[{}] ({}) {}".format(self.a1.__class__.__name__,
                                        self.a1.id, self.a1.__dict__)
        output2 = "[{}] ({}) {}".format(self.a2.__class__.__name__,
                                        self.a2.id, self.a2.__dict__)
        output4 = "[{}] ({}) {}".format(self.a4.__class__.__name__,
                                        self.a4.id, self.a4.__dict__)
        self.assertEqual(str(self.a1), output1)
        self.assertEqual(str(self.a2), output2)
        # test with dict passed as an arg unpon instantiation
        self.assertEqual(str(self.a4), output4)

    def test_date_update_on_save(self) -> None:
        """Check if updated_at attr is updated upon save"""
        self.a1.save()
        self.a4.save()
        current_date = datetime.now()
        self.assertAlmostEqual(self.a1.updated_at,
                               current_date,
                               delta=timedelta(seconds=1))
        # test with dict passed as an arg unpon instantiation
        self.assertAlmostEqual(self.a4.updated_at,
                               current_date,
                               delta=timedelta(seconds=1))

    def test_to_dict_return_type(self) -> None:
        """check if the return type of to_dict method is a dictionary"""
        self.assertIsInstance(self.a2.to_dict(), dict)
        # test with dict passed as an arg unpon instantiation
        self.assertIsInstance(self.a4.to_dict(), dict)
        self.assertIsInstance(self.a3.to_dict(), dict)

    def test_to_dict_correct_values(self) -> None:
        """
        Check if correct values have been added to the dictionary
        returned by to_dict method
        """
        dict1 = self.a1.__dict__
        dict2 = self.a1.to_dict()
        self.assertTrue("__class__" in dict2.keys())
        self.assertTrue(dict2["__class__"] == self.a1.__class__.__name__)
        # check if all value in dict1 are in dict2
        self.assertTrue(all(key in dict2.keys() for key in dict1.keys()))

    def test_date_formats(self) -> None:
        """
        check if dates in the to_dict method returned dictionary
        are strings in format %Y-%m-%dT%H:%M:%S.%f
        """
        created = self.a1.to_dict()["created_at"]
        updated = self.a1.to_dict()["updated_at"]
        created2 = self.a4.to_dict()["created_at"]
        updated2 = self.a4.to_dict()["updated_at"]
        self.assertIsInstance(created, str)
        self.assertIsInstance(updated, str)
        self.assertEqual(created, self.a1.created_at.isoformat())
        self.assertEqual(updated, self.a1.updated_at.isoformat())
        # test with dict passed as an arg unpon instantiation
        self.assertIsInstance(created2, str)
        self.assertIsInstance(updated2, str)
        self.assertEqual(created2, self.a4.created_at.isoformat())
        self.assertEqual(updated2, self.a4.updated_at.isoformat())

    def test_object_creation_from_dict(self) -> None:
        """
        Check is an is correctly created
        when dict is passed as an arguments during instantiation
        """
        self.assertEqual(self.a3.created_at,
                         datetime.fromisoformat(self.out_dict["created_at"]))
        self.assertEqual(self.a3.updated_at,
                         datetime.fromisoformat(self.out_dict["updated_at"]))
        # check if self.a3 has not attribute __class__
        self.assertFalse("__class__" in self.a4.__dict__.keys())
        self.assertIsInstance(self.a4.id, str)
        self.assertFalse("__class__" in self.a3.__dict__.keys())
        self.assertIsInstance(self.a3.id, str)

    def test_pep8_complaince(self) -> None:
        """Check if module is complaint when you run pycodestyle on it"""
        style_checker = pycodestyle.StyleGuide()
        result = style_checker.check_files(['models/amenity.py'])
        self.assertEqual(result.total_errors, 0, "PEP 8 violations found")


if __name__ == "__main__":
    unittest.main()
