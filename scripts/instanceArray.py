#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 


from ghidra.app.util.datatype import DataTypeSelectionDialog
from ghidra.framework.plugintool import PluginTool
from ghidra.program.model.data import DataType
from ghidra.program.model.data import ArrayDataType
from ghidra.program.model.data import DataTypeManager
from ghidra.util.data.DataTypeParser import AllowedDataTypes

 
tool = state.getTool()
dtm = currentProgram.getDataTypeManager()
selectionDialog = DataTypeSelectionDialog(tool, dtm, -1, AllowedDataTypes.FIXED_LENGTH)
tool.showDialog(selectionDialog)
dataType = selectionDialog.getUserChosenDataType()
if dataType is not None:
    print "Chosen data type: " + str(dataType)
    int1 = askInt("how many?", "enter num")
    start = state.currentAddress
    end = start.add(int1-1)	
    clearListing(start, end)
    working = start
    # for i in range(int1):
    #    createData(working,dataType)
    #    working = working.add(dataType.getLength())
    arrayDT = ArrayDataType(dataType, int1, dataType.getLength())
    createData(start,arrayDT)
