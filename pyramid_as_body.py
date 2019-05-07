#import FreeCAD
#import PartDesign

import math

import sys
from PySide import QtGui, QtCore

def say(s):
	msg = QtGui.QMessageBox()
	msg.move(800,200)
	msg.setIcon(QtGui.QMessageBox.Information)
	msg.setText(s)
	msg.setWindowTitle("Message")
	msg.setStandardButtons(QtGui.QMessageBox.Ok )	
	retval = msg.exec_()


def pyramid_as_body(n,radiusb,radiust,height):


    if (sideb == 0 and diamb == 0 and sidet == 0 and diamt == 0) or n < 3  or height == 0:
        say ("INPUT ERROR")

    else:
	    
	    # depending values
	    alfa = 2 * math.pi / n
	    beta = (math.pi/2 - alfa/2)
	    
	    if sideb != 0 :
	        radiusb = abs((sideb / 2 )/ math.sin( alfa / 2 ))
	        distb = abs(sideb / 2 * math.tan(beta))
	    else:     
	        sideb = abs(radiusb * math.sin( alfa / 2) * 2)
	        distb = abs(radiusb * math.cos (alfa / 2))
	    
	    if sidet != 0 :
	        radiust = abs((sidet / 2 )/ math.sin( alfa / 2 ))
	        distt = abs(sidet / 2 * math.tan(beta))
	    else:     
	        sidet = abs(radiust * math.sin( alfa / 2) * 2)
	        distt = abs(radiust * math.cos (alfa / 2))
	    
	    angle2z = math.atan ((distb-distt) / height)
	    angle2zdeg = math.atan ((distb-distt) / height)* 180 / math.pi
	    #cone
	    coneradiusb = round(radiusb * 1.02) 
	    coneradiust = round(radiust * 1.02) 
	    coneheight = height * 1.025
	    
	    # cube
	    cubex_length = round(abs(sideb * 1.2))
	    cubey_width = round(abs((coneradiusb - distb) * 1.05))
	    cubez_height = round(abs((height + cubey_width) * 1.05))
	
	    cubex = - cubex_length / 2
	    cubey = - distb - cubey_width / math.cos(angle2z)
	    cubez = 0
	
	   
	    
	    
	    
	    App.activeDocument().addObject('PartDesign::Body','Body')
	    App.ActiveDocument.recompute()
	    
	    App.ActiveDocument.addObject('PartDesign::AdditiveCone','Cone')
	    App.ActiveDocument.Body.addObject(App.activeDocument().Cone)
	    App.ActiveDocument.recompute()
	
	    App.ActiveDocument.Cone.MapMode = 'FlatFace'
	    App.ActiveDocument.Cone.Radius1=coneradiusb
	    App.ActiveDocument.Cone.Radius2=coneradiust
	    App.ActiveDocument.Cone.Height=coneheight
	    App.ActiveDocument.Cone.Angle=360.00    
	    App.ActiveDocument.recompute()
	
	    App.ActiveDocument.addObject('PartDesign::SubtractiveBox','Box')
	    App.ActiveDocument.Body.addObject(App.activeDocument().Box)
	    App.ActiveDocument.recompute()
	    App.ActiveDocument.Box.MapMode = 'FlatFace'
	    App.ActiveDocument.Box.Length=cubex_length
	    App.ActiveDocument.Box.Width=cubey_width
	    App.ActiveDocument.Box.Height=cubez_height 
	    App.ActiveDocument.recompute()
	    App.ActiveDocument.Box.Placement = App.Placement(App.Vector(cubex,cubey,cubez),App.Rotation(App.Vector(-1,0,0),angle2zdeg))
	    App.ActiveDocument.recompute()
	
	
	    App.activeDocument().Body.newObject("PartDesign::PolarPattern","PolarPattern")
	    App.ActiveDocument.recompute()
	    App.activeDocument().PolarPattern.Originals = [App.activeDocument().Box,]
	    App.activeDocument().PolarPattern.Axis = (App.activeDocument().Z_Axis, [""])
	    App.activeDocument().PolarPattern.Angle = 360
	    App.activeDocument().PolarPattern.Occurrences = n
	    App.activeDocument().Body.Tip = App.activeDocument().PolarPattern  
	    App.ActiveDocument.PolarPattern.Originals = [App.ActiveDocument.Box,]
	    App.ActiveDocument.recompute()
	
	    App.ActiveDocument.Cone.ViewObject.Visibility=False
	    App.ActiveDocument.Box.ViewObject.Visibility=False
	    App.ActiveDocument.recompute()
	    Gui.SendMsgToActiveView("ViewFit")
	


class PyramidDialog(QtGui.QWidget):

	def __init__(self):
		super(PyramidDialog, self).__init__()
        
		self.initUI()
        
	def initUI(self): 
		grid = QtGui.QGridLayout()

		button = QtGui.QPushButton('Cancel')
		grid.addWidget(button, 10, 3)
		button.clicked.connect(self.cancel_method)
		button2 = QtGui.QPushButton('OK')
		grid.addWidget(button2, 10, 5)
		button2.clicked.connect(self.slot_method)

		grid.addWidget(QtGui.QLabel('sides count :'), 0, 2)
		self.count = QtGui.QLineEdit()
		self.count.setMinimumWidth(50)
		self.count.setMaximumWidth(50)
		grid.addWidget(self.count, 0,3)

		grid.addWidget(QtGui.QLabel('height :'), 1, 2)
		self.height = QtGui.QLineEdit()
		grid.addWidget(self.height,1,3)


		grid.addWidget(QtGui.QLabel('Bottom :'), 2, 2)

		grid.addWidget(QtGui.QLabel('radius :'), 3, 2)
		self.radiusb = QtGui.QLineEdit()
		grid.addWidget(self.radiusb,3,3)

		grid.addWidget(QtGui.QLabel('or sidelength:'), 3, 4)
		self.sideb = QtGui.QLineEdit()
		grid.addWidget(self.sideb, 3,5)

		grid.addWidget(QtGui.QLabel('Top :'),4, 2)

		grid.addWidget(QtGui.QLabel('radius :'), 5, 2)
		self.radiust = QtGui.QLineEdit()
		grid.addWidget(self.radiust, 5,3)

		grid.addWidget(QtGui.QLabel('or sidelength:'), 5, 4)
		self.sidet = QtGui.QLineEdit()
		grid.addWidget(self.sidet, 5,5)
		
		self.warninglabel = QtGui.QLabel('')
		grid.addWidget(self.warninglabel, 6, 2)


		self.setLayout(grid)   
		self.move(500, 350)
		self.setWindowTitle('Pyramid as FreeCad-body')    
		self.show()


	def slot_method(self):
		
		if (str(self.count.text()))== "":
			n = 0
		else:
			n = int(float(str(self.count.text())))
		if (str(self.height.text()))== "":
			height = 0
		else:
			height = float(str(self.height.text()))
		if (str(self.radiusb.text()))== "":
			radiusb = 0
		else:
			radiusb = float(str(self.radiusb.text()))
		if (str(self.radiust.text()))== "":
			radiust = 0
		else:
			radiust = float(str(self.radiust.text()))
		if (str(self.sideb.text()))== "":
			sideb = 0
		else:
			sideb = float(str(self.sideb.text()))
		if (str(self.sidet.text()))== "":
			sidet = 0
		else:
			sidet = float(str(self.sidet.text()))

		if (n < 3) or ( radiusb == 0 and radiust == 0 and sideb == 0 and sidet == 0):
			say("INPUT ERROR!")
			self.close()
		else :
			angle_center = 2 * math.pi / n
			if sideb != 0 :
				radiusb = (sideb/2) / cos ((math.pi - angle_center) / 2)
			if sidet != 0 :
				radiust = (sidet/2) / cos ((math.pi - angle_center) / 2)
			
			pyramid_as_body(n,radiusb,radiust,height)
			
			self.close()

	def cancel_method(self):
		self.close()
        

mainaction = PyramidDialog()





