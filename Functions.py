###########
#Functions#
###########

def Update_Add(Index, rowMap):
	SFMap = rowMap.lstrip('{')
	SFMap = SFMap.rstrip('}')
	SF_Map = SFMap.split(', ')
	print "New SF Map to add: " + str(SF_Map) + "\n"

	#Adding configuration to the Ingress Node
	SF = SF_Map[0]
	try:
		#Reading locator of the first SF Node 
		sql1 = "SELECT Locator1 FROM Locators WHERE SF = '%s'" % (SF)
		cursor.execute(sql1)
		result = cursor.fetchone()
		IPx = result[0]
				
	except:
		print "Error: unable to read data from the local server!"


	try:
		remoteDB = MySQLdb.connect("10.1.0.99","sfcuser","sfc123","SFC") #IP address of the Ingress Node
		remoteCursor = remoteDB.cursor()
		try:
			#Inserting new entry 
			sql = "INSERT INTO SFCRoutingTable (SF_MAP_INDEX, NextSFHop, Encap) VALUES (%d,'%s', NULL)" % (Index,IPx)
			remoteCursor.execute(sql)
			remoteDB.commit()
			print "Adding data to the Ingress Node: Success!"
		except:
			print sql
			remoteDB.rollback()
			print "Error: unable to add data to the Ingress Node!"
			remoteDB.close()

		remoteDB.close()
	except:
		print "Error: connecting to remote server %s failed! (SFCRoutingTable add update failed)" % IP

	print ""


	#Adding configuration to the Involved Nodes
	for SF in SF_Map:
		print "Adding configuration to the SF Node embedding Function: %s" % SF 
		#Looking for the Locator of the next SF
		if(SF!=SF_Map[len(SF_Map)-1]):
			try:
				sql1 = "SELECT Locator1 FROM Locators WHERE sf = '%s'" % (SF)
				sql2 = "SELECT Locator1 FROM Locators WHERE sf = '%s'" % SF_Map[SF_Map.index(SF) + 1] 
				cursor.execute(sql1)
			   	result = cursor.fetchone()
				IP = result[0] #Converting from tuple to normal string: SF node IP
				cursor.execute(sql2)
			   	result = cursor.fetchone()
				IPx = result[0] #Next SF Node IP
				print "Node IP = " + IP
			  	print "Next SF Hop @IP = " + IPx
				sql = "INSERT INTO SFCRoutingTable (SF_MAP_INDEX, NextSFHop, Encap) VALUES ('%d','%s', NULL)" % (Index,IPx)

			except:
				print "Error: unable to fecth data (IP addresses)"

		#Last node in the Map
		else: 
			try:
				sql1 = "SELECT Locator1 FROM Locators WHERE sf = '%s'" % (SF)
				cursor.execute(sql1)
			   	result = cursor.fetchone()
				IP = result[0] #SF node IP
				print "The Node is the last Node in the SF Map"
				sql = "INSERT INTO SFCRoutingTable (SF_MAP_INDEX, NextSFHop, Encap) VALUES ('%d', NULL, NULL)" % Index
			except:
				print "Error: unable to fecth data (IP addresses)"

		#Adding row to the remote table 'SFCRoutingTable' of the SF Node 
		try:
			remoteDB = MySQLdb.connect(IP,"sfcuser","sfc123","SFC")
			remoteCursor = remoteDB.cursor()
			try:
				print sql
				remoteCursor.execute(sql)
				remoteDB.commit()
				print "Adding data to remote Node %s: Success!" % IP
			except:
				remoteDB.rollback()
				print "Error: unable to add data to remote Node %s!" % IP
				remoteDB.close()

			remoteDB.close()
		except:
			print "Error: connecting to remote server %s failed! (SFCRoutingTable add update failed)" % IP

		print ""


def Update_Del(Index, rowMap):
	SFMap = rowMap.lstrip('{')
	SFMap = SFMap.rstrip('}')
	SF_Map = SFMap.split(', ')

	#Deleting row from the 'SFCRoutingTable' of the Ingress Node
	try:
		remoteDB = MySQLdb.connect("10.1.0.99","sfcuser","sfc123","SFC") #IP address of the Ingress Node
		remoteCursor = remoteDB.cursor()
		sql = "DELETE FROM SFCRoutingTable WHERE SF_Map_Index=%d" % Index
		try:
			print sql
			remoteCursor.execute(sql)
			remoteDB.commit()
			print "Deleting data from the Ingress Node: Success!"
		except:
			remoteDB.rollback()
			print "Error: unable to delete data from the Ingress Node!"
			remoteDB.close()

		remoteDB.close()
	except:
		print "Error: connecting to the Ingress Node failed! (SFCRoutingTable delete update failed)"
	

	#Deleting row from the remote 'SFCRoutingTable' of each SF Node 
	for SF in SF_Map:
		try:
			sql = "SELECT Locator1 FROM Locators WHERE SF = '%s'" % (SF)
			cursor.execute(sql)
			result = cursor.fetchone()
			IP = result[0] #SF node IP
		except:
			print "Error: unable to fecth data (IP addresses for remove)"

		try:
			sql = "DELETE FROM SFCRoutingTable WHERE SF_Map_Index=%d" % Index
			remoteDB = MySQLdb.connect(IP,"sfcuser","sfc123","SFC")
			remoteCursor = remoteDB.cursor()
			try:
				print sql
				remoteCursor.execute(sql)
				remoteDB.commit()
				print "Removing data from remote Node %s: Success!" % IP
			except:
				remoteDB.rollback()
				print "Error: unable to remove data from remote server %d!" % IP
				remoteDB.close()

			remoteDB.close()
		except:
			print "Error: connecting to remote server %s failed!" % IP