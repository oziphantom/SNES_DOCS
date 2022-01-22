#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 

typeByte = getDataTypes("word")[0]

addr = state.currentAddress
size = 0x40

startAddr = addr

for i in range(size): 
    print(addr)
    createData(addr,typeByte)
    addr = addr.add(2)

arr = ghidra.app.cmd.data.CreateArrayCmd(startAddr,size, typeByte,2)
arr.applyTo(getCurrentProgram())
selStart = addr

