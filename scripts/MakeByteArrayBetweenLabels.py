#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 


typeByte = getDataTypes("byte")[0]

selStart = state.currentSelection.minAddress
selEnd = state.currentSelection.maxAddress

while selStart.offset < selEnd.offset:
	addr = selStart
	size = 1

	print("starting at" + str(addr) )

	while not getSymbolAt(addr.add(size)):
		size = size + 1

	startAddr = addr

	for i in range(size): 
	    createData(addr,typeByte)
	    addr = addr.next()

	arr = ghidra.app.cmd.data.CreateArrayCmd(startAddr,size, typeByte,1)
	arr.applyTo(getCurrentProgram())
	selStart = addr