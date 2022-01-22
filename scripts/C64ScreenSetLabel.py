#TODO write a description for this script
#@author 
#@category C64
#@keybinding 
#@menupath 
#@toolbar 


import math

startAddress = 0xD800			# change me to be the start address
baseLabel = "CRAM"			# will build labels in the form baseLabel_L<line>_R<char>
SA = toAddr(startAddress)
EA = SA.add(0x400)

while(SA < EA):
	sym = getSymbolAt(SA)
	if sym:
		print(sym)
		offset = sym.getAddress().offset
		offset = offset-startAddress
		line = int(math.floor(offset/40))
		row = offset%40
		sym.setName(baseLabel+"_L"+str(line)+"_R"+str(row), sym.getSource())
	SA = SA.add(1)

