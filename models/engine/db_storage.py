#!/usr/bin/python3
"""
model to mange DB storage using sqlAlchemy
"""
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv
from datetime import datetime


if getenv("HBNB_TYPE_STORAGE") == "db":
    from models.place import place_amenity


class DBStorage:
    """
        This class manage DB storage for AirBnb
        Clone using sqlAlchemy
    """
    __engine = None
    __session = None
    all_classes = ["State", "City", "User", "Place", "Review"]

    def __init__(self):
        """
            Init __engine based on the Enviroment
        """
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        exec_db = 'mysql+mysqldb://{}:{}@{}/{}'.format(
                                            HBNB_MYSQL_USER,
                                            HBNB_MYSQL_PWD,
                                            HBNB_MYSQL_HOST,
                                            HBNB_MYSQL_DB
                                                )
        self.__engine = create_engine(exec_db, pool_pre_ping=True)
        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ query on the current database session (self.__session)
        all objects depending of the class name"""
        result = {}
        if cls:
            q = self.__session.query(cls).all()
            return(self.to_dict(q))
        else:
            for c in self.all_classes:
                c = eval(c)
                q = self.__session.query(c).all()
                result.update(self.to_dict(q))
            return(result)

    def new(self, obj):
        """
            Creating new instance in db storage
        """
        self.__session.add(obj)

    def save(self):
        """
            save to the db storage
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
            Delete obj from db storage
        """
        if obj is not None:
            self.__session.delete(obj)
        self.save()

    def reload(self):
        """
            create table in database
        """
        Base.metadata.create_all(self.__engine)
        session_db = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_db)
        self.__session = Session()

    def close(self) -> None:
        """
            Closing the session
        """
        self.reload()
        self.__session.close()

    @staticmethod
    def to_dict(query) -> dict:
        """method to turn a query object into a class
        Arg:
            query: The query object
        Return: A dictionary of query contents
        """
        final = {}
        for instance in query:
            instance_key = instance.__class__.__name__ + '.' + instance.id
            final[instance_key] = instance
        return(final)
