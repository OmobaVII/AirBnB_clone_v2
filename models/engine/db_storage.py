#!/usr/bin/pyhon3
"""This is the module for the dbstorage"""
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine, MetaData
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """Manages database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """initializes the class"""
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".\
                                       format(user, passwd, host, db),
                                       pool_pre_ping=True)
        if getenv("HBNB_ENVN") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current db session"""
        classes = {"User": User, "BaseModel": BaseModel,
                   "Place": Place, "State": State, "City": City,
                   "Amenity": Amenity, "Review": Review}
        db_dictionary = {}
        if cls == "" or cls == None:
            for k, v in classes.items():
                if k != "BaseModel":
                    objects = self.__session.query(v).all()
                    if len(objects) > 0:
                        for obj in objects:
                            key = f"{obj.__class__.__name__}.{obj.id}"
                            db_dictionary[key] = obj
                    if hasattr(db_dictionary, "_sa_instance_state"):
                        del db_dictionary["_sa_instance_state"]
            return db_dictionary
        else:
            objects = self.__session.query(classes[cls]).all()
            for obj in objects:
                key = f"{obj.__class__.__name__}.{obj.id}"
                db_dictionary[key] = obj
            if hasattr(db_dictionary, "_sa_instance_state"):
                del db_dictionary["_sa_instance_state"]
            return db_dictionary

    def new(self, obj):
        """add the object to the current db session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current db session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes from the current db session obj"""
        if obj != None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the db"""
        self.__session = Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()

    def close(self):
        """closes the session"""
        self.__session.close()

