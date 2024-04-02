#!/usr/bin/python3
"""
File storage Module
Serialization and Deserialization of JSON data to and from a file
"""
import json
from ..amenity import Amenity
from ..city import City
from ..place import Place
from ..review import Review
from ..state import State
from ..user import User
from ..base_model import BaseModel
from os import getenv


class FileStorage:
    """
    Description:
        serializes instances to a JSON file
        And deserializes JSON file to instances
    Attrs:
        __file_path: string - path to storage file (get from env)
        __objects: dictionary - empty but will store all objects
                    by <class name>.id
    """
    if getenv("HBNB_TYPE_STORAGE"):
        __file_path = getenv("HBNB_TYPE_STORAGE")
    else:
        __file_path = "file.json"
    __objects = {}
    all_classes = {
        "User": User,
        "State": State,
        "Review": Review,
        "Place": Place,
        "City": City,
        "Amenity": Amenity,
        "BaseModel": BaseModel,
        }

    def all(self, cls=None) -> dict:
        """return a dictionary object of __objects
        Arg:
            cls: specific class, which objects should be returned
        Return: Dict of objects
        """
        objects = {}
        if cls:
            # get objects related to a specific class
            for key in self.__objects.keys():
                if key.split(".")[0] == cls.__name__:
                    objects[key] = cls(**self.__objects[key])
            return objects
        for key in self.__objects.keys():
            c = key.split(".")[0]
            if c in self.all_classes.keys():
                objects[key] = self.all_classes[c](**self.__objects[key])
        return objects

    def new(self, obj) -> None:
        """sets in __objects the obj with key <obj class name>.id
        Agrs:
            obj: the object of a class passed
        Return: None
        """
        key = obj.__class__.__name__ + ".{}".format(obj.id)
        self.__objects[key] = obj.to_dict()

    def save(self) -> None:
        """ serializes __objects to the JSON file"""
        with open(self.__file_path, "w") as file:
            json.dump(self.__objects, file, indent="\t")

    def reload(self) -> None:
        """
        Description:
            Deserializes the JSON file to __objects
            only if the JSON file (__file_path) exists ; otherwise, do nothing.
            If the file does not exist, no exception should be raised)
        """
        try:
            with open(self.__file_path, "r") as file:
                self.__objects = json.load(file)
        except FileNotFoundError:
            pass

    def delete(self, obj=None) -> None:
        """Delete obj from __objects if it’s inside
        Arg:
            obj: Object to be deleted
        Return: None
        """
        if obj:
            key = type(obj).__name__ + "." + obj.id
            if self.__objects.get(key):
                self.__objects.pop(key)
            self.save()

    def close(self) -> None:
        """
        Description:
            call reload() method for deserializing the JSON file to objects
        Return: None
        """
        self.reload()

    def get(self, cls, id) -> dict:
        """retrieve one object based on cls and id
        Args:
            cls: class of the object
            id: Id of the object
        Return: object based on the class and its ID, or None
        """
        for key in self.__objects.keys():
            values = key.split(".")
            if values[0] == cls.__name__ and values[1] == id:
                return(cls(**self.__objects[key]))

    def count(self, cls=None) -> int:
        """count the number of objects in storage:
        Args:
            cls: class of the objects
        Return: number of objects in storage matching the given class
                if no class is passed,
                returns the count of all objects in storage.
        """
        if cls:
            return(len(self.all(cls)))
        return(len(self.all()))
