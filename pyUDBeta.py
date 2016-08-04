#!/usr/bin/python



import sys
import csv
from collections import defaultdict

#Open CSV file
try:
	rackCSVreader = csv.reader(open(sys.argv[1],'rU'),quotechar="'",delimiter=',',skipinitialspace = True)
except(IOError):
	print("Inventory CSV file must be supplied in order to proceed.") 
	sys.exit(0)
try:
	rackCSVreader2 = csv.reader(open(sys.argv[2],'rU'),quotechar="'",delimiter=',',skipinitialspace = True)
except(IOError):
	print("Inventory CSV file must be supplied in order to proceed.") 
	sys.exit(0)
#try:
#	dtCSVreader = csv.reader(open("DeviceTypes",'rU'),skipinitialspace=True)
#except(IOError):
#	print("Device Types csv not found, this script uses the csv file 'DeviceTypes' to create RackTables objects.") 
#	sys.exit(0)

#deviceDictFull = {}
orig_stdout = sys.stdout
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
objectType=[]
 print(list(set(rackCSVreader) - set(rackCSVreader)))
#for row in dtCSVreader:
#	try:
#		deviceDictFull.setdefault(row[0],[]).append(row[1])
			
#	except(IndexError):
#		pass
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
		fPpool=((str(row[7:8][0]).split(",",1)[0])).replace('{ppool: "',"").rstrip('"}')
		primaryPool.append(fPpool)
		#primaryPool.append(row[7:8][0].replace("'","").replace('"',"").replace("ppool:","").strip("{} "))
		#fPGroup=((str(row[8:][0:])).replace("{pgroup:","").rstrip('"}\\\'[]')).lstrip("['").replace('"','').replace("'",'')
		fPGroup=((str(row[7:8][0]).split(",",1)[1])).replace('{pgroup: "',"").rstrip('"} ')		
		primaryGroup.append(fPGroup)
		objectType.append(row[8:9][0])
		rowCounter+=1
	except(IndexError):
		pass

#print(primaryGroup)

locSTR=(str("r"+rowNo[0].strip()+"-p"+podNo[0].strip()).upper() + "-" +"C"+cabNo[0].strip())
outFile = ("UPDATED" +"-initialize-objects-csv.txt")
f = file(outFile, 'w')
sys.stdout = f


#cabinetName= str("r"+rowNo[0].strip()+"p"+podNo[0].strip()).lower()+"c"+cabNo[0].strip()

rackName=str("r"+rowNo[0].strip()+"-p"+podNo[0].strip()).upper()
cabinetName = "C"+cabNo[0].strip()
#print("RACK;MIT;MGHPCC;"+rackName+";"+cabinetName)
for i in range(rowCounter):
	try:	
		
		#print("OBJECT;"+ str(objectType[i]).upper()+";"+ deviceName[i].strip()+"-"+primaryPool[i].strip()+ ";" +(deviceType[i].strip())+ ";"+deviceName[i].strip()+"-"+primaryPool[i].strip())
		#print("OBJECTTAG;"+str(deviceName[i].strip()+"-"+primaryPool[i].strip()+ ";" +primaryPool[i].strip()))
		#print(primaryPool[i].strip())
	except(ValueError):
		pass
	
outFile = ("UPDATED"+"-update-csv.txt")
g = file(outFile, 'w')
sys.stdout = g

for i in range(rowCounter):
	try:	
		rackName=str("r"+rowNo[i].strip()+"-p"+podNo[i].strip()).upper()
		cabinetName = "C"+cabNo[i].strip()
		#print("RACK;MIT;MGHPCC;"+rackName+";"+cabinetName)
		uRange= str(range((int(uLo[i])),(int(uHi[i]))+1)).strip("[]").replace(" ","")
		fLoc=str("r"+rowNo[i].strip()+"-p"+podNo[i].strip()+"-c"+cabNo[i]).upper()
		#print("DEBUG" + deviceName[i]+ "loc="+fLoc+ " Unumbers="+uRange+" DEVICETYPE="+deviceType[i]+" PrimaryPool="+primaryPool[i]+" primaryGroup="+primaryGroup[i])
		#template="{deviceName:40}|{Pool:20}|{deviceType:30}"
		#print template.format(deviceName=deviceName[i],deviceType=deviceType[i],Pool=primaryPool[i])
		
		#print("OBJECTATTRIBUTE;"+str(deviceName[i].strip()+"-"+primaryPool[i].strip()+ ";" + "COMMENT;"+ "Primary Pool: " + primaryPool[i] + "    Primary Group: " + primaryGroup[i]))
		#print("RACKASSIGNMENT;"+deviceName[i].strip()+"-"+primaryPool[i].strip()+";"+cabinetName+";"+uRange)+";"+((len(range(int(uLo[i]),int(uHi[i]))))*"fib,"+"fib;" + rackName)
	except(ValueError):
		pass	

sys.stdout = orig_stdout
f.close()	
