#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from math import sqrt
import re
from PyQt4 import QtGui, QtCore
import MySQLdb
from manRules import *
from addSF import *
from delSF import *

from addLoc import *
from updateLoc import *
from delLoc import *

from addMap import *
from Functions import *

count=0
locCount=0


db = MySQLdb.connect("localhost","sfcuser","sfc123","SFC")
cursor = db.cursor()

DSCP = []
i=1
while(i<=63):
	DSCP.append(i)
	i += 1

sql = "SELECT SF_MAP_INDEX FROM SFMaps"
try:	
	cursor.execute(sql)
	results = cursor.fetchall()
	for val in results:
		DSCP.remove(val[0])
except:
	print "Error updating DSCP available values!!"


##########################
##########Frames##########
##########################
class MainFrame(QtGui.QFrame):
	def __init__(self, parent):
        	super(MainFrame, self).__init__(parent)

	    	self.vbox = QtGui.QVBoxLayout(self)
		self.vbox.addWidget(self.ClassificationBox())
		self.vbox.addWidget(self.SFBox())
		self.vbox.addWidget(self.MapBox())
		self.setLayout(self.vbox)


    	def ClassificationBox(self):
        	groupBox = QtGui.QGroupBox("Classification")
		self.addRule = QtGui.QPushButton("Add &Rules",self)
		self.addRule.setToolTip('Add new classification rule')
		self.delRule = QtGui.QPushButton("&Delete Rules",self)
		self.delRule.setToolTip('Delete an existing rule')

		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(self.addRule)
		vbox.addWidget(self.delRule)
		groupBox.setLayout(vbox)

		return groupBox

    	def SFBox(self):
        	groupBox = QtGui.QGroupBox("SF Functions Management")
		self.addSF = QtGui.QPushButton("Add SF &Function",self)
		self.addSF.setToolTip('Add new Service Function')
		self.delSF = QtGui.QPushButton("Delete &SF Function",self)
		self.delSF.setToolTip('Delete Existing Service Function')
		self.updateSF = QtGui.QPushButton("&Update SF Functions",self)
		self.updateSF.setToolTip('Update Locator of an existing SF Function')

		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(self.addSF)
		vbox.addWidget(self.delSF)
		vbox.addWidget(self.updateSF)
		groupBox.setLayout(vbox)

		return groupBox

	def MapBox(self):
		groupBox = QtGui.QGroupBox("SF Maps Management")
		vbox = QtGui.QVBoxLayout()

		self.addMap = QtGui.QPushButton("Add SF &Map",self)
		self.addMap.setToolTip('Add new SF Map')
		self.delMap = QtGui.QPushButton("&Delete SF Map",self)
		self.delMap.setToolTip('Delete an existing SF Map')

		vbox.addWidget(self.addMap)
		vbox.addWidget(self.delMap)
		groupBox.setLayout(vbox)

        	return groupBox

class addRule_Frame(QtGui.QFrame):
	def __init__(self, parent):
        	super(addRule_Frame, self).__init__(parent)

	    	self.vbox = QtGui.QVBoxLayout(self)

		#Grid Layout
       		grid = QtGui.QGridLayout()
		rules_IP_l = QtGui.QLabel("IP Source")
       		self.rules_IP_le = QtGui.QLineEdit()
		rules_port_l = QtGui.QLabel("Destination Port")
       		self.rules_port_le = QtGui.QLineEdit()

		grid.addWidget(rules_IP_l, 0, 0)
		grid.addWidget(self.rules_IP_le, 0, 1)
		grid.addWidget(rules_port_l, 1, 0)
		grid.addWidget(self.rules_port_le, 1, 1)

		#HBox
	    	hbox = QtGui.QHBoxLayout()
      		self.back = QtGui.QPushButton("Back")
       		self.addRule = QtGui.QPushButton("Add")
		hbox.addWidget(self.back)
		hbox.addWidget(self.addRule)

		#Combo Box
		self.combo = QtGui.QComboBox(self)
		sql = "SELECT SF_MAP_INDEX FROM SFMaps"			
		try:	
			cursor.execute(sql)
   			results = cursor.fetchall()
		except:
   			print "Error: unable to fecth data (SF_MAP_INDEX)"

		for result in results:
			self.combo.addItem(str(result[0]))

		self.error = QtGui.QLabel("")
		self.error.setStyleSheet('color: red')


 		#Main Box
		self.vbox.addLayout(grid)
		self.vbox.addWidget(self.combo)
		self.vbox.addWidget(self.error)
        	self.vbox.addStretch()
		self.vbox.addLayout(hbox)
		self.setLayout(self.vbox)


class delRule_Frame(QtGui.QFrame):
	def __init__(self, parent):
        	super(delRule_Frame, self).__init__(parent)

		#HBox
	    	hbox = QtGui.QHBoxLayout()
       		self.back = QtGui.QPushButton("Back")
       		self.delRule = QtGui.QPushButton("Delete")
		hbox.addWidget(self.back)
		hbox.addWidget(self.delRule)

		#Combo Box
		self.combo = QtGui.QComboBox(self)
		sql = "SELECT SF_MAP_INDEX, IP, port FROM Rules"			
		try:	
			cursor.execute(sql)
   			results = cursor.fetchall()
		except:
   			print "Error: unable to fecth data (Reading Rules)"

		for result in results:
			if(str(result[1])!= None):
				IP = "IP=" + str(result[1])

			if(str(result[2])!= None):
				port = "Port=" + str(result[2])

			self.combo.addItem(str(result[0]) + ": " + IP + ", " + port)
			IP = ""
			port = ""

		#Main Box
	    	self.vbox = QtGui.QVBoxLayout()
		self.label = QtGui.QLabel("Choose the Rule to delete:", self)
		self.vbox.addWidget(self.label)
		self.vbox.addWidget(self.combo)
		self.vbox.addStretch()
		self.vbox.addLayout(hbox)
		self.setLayout(self.vbox)

class addFunction_Frame(QtGui.QFrame):
	def __init__(self, parent):
        	super(addFunction_Frame, self).__init__(parent)

		#Grid Layout
       		grid = QtGui.QGridLayout()

		func_l = QtGui.QLabel("SF Function")
       		self.func_le = QtGui.QLineEdit()
		self.func_le.setMaxLength(30)

		loc1_l = QtGui.QLabel("SF Locator 1 ")
       		self.loc1_le = QtGui.QLineEdit()
		self.loc1_le.setMaxLength(15)

		loc2_l = QtGui.QLabel("SF Locator 2 ")
       		self.loc2_le = QtGui.QLineEdit()
		self.loc2_le.setMaxLength(15)

		loc3_l = QtGui.QLabel("SF Locator 3 ")
       		self.loc3_le = QtGui.QLineEdit()
		self.loc3_le.setMaxLength(15)


		desc_l = QtGui.QLabel("SF Description ")
       		self.desc_te = QtGui.QTextEdit()

		grid.addWidget(func_l, 0, 0)
		grid.addWidget(self.func_le, 0, 1)
		grid.addWidget(loc1_l, 1, 0)
		grid.addWidget(self.loc1_le, 1, 1)
		grid.addWidget(loc2_l, 2, 0)
		grid.addWidget(self.loc2_le, 2, 1)
		grid.addWidget(loc3_l, 3, 0)
		grid.addWidget(self.loc3_le, 3, 1)
		grid.addWidget(desc_l, 4, 0)
		grid.addWidget(self.desc_te, 4, 1)

		#Box3
	    	hbox3 = QtGui.QHBoxLayout()
       		self.back = QtGui.QPushButton("Back")
       		self.addFunc = QtGui.QPushButton("OK")
		hbox3.addWidget(self.back)
		hbox3.addWidget(self.addFunc)

		#Main Box
		self.msg = QtGui.QLabel("")
		self.msg.setStyleSheet('color: red')
	    	self.vbox = QtGui.QVBoxLayout()
		self.vbox.addLayout(grid)
		self.vbox.addWidget(self.msg)
        	self.vbox.addStretch()
		self.vbox.addLayout(hbox3)
		self.setLayout(self.vbox)


class updateFunction_Frame(QtGui.QFrame):
	def __init__(self, parent):
        	super(updateFunction_Frame, self).__init__(parent)

		self.addLocator = QtGui.QPushButton("&Add Locator",self)
		self.addLocator.setToolTip('Add new Locator to a specific SF Function')
		self.updateLocator = QtGui.QPushButton("&Update Locator",self)
		self.updateLocator.setToolTip('Update existing Locators of a specific SF Function')
		self.delLocator = QtGui.QPushButton("&Delete Locator",self)
		self.delLocator.setToolTip('Delete specific locator')
       		self.back = QtGui.QPushButton("Back")

	    	self.vbox = QtGui.QVBoxLayout(self)
        	self.vbox.addStretch()
		self.vbox.addWidget(self.addLocator)
		self.vbox.addWidget(self.updateLocator)
		self.vbox.addWidget(self.delLocator)
		self.vbox.addWidget(self.back)
        	self.vbox.addStretch()
		self.setLayout(self.vbox)


class delFunction_Frame(QtGui.QFrame):
	def __init__(self, parent):
        	super(delFunction_Frame, self).__init__(parent)

		#HBox
	    	hbox = QtGui.QHBoxLayout()
       		self.back = QtGui.QPushButton("Back")
       		self.delFunc = QtGui.QPushButton("Delete")
		hbox.addWidget(self.back)
		hbox.addWidget(self.delFunc)

		#Combo Box
		self.combo = QtGui.QComboBox(self)
		sql = "SELECT SF, Locator1, Locator2, locator3 FROM Locators"			
		try:	
			cursor.execute(sql)
   			results = cursor.fetchall()
		except:
   			print "Error: unable to fecth data"

		for result in results:
			self.combo.addItem(str(result[0]))

		#Main Box
	    	self.vbox = QtGui.QVBoxLayout()
		self.label = QtGui.QLabel("Choose the SF Function to delete:", self)
		self.vbox.addWidget(self.label)
		self.vbox.addWidget(self.combo)
		self.vbox.addStretch()
		self.vbox.addLayout(hbox)
		self.setLayout(self.vbox)

class addLocator_Frame(QtGui.QFrame):
	def __init__(self, parent):
        	super(addLocator_Frame, self).__init__(parent)

		self.loc1 = []
		self.loc2 = []
		self.loc3 = []

		#Grid
       		grid = QtGui.QGridLayout()

		newLoc2_l = QtGui.QLabel("New SF Locator 2 ")
       		self.newLoc2_le = QtGui.QLineEdit()
		self.newLoc2_le.setMaxLength(15)

		newLoc3_l = QtGui.QLabel("New SF Locator 3 ")
       		self.newLoc3_le = QtGui.QLineEdit()
		self.newLoc3_le.setMaxLength(15)


		grid.addWidget(newLoc2_l, 0, 0)
		grid.addWidget(self.newLoc2_le, 0, 1)
		grid.addWidget(newLoc3_l, 1, 0)
		grid.addWidget(self.newLoc3_le, 1, 1)

		#HBox
	    	hbox = QtGui.QHBoxLayout()
       		self.back = QtGui.QPushButton("Back")
       		self.addLoc = QtGui.QPushButton("Add")
		hbox.addWidget(self.back)
		hbox.addWidget(self.addLoc)

		#Combo Box
		self.combo = QtGui.QComboBox(self)
		sql = "SELECT SF, Locator1, Locator2, Locator3, LocNum FROM Locators"
		try:	
			cursor.execute(sql)
   			results = cursor.fetchall()
		except:
   			print "Error: unable to fecth data"

		for result in results:
			self.loc1.append(result[1])
			self.loc2.append(result[2])
			self.loc3.append(result[3])
			if result[4]==3:	
				self.combo.addItem(str(result[0]) + " => " + str(result[1]) + "|" + str(result[2]) + "|" + str(result[3]))
			elif result[4]==2:	
				self.combo.addItem(str(result[0]) + " => " + str(result[1]) + "|" + str(result[2]))
			elif result[4]==1:
				self.combo.addItem(str(result[0]) + " => " + str(result[1]))
			else:
				print "Error displaying SF Functions' list"


		#Main Box
	    	self.vbox = QtGui.QVBoxLayout()
		self.error_msg = QtGui.QLabel("")
		self.error_msg.setStyleSheet('color: red')
		self.success_msg = QtGui.QLabel("")
		self.success_msg.setStyleSheet('color: green')
		self.label = QtGui.QLabel("Choose the Entry to update:", self)
		self.vbox.addWidget(self.label)
		self.vbox.addWidget(self.combo)
		self.vbox.addLayout(grid)
		self.vbox.addWidget(self.error_msg)
		self.vbox.addWidget(self.success_msg)
		self.vbox.addStretch()
		self.vbox.addLayout(hbox)
		self.setLayout(self.vbox)

class updateLocator_Frame(QtGui.QFrame):
	def __init__(self, parent):
        	super(updateLocator_Frame, self).__init__(parent)

		self.SFList = []
		self.loc1 = []
		self.loc2 = []
		self.loc3 = []

		#Grid
       		grid = QtGui.QGridLayout()

		newLoc1_l = QtGui.QLabel("New SF Locator 1 ")
       		self.newLoc1_le = QtGui.QLineEdit()
		self.newLoc1_le.setMaxLength(15)

		newLoc2_l = QtGui.QLabel("New SF Locator 2 ")
       		self.newLoc2_le = QtGui.QLineEdit()
		self.newLoc2_le.setMaxLength(15)

		newLoc3_l = QtGui.QLabel("New SF Locator 3 ")
       		self.newLoc3_le = QtGui.QLineEdit()
		self.newLoc3_le.setMaxLength(15)

		grid.addWidget(newLoc1_l, 0, 0)
		grid.addWidget(self.newLoc1_le, 0, 1)
		grid.addWidget(newLoc2_l, 1, 0)
		grid.addWidget(self.newLoc2_le, 1, 1)
		grid.addWidget(newLoc3_l, 2, 0)
		grid.addWidget(self.newLoc3_le, 2, 1)

		#HBox
	    	hbox = QtGui.QHBoxLayout()
       		self.back = QtGui.QPushButton("Back")
       		self.updateLoc = QtGui.QPushButton("Update")
		hbox.addWidget(self.back)
		hbox.addWidget(self.updateLoc)

		#Combo Box
		self.combo = QtGui.QComboBox(self)
		sql = "SELECT SF, Locator1, Locator2, Locator3, LocNum FROM Locators"
		try:	
			cursor.execute(sql)
   			results = cursor.fetchall()
		except:
   			print "Error: unable to fecth data"

		for result in results:
			self.SFList.append(str(result[0]))
			self.loc1.append(result[1])
			self.loc2.append(result[2])
			self.loc3.append(result[3])
			if result[4]==3:
				self.combo.addItem(str(result[0]) + " => " + str(result[1]) + "|" + str(result[2]) + "|" + str(result[3]))
			elif result[4]==2:	
				self.combo.addItem(str(result[0]) + " => " + str(result[1]) + "|" + str(result[2]))
			else:
				self.combo.addItem(str(result[0]) + " => " + str(result[1]))


		#Main Box
	    	self.vbox = QtGui.QVBoxLayout()
		self.error_msg = QtGui.QLabel("")
		self.error_msg.setStyleSheet('color: red')
		self.success_msg = QtGui.QLabel("")
		self.success_msg.setStyleSheet('color: green')
		self.label = QtGui.QLabel("Choose the Entry to update:", self)
		self.vbox.addWidget(self.label)
		self.vbox.addWidget(self.combo)
		self.vbox.addLayout(grid)
		self.vbox.addWidget(self.error_msg)
		self.vbox.addWidget(self.success_msg)
		self.vbox.addStretch()
		self.vbox.addLayout(hbox)
		self.setLayout(self.vbox)

class delLocator_Frame(QtGui.QFrame):
	def __init__(self, parent):
        	super(delLocator_Frame, self).__init__(parent)

		self.error_msg = QtGui.QLabel("")
		self.error_msg.setStyleSheet('color: red')
		self.success_msg = QtGui.QLabel("")
		self.success_msg.setStyleSheet('color: green')
		typeLoc = QtGui.QLabel("Type the IP address of the locator to remove:")

		#HBox
	    	hbox1 = QtGui.QHBoxLayout()
		loc_l= QtGui.QLabel("SF Locator")
       		self.loc = QtGui.QLineEdit()
		self.loc.setMaxLength(15)
		hbox1.addWidget(loc_l)
		hbox1.addWidget(self.loc)

		#HBox
	    	hbox2 = QtGui.QHBoxLayout()
       		self.back = QtGui.QPushButton("Back")
       		self.delLoc = QtGui.QPushButton("Delete")
		hbox2.addWidget(self.back)
		hbox2.addWidget(self.delLoc)


		#Main Box
	    	self.vbox = QtGui.QVBoxLayout()
		self.vbox.addWidget(typeLoc)
		self.vbox.addLayout(hbox1)
		self.vbox.addWidget(self.error_msg)
		self.vbox.addWidget(self.success_msg)
		self.vbox.addStretch()
		self.vbox.addLayout(hbox2)
		self.setLayout(self.vbox)

class addMap_Frame(QtGui.QFrame):
	def __init__(self, parent):
        	super(addMap_Frame, self).__init__(parent)

		#Box1
	    	hbox1 = QtGui.QHBoxLayout()
		self.index_l2 = QtGui.QLabel("SF_Map_Index")
		self.msg = QtGui.QLabel("")
		self.msg.setStyleSheet('color: red')
       		self.index_le = QtGui.QLineEdit()
		self.index_le.setMaxLength(2)
		self.index_le.sizeHint()
		self.index_le.setToolTip("A new valid value is automatically affected if no value typed")
		hbox1.addWidget(self.index_l2)
		hbox1.addWidget(self.index_le)
		hbox1.addWidget(self.msg)
        	hbox1.addStretch()

		#Box3
	    	hbox3 = QtGui.QHBoxLayout()
       		self.back = QtGui.QPushButton("Back")
       		self.addMap = QtGui.QPushButton("OK")
		hbox3.addWidget(self.back)
		hbox3.addWidget(self.addMap)


		#Main Box
	    	self.vbox = QtGui.QVBoxLayout()
		self.SFLabel = QtGui.QLabel("New SF Map: ", self)
       		self.resetMap = QtGui.QPushButton("Reset Map")
		self.vbox.addLayout(hbox1)
		self.vbox.addWidget(self.SFCheckList())
		self.vbox.addWidget(self.resetMap)
		self.vbox.addWidget(self.SFLabel)
        	hbox1.addStretch()
		self.vbox.addLayout(hbox3)
		self.setLayout(self.vbox)

	def SFCheckList(self):
		groupBox = QtGui.QGroupBox("SF Functions List")
       		self.grid = QtGui.QGridLayout()
		self.checkBoxList = [[], []]

		#Reading supported SF functions
		try:
			sql = "SELECT SF FROM Locators"
			cursor.execute(sql)
			results = cursor.fetchall()
		except:
			print "Error: unable to fecth data (SF Functions)"


		#Building the Checkbox List
		for SF in results:
			self.checkBoxList[0].append(QtGui.QCheckBox(SF[0])) 
			self.checkBoxList[1].append(SF[0])
		
		self.SFCheckListDisplay()
		groupBox.setLayout(self.grid)

		return groupBox
		
	def SFCheckListDisplay(self):
		l = sqrt(len(self.checkBoxList[0]))
		if(l!=int(l)):
			l= int(l) + 1

		i=0
		j=0
		for cb in self.checkBoxList[0]:
			self.grid.addWidget(cb, i, j)
			j+=1
			if(j==l):
				i+=1
				j=0


class delMap_Frame(QtGui.QFrame):
	def __init__(self, parent):
        	super(delMap_Frame, self).__init__(parent)

		self.SFMapIndexesList = []

		#HBox
	    	hbox = QtGui.QHBoxLayout()
       		self.back = QtGui.QPushButton("Back")
       		self.delMap = QtGui.QPushButton("Delete")
		hbox.addWidget(self.back)
		hbox.addWidget(self.delMap)

		#Combo Box
		self.combo = QtGui.QComboBox(self)
		sql = "SELECT SF_Map_Index, SFMap FROM SFMaps ORDER BY SF_Map_Index"			
		try:	
			cursor.execute(sql)
   			results = cursor.fetchall()
		except:
   			print "Error: unable to fecth data (SF Maps to delete)"

		for result in results:
			self.SFMapIndexesList.append(result[0])
			self.combo.addItem(str(result[0]) + " " + str(result[1]))

		#Main Box
	    	self.vbox = QtGui.QVBoxLayout()
		self.label = QtGui.QLabel("Choose the SF Map to delete:", self)
		self.vbox.addWidget(self.label)
		self.vbox.addWidget(self.combo)
		self.vbox.addStretch()
		self.vbox.addLayout(hbox)
		self.setLayout(self.vbox)


class MainWindow(QtGui.QMainWindow):

    	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.mainFrame = MainFrame(QtGui.QFrame(self))

		self.addRuleFrame = addRule_Frame(QtGui.QFrame(self))
		self.delRuleFrame = delRule_Frame(QtGui.QFrame(self))

		self.addFuncFrame = addFunction_Frame(QtGui.QFrame(self))
		self.delFuncFrame = delFunction_Frame(QtGui.QFrame(self))
		self.updateFuncFrame = updateFunction_Frame(QtGui.QFrame(self))

		self.addLocFrame = addLocator_Frame(QtGui.QFrame(self))
		self.updateLocFrame = updateLocator_Frame(QtGui.QFrame(self))
		self.delLocFrame = delLocator_Frame(QtGui.QFrame(self))

		self.addMapFrame = addMap_Frame(QtGui.QFrame(self))
		self.delMapFrame = delMap_Frame(QtGui.QFrame(self))


		self.central_widget = QtGui.QStackedWidget()
       		self.central_widget.addWidget(self.mainFrame)

       		self.central_widget.addWidget(self.addRuleFrame)
       		self.central_widget.addWidget(self.delRuleFrame)

       		self.central_widget.addWidget(self.addFuncFrame)
       		self.central_widget.addWidget(self.updateFuncFrame)
       		self.central_widget.addWidget(self.delFuncFrame)

       		self.central_widget.addWidget(self.addLocFrame)
       		self.central_widget.addWidget(self.updateLocFrame)
       		self.central_widget.addWidget(self.delLocFrame)

       		self.central_widget.addWidget(self.addMapFrame)
       		self.central_widget.addWidget(self.delMapFrame)

		self.central_widget.setCurrentWidget(self.mainFrame)
		self.setCentralWidget(self.central_widget)

		####################
		#Events connections#
		####################
		#Main Frame
		self.mainFrame.addRule.clicked.connect(self.addRules_buttonClicked)
		self.mainFrame.delRule.clicked.connect(self.delRules_buttonClicked)

		self.mainFrame.addSF.clicked.connect(self.addSF_buttonClicked) 
		self.mainFrame.updateSF.clicked.connect(self.updateSF_buttonClicked)  
		self.mainFrame.delSF.clicked.connect(self.delSF_buttonClicked) 

		self.mainFrame.addMap.clicked.connect(self.addSFC_buttonClicked) 
		self.mainFrame.delMap.clicked.connect(self.delSFC_buttonClicked) 


		#Add Rule Frame
		self.addRuleFrame.back.clicked.connect(self.back_buttonClicked) 
		self.addRuleFrame.addRule.clicked.connect(self.addRule_buttonClicked)  
		#Delete Rule Frame
		self.delRuleFrame.back.clicked.connect(self.back_buttonClicked) 
		self.delRuleFrame.delRule.clicked.connect(self.delRule_buttonClicked)  

		#Add Function Frame
		self.addFuncFrame.back.clicked.connect(self.back_buttonClicked)
		self.addFuncFrame.addFunc.clicked.connect(self.addFunc_buttonClicked)
		#Update Function Frame
		self.updateFuncFrame.back.clicked.connect(self.back_buttonClicked)
		self.updateFuncFrame.addLocator.clicked.connect(self.addLocator_buttonClicked)   
		self.updateFuncFrame.updateLocator.clicked.connect(self.updateLocator_buttonClicked)   
		self.updateFuncFrame.delLocator.clicked.connect(self.delLocator_buttonClicked)
		#Delete Function Frame
		self.delFuncFrame.back.clicked.connect(self.back_buttonClicked)
		self.delFuncFrame.delFunc.clicked.connect(self.delFunc_buttonClicked)

		#Add Locator Frame
		self.addLocFrame.back.clicked.connect(self.backToSFUpdate_buttonClicked)
		self.addLocFrame.addLoc.clicked.connect(self.addLoc_buttonClicked)
		self.addLocFrame.combo.currentIndexChanged.connect(self.addLocUpdate_comboEventHandler)
		#Update Locator Frame
		self.updateLocFrame.back.clicked.connect(self.backToSFUpdate_buttonClicked)
		self.updateLocFrame.updateLoc.clicked.connect(self.updateLoc_buttonClicked)
		self.updateLocFrame.combo.currentIndexChanged.connect(self.updateLocUpdate_comboEventHandler)
		#Delete Locator Frame
		self.delLocFrame.back.clicked.connect(self.backToSFUpdate_buttonClicked)

		#Add Map Frame
		self.addMapFrame.resetMap.clicked.connect(self.resetMap_buttonClicked)
		self.addMapFrame.back.clicked.connect(self.back_buttonClicked)
		self.addMapFrame.addMap.clicked.connect(self.addMap_buttonClicked)
		for checkbox in self.addMapFrame.checkBoxList[0]:
			checkbox.clicked.connect(self.checkBoxClicked) 
		#Delete Map Frame
		self.delMapFrame.back.clicked.connect(self.back_buttonClicked)
		self.delMapFrame.delMap.clicked.connect(self.delMap_buttonClicked)
                                                        
		###################
		#Window Parameters#
		###################
		QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10)) 
		self.setWindowIcon(QtGui.QIcon('network.png')) 
		self.setGeometry(300, 300, 300, 200)
		self.setWindowTitle('SFC GUI')
		self.statusBar()



	#********************#
	#*Main Frame FEvents*#
	#********************#
	def addRules_buttonClicked(self):
		self.central_widget.setCurrentWidget(self.addRuleFrame)
		self.statusBar().showMessage("Adding Classification Rules",0)

	def delRules_buttonClicked(self):
		self.central_widget.setCurrentWidget(self.delRuleFrame)
		self.statusBar().showMessage("Deleting Classification Rules",0)

	def addSF_buttonClicked(self):
		self.central_widget.setCurrentWidget(self.addFuncFrame)
		self.statusBar().showMessage("Adding New SF Function",0)

	def updateSF_buttonClicked(self):
		self.central_widget.setCurrentWidget(self.updateFuncFrame)
		self.statusBar().showMessage("Updating an existing SF Function",0)

	def delSF_buttonClicked(self):
		self.central_widget.setCurrentWidget(self.delFuncFrame)
		self.statusBar().showMessage("Deleting an existing SF Function",0)

	def addSFC_buttonClicked(self):
		self.central_widget.setCurrentWidget(self.addMapFrame)
		self.statusBar().showMessage("Adding New SF Map",0)

	def delSFC_buttonClicked(self):
		self.central_widget.setCurrentWidget(self.delMapFrame)
		self.statusBar().showMessage("Deleting an existing SF Map",0)

	#********************#
	#*Other Frame FEvents*#
	#********************#
	def back_buttonClicked(self): 
		self.central_widget.setCurrentWidget(self.mainFrame)
		self.statusBar().showMessage("Welcome Window",0)

	def backToSFUpdate_buttonClicked(self): 
		self.central_widget.setCurrentWidget(self.updateFuncFrame)
		self.statusBar().showMessage("Updating an existing SF Function",0)

	def addLocator_buttonClicked(self):
		self.central_widget.setCurrentWidget(self.addLocFrame)
		self.statusBar().showMessage("Adding locator to an existing SF Function",0)
		self.addLocUpdate_comboEventHandler()

	def updateLocator_buttonClicked(self):
		self.central_widget.setCurrentWidget(self.updateLocFrame)
		self.statusBar().showMessage("Updating an existing SF Function",0)
		self.updateLocUpdate_comboEventHandler()

	def delLocator_buttonClicked(self):
		self.central_widget.setCurrentWidget(self.delLocFrame)
		self.statusBar().showMessage("Deleting locator from an existing SF Function",0)
		self.addLocUpdate_comboEventHandler()
			

	#******************************#
	#*Classification Rules FEvents*#
	#******************************#
	def addRule_buttonClicked(self): #Adding a new rule
		addRule(self)
	def delRule_buttonClicked(self): #Deleting an existing Rule
		delRule(self)

	#***********************#
	#*SF Management FEvents*#
	#***********************#
	def addFunc_buttonClicked(self):
		addFunc(self)

	def delFunc_buttonClicked(self): #Deleting an existing SF Function
		delFunc(self)

	#*******************#
	#*SF Update FEvents*#
	#*******************#
	def addLocUpdate_comboEventHandler(self):
		addLocUpdate(self)

	def updateLocUpdate_comboEventHandler(self):
		updateLocUpdate(self)

	def addLoc_buttonClicked(self): 
		addLoc(self) 

	def updateLoc_buttonClicked(self):
		updateLoc(self)

	def delLoc_buttonClicked(self):
		delLoc(self)

	#****************************#
	#*SF Maps Management FEvents*#
	#****************************#
	def resetMap_buttonClicked(self):
		global count
		count=0
		self.addMapFrame.SFLabel.setText("New SF Map:  ")
		for checkbox in self.addMapFrame.checkBoxList[0]:
			checkbox.setCheckState(0)




	def addMap_buttonClicked(self):
		addMap(self)
		

	def checkBoxClicked(self):
		global count
        	sender = self.sender()
		ltext = str(self.addMapFrame.SFLabel.text())

		if sender.isChecked() is True:
			if(count==0):
				self.addMapFrame.SFLabel.setText("New SF Map:  " + "{" + sender.text() + "}")

			else:
				ltext = ltext.rstrip('}')
				self.addMapFrame.SFLabel.setText(ltext + ", " + sender.text() + "}")

			count+=1
		else:
			count-=1
			if(count==0):
				self.addMapFrame.SFLabel.setText("New SF Map:  ")
			else:
 				ltext = ltext.replace(", " + sender.text(), "")
 				ltext = ltext.replace(sender.text() + ", ", "")
				self.addMapFrame.SFLabel.setText(ltext)

def main():
    
	app = QtGui.QApplication(sys.argv)
   	mainw = MainWindow()
   	mainw.show()
   	sys.exit(app.exec_())
	db.close()


if __name__ == '__main__':
    	main()