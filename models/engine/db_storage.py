#!/usr/bin/python3
"""This is the module for the dbstorage"""
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.base_model import BaseModel, Base
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
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(user, passwd, host, db),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current db session"""
        classes = {"User": User, "BaseModel": BaseModel,
                   "Place": Place, "State": State, "City": City,
                   "Amenity": Amenity, "Review": Review}
        db_dictionary = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    db_dictionary[key] = obj
                return db_dictionary
            else:
                for k, v in classes.items():
                    if k != "BaseModel":
                        objs = self.__session.query(v).all()
                        if len(objs) > 0:
                            for obj in objs:
                                key = "{}.{}".format(obj.__class__.__name__,
                                                     obj.id)
                                db_dictionary[key] = obj
            return db_dictionary

    def new(self, obj):
        """add the object to the current db session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current db session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes from the current db session obj"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the db"""
        from models.user import User
        from models.city import City
        from models.state import State
        from models.place import Place
        from models.review import Review
        from models.amenity import Amenity
        self.__session = Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()

    def close(self):
        """closes the session"""
        self.__session.close()
