#!/usr/bin/python3
import unittest
from datetime import datetime, timedelta
from uuid import UUID
import pycodestyle
import inspect
import models

user = models.user


class Test_user(unittest.TestCase):
    """
    Test class for User model
    All test cases writen in method like tests
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Setup model instance to use in the test cases"""
        cls.u1 = user.User(email="markd@muni.ac.ug", first_name="Donald",
                           password="Calme342@")
        cls.u2 = user.User(email="Mutyaba@gfa.org", first_name="Ibra",
                           password="DoyourWork#124")
        cls.out_dict = cls.u1.to_dict()
        cls.temp_dict = {
            "age": 56,
            "first_name": "Denis",
            "__class__": "User",
            "updated_at": "2017-09-28T21:05:54.119572",
            "id": "b6a6e15c-c67d-4312-9a75-9d084935e579",
            "created_at": "2017-09-28T21:05:54.119427",
            "email": "deno@gmail.com",
            "password": "COYG@deno",
        }
        cls.u3 = user.User(**cls.out_dict)
        cls.u4 = user.User(**cls.temp_dict)
        cls.fun_names = [name for name, _ in
                         inspect.getmembers(user.User,
                                            inspect.ismethod)]

    def test_documentation(self) -> None:
        """Test if module, class and methods documentations exist"""
        self.assertGreater(len(self.u1.__doc__), 0)
        self.assertGreater(len(user.__doc__), 0)
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
        self.assertAlmostEqual(self.u1.created_at,
                               current_date,
                               delta=timedelta(seconds=1))
        self.assertAlmostEqual(self.u1.updated_at,
                               current_date,
                               delta=timedelta(seconds=1))
        self.assertIsNotNone(self.u2.id)

    def test_uuid(self) -> None:
        """Check if the generated id is a string and a UUID instance"""
        self.assertIsInstance(self.u2.id, str)
        self.assertIsInstance(UUID(self.u2.id), UUID)
        # test with dict passed as an arg unpon instantiation
        self.assertIsInstance(self.u4.id, str)
        self.assertIsInstance(UUID(self.u4.id), UUID)

    def test_inbuilt_str(self) -> None:
        """Check correct output of __str__ method"""
        output1 = "[{}] ({}) {}".format(self.u1.__class__.__name__,
                                        self.u1.id, self.u1.__dict__)
        output2 = "[{}] ({}) {}".format(self.u2.__class__.__name__,
                                        self.u2.id, self.u2.__dict__)
        output4 = "[{}] ({}) {}".format(self.u4.__class__.__name__,
                                        self.u4.id, self.u4.__dict__)
        self.assertEqual(str(self.u1), output1)
        self.assertEqual(str(self.u2), output2)
        # test with dict passed as an arg unpon instantiation
        self.assertEqual(str(self.u4), output4)

    def test_date_update_on_save(self) -> None:
        """Check if updated_at attr is updated upon save"""
        self.u1.save()
        self.u4.save()
        current_date = datetime.now()
        self.assertAlmostEqual(self.u1.updated_at,
                               current_date,
                               delta=timedelta(seconds=1))
        # test with dict passed as an arg unpon instantiation
        self.assertAlmostEqual(self.u4.updated_at,
                               current_date,
                               delta=timedelta(seconds=1))

    def test_to_dict_return_type(self) -> None:
        """check if the return type of to_dict method is a dictionary"""
        self.assertIsInstance(self.u2.to_dict(), dict)
        # test with dict passed as an arg unpon instantiation
        self.assertIsInstance(self.u4.to_dict(), dict)
        self.assertIsInstance(self.u3.to_dict(), dict)

    def test_to_dict_correct_values(self) -> None:
        """
        Check if correct values have been added to the dictionary
        returned by to_dict method
        """
        dict1 = self.u1.__dict__
        dict2 = self.u1.to_dict()
        self.assertTrue("__class__" in dict2.keys())
        self.assertTrue(dict2["__class__"] == self.u1.__class__.__name__)
        # check if all value in dict1 are in dict2
        self.assertTrue(all(key in dict2.keys() for key in dict1.keys()))

    def test_date_formats(self) -> None:
        """
        check if dates in the to_dict method returned dictionary
        are strings in format %Y-%m-%dT%H:%M:%S.%f
        """
        created = self.u1.to_dict()["created_at"]
        updated = self.u1.to_dict()["updated_at"]
        created2 = self.u4.to_dict()["created_at"]
        updated2 = self.u4.to_dict()["updated_at"]
        self.assertIsInstance(created, str)
        self.assertIsInstance(updated, str)
        self.assertEqual(created, self.u1.created_at.isoformat())
        self.assertEqual(updated, self.u1.updated_at.isoformat())
        # test with dict passed as an arg unpon instantiation
        self.assertIsInstance(created2, str)
        self.assertIsInstance(updated2, str)
        self.assertEqual(created2, self.u4.created_at.isoformat())
        self.assertEqual(updated2, self.u4.updated_at.isoformat())

    def test_object_creation_from_dict(self) -> None:
        """
        Check is an is correctly created
        when dict is passed as an arguments during instantiation
        """
        self.assertEqual(self.u3.created_at,
                         datetime.fromisoformat(self.out_dict["created_at"]))
        self.assertEqual(self.u3.updated_at,
                         datetime.fromisoformat(self.out_dict["updated_at"]))
        # check if self.u3 has not attribute __class__
        self.assertFalse("__class__" in self.u4.__dict__.keys())
        self.assertIsInstance(self.u4.id, str)
        self.assertFalse("__class__" in self.u3.__dict__.keys())
        self.assertIsInstance(self.u3.id, str)

    def test_pep8_complaince(self) -> None:
        """Check if module is complaint when you run pycodestyle on it"""
        style_checker = pycodestyle.StyleGuide()
        result = style_checker.check_files(['models/user.py'])
        self.assertEqual(result.total_errors, 0, "PEP 8 violations found")


if __name__ == "__main__":
    unittest.main()
