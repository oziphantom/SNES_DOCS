#TODO write a description for this script
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 


from HarvestMoonUncompress import uncompress

bytes,size = uncompress(state.currentAddress)

typeByte = getDataTypes("byte")[0]

arrayAddr = state.currentAddress.add(0)

while arrayAddr.offset < state.currentAddress.offset+size:
	createData(arrayAddr,typeByte)
	arrayAddr = arrayAddr.add(1)
	
Itemsize = 1
arr = ghidra.app.cmd.data.CreateArrayCmd(state.currentAddress,size, typeByte,Itemsize)
arr.applyTo(getCurrentProgram())

