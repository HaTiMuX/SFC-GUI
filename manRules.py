

#Adding a new rule
def addRule(self):
	ruleIP = self.addRuleFrame.rules_IP_le.text()
	ruleport = self.addRuleFrame.rules_port_le.text()
	mark  = int(self.addRuleFrame.combo.currentText())
	IPexp = "^((25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)$"
	portExp = "^[0-9][0-9]?[0-9]?[0-9]?$"

	
	if(ruleIP=="" and ruleport==""):
		self.addRuleFrame.error.setText("fill at least one field for the rule!")

	elif (re.search(IPexp, ruleIP) is None) and ruleport=="":
		self.addRuleFrame.error.setText("Type a valid IP address!")
		
	elif (re.search(portExp, ruleport) is None) and ruleIP=="":
		self.addRuleFrame.error.setText("Type a valid Port Number!")

	elif (re.search(IPexp, ruleIP) is None) and (re.search(portExp, ruleport) is None):
		self.addRuleFrame.error.setText("Type valid Information!")

	else:
		reply = QtGui.QMessageBox.question(self, 'Confirmation', "Confirm add rule operation?",
			QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

		if reply == QtGui.QMessageBox.Yes:
			try:
				sql = "INSERT INTO Rules (SF_MAP_INDEX, IP, port) VALUES ('%d','%s', '%s')" % (mark, ruleIP, ruleport)
				cursor.execute(sql)
		   		db.commit()

			except:
		  		db.rollback()
				print "Error inserting New Rule"


#Deleting an existing Rule
def delRule(self): 
	if self.delRuleFrame.combo.count() != 0:
		curtext = self.delRuleFrame.combo.currentText()
		mark = curtext.split(':')
		msg = "Are you sure to delete the selected Entry?"
		reply = QtGui.QMessageBox.question(self, 'Confirmation', msg , QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
		'''
		if reply == QtGui.QMessageBox.Yes:
			sql = "DELETE FROM Rules WHERE SF_MAP_INDEX='%s'" % SF[0]
			try:	
				cursor.execute(sql)
		   		db.commit()
				index = self.delFuncFrame.combo.currentIndex()	
				self.delFuncFrame.combo.removeItem(index)
				self.updateFuncFrame.combo.removeItem(index)


			except:
  				db.rollback()
				print "Error Deleting (Rule)"
		'''		
	else:
		QtGui.QMessageBox.critical(self, 'Error', "No Entry remaining!" , QtGui.QMessageBox.Ok)
