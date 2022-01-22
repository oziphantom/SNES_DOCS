#TODO write a description for this script
#@author 
#@category C64
#@keybinding 
#@menupath 
#@toolbar 

lookup = "@ABCDEFGHIJKLMNOPQRSTUVWXYZ[?]-< !\"#$%&,()*+,-//0123456789:;<=>?"
if state.currentSelection != None:
	start = state.currentSelection.minAddress
	end = state.currentSelection.maxAddress
	while(start.getOffset() <=end.getOffset()):
		signed = getShort(start) & 0xff		
		signed = signed & 0x3f
		print(signed)
		if signed < len(lookup):
			setEOLComment(start,lookup[signed])
		start = start.add(1)

