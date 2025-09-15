#!/usr/bin/python3
"""
Module documentation
"""

import unittest
from models.base_model import BaseModel
from models.city import City


class TestCity(unittest.TestCase):
    """ Test the City Class """

    def test_instance(self):
        """ Test instance """
        obj = City()
        self.assertIsInstance(obj, City)

    def test_is_subclass(self):
        """ Test the instance of sub classes """
        city = City()
        self.assertTrue(issubclass(type(city), BaseModel))

    def test_name(self):
        """ Test name """
        city = City()
        self.assertEqual(city.name, "")
        city.name = "Kigali"
        self.assertEqual(city.name, "Kigali")

    def test_city_id(self):
        """ Test city id """
        city = City()
        self.assertEqual(city.state_id, "")


if __name__ == "__main__":
    unittest.main()
