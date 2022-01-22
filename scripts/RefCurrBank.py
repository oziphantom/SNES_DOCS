#TODO write a description for this script
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 


r = getReferencesFrom(state.currentAddress)

bank = state.currentAddress.offset & 0xFF0000

print(bank)
for ref in r:
	print(ref)
	dest = ref.getToAddress().offset
	dest = (dest & 0xFFFF) | bank
	dest = toAddr(dest)
	fromA = ref.getFromAddress()
	data = None
	while data == None:
		data = getDataAt(fromA)
		if data == None:
			fromA = fromA.add(-1)
	if fromA.offset != state.currentAddress:
		delta = state.currentAddress.offset - fromA.offset
		data = data.getComponentAt(delta)
	removeReference(ref)
	createMemoryReference( data, dest, ref.getReferenceType())

