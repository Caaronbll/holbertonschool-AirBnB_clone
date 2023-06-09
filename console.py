#!/usr/bin/python3
"""Command line interface for AirBnB clone"""
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
import cmd


class_list = {'BaseModel': BaseModel,
              'Amenity': Amenity,
              'City': City,
              'Place': Place,
              'Review': Review,
              'State': State,
              'User': User}
error_messages = {'classMiss': '** class name missing **',
                  'classNotExist': "** class doesn't exist **",
                  'idMiss': "** instance id missing **",
                  'idNoInstance': "** no instance found **",
                  'attrNameMiss': '** attribute name missing **',
                  'attrValMiss': '** value missing **'}

class HBNBCommand(cmd.Cmd):
    """Command line interface for AirBnB clone"""
    prompt = '(hbnb) '

    def do_create(self, arg):
        """Creates a new BaseModel instance, saves it and prints the id
        ex: create BaseModel
        """
        if not arg:
            print(error_messages['classMiss'])
            return
        for key, value in class_list.items():
            if key == arg:
                new_obj = value()
                new_obj.save()
                print(new_obj.id)
                return
        print(error_messages['classNotExist'])

    def do_show(self, arg):
        """Show an instance ex: show <obj> <id>"""
        if not arg:
            print(error_messages['classMiss'])
            return
        args = self.split_arg(arg)
        name = args[0]
        objects = storage.all()

        if name not in class_list.keys():
            print(error_messages['classNotExist'])
            return

        if len(args) != 2:
            print(error_messages['idMiss'])
            return
        id = args[1]

        try: print(objects[f'{name}.{id}'])
        except: print(error_messages['idNoInstance']); return

    def do_destroy(self, arg):
        """Deletes an instance, and saves the change
        ex: destroy BaseModel 1234-1234
        """
        if not arg:
            print(error_messages['classMiss'])
            return
        args = self.split_arg(arg)
        name = args[0]
        objects = storage.all()

        if name not in class_list.keys():
            print(error_messages['classNotExist'])
            return

        if len(args) != 2:
            print(error_messages['idMiss'])
            return
        id = args[1]

        try: objects.pop(f'{name}.{id}')
        except: print(error_messages['idNoInstance']); return
        storage.save()

    def do_all(self, arg):
        """Prints all string representation based on class name"""
        all = storage.all()
        if arg:
            if arg not in class_list.keys():
                print(error_messages['classMiss'])
            for key, val in all.items():
                if isinstance(val, class_list[arg]):
                    print(val)
        else:
            for key, val in all.items():
                print(val)

    def do_update(self, arg):
        """Updates an instance based on the class name and id by adding or
        updating attribute
        ex: <class name> <id> <attribute name> "<attribute value>"
        """
        objects = storage.all()
        if not arg:
            print(error_messages['classMiss'])
            return
        args = self.split_arg(arg)
        name = args[0]

        try: id = args[1]
        except IndexError: print(error_messages['idMiss']); return

        try: update = objects[f'{name}.{id}']
        except KeyError: print(error_messages['idNoInstance']); return

        try: attr_name = args[2]
        except IndexError: print(error_messages['attrNameMiss']); return

        try: attr_val = args[3]
        except IndexError: print(error_messages['attrValMiss']); return

        update.__setattr__(attr_name, self.parse_attr_val(attr_val, arg))
        storage.save()

    def do_quit(self, arg):
        """Quit hbnb shell"""
        return True

    def do_EOF(self, arg):
        """Quit hbnb shell"""
        return True

    @staticmethod
    def split_arg(arg):
        """"method that splits args"""
        return arg.split(sep=' ')

    @staticmethod
    def parse_attr_val(val, arg):
        """Converts val to a int/float or if it detects not a number
        just return val
        """
        import re
        if val.startswith('"'):
            start = arg.find('"') + 1
            end = arg.find('"', start)
            val = arg[start:end]
        val = str(val)
        if val.isnumeric():
            try: return int(val)
            except ValueError: pass
        if val.replace('.', '').isnumeric():
            try: return float(val)
            except ValueError: pass
        else:
            return(val)

    def emptyline(self):
        """does nothing"""
        pass

if __name__ == '__main__':
    HBNBCommand().cmdloop()
