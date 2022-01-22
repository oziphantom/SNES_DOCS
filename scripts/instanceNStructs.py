#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 

from ghidra.app.util.datatype import DataTypeSelectionDialog
from ghidra.framework.plugintool import PluginTool
from ghidra.program.model.data import DataType
from ghidra.program.model.data import DataTypeManager
from ghidra.util.data.DataTypeParser import AllowedDataTypes
from ghidra.util import Msg
 
# tool = state.getTool()
# dtm = currentProgram.getDataTypeManager()
# selectionDialog = DataTypeSelectionDialog(tool, dtm, -1, AllowedDataTypes.FIXED_LENGTH)
# tool.showDialog(selectionDialog)
# dataType = selectionDialog.getUserChosenDataType()
dataTypes = getDataTypes("sPalette")
numTypes = len(dataTypes)
print(numTypes)

if numTypes >0 :
	#baseAddr = 0x03002930
	baseAddr = state.currentAddress.offset
	count = 256
	#count = askInt("number of", "enter count")

	#addr = state.currentAddress
	#addr = toAddr(0x8000000+baseAddr)
	addr = toAddr(baseAddr)

	dataType = dataTypes[0]

	for i in range(count):
		#print(addr)
		createData(addr,dataType)
		addr = addr.add(dataType.getLength())

	arr = ghidra.app.cmd.data.CreateArrayCmd(toAddr(baseAddr),count, dataType,dataType.getLength())
	arr.applyTo(getCurrentProgram())
	selStart = state.currentAddress
		

