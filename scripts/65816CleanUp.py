#Does what the spec should do
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 

from SNESLib import *
from  ghidra.program.model.symbol import RefType,FlowType

g_immOpcodes = [0x69, 0x29, 0x89, 0xc9, 0xe0, 0xc0, 0x49, 0xa9, 0xa2, 0xa0, 0x09, 0xc2, 0xe9, 0xe2]

def instToAddr(inst):
	return inst.getInstructionContext().getAddress()
'''
def getUByte(addr):
	val = getByte(addr)
	if val <0:
		val = 256+val
	return val
'''
def getOpCode(instruction):
	return getUByte(instToAddr(instruction))

def isOpcodeImm(opCode):
	return opCode in g_immOpcodes

def isOpCodeAbsLong(opCode):
	if (opCode&0xf0)==0xf0:
		if opCode == 0xfc: # JSR (ABS,x) is not what we want
			return False
		if opCode == 0xf0: #BEQ is not what we want
			return False
		return True 
	if (opCode == 0xBF):
		return True
	return False
'''
def getWord(addr):
	return getUByte(addr.add(1)) | (getUByte(addr.add(2))<<8)

def getLong(addr):
	return getUByte(addr.add(1)) | (getUByte(addr.add(2))<<8) | (getUByte(addr.add(3))<<16)
'''
def removeAllRefs(addr):
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

	if op == 0xE2: #SEP
		com = getSEPComment(getByteParam(currAddress))
		setEOLComment(currAddress, com)
	elif op == 0xC2: #REP
		com = getREPComment(getByteParam(currAddress))
		setEOLComment(currAddress, com)

	if isOpcodeImm(op):
		refs = getReferencesFrom(currAddress)
		for r in refs:
			removeReference(r)
		currentInst = currentInst.getNext()
		continue
	
	refs = getReferencesFrom(currAddress)
	'''
	if isOpCodeAbsLong(op):
		removeAllRefs(refs)
		dest = getLongParam(currAddress)
		ref = RefType.READ
		if op == 0x9f: # STA ABS LONG
			ref = RefType.WRITE
		createMemoryReference(currentInst,0,toAddr(dest),ref)
	if op == 0x5c: # JMP XX:XXXX
		removeAllRefs(refs)
		dest = getLongParam(currAddress)
		createMemoryReference(currentInst,0,toAddr(dest),FlowType.UNCONDITIONAL_JUMP)
	if op == 0x22: # JSR XX:XXXX
		removeAllRefs(refs)
		dest = getLongParam(currAddress)
		createMemoryReference(currentInst,0,toAddr(dest),FlowType.UNCONDITIONAL_CALL)
	if op == 0x4c: # JMP XXXX
		removeAllRefs(refs)
		dest = getWordParam(currAddress) | bankOffset
		createMemoryReference(currentInst,0,toAddr(dest),FlowType.UNCONDITIONAL_JUMP)
	if op == 0x20: # JSR XXXX
		removeAllRefs(refs)
		dest = getWordParam(currAddress) | bankOffset
		createMemoryReference(currentInst,0,toAddr(dest),FlowType.UNCONDITIONAL_CALL)
	if op == 0x7c or op == 0xFC: # JSR XXXX
		removeAllRefs(refs)
		dest = getWordParam(currAddress) | bankOffset
		createMemoryReference(currentInst,0,toAddr(dest),RefType.UNCONDITIONAL_CALL)
	if isOpcodeR_W_Abs(op):
			param = getWordParam(currAddress)
			if param < 0x8000:
				AddReferenceForInstructionAtAddress(currAddress,0,0)
	'''
	
	if op == 0x5B: #TCD
		setPreComment(currAddress, "TCD START")
	elif op == 0x2B: #PLB
		setPostComment(currAddress, "TCD END")
	elif op == 0xAB: #PLB
		setPreComment(currAddress, "DATA BANK CHANGE")
	else:
		AddReferenceForInstructionAtAddress(currAddress,getDBRVal(currentAddress),getDPVal(currentAddress))
	currentInst = currentInst.getNext()
