#This adds a Long reference and sets a label based on address and prefix
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 

from  ghidra.program.model.symbol import RefType,FlowType
from SNESLib import getLongData

myStr = askString("Prefix", "suffix without _: ")

start = state.currentSelection.minAddress.offset
end = state.currentSelection.maxAddress.offset

for a in range(start, end, 3):
	dest = getLongData(toAddr(a))
	destAddr = toAddr(dest)
	createMemoryReference(getDataAt(toAddr(a)), destAddr, RefType.INDIRECTION)
	createLabel(destAddr, "{0}_{1:06X}".format(myStr, dest), True)

