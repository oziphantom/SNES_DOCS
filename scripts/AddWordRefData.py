#TODO write a description for this script
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

def makeWordRef(cA,index):
	(lo,hi,bank) = getDestForABS(cA)

	dest = toAddr(bank<<16|hi<<8|lo)
	if lo != 0xFF and hi != 0xFF:
		data = getDataContaining(cA).getComponent(index)
		createMemoryReference(data, dest, RefType.DATA_IND)

if state.currentSelection != None:
	start = state.currentSelection.minAddress
	end = state.currentSelection.maxAddress
	while(start.getOffset() <=end.getOffset()):
		makeWordRef(start)
		start = start.add(2)
else:
	cA = state.currentAddress
	for i in range(5):
		makeWordRef(cA,i)
		cA = cA.add(2)

