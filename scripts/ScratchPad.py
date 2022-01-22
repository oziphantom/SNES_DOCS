#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 

start = state.currentAddress
seasons = ["Spring","Summer","Autumn","Winter"]
for a in range (0x82):
	for b in range(4):
		setEOLComment(start,"${0:2X} - {1}".format(a,seasons[b]))
		start = start.add(1)
	

