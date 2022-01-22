#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 

#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 

typeByte = getDataTypes("byte")[0]

addr = state.currentAddress
size = 0xfa0

startAddr = addr

for i in range(size): 
    createData(addr,typeByte)
    addr = addr.next()

arr = ghidra.app.cmd.data.CreateArrayCmd(startAddr,size, typeByte,1)
arr.applyTo(getCurrentProgram())
selStart = addr

