#!/usr/bin/python3
"""Test Review module"""

import unittest
from datetime import datetime, timedelta
from uuid import UUID
import pycodestyle
import inspect
import models

review = models.review
place = models.place
user = models.user
city = models.city
state = models.state


class Test_review(unittest.TestCase):
    """
    Test class for Review model
    All test cases writen in method like tests
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Setup model instance to use in the test cases"""
        cls.u = user.User(email="dora@hotmail.com", first_name="Doreen",
                          password="123hysgy")
        cls.u1 = user.User(email="su@yahoo.com", first_name="Suzan",
                           password="SenseD0")
        cls.u.save()
        cls.u1.save()
        cls.s = state.State(name="Rwanda")
        cls.s.save()
        cls.c = city.City(name="Kigali", state_id=cls.s.id)
        cls.c.save()
        cls.p = place.Place(name="ishina", city_id=cls.c.id,
                            user_id=cls.u.id)
        cls.p1 = place.Place(name="nyama", city_id=cls.c.id,
                             user_id=cls.u1.id)
        cls.p.save()
        cls.p1.save()
        cls.r1 = review.Review(text="A good place", user_id=cls.u.id,
                               place_id=cls.p.id)
        cls.r2 = review.Review(text="welcoming", user_id=cls.u1.id,
                               place_id=cls.p1.id)
        cls.out_dict = cls.r1.to_dict()
        cls.temp_dict = {
            "user_id": cls.u1.id,
            "text": "Hospitable and clean",
            "__class__": "Review",
            "updated_at": "2017-09-28T21:05:54.119572",
            "id": "b6a6e15c-c67d-4312-9a75-9d084935e579",
            "created_at": "2017-09-28T21:05:54.119427",
            "place_id": cls.p1.id,
        }
        cls.r3 = review.Review(**cls.out_dict)
        cls.r4 = review.Review(**cls.temp_dict)
        cls.fun_names = [name for name, _ in
                         inspect.getmembers(review.Review,
                                            inspect.ismethod)]

    def test_documentation(self) -> None:
        """Test if module, class and methods documentations exist"""
        self.assertGreater(len(self.r1.__doc__), 0)
        self.assertGreater(len(review.__doc__), 0)
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
        self.assertAlmostEqual(self.r1.created_at,
                               current_date,
                               delta=timedelta(seconds=1))
        self.assertAlmostEqual(self.r1.updated_at,
                               current_date,
                               delta=timedelta(seconds=1))
        self.assertIsNotNone(self.r2.id)

    def test_uuid(self) -> None:
        """Check if the generated id is a string and a UUID instance"""
        self.assertIsInstance(self.r2.id, str)
        self.assertIsInstance(UUID(self.r2.id), UUID)
        # test with dict passed as an arg unpon instantiation
        self.assertIsInstance(self.r4.id, str)
        self.assertIsInstance(UUID(self.r4.id), UUID)

    def test_inbuilt_str(self) -> None:
        """Check correct output of __str__ method"""
        output1 = "[{}] ({}) {}".format(self.r1.__class__.__name__,
                                        self.r1.id, self.r1.__dict__)
        output2 = "[{}] ({}) {}".format(self.r2.__class__.__name__,
                                        self.r2.id, self.r2.__dict__)
        output4 = "[{}] ({}) {}".format(self.r4.__class__.__name__,
                                        self.r4.id, self.r4.__dict__)
        self.assertEqual(str(self.r1), output1)
        self.assertEqual(str(self.r2), output2)
        # test with dict passed as an arg unpon instantiation
        self.assertEqual(str(self.r4), output4)

    def test_date_update_on_save(self) -> None:
        """Check if updated_at attr is updated upon save"""
        self.r1.save()
        self.r4.save()
        current_date = datetime.now()
        self.assertAlmostEqual(self.r1.updated_at,
                               current_date,
                               delta=timedelta(seconds=1))
        # test with dict passed as an arg unpon instantiation
        self.assertAlmostEqual(self.r4.updated_at,
                               current_date,
                               delta=timedelta(seconds=1))

    def test_to_dict_return_type(self) -> None:
        """check if the return type of to_dict method is a dictionary"""
        self.assertIsInstance(self.r2.to_dict(), dict)
        # test with dict passed as an arg unpon instantiation
        self.assertIsInstance(self.r4.to_dict(), dict)
        self.assertIsInstance(self.r3.to_dict(), dict)

    def test_to_dict_correct_values(self) -> None:
        """
        Check if correct values have been added to the dictionary
        returned by to_dict method
        """
        dict1 = self.r1.__dict__
        dict2 = self.r1.to_dict()
        self.assertTrue("__class__" in dict2.keys())
        self.assertTrue(dict2["__class__"] == self.r1.__class__.__name__)
        # check if all value in dict1 are in dict2
        self.assertTrue(all(key in dict2.keys() for key in dict1.keys()))

    def test_date_formats(self) -> None:
        """
        check if dates in the to_dict method returned dictionary
        are strings in format %Y-%m-%dT%H:%M:%S.%f
        """
        created = self.r1.to_dict()["created_at"]
        updated = self.r1.to_dict()["updated_at"]
        created2 = self.r4.to_dict()["created_at"]
        updated2 = self.r4.to_dict()["updated_at"]
        self.assertIsInstance(created, str)
        self.assertIsInstance(updated, str)
        self.assertEqual(created, self.r1.created_at.isoformat())
        self.assertEqual(updated, self.r1.updated_at.isoformat())
        # test with dict passed as an arg unpon instantiation
        self.assertIsInstance(created2, str)
        self.assertIsInstance(updated2, str)
        self.assertEqual(created2, self.r4.created_at.isoformat())
        self.assertEqual(updated2, self.r4.updated_at.isoformat())

    def test_object_creation_from_dict(self) -> None:
        """
        Check is an is correctly created
        when dict is passed as an arguments during instantiation
        """
        self.assertEqual(self.r3.created_at,
                         datetime.fromisoformat(self.out_dict["created_at"]))
        self.assertEqual(self.r3.updated_at,
                         datetime.fromisoformat(self.out_dict["updated_at"]))
        # check if self.r3 has not attribute __class__
        self.assertFalse("__class__" in self.r4.__dict__.keys())
        self.assertIsInstance(self.r4.id, str)
        self.assertFalse("__class__" in self.r3.__dict__.keys())
        self.assertIsInstance(self.r3.id, str)

    def test_pep8_complaince(self) -> None:
        """Check if module is complaint when you run pycodestyle on it"""
        style_checker = pycodestyle.StyleGuide()
        result = style_checker.check_files(['models/review.py'])
        self.assertEqual(result.total_errors, 0, "PEP 8 violations found")


if __name__ == "__main__":
    unittest.main()
