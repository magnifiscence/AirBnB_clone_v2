#!/usr/bin/python3
"""Database Storage"""
from sqlalchemy import create_engine
from models.base_model import BaseModel, Base
import os
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Instantiates a DBStorage object"""
        user = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, password, host, database),
                                      pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Queries the current database session based on class.
        Returns a dictionary representation of the query"""
        cls_dict = {
                    'State': State, 'City': City, 'User': User,
                    'Place': Place, 'Amenity': Amenity, 'Review': Review
                  }
        if cls is None:
            objs = []
            for k, v in cls_dict.items():
                objs += self.__session.query(v).all()
        else:
            objs = self.__session.query(cls).all()
        return {"{}.{}".format(type(obj).__name__,
                               obj.id): obj for obj in objs}

    def new(self, obj):
        """Adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """
        Creates all tables in the database and
        creates the current database session
        """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """Closes the current database session"""
        self.__session.close()
