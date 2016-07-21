#!/usr/bin/python



import sys
import csv
from collections import defaultdict

#Open CSV file
try:
	rackCSVreader = csv.reader(open(sys.argv[1],'rU'),skipinitialspace = True)
except(IOError):
	print("Inventory CSV file must be supplied in order to proceed.") 
	sys.exit(0)
try:
	dtCSVreader = csv.reader(open("DeviceTypes",'rU'),skipinitialspace=True)
except(IOError):
	print("Device Types csv not found, this script uses the csv file 'DeviceTypes' to create RackTables objects.") 
	sys.exit(0)

deviceDictFull = {}
rowCounter = 0
deviceName = []
rowNo = []
podNo = []
cabNo = []
uLo = []
uHi = []
deviceType = []
primaryPool = []
primaryGroup = []
fullCSV = []
for row in dtCSVreader:
	try:
		deviceDictFull.setdefault(row[0],[]).append(row[1])
			
	except(IndexError):
		pass
for row in rackCSVreader:
	try:
		fullCSV.append(row)
		deviceName.append(row[0].replace("'",""))
		rowNo.append(row[1:2][0].replace("'",""))
		podNo.append(row[2:3][0].replace("'",""))
		cabNo.append(row[3:4][0].replace("'",""))
		uLo.append((row[4:5][0].replace("'","")))
		uHi.append((row[5:6][0].replace("'","")))
		deviceType.append(row[6:7][0].replace("'",""))
		primaryPool.append(row[7:8][0].replace("'","").replace('"',"").replace("ppool:","").strip("{} "))
		fPGroup=((str(row[8:][0:])).replace("{pgroup:","").rstrip('"}\\\'[]')).lstrip("['").replace('"','').replace("'",'')
		primaryGroup.append(fPGroup)
		rowCounter+=1
	except(IndexError):
		pass
#print(deviceDictFull)
print("RACK;MIT;MGHPCC;"+str("r"+rowNo[0].strip()+"-p"+podNo[0].strip()).upper() + ";" +"C"+cabNo[0].strip())
for i in range(rowCounter):
	try:	
		uRange= str(range((int(uLo[i])),(int(uHi[i]))+1)).strip("[]").replace(" ","")
		fLoc=str("r"+rowNo[i].strip()+"-p"+podNo[i].strip()+"-c"+cabNo[i]).upper()
		#print(deviceName[i]+ "loc="+fLoc+ " Unumbers="+uRange+" DEVICETYPE="+deviceType[i]+" PrimaryPool="+primaryPool[i]+" primaryGroup="+primaryGroup[i])
		#template="{deviceName:40}|{Pool:20}|{deviceType:30}"
		#print template.format(deviceName=deviceName[i],deviceType=deviceType[i],Pool=primaryPool[i])
		print("OBJECT;"+ str(deviceDictFull[deviceType[i].strip()]).lstrip("['").rstrip("']").upper() +";"+ deviceName[i].strip()+"-"+primaryPool[i].strip()+ ";" +(deviceType[i].strip())+ ";"+deviceName[i].strip()+"-"+primaryPool[i].strip())
		print("OBJECTTAG;"+str(deviceName[i].strip()+"-"+primaryPool[i].strip()+ ";" +primaryPool[i].strip()))
		print("OBJECTATTRIBUTE;"+str(deviceName[i].strip()+"-"+primaryPool[i].strip()+ ";" + "COMMENT;"+ "Primary Pool: " + primaryPool[i].strip() + "    Primary Group: " + primaryGroup[i]))
		print("RACKASSIGNMENT;"+deviceName[i].strip()+"-"+primaryPool[i].strip()+";"+"C"+cabNo[0].strip()+";"+uRange)+";"+((len(range(int(uLo[i]),int(uHi[i]))))*"fib,"+"fib")
	except(ValueError):
		pass		
	
