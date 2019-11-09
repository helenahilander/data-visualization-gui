
"""
The module explainded:
	
	readfiletest.py is a module for testing the ReadFile class unvalid file formats.

"""


import unittest
from io import StringIO 


from datareadingerror import DataReadingError
from readfile import ReadFile



class Test(unittest.TestCase):


	#testing with a header without #
	#testing that DataReadingError is raised with unvalid file
	def test_1(self):

		self.input_file = StringIO()
		self.input_file.write(' data1\n')
		self.input_file.write('x,y\n#float,float\n')
		self.input_file.write('-1.69,0.21\n-0.80,0.95\n-0.41,1.87\n-0.14,2.16\n-0.13,-0.97\n0.42,-0.30')
		self.input_file.write('-0.92,-0.61\n0.66,0.41\n')
		self.input_file.seek(0, 0) 

		data_list = None

		with self.assertRaises(DataReadingError):
			data_list = ReadFile.create_data_objects( self.input_file)

		self.input_file.close()



	#testing with unvalid #x_name,y_name row
	#testing that DataReadingError is raised with unvalid file
	def test_2(self):

		self.input_file = StringIO()
		self.input_file.write('#data1\n')
		self.input_file.write('x,y\n#float,float\n')
		self.input_file.write('-1.69,0.21\n-0.80,0.95\n-0.41,1.87\n-0.14,2.16\n-0.13,-0.97\n0.42,-0.30')
		self.input_file.write('-0.92,-0.61\n0.66,0.41\n')
		self.input_file.seek(0, 0) 


		data_list = None


		with self.assertRaises(DataReadingError):
			data_list = ReadFile.create_data_objects(self.input_file)

		self.input_file.close()

	#testing with unvalid #x_type, y_type row
	#testing that DataReadingError is raised with unvalid file
	def test_3(self):


		self.input_file = StringIO()
		self.input_file.write('#data1\n')
		self.input_file.write('#x,y\nfloat,float\n')
		self.input_file.write('-1.69,0.21\n-0.80,0.95\n-0.41,1.87\n-0.14,2.16\n-0.13,-0.97\n0.42,-0.30')
		self.input_file.write('-0.92,-0.61\n0.66,0.41\n')
		self.input_file.seek(0, 0) 

		data_list = None


		with self.assertRaises(DataReadingError):
			data_list = ReadFile.create_data_objects(self.input_file)


		self.input_file.close()



	#testing with unvalid #x_name
	#testing that DataReadingError is raised with unvalid file
	def test_4(self):

		self.input_file = StringIO()
		self.input_file.write('#data1\n')
		self.input_file.write('x\n#float\n')
		self.input_file.seek(0, 0) 

		data_list = None

		with self.assertRaises(DataReadingError):
			data_list = ReadFile.create_data_objects(self.input_file)


		self.input_file.close()



	#invalid data_type with x data
	#testing that DataReadingError is raised with unvalid file
	def test_5(self):

		self.input_file = StringIO()
		self.input_file.write('#data1\n')
		self.input_file.write('#x\nfloat\n')
		self.input_file.seek(0, 0) 


		data_list = None


		with self.assertRaises(DataReadingError):

			data_list = ReadFile.create_data_objects(self.input_file)


		self.input_file.close()



	#tests if the created Data object has rigth attributes
	def test_6(self):

		self.input_file = StringIO()
		self.input_file.write('#data1\n')
		self.input_file.write('#x,y\n#float,float\n')
		self.input_file.write('-1.69,0.21\n-0.80,0.95\n-0.41,1.87\n-0.14,2.16\n-0.13,-0.97\n0.42,-0.30\n')
		self.input_file.write('-0.92,-0.61\n0.66,0.41\n')

		self.input_file.seek(0, 0) 

		data_list = None
		data_list = ReadFile.create_data_objects(self.input_file)
	   
		self.input_file.close()

		self.assertEqual( data_list[0].data_length, 8)
		self.assertEqual(data_list[0].x_name, "x")
		self.assertEqual(data_list[0].y_name, "y")
		self.assertEqual(data_list[0].number_of_decimals, 2)
		self.assertEqual( data_list[0].data_type, "doublenum")
		self.assertEqual( data_list[0].data_title, "data1")
		self.assertEqual(type(data_list[0].x[1]), type(0.2))
		self.assertEqual(type(data_list[0].y[1]), type(0.2))



if __name__ == '__main__':
	unittest.main()
