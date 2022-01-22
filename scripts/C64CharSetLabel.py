#TODO write a description for this script
#@author 
#@category C64
#@keybinding 
#@menupath 
#@toolbar 

import math

startAddress = 0x2800			# change me to be the start address
baseLabel = "Charset"			# will build labels in the form baseLabel_C<char num>_R<row in char>
SA = toAddr(startAddress)
EA = SA.add(0x800)

while(SA < EA):
	sym = getSymbolAt(SA)
	if sym:
		print(sym)
		offset = sym.getAddress().offset
		offset = offset-startAddress
		charNum = int(math.floor(offset/8))
		row = offset%8
		sym.setName(baseLabel+"_C"+str(charNum)+"_R"+str(row), sym.getSource())
	SA = SA.add(1)

