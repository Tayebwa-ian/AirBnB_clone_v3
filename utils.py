#!/usr/bin/python3
"""The utility Module
Description:
    Implement utility functions that will be used across other modules
"""


def dict_from_cmd_args(value) -> dict:
    """Generate a dictionary of values to be used as function parameters
    Arg:
        value: A string of command line arguments
    """
    result = {}
    value_list = value.split(" ")[1:]
    for val in value_list:
        temp = val.split("=")
        if "_" in temp[1]:
            temp[1].replace("_", " ")
        result[temp[0]] = temp[1].replace('"', '')
    return(result)
