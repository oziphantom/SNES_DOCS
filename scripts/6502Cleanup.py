#TODO write a description for this script
#@author 
#@category C64
#@keybinding 
#@menupath 
#@toolbar 


from Lib6502 import *
from  ghidra.program.model.symbol import RefType,FlowType

g_immOpcodes = [0x69, 0x29, 0x89, 0xc9, 0xe0, 0xc0, 0x49, 0xa9, 0xa2, 0xa0, 0x09, 0xc2, 0xe9, 0xe2]

def instToAddr(inst):
	return inst.getInstructionContext().getAddress()

def getOpCode(instruction):
	return getUByte(instToAddr(instruction))

def isOpcodeImm(opCode):
	return opCode in g_immOpcodes

def removeAllRefs(refs):
	for r in refs:
		removeReference(r)

start = state.currentSelection.minAddress
end = state.currentSelection.maxAddress

bankOffset = start.getOffset() & 0xFF0000

currentInst = getInstructionAt(start)

while currentInst.getInstructionContext().getAddress() < end:
	currAddress = instToAddr(currentInst)
	op = getOpCode(currentInst)
	# print("looking at {0:2X}".format(op))
	
	AddReferenceForInstructionAtAddress(currAddress)
	currentInst = currentInst.getNext()
