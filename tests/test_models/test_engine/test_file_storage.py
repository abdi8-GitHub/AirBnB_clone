#!/usr/bin/python3
'''
unittest module for module 'file_storage'
module name: 'test_file_storage'
'''

import os
import unittest
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestAll(unittest.TestCase):
    '''class TestAll to test the 'all' method'''

    def test_all_return_type(self):
        """Test all return types"""

        fs = FileStorage()
        all_objs = fs.all()
        self.assertIsInstance(all_objs, dict)


class TestNew(unittest.TestCase):
    '''class TestNew to test the 'new' method'''

    def test_new_adds_object(self):
        """Test new added objs"""

        fs = FileStorage()
        obj = User()
        fs.new(obj)
        key = f'{obj.__class__.__name__}.{obj.id}'
        self.assertIn(key, fs.all())

    def test_new_skips_none(self):
        """Test new skips"""

        fs = FileStorage()
        before = fs.all()
        fs.new(None)
        after = fs.all()
        self.assertEqual(before, after)


class TestSave(unittest.TestCase):
    '''class TestSave to test the 'save' method'''

    '''def test_save_creates_file(self):
        fs = FileStorage()
        fs.save()
        with open(fs._FileStorage__file_path, 'r') as f:
            self.assertEqual(f.read(), '{}')'''

    def test_save_updates_file(self):
        """Test updated files"""

        fs = FileStorage()
        obj = State()
        fs.new(obj)
        fs.save()
        with open(fs._FileStorage__file_path, 'r') as f:
            self.assertIn(obj.id, f.read())


class TestReload(unittest.TestCase):
    '''class TestReload to test the 'reload' method'''

    def test_reload_from_existing_file(self):
        """Test reload from a file"""

        fs = FileStorage()
        obj = User()
        fs.new(obj)
        fs.save()
        fs.reload()
        key = f'{obj.__class__.__name__}.{obj.id}'
        self.assertIn(key, fs.all())

    def test_reload_without_file(self):
        """Test reload without files"""

        fs = FileStorage()
        os.remove(fs._FileStorage__file_path)
        try:
            fs.reload()
        except FileNotFoundError:
            s = "reload method raised FileNotFoundError unexpectedly"
            self.fail(s)

    def test_reload_with_invalid_data(self):
        """Test reload with invalid data"""

        fs = FileStorage()
        with open(fs._FileStorage__file_path, 'w') as f:
            f.write(
                    '{"invalid_key": {"__class__": "InvalidClass",'
                    '"id": "123"}}'
                    )
        try:
            fs.reload()
        except NameError:
            self.fail("reload unexpectedly raised NameError!")

    def test_reload_with_invalid_class(self):
        """Test reload with invalid class"""

        fs = FileStorage()
        with open(fs._FileStorage__file_path, 'w') as f:
            f.write(
                    '{"invalid_key": {"__class__": "InvalidClass",'
                    '"id": "123"}}'
                    )
        try:
            fs.reload()
        except NameError:
            self.fail("reload method raised NameError unexpectedly")

    def test_reload_with_invalid_id(self):
        """Test reload with invalid id"""

        fs = FileStorage()
        with open(fs._FileStorage__file_path, 'w') as f:
            f.write(
                    '{"User.invalid_id": {"__class__": "User", '
                    '"invalid_key": "invalid_value"}}'
                    )
        try:
            fs.reload()
        except ValueError:
            self.fail("reload method raised ValueError unexpectedly")

    def test_reload_with_missing_attribute(self):
        """Test reload without attributes"""

        fs = FileStorage()
        with open(fs._FileStorage__file_path, 'w') as f:
            f.write(
                    '{"User.missing_attribute": {"__class__": "User",'
                    '"id": "123"}}'
                    )
        try:
            fs.reload()
        except TypeError:
            self.fail("reload method raised TypeError unexpectedly")

    def test_reload_with_valid_data(self):
        """Test reload with valid data"""

        fs = FileStorage()
        obj = User()
        fs.new(obj)
        fs.save()
        fs.reload()
        key = f'{obj.__class__.__name__}.{obj.id}'
        self.assertIn(key, fs.all())


if __name__ == '__main__':
    unittest.main()
