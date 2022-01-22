#TODO add data and defines for the SNES header
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 

from ghidra.program.model.data import DataType

def makeArray(addressOffset, dataType, length, typeSize):
	addr = toAddr(addressOffset)
	for i in range(length):
	    createData(addr,dataType)
	    addr = addr.next()

	arr = ghidra.app.cmd.data.CreateArrayCmd(toAddr(addressOffset),length, dataType,typeSize)
	arr.applyTo(getCurrentProgram())


#make the Game Title String
offset = toAddr(0xffc0)
typeChar = getDataTypes("char")[0]
typeByte = getDataTypes("byte")[0]
typeWord = getDataTypes("word")[0]

makeArray(0xFFC0,typeChar,21,1)

createByte(toAddr(0xFFd5)) # mapping mode
createByte(toAddr(0xFFd6)) # rom type
createByte(toAddr(0xFFd7)) # rom size
createByte(toAddr(0xFFd8)) # sram size
createByte(toAddr(0xFFd9)) # country
createByte(toAddr(0xFFda)) # developer
createByte(toAddr(0xFFdb)) # version #
createWord(toAddr(0xFFdc)) # checksum comp
createWord(toAddr(0xFFde)) # checksum

mapping = getByte(toAddr(0xffd5))
if (mapping & 0x10) == 0x10:
	mapComment = "FAST "
else:
	mapComment = "SLOW "
mapping = mapping & 0xF;
if mapping == 0:
	mapComment += "LoROM"
elif mapping == 1:
	mapComment += "HiROM"
elif mapping == 2:
	mapComment += "SDD-1 ROM"
elif mapping == 3:
	mapComment += "SA-1 ROM"
elif mapping == 4:
	mapComment += "ExLoROM" # I think, its make believe anyway
elif mapping == 5:
	mapComment += "ExHiROM"

#extended
addr = toAddr(0xffb0)
if getByte(toAddr(0xffd4)) != 0x33:
	makeArray(0xffb0,typeByte,15,1)
else :
	makeArray(0xffb0,typeChar,2,1)	# maker code
	makeArray(0xffb2,typeChar,4,1)	# game code
	makeArray(0xffb6,typeByte,6,1)	# reserved
	createByte(toAddr(0xffbc))	# Flash size
	createByte(toAddr(0xffbd))	# Expansion RAM size
	createByte(toAddr(0xffbe))	# Special version

makeArray(0xffe0, typeByte,4,1)		# empty area

for addr in range(0xffe4,0xffff,2):	# VECTORS
	createWord(toAddr(addr)) 

#add auto entry points, I will just go with EMU RESET and NATIVE NMI the other may be used but mostly not
addEntryPoint(toAddr(getShort(toAddr(0xffea)))) #NMI NATIVE
addEntryPoint(toAddr(getShort(toAddr(0xfffc))))	#EMU RESET
