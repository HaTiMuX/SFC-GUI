import re
from PyQt4 import QtGui

#Adding a new rule
def addRule(self, db, cursor):
	self.addRuleFrame.error.setText("")
	SIP = self.addRuleFrame.rules_SIP_le.text()
	DIP = self.addRuleFrame.rules_DIP_le.text()
	proto = self.addRuleFrame.protoCombo.currentText()
	sport = self.addRuleFrame.rules_sport_le.text()
	dport = self.addRuleFrame.rules_dport_le.text()
	prio  = self.addRuleFrame.rules_prio_le.text()
	mark  = self.addRuleFrame.markCombo.currentText()
	IPExp = "^((25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)$"
	portExp = "^([0-5]([0-9]?){4}|6[0-4]?([0-9]?){3}|65[0-4]?([0-9]?){2}|655[0-2]?[0-9]?|6553[0-5]?)$"
	prioExp = "^[1-9][0-9]?$"


	
	if(self.addRuleFrame.markCombo.count()==0):
		if((re.search(prioExp, prio) is not None) or prio==""):
			if(SIP=="" and  DIP=="" and sport=="" and dport==""):
				self.addRuleFrame.error.setText("Fill at least one criterian for the rule!")

			elif ((re.search(IPExp, DIP) is None) and DIP!="") or ((re.search(IPExp, SIP) is None) and SIP!=""):
				self.addRuleFrame.error.setText("Type a valid IP address!")
		
			elif ((re.search(portExp, dport) is None) and dport!="") or ((re.search(portExp, sport) is None) and sport!=""):
				self.addRuleFrame.error.setText("Type a valid Port Number!")

			else:
				reply = QtGui.QMessageBox.question(self, 'Confirmation', "Confirm add rule operation?",
					QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

				if reply == QtGui.QMessageBox.Yes:
					if prio=="":
						prio=99
				try:
					classifierDB = MySQLdb.connect("10.1.0.99","sfcuser","sfc123","SFC")
					classifierCursor = classifierDB.cursor()

					try:
						sql = "INSERT INTO ClassRules (SF_MAP_INDEX, SIP, DIP, Protocol, SPort, DPort) VALUES ('%d','%s', '%s', '%s', '%d', '%d', '%d')" % (int(mark), SIP, DIP, proto, int(sport), int(dport), int(prio))
						classifierCursor.execute(sql)
				   		classifierDB.commit()

					except:
				  		classifierDB.rollback()
						print "Error inserting New Rule"

					classifierDB.close()
				except:
					print "Problem Connection to the classifier DB"
					classifierDB.close()
		else:
			self.addRuleFrame.error.setText("Type a valid Priority for the rule!")
	else:
		self.addRuleFrame.error.setText("No mark available!")

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