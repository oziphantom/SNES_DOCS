#This will add an EOL comment of the value for 2100/INIDISP
#@author 
#@category SNES
#@keybinding 
#@menupath Script.Param.INIDISP
#@toolbar 

def getUByte(addr):
	val = getByte(addr)
	if val <0:
		val = 256+val
	return val

cA = state.currentAddress
getUByte(cA.add(1))
com = ""


