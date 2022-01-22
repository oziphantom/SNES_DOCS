#TODO write a description for this script
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 


from  ghidra.program.model.symbol import RefType
from ghidra.program.model.data import DataType

def getUByte(addr):
	val = getByte(addr)
	if val <0:
		val = 256+val
	return val

def getWord(cA):
	lo = getUByte(cA.add(0))
	hi = getUByte(cA.add(1))
	return (hi<<8)|lo

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
'''
dataTypes = getDataTypes("sWordByteSomething")
numTypes = len(dataTypes)
print(numTypes)

if numTypes >0 :
	dataType = dataTypes[0]
	if state.currentSelection != None:
		start = state.currentSelection.minAddress
		end = state.currentSelection.maxAddress
		while(start.getOffset() <=end.getOffset()):
			val = getWord(start)
			if val != 0:
				createData(start,dataType)
				makeWordRef(start,0)
				start = start.add(dataType.getLength())
			else:
				createWord(start)
				start = start.add(2)
'''
start = state.currentSelection.minAddress
end = state.currentSelection.maxAddress

typeShort = getDataTypes("byte")[0]

number = 0
while start.offset < end.offset:
	addr = start.add(0)
	for i in range(32): # we want 64 colours
	    createData(addr,typeShort)
	    addr = addr.next()

	arr = ghidra.app.cmd.data.CreateArrayCmd(start,32, typeShort,1)
	arr.applyTo(getCurrentProgram())
	start = start.add(32)
