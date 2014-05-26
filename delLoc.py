import re

def delLoc(self):
		IPExp = "^((25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)$"
		emptyExp = "^( ?){15}$"
		self.delLocFrame.success_msg.setText("")
		error = None

		delLoc = self.delLocFrame.loc.text()

		IPCond= re.search(IPExp, delLoc) is not None
		emptyCond = re.search(emptyExp, delLoc) is not None 

		if (IPCond1 is False) and (emptyCond1 is False):
			error = "Type valid IP address for the locator to remove"

		else:
			sql = "SELECT SF from Locators"

		if error is None:
			self.updateLocFrame.msg.setText("")
			msg = "Are you sure to remove the typed locator?"
			reply = QtGui.QMessageBox.question(self, 'Confirmation', msg , QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

			if reply == QtGui.QMessageBox.Yes:
				try:
					cursor.execute(sql)
	   				results = cursor.fetchall()
				except:
					print "Error reading SF Funcitons"