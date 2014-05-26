from PyQt4 import QtGui
from Functions import Update_Del

#Deleting an existing SF Map
def delMap(self, db, cursor, DSCP): 
	if self.delMapFrame.combo.count() != 0:
		curtext = str(self.delMapFrame.combo.currentText()) #Converting to str to use lstrip 

		text = curtext.split(" ")
		mapIndex = int(text[0])

		SFMap = curtext.lstrip(str(mapIndex) + " ") #Strip the Map index 
		SF = curtext.split(' ')

		msg = "Are you sure to delete the selected Entry?"
		reply = QtGui.QMessageBox.question(self, 'Confirmation', msg , QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

		if reply == QtGui.QMessageBox.Yes:
			print "Map to delete: " + curtext
			DSCP.append(mapIndex) #Updating DSCP available values
			sql = "DELETE FROM SFMaps WHERE SF_Map_Index=%d" % mapIndex
			cb_index = self.delMapFrame.combo.currentIndex()	
			self.delMapFrame.combo.removeItem(cb_index)

			try:	
				cursor.execute(sql)
	   			db.commit()
			except:
  				db.rollback()
				print "Error Deleting SF Map from the local repositry"

			#Updating SFC Routing Tables of the Nodes involved in the deleted SF Map
			Update_Del(mapIndex, SFMap, db, cursor)

	else:
		QtGui.QMessageBox.critical(self, 'Error', "No Entry remaining!" , QtGui.QMessageBox.Ok)
