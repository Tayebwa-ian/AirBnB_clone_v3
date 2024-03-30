#!/usr/bin/python3
"""The console Module
Description:
    This is provides shell like functionalities to run commands in this project
    More explicitly it provides a prompt to run basic commands
    commands that interact with the overall project
"""
import cmd
import re
from models import (storage, User, City,
                    Amenity, Place, BaseModel, State, Review)
from utils import dict_from_cmd_args


classes = {
    "User": User,
    "City": City,
    "Place": Place,
    "State": State,
    "BaseModel": BaseModel,
    "Review": Review,
    "Amenity": Amenity,
}


class HBNBCommand(cmd.Cmd):
    """Customised AirBnB console (command prompt)
    Description:
        Functions under this class run several commands input via the prompt
    """
    prompt = "(hbnb) "

    def do_quit(self, value) -> bool:
        """Exits the program"""
        return True

    def help_quit(self) -> None:
        """Text to display when help command is run with quit cmd"""
        print("Quit command to exit the program")

    def do_EOF(self, value) -> bool:
        """Exits the program"""
        return True

    def help_EOF(self) -> None:
        """Text to display when help command is run with EOF cmd"""
        print("EOF command to exit the program")

    def do_create(self, value) -> None:
        """Create an instance of the specified class saves it and print id
        Arg:
            value: the string containing the class and other needed value
        Return: None
        """
        if not value:
            print("** class name missing **")
        else:
            try:
                params = dict_from_cmd_args(value)
                if len(params) > 0:
                    cl = value.split(" ")[0]
                    obj = classes[cl](**params)
                else:
                    obj = classes[value]()
                obj.save()
                print(f"{obj.id}")
            except NameError:
                print("** class doesn't exist **")

    def help_create(self) -> None:
        """Text to display when help command is run with create cmd"""
        print("Create a new instance of a class "
              "\nUsage: create User (creates a new user instance)")

    def do_show(self, value) -> None:
        """
        Description:
            Prints the string representation of an instance
            based on the class name and id
        Arg:
            value: the string containing the class and other needed value
        Return: None
        """
        temp_obj = value.split()
        if len(temp_obj) < 1:
            print("** class name missing **")
        elif len(temp_obj) < 2:
            print("** instance id missing **")
        else:
            all_obj = storage.all()
            # join the class name and id with a dot in middle
            key = ".".join(temp_obj)
            if key in all_obj.keys():
                new_obj = all_obj[key].to_dict()
                print(new_obj)
            else:
                try:
                    classes[temp_obj[0]]
                    print("** no instance found **")
                except KeyError:
                    print("** class doesn't exist **")

    def help_show(self) -> None:
        """Text to display when help command is run with show cmd"""
        print("Prints a string representation of an instance "
              "\nUsage: show User user-id "
              "(prints a str rep of a user instance)")

    def do_destroy(self, value) -> None:
        """
        Description:
            Delete an instance based on the class name and id
        Arg:
            value: the string containing the class and other needed value
        Return: None
        """
        temp_obj = value.split()
        if len(temp_obj) < 1:
            print("** class name missing **")
        elif len(temp_obj) < 2:
            print("** instance id missing **")
        else:
            all_obj = storage.all()
            # join the class name and id with a dot in middle
            key = ".".join(temp_obj)
            if key in all_obj.keys():
                all_obj[key].delete()
            else:
                try:
                    classes[temp_obj[0]]
                    print("** no instance found **")
                except KeyError:
                    print("** class doesn't exist **")

    def help_destroy(self) -> None:
        """Text to display when help command is run with destroy cmd"""
        print("Delete an instance based on the class name and id "
              "\nUsage: delete User user-id "
              "(deletes user instance with id user-id)")

    def do_all(self, value) -> None:
        """
        Description:
            Prints all string representation of all instances
            based or not on the class name
        Arg:
            value: the string containing the class and other needed value
        Return: None
        """
        print_list = []
        if value:
            try:
                cls = classes[value]
                all_obj = storage.all(cls=cls)
                for key in all_obj.keys():
                    cl = key.split(".")
                    if cl[0] == value:
                        # create object from all_obj dict and store in list
                        li = all_obj[key].to_dict()
                        print_list.append(str(li))
            except KeyError:
                print("** class doesn't exist **")
        else:
            all_obj = storage.all()
            for key in all_obj.keys():
                cl = key.split(".")
                # create object from all_obj dict and store in list
                li = all_obj[key].to_dict()
                print_list.append(str(li))
        if len(print_list) > 0:
            print(print_list)

    def help_all(self) -> None:
        """Text to display when help command is run with all cmd"""
        print("Prints all string representation of all instances "
              "based or not on the class name \nUsage: all User "
              "(print all str rep of User objects)")

    def do_update(self, value) -> None:
        """
        Description:
            Updates an instance based on the class name
            and id by adding or updating attribute
        Arg:
            value: the string containing the class and other needed value
        Return: None
        """
        temp_obj = value.split()
        if len(temp_obj) < 1:
            print("** class name missing **")
        elif len(temp_obj) < 2:
            print("** instance id missing **")
        elif len(temp_obj) < 3:
            print("** attribute name missing **")
        elif len(temp_obj) < 4:
            print("** value missing **")
        else:
            all_obj = storage.all()
            # join the class name and id with a dot in middle
            key = ".".join(temp_obj[:2])
            if "{" and "}" in value:  # handles dictionary
                delimiters = r'[ {} :,\']'
                n_value = re.split(delimiters, value)
                new_value = [i for i in n_value if i != ""]
                if key in all_obj.keys():
                    temp_new = new_value[2:]
                    for i in range(len(temp_new) - 1):
                        if i % 2 == 0:
                            attr = temp_obj[2]
                            all_obj[key].__dict__[attr] = temp_new[i + 1]
                    for k in all_obj.keys():
                        all_obj[k].save()
                else:
                    try:
                        classes[temp_obj[0]]
                        print("** no instance found **")
                    except NameError:
                        print("** class doesn't exist **")
            else:
                if key in all_obj.keys():
                    attr = temp_obj[2]
                    all_obj[key].__dict__[attr] = temp_obj[3]
                    for k in all_obj.keys():
                        all_obj[k].save()
                else:
                    try:
                        classes[temp_obj[0]]
                        print("** no instance found **")
                    except NameError:
                        print("** class doesn't exist **")

    def help_update(self) -> None:
        """Text to display when help command is run with update cmd"""
        print("Updates an instance based on the class name "
              "and id by adding or updating attribute "
              "\nUsage: update User 1234-1234-1234 first_name IAN "
              "(updates User with ID 1234-1234-1234 with "
              "first_name attribute and value IAN)\n"
              "Usage: User.update(\"38f22813-2753-4d42-b37c-57a17f1e4f88\""
              ", \"first_name\", \"John\")")

    def do_count(self, value) -> None:
        """Retrieves and prints the number of instances of a class:
        Arg:
            Value: the class name
        Return: None
        """
        count = 0
        all_obj = storage.all()
        temp_obj = value.split()
        if len(temp_obj) < 1:
            print("** class name missing **")
        else:
            try:
                classes[value]
                for key in all_obj.keys():
                    cl = key.split(".")
                    if cl[0] == value:
                        count += 1
                print(count)
            except KeyError:
                print("** class doesn't exist **")

    def help_count(self) -> None:
        """Text to display when help command is run with count cmd"""
        print("Prints the number of all instances "
              "based on the class name \nUsage: count User\n"
              "Usage: User.count()\n"
              "(print number of User objects)")

    def precmd(self, line: str) -> str:
        """Handle and Parse commands that are in form (User.all())"""
        if line:
            if line[-1] == ")":
                # use regular expressions to remove split the command
                delimiters = r'[.()" :{}\']'
                split_result = re.split(delimiters, line)
                # create a line with only neccesary parts of the command
                fr = [i for i in split_result if i not in ["", ","]]
                if len(fr) == 2:
                    line = fr[1] + " " + fr[0]
                elif len(fr) == 3:
                    line = fr[1] + " " + fr[0] + " " + fr[2]
                elif len(fr) > 3:
                    # create a dictionary and parse it as the fourth arg
                    if "{" and "}" in line:
                        temp_dict = {}
                        new_fr = fr[3:]
                        for i in range(len(new_fr)):
                            if i != (len(new_fr) - 1) and i % 2 == 0:
                                temp_dict[new_fr[i]] = new_fr[i + 1]
                        line = fr[1] + " " + fr[0] + " "\
                            + fr[2] + " " + str(temp_dict)
                    else:
                        line = fr[1] + " " + fr[0] + " " + " ".join(fr[2:])
        return super().precmd(line)

    def emptyline(self) -> None:
        """Execute nothing on pressing an empty line + ENTER"""
        return


if __name__ == '__main__':
    HBNBCommand().cmdloop()
