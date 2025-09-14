#!/usr/bin/python3
"""This module contains the BaseModel class"""

import uuid
from datetime import datetime


class BaseModel:
    def __init__(self, *args, **kwargs):
        """Initialization of the BaseModel class"""
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        from models import storage
        storage.new(self)

    def __str__(self):
        """String representation of the BaseModel class"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Update the updated_at
        attribute with the current datetime and save to storage
        """
        self.updated_at = datetime.now()
        from models import storage
        # print(storage.all())
        storage.save()

    def to_dict(self):
        """Returns the dict representation of BaseModel class"""
        dict_copy = self.__dict__.copy()
        dict_copy["created_at"] = self.created_at.isoformat()
        dict_copy["updated_at"] = self.updated_at.isoformat()
        dict_copy["__class__"] = self.__class__.__name__
        return dict_copy
