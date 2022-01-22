#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 

typeArray = getDataTypes("eJoyTo8WayDirNum")
sizeOfElement = 1
enum = typeArray[0]

allValues = enum.getValues()

for value in allValues:
	name = enum.getName(value)
	setEOLComment(state.currentAddress.add(value*sizeOfElement), name)


