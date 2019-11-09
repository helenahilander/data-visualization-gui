
"""
The module explainded:
	
	data.py includes the class Data that stores the information of the data of a selected file.




Data object has following attributes:

data_title = string, the title of the data, read from the data file.

x_name = string, name of the x data.

y_name = string, name of the y data (if the data is one dimensional, y_name = None)

x = list, one dimensional array of numerical or string values

y = list, one dimensional array of numerical or string values (if the data is one dimensional, y = None)

data_length = int, the length of the data array.

data_type = string, different data types are singlenum (1D numerical data), doublenum (2D data with both x and y being numerical), 
			doublestring (2D data with EITHER x OR y being string and other one being numerical), singlestring (1D data with string values).

number_of_decimals = int, the largest number of decimals in whole data. 
					Both x and y values are looked and the the largest number of decimals is saved to this variable.
					If data is non numerical, number_of_decimals = None
"""


class Data():



	def __init__(self,data_title, x_name, y_name, x,y, data_type, number_of_decimals ):

		self.data_title = data_title
		self.x_name = x_name
		self.y_name = y_name
		self.x = x
		self.y = y
		self.data_length = len(x)
		self.data_type = data_type
		self.number_of_decimals = number_of_decimals
