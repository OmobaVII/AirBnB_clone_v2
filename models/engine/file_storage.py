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
import models

classes = {"BaseModel": BaseModel, "User": User, "State": State,
           "City": City, "Amenity": Amenity, "Place": Place,
           "Review": Review}


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
            return self.__objects

        if cls != "":
            for k, v in self.__objects.items():
                if cls == k.split(".")[0]:
                    fil_dict[k] = v
            return fil_dict
        else:
            return self.__objects

    def new(self, obj):
        '''
            Adds new object to storage dictionary
        '''
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        '''
        Saves storage dictionary to file
        '''
        temp = {}
        for key in self.__objects:
            temp[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(temp, f)

    def reload(self):
        '''
        Loads storage dictionary from file
        '''
        try:
            with open(self.__file_path, 'r') as myFile:
                items = json.load(myFile)
            for key in items:
                for key, val in FileStorage.__objects.items():
                    class_name = val["__class__"]
                    class_name = classes[class_name]
                    FileStorage.__objects[key] = class_name(**val)
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

    def close(self):
        """for deserializing the json file to objects"""
        self.reload()
