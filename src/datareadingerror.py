

"""
The module explainded:

datareadingerror.py includes class DataReadingError. 
Class ReadFile raises this type of error when it fails to read a file.
"""


class DataReadingError(Exception):

    def __init__(self, message):
        super(DataReadingError, self).__init__(message)
