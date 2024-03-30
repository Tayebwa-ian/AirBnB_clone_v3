#!/usr/bin/python3
"""create a unique FileStorage instance for the application"""
from .engine import file_storage, db_storage
from .base_model import BaseModel
from .amenity import Amenity
from .city import City
from .place import Place
from .review import Review
from .state import State
from .user import User
from os import getenv


# load from database or from storage file
storage_type = getenv("HBNB_TYPE_STORAGE")
if storage_type == "db":
    storage = db_storage.DBStorage()
    storage.reload()
else:
    storage = file_storage.FileStorage()
    storage.reload()
