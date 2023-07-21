#!/usr/bin/python3
'''
    This module defines a class to manage file storage
    For hbnb clone
'''
import json
import models
from models.state import State


class FileStorage:
    '''
        This class manages storage of hbnb models in JSON format
    '''
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        '''
            Returns a dictionary of models currently in storage
        '''
        fil_dict = {}
        if cls is None:
            return self.__objects

        if cls != "":
            for key, val in self.__objects.items():
                if type(val) == cls:
                    fil_dict[key] = val
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
        for key, val in self.__objects.items():
            temp[key] = val.to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(temp, f)

    def reload(self):
        '''
        Loads storage dictionary from file
        '''
        try:
            with open(self.__file_path, 'r') as myFile:
                FileStorage.__objects = json.load(myFile)
            for key, val in FileStorage.__objects.items():
                class_name = val["__class__"]
                class_name = models.classes[class_name]
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
            self.save()
        except Exception as e:
            pass

    def close(self):
        """for deserializing the json file to objects"""
        self.reload()
