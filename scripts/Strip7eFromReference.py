#TODO write a description for this script
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 


refs = getReferencesFrom(state.currentAddress)
for r in refs:
	fromAddr = r.getFromAddress()
	toAddr = r.getToAddress()
	print("{0},{1}".format(fromAddr, toAddr))
	inst = getInstructionAt(fromAddr)
	print(inst)
	toAddr = toAddr.add(-0x7e0000)
	n = createMemoryReference(inst,0,toAddr,r.getReferenceType())
	removeReference(r)
	setReferencePrimary(n)
