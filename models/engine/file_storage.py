#!/usr/bin/python3
'''
    This module defines a class to manage file storage
    For hbnb clone
'''
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    '''
        This class manages storage of hbnb models in JSON format
    '''
    __file_path = 'file.json'
    __objects = {}
    classes = {"BaseModel": BaseModel, "User": User, "State": State,
               "City": City, "Amenity": Amenity, "Place": Place,
               "Review": Review}

    def all(self, cls=None):
        '''
            Returns a dictionary of models currently in storage
        '''
        fil_dict = {}
        if cls is None:
            return FileStorage.__objects

        if cls != "":
            for k, v in FileStorage.__objects.items():
                if isinstance(v, cls):
                    fil_dict[k] = v
            return fil_dict

        else:
            return FileStorage.__objects

    def new(self, obj):
        '''
            Adds new object to storage dictionary
        '''
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        '''
        Saves storage dictionary to file
        '''
        temp = {}
        for key, val in self.__objects.items():
            temp[key] = val.to_dict()
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(temp, f)

    def reload(self):
        '''
        Loads storage dictionary from file
        '''
        try:
            with open(self.__file_path, "r") as myFile:
                objects = json.load(myFile)
                for key, value in objects.items():
                    class_name = value.get("__class__")
                    if class_name in self.classes:
                        class_obj = self.classes[class_name]
                        obj = class_obj(**value)
                        self.__objects[key] = obj
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        '''
        Deletes obj from __objects if present
        '''
        try:
            k = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[k]
        except Exception as e:
            pass
