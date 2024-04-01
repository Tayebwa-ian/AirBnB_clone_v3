#!/usr/bin/python3
"""Base Model - Module
Description:
    It holds common (a union of) characteristics for other models
    Its herited by other model classes in this project
"""
import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, DateTime
from os import getenv

if getenv("HBNB_TYPE_STORAGE") == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """Holds common model attrs and functions for this project
    Attrs:
        id: ID of the row in the database
        created_at: the time the row was created
        updated_at: When the row was last edited
    """
    if getenv("HBNB_TYPE_STORAGE") == "db":
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime(), default=datetime.now(), nullable=False)
        updated_at = Column(DateTime(), default=datetime.now(), nullable=False)
    else:
        id = ""
        created_at = ""
        updated_at = ""

    def __init__(self, *args, **kwargs) -> None:
        """Intializes the class
        Args:
            args: unused arguments
            kwargs: a dictionary of elements used to create
                    object attributes names (only if kwargs is not empty)
        Return: None
        """
        if kwargs:
            int_attrs = [
                "number_rooms",
                "number_bathrooms",
                "max_guest",
                "price_by_night"
            ]
            float_attrs = [
                "longitude",
                "latitude"
            ]
            obj_id = getattr(kwargs, "id", None)
            if obj_id is None:
                self.id = str(uuid4())
                self.created_at = datetime.now()
                self.updated_at = datetime.now()
            for key in kwargs.keys():
                if key != "__class__":
                    if key == "created_at":
                        self.created_at = datetime\
                            .fromisoformat(kwargs[key])
                    elif key == "updated_at":
                        self.updated_at = datetime\
                            .fromisoformat(kwargs[key])
                    elif key == "id":
                        self.id = kwargs[key]
                    elif key in int_attrs:
                        setattr(self, key, int(kwargs[key]))
                    elif key in float_attrs:
                        setattr(self, key, float(kwargs[key]))
                    else:
                        setattr(self, key, kwargs[key])
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def save(self) -> None:
        """
        Description:
            Update the updated_at field with current date
            and save to JSON file
        """
        # If storage is database, Update the date if the object dict
        # has _sa_instance_state attribute
        if (getenv("HBNB_TYPE_STORAGE") != "db" or
           "_sa_instance_state" in self.__dict__.keys()):
            self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self) -> dict:
        """
        Description:
            Creates a dictionary containing all keys/values
            of __dict__ of the instance
            This is the first piece
            of the serialization/deserialization process
        Return: dictionary
        """
        dict_obj = {}
        # dict of obj attrs
        self_dict = self.__dict__
        for key in self_dict.keys():
            if key in ["created_at", "updated_at"]:
                dict_obj[key] = datetime.isoformat(self_dict[key])
            elif key == "_sa_instance_state":
                continue
            elif key == "password" and getenv('HBNB_TYPE_STORAGE') == 'db':
                continue
            else:
                dict_obj[key] = self_dict[key]
        # add key __class__ with the class name of the object
        dict_obj["__class__"] = self.__class__.__name__
        return(dict_obj)

    def delete(self) -> None:
        """delete the current instance from the storage"""
        models.storage.delete(self)

    def __str__(self) -> str:
        """Return string representation of the object"""
        self_dict = self.__dict__
        if "_sa_instance_state" in self_dict:
            del self_dict['_sa_instance_state']
        rep = f"[{self.__class__.__name__}] ({self.id}) {self_dict}"
        return(rep)
