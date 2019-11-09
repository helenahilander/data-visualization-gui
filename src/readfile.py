
"""

The module explainded:

This module readfile.py includes class Readile. 
ReadFile recieves a file and tries to create objects of the class Data from the received file.
If ReadFile fails at reading the file, DataReadingError is raised.


ReadFile only accepts file with following file format:



#data1_title
#x1_name ,y1_name
#x1_type ,y1_type
x0 , y0
xn , yn
#data2_title
#x2_name ,y2_name
#x2_type ,y2_type
x0 , y0
xn , yn




comments about the format: 
	- the number of spaces on a row does not matter
	 but NO spaces between datasets (no space between rows xn , yn)
	and #data2_title)
	- there can be any number of data pairs xn , yn and datasets
	-x_type is either int, float or string



"""




from data import Data
from datareadingerror import DataReadingError




class ReadFile():


	@staticmethod
	def create_data_objects(input_file):

		#initialize data list
		data_list = []

		try: #try reading line at a time from the file
			line = input_file.readline()

			#while we reach the end of file
			while line != "" :

				#if we have header line go here
				if line[0] == "#":
					#read data title 
					data_title = line[1:]
					data_title = data_title.strip()
					line = input_file.readline()

					#if we reach end of file, break
					if line == "":
						break 

					#if we have unvalid line after title, raise error
					if line[0] != "#":
						raise DataReadingError('the beginning of each data block must be written as follow: #data_title\n#x_name(,y_name)\n#x_type(,y_type)')


					try: #try splitting, go to except if next line after title does not have two parts i.e data is single type data
						line = line.split(",")

						#try getting the name of x and y data
						try:
							x_name, y_name = line[0][1:], line[1] 
							x_name, y_name = x_name.strip(), y_name.strip()

						#go here if there is unvalid line
						except IndexError:
							raise DataReadingError('the beginning of each data block must be written as follow: #data_title\n#x_name(,y_name)\n#x_type(,y_type)')
						
						#initialize x and y data
						x = []
						y = []

						line = input_file.readline()

						#break if we reach end of file
						if line == "":
							break

						#raise errof if there is no data type -line
						if line[0] != "#":
							raise DataReadingError('the beginning of each data block must be written as follow: #data_title\n#x_name(,y_name)\n#x_type(,y_type)')

						try:
							line = line.split(",")
							x_type, y_type = line[0][1:].strip().lower(), line[1].strip().lower()

						except ValueError:
							DataReadingError('the beginning of each data block must be written as follow: #data_title\n#x_name(,y_name)\n#x_type(,y_type)')



					#go here if we have single data
					except ValueError: 

						#read name and initialize x data
						x_name = line[1:]
						x = []
						y = None
						line = input_file.readline()

						#break if we reach end of file
						if line == "":
							break
						#raise errof if there is no data type -line
						if line[0] != "#":
							raise DataReadingError('the beginning of each data block must be written as follow: #data_title\n#x_name(,y_name)\n#x_type(,y_type)')
						
						#get the type of x data
						x_type = line.strip().lower()
						y_type = None


					#read next line for both single and double data
					line = input_file.readline()
					if line == "":
						break

					#while we reach the title of next data set
					while line[0] != "#":

						#go here if we have double data
						if y_type != None:

							#save x and y values
							line = line.split(",")
							x.append(line[0].strip())
							y.append(line[1].strip())

						#go here with single data
						else:
							line = line.strip()
							x.append(line)

						#if we reach end of file, break
						line = input_file.readline()
						if line == "":
							break


					decimals = None #initializing the decimals. if data is float type, this will change later in the code otherwise it will remain None.



					"""Following if-else structure is for finding out the data type.
					if both x and y are numerical (float or int), data_type is "doublenum".
					if one of x or y is numerical (float or int) and other categorical (string), data_type is "doublestring"
					if y value is none data_type is either singlenum (if x_type is int or float ) or singlestring  (if x_type is string)
					"""

					if x_type == "string":

						if y_type == "int":
							#make y values' type int
							y = ReadFile.make_int(y)
							data_type = "doublestring"

						elif y_type == "float":
							#make y values' type float
							y, decimals = 	ReadFile.make_float(y)
							data_type = "doublestring"

						elif y_type == None:
							data_type = "singlestring"


					elif x_type == "int":
	
						x = ReadFile.make_int(x)

						if y_type == "int":
							y = ReadFile.make_int(y)
							data_type = "doublenum"

						elif y_type == "float":
							y, decimals = 	ReadFile.make_float(y)
							data_type = "doublenum"
							
						elif y_type == "string":
							data_type = "doublestring"

						elif y_type == None:
							data_type = "singlenum"



					elif x_type == "float":

						x, decimals = 	ReadFile.make_float(x)

						if y_type == "int":
							y = Readfile.make_int(y)
							data_type = "doublenum"

						elif y_type == "float":
							y, decimals = ReadFile.make_float(y)
							data_type = "doublenum"

						elif y_type == "string":
							data_type = "doublestring"

						elif y_type == None:
							data_type = "singlenum"

					#go here if we have unvalid data type written in the file
					else:
						raise DataReadingError("Unknown data type in file. Not string, int or float.")

					#create Data-object for the dataset and add it to the data_list
					data_object = Data(data_title, x_name, y_name, x,y, data_type, decimals)
					data_list.append(data_object)


				#go here until we find line with next #
				else: 
					 line = input_file.readline()

			#raise error if there was no data in the file
			if data_list == []:
				raise DataReadingError("No valid data in the file")


			return data_list

		#raise error if opening the file fails
		except OSError:
			print("Could not open {}".format(path), file=sys.stderr)






	@staticmethod
	def make_float(x):

		try: #try making the type of values in x or y float
		#the variable in here is x but we use this same code for converting y data as well.
			number_of_decimals = 0

			for i in range(len(x)):
				if x[i].lower() == "nan": #this assumes that if there is y data. it has nan in the same place.
					pass
				
				else: #replace 5,6 with 5.6 
					if "," in x[i]:
						x[i] = x[i].replace(",", ".")

					#calculate number of decimals and compare it to the current max value of decimals
					decimals = len(x[i].split(".")[1])
					if decimals > number_of_decimals:
						number_of_decimals = decimals

					x[i] = float(x[i])

			return x, number_of_decimals

		except ValueError: 
			raise DataReadingError("Error in converting data to numerical that is reported to be float")







	@staticmethod
	def make_int(x):

		try: #try making values in x int except if value cannot be made float
		#the variable in here is x but we use this same code for converting y data as well.
			for i in range(len(x)):

				if x[i].lower() == "nan":
					pass
				
				else:
					x[i] = int(x[i])

			return x


		except ValueError: 
			raise DataReadingError("Error in converting data to numerical that is reported to be float")      

