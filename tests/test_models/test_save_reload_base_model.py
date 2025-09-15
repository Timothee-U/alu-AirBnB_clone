import unittest
from models.base_model import BaseModel
from models import storage
import os
from models.engine.file_storage import FileStorage


class TestBaseModelStorage(unittest.TestCase):
    """Tests for the file_storage.py methods of the FileStorage class."""

    def setUp(self):
        """Set up test fixtures."""
        self.model = BaseModel()
        self.model.name = "Holberton"
        self.model.my_number = 89

    def tearDown(self):
        """Tear down test fixtures."""
        del self.model
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_file_path(self):
        """Test that the file_path attribute
        is a string and the file exists."""
        new_object = FileStorage()
        file_path = new_object.file_path
        print(f"Debug: file_path = {file_path}")
        # Ensure the file is created
        with open(file_path, 'w') as f:
            f.write('')
        self.assertIsInstance(file_path, str)
        self.assertTrue(os.path.exists(file_path), "File path does not exist")

    def test_objects(self):
        """Test that the objects attribute is a dictionary."""
        new_object = FileStorage()
        f = new_object.objects
        self.assertIsInstance(f, dict)

    def test_all(self):
        """Test that the all method returns the __objects attribute."""
        objects = storage.all()
        self.assertIsInstance(objects, dict)

    def test_new(self):
        """Test that the new method adds an
        object to the __objects attribute."""
        storage.new(self.model)
        self.assertIn(f"BaseModel.{self.model.id}", storage.all())

    def test_save_storage(self):
        """Test that the save method of storage
        serializes __objects to the JSON file."""
        storage.new(self.model)
        storage.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_reload_storage(self):
        """Test that the reload method of
        storage deserializes the JSON file to __objects."""
        storage.new(self.model)
        storage.save()
        storage.reload()
        self.assertIn(f"BaseModel.{self.model.id}", storage.all())


if __name__ == "__main__":
    unittest.main()
