#TODO write a description for this script
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 


dataTypes = getDataTypes("sPalSetDesc")
sStruct = dataTypes[0]
dataTypes = getDataTypes("byte")
sByte = dataTypes[0]

start = state.currentSelection.minAddress
end = state.currentSelection.maxAddress

#bank = start.offset & 0xFF0000
bank = 0x050000 # force other bank

while(start.getOffset() <= end.getOffset()):
	if getByte(start) != 0:
		data = createData(start,sStruct)
		r = getReferencesFrom(start.add(1))
		ref = r[0]
		
		dest = ref.getToAddress().offset
		dest = (dest & 0xFFFF) | bank
		dest = toAddr(dest)
		fromA = ref.getFromAddress()
		dataRef = data.getComponentAt(1)
		removeReference(ref)
		createMemoryReference( dataRef, dest, ref.getReferenceType())
		start = start.add(sStruct.getLength())
	else:
		createData(start,sByte)
		start = start.add(1)