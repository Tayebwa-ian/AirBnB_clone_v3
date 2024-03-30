#!/usr/bin/python3
"""Test Place Module"""
import unittest
from datetime import datetime, timedelta
from uuid import UUID
import pycodestyle
import inspect
import models

place = models.place


class Test_base_model(unittest.TestCase):
    """
    Test class for Place model
    All test cases writen in method like tests
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Setup model instance to use in the test cases"""
        cls.p1 = place.Place()
        cls.p2 = place.Place()
        cls.out_dict = cls.p1.to_dict()
        cls.temp_dict = {
            "city_id": "9089bd19-f489-4540-9ffc-5c60f409d86d",
            "name": "Arua",
            "__class__": "Place",
            "updated_at": "2017-09-28T21:05:54.119572",
            "id": "b6a6e15c-c67d-4312-9a75-9d084935e579",
            "created_at": "2017-09-28T21:05:54.119427",
        }
        cls.p3 = place.Place(**cls.out_dict)
        cls.p4 = place.Place(**cls.temp_dict)
        cls.fun_names = [name for name, _ in
                         inspect.getmembers(place.Place,
                                            inspect.ismethod)]

    def test_documentation(self) -> None:
        """Test if module, class and methods documentations exist"""
        self.assertGreater(len(self.p1.__doc__), 0)
        self.assertGreater(len(place.__doc__), 0)
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
        self.assertAlmostEqual(self.p1.created_at,
                               current_date,
                               delta=timedelta(seconds=1))
        self.assertAlmostEqual(self.p1.updated_at,
                               current_date,
                               delta=timedelta(seconds=1))
        self.assertIsNotNone(self.p2.id)

    def test_uuid(self) -> None:
        """Check if the generated id is a string and a UUID instance"""
        self.assertIsInstance(self.p2.id, str)
        self.assertIsInstance(UUID(self.p2.id), UUID)
        # test with dict passed as an arg unpon instantiation
        self.assertIsInstance(self.p4.id, str)
        self.assertIsInstance(UUID(self.p4.id), UUID)

    def test_inbuilt_str(self) -> None:
        """Check correct output of __str__ method"""
        output1 = "[{}] ({}) {}".format(self.p1.__class__.__name__,
                                        self.p1.id, self.p1.__dict__)
        output2 = "[{}] ({}) {}".format(self.p2.__class__.__name__,
                                        self.p2.id, self.p2.__dict__)
        output4 = "[{}] ({}) {}".format(self.p4.__class__.__name__,
                                        self.p4.id, self.p4.__dict__)
        self.assertEqual(str(self.p1), output1)
        self.assertEqual(str(self.p2), output2)
        # test with dict passed as an arg unpon instantiation
        self.assertEqual(str(self.p4), output4)

    def test_date_update_on_save(self) -> None:
        """Check if updated_at attr is updated upon save"""
        self.p1.save()
        self.p4.save()
        current_date = datetime.now()
        self.assertAlmostEqual(self.p1.updated_at,
                               current_date,
                               delta=timedelta(seconds=1))
        # test with dict passed as an arg unpon instantiation
        self.assertAlmostEqual(self.p4.updated_at,
                               current_date,
                               delta=timedelta(seconds=1))

    def test_to_dict_return_type(self) -> None:
        """check if the return type of to_dict method is a dictionary"""
        self.assertIsInstance(self.p2.to_dict(), dict)
        # test with dict passed as an arg unpon instantiation
        self.assertIsInstance(self.p4.to_dict(), dict)
        self.assertIsInstance(self.p3.to_dict(), dict)

    def test_to_dict_correct_values(self) -> None:
        """
        Check if correct values have been added to the dictionary
        returned by to_dict method
        """
        dict1 = self.p1.__dict__
        dict2 = self.p1.to_dict()
        self.assertTrue("__class__" in dict2.keys())
        self.assertTrue(dict2["__class__"] == self.p1.__class__.__name__)
        # check if all value in dict1 are in dict2
        self.assertTrue(all(key in dict2.keys() for key in dict1.keys()))

    def test_date_formats(self) -> None:
        """
        check if dates in the to_dict method returned dictionary
        are strings in format %Y-%m-%dT%H:%M:%S.%f
        """
        created = self.p1.to_dict()["created_at"]
        updated = self.p1.to_dict()["updated_at"]
        created2 = self.p4.to_dict()["created_at"]
        updated2 = self.p4.to_dict()["updated_at"]
        self.assertIsInstance(created, str)
        self.assertIsInstance(updated, str)
        self.assertEqual(created, self.p1.created_at.isoformat())
        self.assertEqual(updated, self.p1.updated_at.isoformat())
        # test with dict passed as an arg unpon instantiation
        self.assertIsInstance(created2, str)
        self.assertIsInstance(updated2, str)
        self.assertEqual(created2, self.p4.created_at.isoformat())
        self.assertEqual(updated2, self.p4.updated_at.isoformat())

    def test_object_creation_from_dict(self) -> None:
        """
        Check is an is correctly created
        when dict is passed as an arguments during instantiation
        """
        self.assertEqual(self.p3.created_at,
                         datetime.fromisoformat(self.out_dict["created_at"]))
        self.assertEqual(self.p3.updated_at,
                         datetime.fromisoformat(self.out_dict["updated_at"]))
        # check if self.p3 has not attribute __class__
        self.assertFalse("__class__" in self.p4.__dict__.keys())
        self.assertIsInstance(self.p4.id, str)
        self.assertFalse("__class__" in self.p3.__dict__.keys())
        self.assertIsInstance(self.p3.id, str)

    def test_pep8_complaince(self) -> None:
        """Check if module is complaint when you run pycodestyle on it"""
        style_checker = pycodestyle.StyleGuide()
        result = style_checker.check_files(['models/place.py'])
        self.assertEqual(result.total_errors, 0, "PEP 8 violations found")


if __name__ == "__main__":
    unittest.main()
