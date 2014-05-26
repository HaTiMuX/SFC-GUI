from PyQt4 import QtGui


def addMap_buttonClicked(self):
	if(count!=0):
		index_text = self.addMapFrame.index_le.text()
		DSCPexp = "^([1-9]|[1-5][0-9]|6[0-3])$"
		if(index_text==""):
			try:
				#Preparing the new SF Map
				index = DSCP[0]
				DSCP.remove(DSCP[0]) #Updating DSCP available values
				Map = str(self.addMapFrame.SFLabel.text()).split('{') #Cant split using space 
				newSFMap = "{" + Map[1]

				#Adding new SF Map on confirmation
				reply = QtGui.QMessageBox.question(self, 'Message',
				"Do you really want to add this new SF Map?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

				if reply == QtGui.QMessageBox.Yes:
					sql = "INSERT INTO SFMaps (SF_MAP_INDEX, SFMap) VALUES (%d, '%s')" % (index, newSFMap)
					print sql
					try:	
						cursor.execute(sql)
				   		db.commit()
					except:
				  		db.rollback()
						print "Error Adding new SF Map"

					self.delMapFrame.combo.addItem(str(index) + " " + newSFMap)

					#Updating SFC Routing Tables of the Nodes involved in the new SF Map
					Update_Add(index, newSFMap)
			except:
				QtGui.QMessageBox.critical(self, 'Error', "No DSCP value remaining!" , QtGui.QMessageBox.Ok)


		elif re.search(DSCPexp, index_text) is None:
			self.addMapFrame.msg.setText("Type a valid\nDSCP value!")

		else:
			self.addMapFrame.msg.setText("")
			index = int(index_text) #Converting the typed number in the LineEdit to Integer
			Map = str(self.addMapFrame.SFLabel.text()).split('{') #Cant split using space 
			newSFMap = "{" + Map[1]

			#Checking if the SF_Map_index already exists
			sql = "SELECT SF_MAP_INDEX FROM SFMaps WHERE SF_MAP_INDEX=%d" % int(index)
			try:	
				cursor.execute(sql)
	   			result = cursor.fetchone()

				if result is None:
					DSCP.remove(index) #Updating DSCP available values
					#Adding new SF Map on confirmation
					reply = QtGui.QMessageBox.question(self, 'Message',
					"Do you really want to add this new SF Map?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

					if reply == QtGui.QMessageBox.Yes:
						sql = "INSERT INTO SFMaps (SF_MAP_INDEX, SFMap) VALUES (%d, '%s')" % (index, newSFMap)
						try:	
							cursor.execute(sql)
				   			db.commit()
						except:
				  			db.rollback()
							print "Error Adding new SF Map"

						self.delMapFrame.combo.addItem(str(index) + " " + newSFMap)

						#Updating SFC Routing Tables of the Nodes involved in the new SF Map
						Update_Add(index, newSFMap)

				else:
					#Printing Error: Index already exists
					self.addMapFrame.msg.setText("Index already exists!")
					print "SF_Map_Index already exists!! Try again."
			except:
				print "Error While Testing if the typed SF_Map_Index already exists!!"


	else:
		QtGui.QMessageBox.critical(self, 'Error', "No SF Function selected!" , QtGui.QMessageBox.Ok)