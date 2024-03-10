#!/usr/bin/python3
"""base class module"""

import uuid
from datetime import datetime
import models


class BaseModel:
    """base model class
    """

    def __init__(self, *args, **kwargs):
        """initializing some instances attributes
        """
        if kwargs:
            for key in kwargs.keys():
                if not key == "__class__":
                    if key == "created_at" or key == "updated_at":
                        val = self.convert_to_datetime_object(kwargs[key])
                        setattr(self, key, val)
                    else:
                        setattr(self, key, kwargs[key])
        else:
            self.id = uuid.uuid4()
            self.id = str(self.id)
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    @classmethod
    def convert_to_datetime_object(self, value):
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")

    def __str__(self):
        """string representation of an object
        """
        return "[{}] ({}) {}".format(
                self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """updates the public instance attribute \
                updated_at with the current datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all \
                keys/values of __dict__ of the instance
        """
        my_dic = {}
        my_dic["__class__"] = self.__class__.__name__
        for key in self.__dict__.keys():
            if self.__dict__[key]:
                if key == "created_at" or key == "updated_at":
                    formating = self.__dict__[key].strftime(
                            "%Y-%m-%dT%H:%M:%S.%f")
                    my_dic[key] = formating
                else:
                    my_dic[key] = self.__dict__[key]
        return my_dic
