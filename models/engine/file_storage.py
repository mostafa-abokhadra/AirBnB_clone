#!/usr/bin/python3
"""FileStorage class module"""

import os.path
import json
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """storing and retrieving objects
    """
    __file_path = "file.json"
    __objects = {}

    def __init__(self):
        """initializing instance
        """
        pass

    def all(self, cls=None):
        """returns the dictionary __objects
        """
        if cls is not None:
            new_di = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_di[key] = value
                return new_di
        return self.__objects

    def new(self, obj):
        """ sets in __objects the obj with key <obj class name>.id
        """
        key = obj.__class__.__name__ + ".{}".format(obj.id)
        FileStorage.__objects[key] = obj

    @staticmethod
    def to_json_string(objects):
        final_dec = {}
        for key in objects.keys():
            val = objects[key].to_dict()
            final_dec[key] = val
        return final_dec

    def save(self):
        """ serializes __objects to the JSON file (path: __file_path)
        """
        jsn_format = FileStorage.to_json_string(FileStorage.__objects)
        with open(FileStorage.__file_path, mode="w", encoding="utf-8") as fily:
            fily.write(json.dumps(jsn_format))

    @staticmethod
    def from_json_string(string):
        if string:
            return json.loads(string)
        else:
            return {}

    def reload(self):
        """ deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists
        """
        if os.path.exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r") as fily:
                var = fily.read()
            if var is None or var == "":
                return

            objects = FileStorage.from_json_string(var)
            for key, value in objects.items():
                FileStorage.__objects[key] = classes[objects[key]["__class__"]](
                    **objects[key])

        else:
            return
