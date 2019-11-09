
"""
The module explainded:

This module mainwindow.py controls and creates the programme's GUI. 

TO OPEN THE PROGRAMME RUN THIS MODULE. 

"""




import sys, random
from PyQt5.QtWidgets import QApplication, QPushButton, QMessageBox, QDesktopWidget, QMainWindow, QAction,  QFileDialog, QInputDialog
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QLine, QLineF, QPointF, QObject

from readfile import ReadFile

import math


#Explanations for imported modules and classes:

#QDesktopWidget provides info about user's desktop for example screen size.

#QMainWindow provides statusbar, toolbar, menubar and other stuff for main window. QMainWindow inherits QWidget

#QAction is abstraction for actions performed with bars

#QInputdialog receives values from user

#QFiledialog allows user to select directories





class MainWindow(QMainWindow):

	def __init__(self):

		super().__init__() #constructs an object from parent class
		self.data_list = []
		self.initUI() #calls for initializing method
	

		#initializes titles that will be plotted later
		self.title = "Plot title"
		self.xtitle = "x axis"
		self.ytitle =  "y axis"



	def initUI(self): #initializing method for main window


		self.setGeometry(300, 300, 1050, 1000) #first numbers are coordinates on the window, latter ones size
		self.setWindowTitle('Data Visualization programme')     
		self.center() #calls for method center
		self.statusBar() 
		self.create_menubar()
		self.grid_button() #creates checkable grid button to menubar
		self.fitline_button() #creates button for fitting a line to points
		self.givetitle_button() #creates button for user to change the title of the plot
		self.giveaxis_button() #creates button for user to change the names of the axis
		self.show()





	#METHODS:


	#centers the window on user's screen
	def center(self):
	

		qr = self.frameGeometry()
		print(qr)
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())




	#creates menubar and adds file menu to it:
	def create_menubar(self):

		self.menubar = self.menuBar() #creates top menubar
		fileMenu = self.menubar.addMenu('&File') #creates filemenu and adds it to menubar
		openfileact = QAction("Open file", self) #creates "Open file" action to file menu
		openfileact.triggered.connect(self.showDialog) #goes to method showDialog(), when user selects "Open file
		fileMenu.addAction(openfileact)   





	#Opens file selection window to user and calls for method create_data_objects() of the ReadFile class to read data from the file:
	def showDialog(self):

		dialog = QFileDialog()
		dialog.setNameFilter('Text files (*.txt *.csv) ')
		path = dialog.getOpenFileName(self, 'Open file', '/home', 'Text files (*.txt *.csv) ')

		try:

			with open(path[0]) as fname:
				self.data_list = ReadFile.create_data_objects(fname) #reads data from file to data_list
				
				#randomly chooces plotting colours that each data set 
				self.colour_list = []
				for i in range( len(self.data_list)):
					self.colour_list.append( self.get_color())
				
		except OSError:

			print("Could not open {}".format(path), file=sys.stderr)


	#randomly selects colours for all the data sets plotted
	def get_color(self):

		red = random.randrange(0,255)
		green = random.randrange(0,255)
		blue = random.randrange(0,255)

		return QColor(red, green, blue)




	#Draws the data points:
	def drawPoints(self, qp):

		for i in range(self.how_many_datasets):
			pen = QPen( self.colour_list[i] ,  14, Qt.SolidLine, Qt.RoundCap )
			qp.setPen(pen)

			for b in range( self.data_list[i].data_length ):

				x0 = self.data_list[i].x[b] 
				y0 = self.data_list[i].y[b]
 
				x0 = (x0 + self.normalizer_x)*self.scaling_x + self.margin_x #here we normalize and scale the x coordinate to be able to plot it
				y0 = (self.height() - 2*self.margin_y) - (y0 + self.normalizer_y)*self.scaling_y + self.margin_y 
				#for y coordinate we also have to substract y from the (heigth - margins) in order to start the drawing from lower left corner instead of upper left corner. 
				#On Qt, (0,0) coordinate is on upper left corner and we change it to be in lower left corner for the data.

				qp.drawPoint(x0,y0)
	




	# scales the data for nice plotting according to the min and max values in data sets:
	def scale(self): 

		"""
		idea:
				1.find min and max values in all the data sets that will be plottet at the same time
				2.calculate the distance between the min and max values
				3.compare the distance of the min and max data values to the plotting window's length minus some margins
				--> Like this we find scaling number that the data needs to be multiplied with to get nice full screen plot. 
				--> Scaling keeps the relative distances between datapoints but makes them spread to entire alvailable plotting area.

		"""
		#initialize values
		max_values_x = []
		min_values_x = []
		max_values_y = []
		min_values_y = []
		how_many_datasets = len(self.data_list)

		#find min and max values on data
		for i in range(how_many_datasets):

			max_values_x.append(max(self.data_list[i].x))
			min_values_x.append(min(self.data_list[i].x))		
			max_values_y.append(max(self.data_list[i].y))
			min_values_y.append(min(self.data_list[i].y))
		self.max_y = max(max_values_y)
		self.max_x = max(max_values_x)
		self.min_y = min(min_values_y)
		self.min_x = min(min_values_x)

		#calculate max distances on data
		self.width_x = abs(self.max_x - self.min_x) 
		self.heigth_y = abs(self.max_y - self.min_y)

		#chooce margin sizes
		self.margin_x = 0.13*self.width()
		self.margin_y = 0.13*self.height()

		#determine scaling factor to get nice plot
		self.scaling_x = (self.width() -2*self.margin_x) / self.width_x
		self.scaling_y = (self.height() - 2*self.margin_y) / self.heigth_y

		#we will normalize the data to start from zero
		self.normalizer_x = 0
		self.normalizer_y = 0

		if(self.min_x < 0):
			self.normalizer_x = abs(self.min_x)

		if(self.min_y < 0 ):
			self.normalizer_y = abs(self.min_y)

		if(self.min_x > 0):
			self.normalizer_x =  -1*self.min_x

		if(self.min_y > 0 ):
			self.normalizer_y = -1*self.min_y		




	#creates figure settings menu and checkable grid button to it:
	def grid_button(self):

		self.plotmenu = self.menubar.addMenu('&Figure settings') #adds Figure settings menu to menubar
		self.gridact = QAction('Grid', self, checkable=True)
		self.gridact.setStatusTip('Set grid on the figure')
		self.gridact.setChecked(True) #first put grid on
		self.gridact.triggered.connect(self.repaint) #repaints window if user wants grid on/off
		self.plotmenu.addAction( self.gridact)



	#creates figure settings menu and checkable fitting line button to it:
	def fitline_button(self):

		self.fitact = QAction('Fit line', self, checkable=True)
		self.fitact.setStatusTip('Draw line between points on the figure')
		self.fitact.setChecked(True)
		self.fitact.triggered.connect(self.repaint) #repaints window if user wants line on/off
		self.plotmenu.addAction( self.fitact)



	#when paintEvent is generated, the window is repainted:
	def paintEvent(self, e):

		qp = QPainter() #Creates a QPainter object that does the painting
		qp.begin(self)

		self.how_many_datasets = len(self.data_list)
		if(self.how_many_datasets != 0): #repaints only if we have data on the list
			self.scale()
			self.drawPoints(qp)
			self.drawGrid(qp)

			if(self.fitact.isChecked()):
				self.fitline(qp)

		qp.end()





	#Draws the grid and number axis:
	def drawGrid(self,qp): 


		"""
		idea: 
		 1.divides the plot into n blocs depending how thick grid we want. 
		 2. starts plotting the horizontal and vertical grid lines from up to down. 
		 Coordinates of the lines are again skaled and for y coordinate we have to substract y from the (heigth - margins) in order to get the maximun value up and lower value down.


		"""

		#select how many grids we want in horizontal and vertical directions
		number_of_blocs = 5

		#calculates the width and height of one grid square
		dist_between_xlines = self.width_x*self.scaling_x/number_of_blocs
		dist_between_ylines = self.heigth_y*self.scaling_y/number_of_blocs
		

		for i in range(number_of_blocs+1):

			#sets color for grid lines
			color = QColor( Qt.black)
			pen = QPen( color,  1, Qt.SolidLine)
			qp.setPen(pen)

			# calculates the coordinates for horizontal lines
			xmin= (self.min_x + self.normalizer_x)*self.scaling_x + self.margin_x
			xmax= (self.max_x + self.normalizer_x)*self.scaling_x + self.margin_x
			yline= ((self.height() - 2*self.margin_y) - (self.max_y + self.normalizer_y)*self.scaling_y + self.margin_y + dist_between_ylines*i)

			#calculates the coordinates for vertical lines
			ymin= (self.height() - 2*self.margin_y) - (self.max_y + self.normalizer_y)*self.scaling_y + self.margin_y
			ymax= (self.height() - 2*self.margin_y) - (self.min_y + self.normalizer_y)*self.scaling_y + self.margin_y
			xline = ((self.min_x + self.normalizer_x)*self.scaling_x + self.margin_x + dist_between_xlines*i)

			#creates plottable QLineF objects from coordinates
			lineHorizontal = QLineF( xmin , yline , xmax, yline )
			lineVertical = QLineF( xline,  ymin , xline  ,ymax  )
		
			#draws grid only if user has checked it from the menu
			if(self.gridact.isChecked()):
				qp.drawLine(lineHorizontal)
				qp.drawLine(lineVertical)

			#draws the axis numbers:
			#to find out the real data number we need to remove all the scaling factors.
			textpointx = QPointF(xline, (ymax + 0.02*ymax))
			textpointy = QPointF((xmin - 0.3*xmin), yline )

			#finds the x number on data (strips all the scaling)
			xnumbertowrite =  xline - self.margin_x 
			xnumbertowrite /= self.scaling_x
			xnumbertowrite -= self.normalizer_x

			#finds y number on data (strips all the scaling)
			ynumbertowrite =  yline - self.margin_y
			ynumbertowrite /= self.scaling_y
			ynumbertowrite -= self.normalizer_y

			#removes more scaling numbers if there is negative data to get the real y number
			if( self.min_y < 0):

				if(ynumbertowrite < 0):
					ynumbertowrite = self.heigth_y -  abs(ynumbertowrite)
				else:
					ynumbertowrite = self.max_y - abs(self.min_y) - ynumbertowrite

			else:

				ynumbertowrite = self.max_y - abs(self.min_y) - ynumbertowrite			

			#draws the real x and y values
			qp.drawText( textpointx, str(round(xnumbertowrite,2)))
			qp.drawText(textpointy, str(round(ynumbertowrite,2)))

		#makes some of the values global for later use when we draw titles and axis names.
		self.xmin = xmin
		self.ymin = ymin
		self.xmax = xmax
		self.ymax = ymax
		self.dist_between_xlines = dist_between_xlines
		self.dist_between_ylines = dist_between_ylines
		self.dist_between_xlines = dist_between_xlines

		#calls for method to draw the title of the plot 
		self.draw_title(qp, self.title, self.xtitle,self.ytitle)
		
		#calls for method to draw the info box of the plot
		self.create_plot_info_box(qp)





	#fits a line between plotted points when user checks "Fit line" from figure settings menu.
	def fitline(self, qp):

		"""
		idea of this method:
		The x and y data is not sorted from min to max value. However, in order to fit the line we need to now the indexes of data points that have x values next to each others. (To combine these points to form the line.)
		To do this we copy the datasets and modify the copied datas in following way:

		1. copy x and y data sets for local variables to be able to modify them only for this line fitting purpose
		2. find the index of min x value. (The corresponding y coordinate has the same index.)
		3. delete the current min x value and its corresponding y value to find out the next smallest value. 
		(The next smallest value is the new min x value after deletation)
		4. draw line between these adjacent points.
		5.repeat until the end of data.
		"""
		#draws lines between all data sets
		for i in range( self.how_many_datasets):

			#set pen for each line with rigth colour
			pen = QPen( self.colour_list[i],  1, Qt.SolidLine)
			qp.setPen(pen)

			#copies data sets so that they can be edited
			xdata = self.data_list[i].x.copy()
			ydata = self.data_list[i].y.copy()

			for b in range(self.data_list[i].data_length -1):

				#find min x value and index corresponding to it
				ind0 = xdata.index(min(xdata))
				x0 = xdata[ind0]
				y0 = ydata[ind0]
 
				x0 = (x0 + self.normalizer_x)*self.scaling_x + self.margin_x #here we normalize and scale the x coordinate to be able to plot it
				y0 = (self.height() - 2*self.margin_y) - (y0 + self.normalizer_y)*self.scaling_y + self.margin_y 
				#for y coordinate we also have to substract y from the (heigth - margins) in order to start the drawing from lower left corner instead of upper left corner. 
				#(On Qt, (0,0) coordinate is on upper left corner and we change it to be in lower left corner for the data.

				#delete min x value and y value corresponding to it to be able to find the second smallest
				del xdata[ind0]
				del ydata[ind0]
				ind1 = xdata.index(min(xdata))
				x1 = xdata[ind1]
				y1 = ydata[ind1]
 	
 				#scale datavalues for plotting
				x1 = (x1 + self.normalizer_x)*self.scaling_x + self.margin_x 
				y1 = (self.height() - 2*self.margin_y) - (y1 + self.normalizer_y)*self.scaling_y + self.margin_y 
				
				#draw line
				line = QLineF( x0,  y0 , x1 ,y1  )
				qp.drawLine(line)



	
	#creates button for changing the title of the plot and adds it to plotmenu
	def givetitle_button(self):

		self.titleact = QAction('Edit title', self)
		self.titleact.setStatusTip('Give a title to the figure')
		self.titleact.triggered.connect( self.edit_title)
		self.plotmenu.addAction( self.titleact)

	
	#reads new title name from the user and calls for repaint.
	def edit_title(self):

		text, ok = QInputDialog.getText(self, 'Enter new title', 'Title:')
		
		if ok:
			self.title=str(text)	

		self.xtitle = self.xtitle
		self.ytitle = self.ytitle
		self.repaint()



	#creates button for changing the names of the axis of the plot and adds it to plotmenu
	def giveaxis_button(self):

		self.axisact = QAction('Edit axis names', self)
		self.axisact.setStatusTip('Give names to the axis of the figure')
		self.axisact.triggered.connect( self.edit_axis)  
		self.plotmenu.addAction( self.axisact)


	
	#reads axis names from the user and calls for repaint
	def edit_axis(self):

		text, ok = QInputDialog.getText(self, 'Enter new axis names', 'Enter new axis names in following format: x-name , y.name')
		
		if ok:
			xname, yname = text.split(",")
			self.xtitle=str(xname)
			self.ytitle=str(yname)

		self.title = self.title
		self.repaint()



	#draws axis names and title name.
	def draw_title(self, qp, plot_title, x_title, y_title):

		#sets pen for title
		color = QColor( Qt.black)
		pen = QPen( color,  1, Qt.SolidLine)
		qp.setFont( QFont('Decorative', 20))
		qp.setPen(pen)


		#sets coordinates for x axis name:
		textx = QPointF( self.width()/1.4 , (self.ymax + 0.06*self.ymax))
		textpointxaxis = QPointF(self.width()/1.35 , (self.ymax + 0.06*self.ymax))
		
		#sets coordinates for y axis name:
		texty = QPointF( (self.xmin - 0.3*self.xmin) , self.ymin - 0.4*self.ymin)
		textpointyaxis = QPointF((self.xmin - 0.15*self.xmin), self.ymin - 0.4*self.ymin )
		
		#sets coordinates for title:
		textpointitle = QPointF((self.width()/2.3) , self.ymin - 0.2*self.ymin)
		
		#draws title
		qp.drawText( textpointitle, plot_title)

		#sets pen smaller for axis names and draws them
		qp.setFont( QFont('Decorative', 10))
		qp.setPen(pen)
		qp.drawText( textx, "x:")
		qp.drawText( texty, "y:")	
		qp.drawText( textpointxaxis, x_title)
		qp.drawText( textpointyaxis, y_title)



	#creates the info box that includes the name and colour of all the datasets plotted
	def create_plot_info_box(self, qp):


		#selects the colour of the box and its outer lines
		color = QColor( Qt.black)
		pen = QPen( color,  1, Qt.SolidLine)
		qp.setBrush( Qt.white)
		qp.setPen(pen)

		#selects the height and width reserved for the name of one data set
		text_height = self.dist_between_ylines/6
		text_width = self.dist_between_xlines

		#draws the info box. First two parameters are coordinates and two latter are height and width of the box. 
		#The height is determined by how many datasets there are and how many names needs to be written.
		qp.drawRect( (self.xmax - 0.2*self.xmax), (self.ymax - 0.2*self.ymax), text_width  , text_height*len(self.data_list) + self.dist_between_ylines*0.14 )


		for i in range(len(self.data_list)):

			#draw the name of every dataset
			color = QColor( Qt.black)
			pen = QPen( color,  1, Qt.SolidLine)
			qp.setFont( QFont('Decorative', 10))
			qp.setPen(pen)
			textpoint = QPointF( (self.xmax - 0.16*self.xmax) , (self.ymax - 0.2*self.ymax) + i*text_height + self.dist_between_ylines*0.14  )		
			qp.drawText( textpoint, self.data_list[i].data_title)

			#draw matching point of every dataset
			pen = QPen( self.colour_list[i] ,  14, Qt.SolidLine, Qt.RoundCap )
			qp.setPen(pen)
			pointcoordinates = QPointF( (self.xmax - 0.18*self.xmax) , (self.ymax - 0.205*self.ymax) + i*text_height + self.dist_between_ylines*0.14  )		
			qp.drawPoint( pointcoordinates)

	



	
	#Verifies closing of the window:
	def closeEvent(self, event): 

		#here we modify closeEvent -method's event handler to verify exit.
		reply = QMessageBox.question(self, 'Exit programme',"Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore() 





if __name__ == '__main__':
	
	app = QApplication(sys.argv) #every PyQt5 application must create an application object. sys.argv parameter includes command line argument
	w = MainWindow()
	sys.exit(app.exec_()) #window's event handling starts