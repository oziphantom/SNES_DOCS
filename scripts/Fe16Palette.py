#Just makes 128 shorts and puts it into an array
#@author oziphantom
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 


offset = state.currentAddress.getOffset()
typeShort = getDataTypes("short")[0]

addr = state.currentAddress
for i in range(16): # we want 16 colours
    createData(addr,typeShort)
    addr = addr.next()
    addr = addr.next()

arr = ghidra.app.cmd.data.CreateArrayCmd(toAddr(offset),16, typeShort,2)
arr.applyTo(getCurrentProgram())