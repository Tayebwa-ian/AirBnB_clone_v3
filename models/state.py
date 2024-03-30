#!/usr/bin/python3
"""State Model-Module(Inherits from the BaseModel)"""
from .base_model import BaseModel, Base
from .city import City
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
from os import getenv
import models


class State(BaseModel, Base):
    """Holds state attributes and Functions
    Attrs:
        name: State's name
    """
    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete-orphan")
    else:
        name = ""
        cities = []

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self) -> list:
            """Get a list of all cities
            with state_id equals to the current State.id
            """
            result = []
            for city in list(models.storage.all(City).values()):
                if city.state_id == self.id:
                    result.append(city)
            return(result)
