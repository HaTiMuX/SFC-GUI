import MySQLdb

def LocalLocators_Update(SF, Locator, operation):
	error=0
	#Setting connexion to local DB to read locators
	db = MySQLdb.connect("localhost","sfcuser","sfc123","SFC")
	cursor = db.cursor()

	#Reading locators of the existing SF Nodes
	try:
		sql = "SELECT SF, Locator1 FROM Locators"
		cursor.execute(sql)
		results = cursor.fetchall()
	except:

		error = 1 
		print "Error: unable to read data from the local server (locators of the existing SF Nodes)!"
	db.close()

	#Updating LocalLocators of the new Added Node
	if operation==1:
		print "Adding information to the LocalLocators database of the new added Node:"
		try:
			remoteDB = MySQLdb.connect(str(Locator),"sfcuser","sfc123","SFC")
			remoteCursor = remoteDB.cursor()
			for result in results:
				remoteSF = result[0]
				Loc = result[1]
				sql1 = "INSERT INTO LocalLocators (SF, Locator) VALUES ('%s','%s')" % (remoteSF, Loc)
				try:
					remoteCursor.execute(sql1)
				except:
					remoteDB.rollback()
					error=1
					break
		except:
			error=1
			print "Error: connecting to remote server %s failed! (Local locators update failed)" % Locator

		if error==0:
			remoteDB.commit()
			print "Adding data to remote Node %s: Success!" % Locator
		else:
			print "Error: unable to add data to remote Node %s!" % Locator

		remoteDB.close()

	#Updating LocalLocators of the new Added Node
	if operation==3:
		print "Deleting information in LocalLocators database of the removed Node:"
		try:
			remoteDB = MySQLdb.connect(str(Locator),"sfcuser","sfc123","SFC")
			remoteCursor = remoteDB.cursor()
			sql1 = "DELETE FROM LocalLocators"
			try:
				remoteCursor.execute(sql1)
			except:
				remoteDB.rollback()
				error=1
				break
		except:
			error=1
			print "Error: connecting to remote server %s failed! (Local locators update failed)" % Locator

		if error==0:
			remoteDB.commit()
			print "Deleting data from the remote Node %s: Success!" % Locator
		else:
			print "Error: unable to delete data from the remote Node %s!" % Locator

		remoteDB.close()


	#Preparing Query
	if operation==1:
		sql = "INSERT INTO LocalLocators (SF, Locator) VALUES ('%s', '%s')" % (SF, Locator)
	elif operation==2:
		sql = "UPDATE LocalLocators SET Locator = '%s' WHERE SF='%s'" % (Locator, SF)
	else:
		sql = "DELETE FROM LocalLocators WHERE SF='%s'" % (SF)

	#Updating LocalLocators Database of the Ingress Node 
	try:
		classifierDB = MySQLdb.connect("10.1.0.99","sfcuser","sfc123","SFC")
		classifierCursor = classifierDB.cursor()

		classifierCursor.execute(sql)
		classifierDB.commit()

		if operation==1:
			print "Adding locator to the Ingress Node: Success!"
		elif operation==2:
			print "Updating locator in the Ingress Node: Success!"
		else:
			print "Deleteing locator from the Ingress Node: Success!"

	except:
		classifierDB.rollback()
		error = 1
		if operation==1:
			print "Error: Adding locator to the Ingress Node: Failed!"
		elif operation==2:
			print "Error: Updating locator in the Ingress Node: Failed!"
		else:
			print "Error: Deleteing locator from the Ingress Node: Failed!"
	classifierDB.close()


	#Updating LocalLocators Database of the SF Nodes
	if error==0:
		for result in results:
			IP = result[1]
			try:
				remoteDB = MySQLdb.connect(IP,"sfcuser","sfc123","SFC")
				remoteCursor = remoteDB.cursor()
				try:
					remoteCursor.execute(sql)
					remoteDB.commit()
					if operation==1:
						print "Adding locator to the remote Node %s: Success!" % IP
					elif operation==2:
						print "Updating locator in the remote Node %s: Success!" % IP
					else:
						print "Deleteing locator from the remote Node %s: Success!" % IP
				except:
					error=1
					remoteDB.rollback()
					if operation==1:
						print "Error: unable to add data to the remote Node %s!" % IP
					elif operation==2:
						print "Error: unable to update data in the remote Node %s!" % IP
					else:
						print "Error: unable to delete data from the remote Node %s!" % IP
				remoteDB.close()
			except:
				error=1
				print "Error: connecting to remote server %s failed! (Local locators add failed)" % IP

			if IP==Locator:
				continue

			if error==1:
				break

	return error

def addMap_Update(Index, rowMap):
	error=0
	SFMap = rowMap.lstrip('{')
	SFMap = SFMap.rstrip('}')
	SF_Map = SFMap.split(', ')
	print "New SF Map to add: " + str(SF_Map) + "\n"

	#Adding configuration to the Ingress Node
	try:
		remoteDB = MySQLdb.connect("10.1.0.99","sfcuser","sfc123","SFC") #IP address of the Ingress Node
		remoteCursor = remoteDB.cursor()
		try:
			#Inserting new entry 
			sql = "INSERT INTO SFCRoutingTable (SF_MAP_INDEX, NextSF, Encap) VALUES (%d,'%s', NULL)" % (Index, SF_Map[0])
			remoteCursor.execute(sql)
			remoteDB.commit()
			print "Adding data to the Ingress Node: Success!"
		except:
			error=1
			remoteDB.rollback()
			print "Error: unable to add data to the Ingress Node!"
		remoteDB.close()
	except:
		error=1
		print "Error: connecting to Ingress Node failed! (SFCRoutingTable add update failed)"

	print ""


	#Setting connexion to local DB to read locators
	db = MySQLdb.connect("localhost","sfcuser","sfc123","SFC")
	cursor = db.cursor()

	#Adding configuration to the Involved Nodes
	for SF in SF_Map:
		print "Adding configuration to the SF Node embedding Function: %s" % SF 

		#Preparing new configuration entry
		if(SF!=SF_Map[len(SF_Map)-1]):
			sql = "INSERT INTO SFCRoutingTable (SF_MAP_INDEX, NextSF, Encap) VALUES ('%d','%s', NULL)" % (Index, SF_Map[SF_Map.index(SF) + 1])
		else: #Last node in the Map
			sql = "INSERT INTO SFCRoutingTable (SF_MAP_INDEX, NextSF, Encap) VALUES ('%d', NULL, NULL)" % (Index)

		#Reading the Locator of the next SF
		try:
			sql1 = "SELECT Locator1 FROM Locators WHERE SF = '%s'" % (SF)
			cursor.execute(sql1)
			result = cursor.fetchone()
			IP = result[0] #Converting from tuple to normal string: SF node IP
			print "Node Locator = " + IP
		except:
			error=1
			print "Error: unable to fecth data (IP address)"

		#Adding row to the remote table 'SFCRoutingTable' of the SF Node 
		try:
			remoteDB = MySQLdb.connect(IP, "sfcuser", "sfc123", "SFC")
			remoteCursor = remoteDB.cursor()
			try:
				remoteCursor.execute(sql)
				remoteDB.commit()
				print "Adding data to remote Node %s: Success!" % IP
			except:
				error=1
				remoteDB.rollback()
				print "Error: unable to add data to remote Node %s!" % IP
			remoteDB.close()
		except:
			error=1
			print "Error: connecting to remote server %s failed! (SFCRoutingTable add update failed)" % IP

		print ""

	db.close()
	return error


def delMap_Update(Index, rowMap):
	error=0
	SFMap = rowMap.lstrip('{')
	SFMap = SFMap.rstrip('}')
	SF_Map = SFMap.split(', ')
	print "  Updating SFC Routing Tables of the involved Nodes!"

	#Deleting row from the 'SFCRoutingTable' of the Ingress Node
	try:
		remoteDB = MySQLdb.connect("10.1.0.99","sfcuser","sfc123","SFC") #IP address of the Ingress Node
		remoteCursor = remoteDB.cursor()
		sql = "DELETE FROM SFCRoutingTable WHERE SF_Map_Index=%d" % Index
		try:
			remoteCursor.execute(sql)
			remoteDB.commit()
			print "\tDeleting data from the Ingress Node: Success!"
		except:
			error=1
			remoteDB.rollback()
			print "\tError: unable to delete data from the Ingress Node!"
		remoteDB.close()
	except:
		error=1
		print "\tError: connecting to the Ingress Node failed! (SFCRoutingTable delete update failed)"
	

	#Setting connexion to local DB to read locators
	db = MySQLdb.connect("localhost","sfcuser","sfc123","SFC")
	cursor = db.cursor()

	#Deleting row from the 'SFCRoutingTable' of each involved SF Node 
	for SF in SF_Map:
		#Reading the Locator of the SF involved in the current Map to remove
		try:
			sql = "SELECT Locator1 FROM Locators WHERE SF = '%s'" % (SF)
			cursor.execute(sql)
			result = cursor.fetchone()
			IP = result[0] 
			print "\tReading Locator of SF Function %s: Success!" % SF
		except:
			error=1
			print "\tError: Reading Locator of SF Function %s failed!" % SF

		try:
			sql = "DELETE FROM SFCRoutingTable WHERE SF_Map_Index=%d" % Index
			remoteDB = MySQLdb.connect(IP,"sfcuser","sfc123","SFC")
			remoteCursor = remoteDB.cursor()
			try:
				remoteCursor.execute(sql)
				remoteDB.commit()
				print "\tDeleting data from remote Node %s: Success!" % IP
			except:
				error=1
				remoteDB.rollback()
				print "\tError: unable to remove data from remote server %d!" % IP
			remoteDB.close()
		except:
			error=1
			print "\tError: connecting to remote server %s failed!" % IP

	db.close()
	return error