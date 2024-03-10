#!/usr/bin/python3

"""here goes evey thing"""

import os
import cmd
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """here commands"""
    prompt = "(hbnb) "
    classes = [BaseModel, User, State, City, Amenity, Place, Review]

    def do_EOF(self, line):
        """Exit on Ctrl-D (EOF)."""
        print()
        return True

    def do_quit(self, line):
        """Exit on quit."""
        return True

    def emptyline(self):
        """Do nothing on empty line."""
        pass

    def do_create(self, line):
        """Creates a new instance of BaseModel"""

        if not line:
            print("** class name missing **")

        elif line not in [cls.__name__ for cls in HBNBCommand.classes]:
            print("** class doesn't exist **")

        else:
            new_instance = None
            for cls in HBNBCommand.classes:
                if line == cls.__name__:
                    new_instance = cls()
                    new_instance.save()
                    print(new_instance.id)

    def do_show(self, line):
        """
            Prints the string representation of an instance
            based on the class name
        """
        args = line.split()
        if not args:
            print("** class name missing **")

        elif args[0] not in [cls.__name__ for cls in HBNBCommand.classes]:
            print("** class doesn't exist **")

        elif len(args) < 2:
            print("** instance id missing **")
            return

        else:
            name = f"{args[0]}.{args[1]}"
            if name not in models.storage.all().keys():
                print("** no instance found **")
                return
            print(models.storage.all()[name])

    def do_destroy(self, line):
        """
            Deletes an instance based on the class name and id
        """
        args = line.split()
        if not args:
            print("** class name missing **")

        elif args[0] not in [cls.__name__ for cls in HBNBCommand.classes]:
            print("** class doesn't exist **")

        elif len(args) < 2:
            print("** instance id missing **")

        else:
            name = f"{args[0]}.{args[1]}"
            if name not in models.storage.all().keys():
                print("** no instance found **")
                return

            del models.storage.all()[name]
            models.storage.save()

    def do_all(self, line):
        """
            Prints all string representation of all instances
            based or not on the class name
        """
        obj_list = []
        if not line:
            for obj in models.storage.all().values():
                obj_list.append(str(obj))
            print(obj_list)
            return

        args = line.split()
        if args[0] not in [cls.__name__ for cls in HBNBCommand.classes]:
            print("** class doesn't exist **")

        else:
            for key, objs in models.storage.all().items():
                if key.startswith(args[0]):
                    obj_list.append(str(objs))
            print(obj_list)

    def do_update(self, line):
        """
            Updates an instance based on the class name and id
            by adding or updating attribute
        """
        args = line.split()
        if not args:
            print("** class name missing **")

        elif args[0] not in [cls.__name__ for cls in HBNBCommand.classes]:
            print("** class doesn't exist **")
            return

        elif len(args) < 2:
            print("** instance id missing **")
            return

        elif len(args) < 3:
            print("** attribute name missing **")
            return
        elif len(args) < 4:
            print("** value missing ** ")
            return

        name = f"{args[0]}.{args[1]}"
        if name not in models.storage.all().keys():
            print("** no instance found **")
            return

        attr_val = args[3]
        type_val = type(eval(attr_val))
        attr_val = attr_val.strip('"')
        setattr(models.storage.all()[name], args[2], type_val(attr_val))
        models.storage.save()

    def default(self, line):
        """Handle custom command format.

            <command> <class_name> or <class_name>.<command>()

        Args:
            line: inputed line
        """
        if "." in line:
            args = line.split(".")
            commands = ["all", "count", "show", "destroy", "update"]
            if len(args) == 2:
                cls = args[0]
                command = args[1].split("(")[0]
                if eval(cls) in HBNBCommand.classes and command in commands:
                    if command == 'all':
                        self.do_all(cls)
                    elif command == 'count':
                        self.do_count(cls)
                    elif command == 'show':
                        id = args[1].split('"')[1]
                        self.do_show(f"{cls} {id}")
                    elif command == 'destroy':
                        id = args[1].split('"')[1]
                        self.do_destroy(f"{cls} {id}")
                    elif command == 'update':
                        id = args[1].split('"')[1]
                        if args[1].split('"')[2].startswith(", {"):
                            in_dict = args[1].split('{')[1].split('}')[0]
                            in_dict = "{" + in_dict + "}"
                            in_dict = eval(in_dict)
                            for key, value in in_dict.items():
                                self.do_update(f"{cls} {id} '{key}' '{value}'")
                        else:
                            key = args[1].split('"')[3]
                            value = "\"" + args[1].split('"')[5] + "\""
                            self.do_update(f"{cls} {id} {key} {value}")
        else:
            return cmd.Cmd.default(self, line)

    def do_count(self, line):
        """Display count of instances specified"""
        if eval(line) in HBNBCommand.classes:
            count = 0
            for key, value in models.storage.all().items():
                if line in key:
                    count += 1
            print(count)
        else:
            print("** class doesn't exist **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
