#TODO this will inspect the TSA/Tilemap data and work out its size, convert to short array
#@author oziphantom
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 

def getuShort(value):
	if value < 0:
		value = value + (64*1024)
	return value

offset = state.currentAddress.getOffset()
print("{0:08X}".format(offset))
rows = getByte(toAddr(offset))+1
tiles = getByte(toAddr(offset+1))+1
print(str(rows))
print(str(tiles))
length = 2 + ((rows*tiles)*2)
end = offset + length
print("end {0:08X}".format(end))

typeShort = getDataTypes("short")[0]
addr = state.currentAddress
for i in range(offset,end,2):
    createData(addr,typeShort)
    addr = addr.next()
    addr = addr.next()

clearListing(toAddr(offset), toAddr(end))

state.setCurrentSelection(ghidra.program.util.ProgramSelection(toAddr(offset), toAddr(end) ))
arr = ghidra.app.cmd.data.CreateArrayCmd(toAddr(offset),length/2, typeShort,2)
arr.applyTo(getCurrentProgram())
