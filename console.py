#!/usr/bin/python3
"""
Personal Property Management System - Command Interpreter
A customized command-line interface for managing properties and users
"""

import cmd
import datetime
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.place import Place
from models.state import State


class PersonalCLI(cmd.Cmd):
    """Command line interface for personal property management"""

    prompt = "[mycli] "

    classes = [
        'BaseModel',
        'User',
        'Amenity',
        'City',
        'Review',
        'Place',
        'State',
    ]

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_exit(self, arg):
        """Exit command to leave the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def do_create(self, arg):
        """Creates a new instance of the specified class
        Usage: create <ClassName>"""
        if not arg:
            print("** class name missing **")
            return

        if arg not in self.classes:
            print("** class doesn't exist **")
            return

        try:
            new_instance = eval(arg)()
            new_instance.save()
            print(new_instance.id)
        except Exception as e:
            print(f"Error creating {arg}: {str(e)}")

    def do_show(self, arg):
        """Prints the string representation of an instance
        Usage: show <ClassName> <id>"""
        args = arg.split()

        if not args:
            print("** class name missing **")
            return

        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return

        print(storage.all()[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id
        Usage: destroy <ClassName> <id>"""
        args = arg.split()

        if not args:
            print("** class name missing **")
            return

        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return

        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """Prints string representation of all instances
        Usage: all [ClassName]"""
        if arg and arg not in self.classes:
            print("** class doesn't exist **")
            return

        objects = storage.all()
        if arg:
            objects = {k: v for k, v in objects.items() if k.startswith(arg)}

        print([str(obj) for obj in objects.values()])

    def do_update(self, arg):
        """Updates an instance by adding or updating attribute
        Usage: update <ClassName> <id> <attribute_name> <attribute_value>"""
        args = arg.split()

        if not args:
            print("** class name missing **")
            return

        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return

        obj = storage.all()[key]
        attr_name = args[2]
        attr_value = args[3].strip('"')

        if hasattr(obj, attr_name):
            attr_type = type(getattr(obj, attr_name))
            try:
                setattr(obj, attr_name, attr_type(attr_value))
            except (ValueError, TypeError):
                setattr(obj, attr_name, attr_value)
        else:
            setattr(obj, attr_name, attr_value)

        obj.save()

    def do_count(self, arg):
        """Count instances of a class
        Usage: count <ClassName>"""
        if not arg:
            print("** class name missing **")
            return

        if arg not in self.classes:
            print("** class doesn't exist **")
            return

        objects = storage.all()
        count = len([k for k in objects.keys() if k.startswith(arg)])
        print(count)

    def do_status(self, arg):
        """Show current storage status"""
        objects = storage.all()
        print(f"Total objects in storage: {len(objects)}")

        class_counts = {}
        for key in objects.keys():
            class_name = key.split('.')[0]
            class_counts[class_name] = class_counts.get(class_name, 0) + 1

        for class_name in sorted(class_counts.keys()):
            print(f"{class_name}: {class_counts[class_name]}")

    def do_clear_all(self, arg):
        """WARNING: Delete all instances of a class
        Usage: clear_all <ClassName>"""
        if not arg:
            print("** class name missing **")
            return

        if arg not in self.classes:
            print("** class doesn't exist **")
            return

        objects = storage.all().copy()
        deleted_count = 0

        for key in objects.keys():
            if key.startswith(arg):
                del storage.all()[key]
                deleted_count += 1

        if deleted_count > 0:
            storage.save()
            print(f"Deleted {deleted_count} {arg} instances")
        else:
            print(f"No {arg} instances found")

    def do_backup(self, arg):
        """Create a backup of current storage"""
        import shutil
        import os

        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"file_backup_{timestamp}.json"

            if os.path.exists("file.json"):
                shutil.copy("file.json", backup_name)
                print(f"Backup created: {backup_name}")
            else:
                print("No storage file found to backup")
        except Exception as e:
            print(f"Backup failed: {str(e)}")


if __name__ == '__main__':
    PersonalCLI().cmdloop()
