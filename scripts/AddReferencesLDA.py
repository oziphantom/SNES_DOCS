#This will look up the opcode and add references as needed
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 

from SNESLib import *
from  ghidra.program.model.symbol import RefType,FlowType


cA = state.currentAddress

DBRVal = getDBRVal(cA)

DPVal =  getDPVal(cA)
	
AddReferenceForInstructionAtAddress(cA, DBRVal, DPVal)

opCode = getUByte(cA)
if opCode == 0xA9:
	bankOffset = cA.getOffset() & 0xFF0000
	dest = getWordParam(cA)
	inst = getInstructionAt(cA)
	createMemoryReference(inst,0,toAddr(bankOffset|dest),RefType.READ)
