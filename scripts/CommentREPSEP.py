#This will add a EOL comment for what the REP/SEP is
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 

cA = state.currentAddress
opCode = 256+getByte(cA)
print("{0:2X}".format(opCode))
raw = getByte(cA.add(1))
param = raw & 0x30

if param == 0x10: #XY
	com = "XY "
elif param == 0x20: #A
	com = "A "
elif param == 0x30: #AXY
	com = "AXY "

if opCode == 0xc2: #REP
	com += "16 bits"
	extra = " clear "
else: #SEP
	com += "8 bits"
	extra = " set "

if (raw & 0x1) == 0x1:
	com += extra + "C"

setEOLComment(cA, com)
