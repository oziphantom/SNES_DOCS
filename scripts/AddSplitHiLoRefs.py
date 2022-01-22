#TODO write a description for this script
#@author 
#@category C64
#@keybinding 
#@menupath 
#@toolbar 


from Lib6502 import *
from  ghidra.program.model.symbol import RefType,FlowType

start = state.currentSelection.minAddress
end = state.currentSelection.maxAddress
HiAddr = state.currentSelection.maxAddress.add(1)


while (start<=end):
	hi = getUByte(start)
	lo = getUByte(HiAddr)
	createMemoryReference(getDataAt(start),toAddr((hi<<8)|lo),FlowType.INDIRECTION)
	start = start.add(1)
	HiAddr = HiAddr.add(1)

