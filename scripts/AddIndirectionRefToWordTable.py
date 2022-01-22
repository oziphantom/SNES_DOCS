#take word, make reference to BANK:WORD Indirection
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 
from  ghidra.program.model.symbol import RefType
def getUByte(addr):
	val = getByte(addr)
	if val <0:
		val = 256+val
	return val

def getDestForABS(cA):
	lo = getUByte(cA.add(0))
	hi = getUByte(cA.add(1))
	bank = cA.getOffset()>>16
	return (lo,hi,bank)

def makeWordRef(cA):
	(lo,hi,bank) = getDestForABS(cA)

	dest = toAddr(bank<<16|hi<<8|lo)
	data = createWord(cA)
	#createMemoryReference(data, dest, RefType.INDIRECTION)
	createMemoryReference(data, dest, RefType.DATA_IND)
	#clearListing(dest)
	#disassemble(dest)

if state.currentSelection != None:
	start = state.currentSelection.minAddress
	end = state.currentSelection.maxAddress
	while(start.getOffset() <=end.getOffset()):
		makeWordRef(start)
		start = start.add(2)
else:
	cA = state.currentAddress
	makeWordRef(cA)






