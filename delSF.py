from PyQt4 import QtGui

#Deleting an existing SF Function
def delFunc(self, db, cursor, DSCP): 
	if self.delFuncFrame.combo.count() != 0:
		curtext = self.delFuncFrame.combo.currentText()
		SF = curtext.split(' ')
		removedSF = SF[0]
		indexesList = []
		print "SF Map to remove: " + removedSF + "\n"

		msg = "Are you sure to delete the selected Entry?"
		reply = QtGui.QMessageBox.question(self, 'Confirmation', msg , QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

		if reply == QtGui.QMessageBox.Yes:
			try:	

				#Updating the list of availble SF functions (addMapFrame
				cb_index = self.addMapFrame.checkBoxList[1].index(removedSF) 
				self.addMapFrame.checkBoxList[0].pop(cb_index)
				self.addMapFrame.checkBoxList[1].pop(cb_index)
				self.addMapFrame.grid.itemAt(cb_index).widget().deleteLater()
				self.addMapFrame.SFCheckListDisplay()

				#Updating the list of availble SF functions to delete "delFuncFrame"
				index = self.delFuncFrame.combo.currentIndex()	
				self.delFuncFrame.combo.removeItem(index)

				#Updating the list of "updateLocFrame"
				self.updateLocFrame.combo.removeItem(index)

				#Updating the list of "addLocFrame"
				self.addLocFrame.combo.removeItem(index)

				#Removing associeted SFMaps
				sql = "SELECT SF_MAP_INDEX, SFMap FROM SFMaps";
				try:	
					cursor.execute(sql)
					results = cursor.fetchall()

					for result in results:
						index = int(result[0])
						rowMap = result[1]
						SFMap = rowMap.lstrip('{')
						SFMap = SFMap.rstrip('}')
						SF_Map = SFMap.split(', ')

						for SF in SF_Map:
							if SF==removedSF: 
								#The SFMap is associated with the removed SF function
								#Deleting the associated SF Map and applying necessary updates
								print "Deleting associated SF Map: %d %s" % (index, rowMap)

								#Updating DSCP available values
								DSCP.append(index) 

								#Updating List of availble SF Maps
								cb_index = self.delMapFrame.SFMapIndexesList.index(index) #getting index of the current map to remove
								self.delMapFrame.SFMapIndexesList.pop(cb_index)
								self.delMapFrame.combo.removeItem(cb_index)

								#Updating SFMaps database
								sql = "DELETE FROM SFMaps WHERE SF_Map_Index=%d" % index
								try:	
									cursor.execute(sql)
					   				db.commit()
								except:
				  					db.rollback()
									print "Error Deleting SF Map from the local repositry"

								#Updating SFC Routing Tables of the Nodes involved in the deleted SF Map
								Update_Del(index, rowMap, db, cursor)
								break;

				except:
					print "Error removing associeted SFMaps!" 


				#Updating SF Locators Database (Deleting the selected SF Function)
				sql = "DELETE FROM Locators WHERE SF='%s'" % removedSF
				print sql
				cursor.execute(sql)
		   		db.commit()


			except:
  				db.rollback()
				print "Error Deleting SF Function"

	else:
		QtGui.QMessageBox.critical(self, 'Error', "No Entry remaining!" , QtGui.QMessageBox.Ok)
