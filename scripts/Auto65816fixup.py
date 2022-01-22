#TODO write a description for this script
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 

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

def removeAllRefs(addr):
	for r in refs:
		removeReference(r)

def isAddressAlreadyCode(address):
	CU = currentProgram.listing.getCodeUnitAt(address)
	if not CU:
		return False
	tempStr = CU.getMnemonicString()
	# print(tempStr)
	# print(len(tempStr))
	# print(tempStr.isalpha())
	# print(tempStr.isupper())
	if len(tempStr) != 3:	# all menomics are 3 chars 
		return False
	return tempStr.isalpha() and tempStr.isupper()

targetAddressOffset = [state.currentAddress.offset] # this should hold raw numbers not Address objects
doneAddresses = []

while(len(targetAddressOffset)):
	start = toAddr(targetAddressOffset[0])
	doneAddresses.append(targetAddressOffset[0])
	targetAddressOffset = targetAddressOffset[1:]
	
	if(isAddressAlreadyCode(start)) == False:
		print("do dissasemble")
		clearListing(start)
		disassemble(start)				# get code
		analyzeChanges(currentProgram)
	
	CU = currentProgram.listing.getCodeUnitAt(start)

	print("start at {0:6X}".format(start.offset))
	currentInst = getInstructionAt(start)

	while currentInst:
		currAddress = instToAddr(currentInst)
		op = getOpCode(currentInst)
		print("looking at {0:2X}".format(op))

		if op == 0xE2: #SEP
			com = getSEPComment(getByteParam(currAddress))
			setEOLComment(currAddress, com)
		elif op == 0xC2: #REP
			com = getREPComment(getByteParam(currAddress))
			setEOLComment(currAddress, com)

		if isOpcodeImm(op):
			print("found immediate mode")
			refs = getReferencesFrom(currAddress)
			print("looking at {0:6X}".format(currAddress.offset))
			print(refs)
			for r in refs:
				print("removeing ref")
				removeReference(r)
			currentInst = currentInst.getNext()
			continue
		
		#refs = getReferencesFrom(currAddress)
		
		if op == 0x5B: #TCD
			setPreComment(currAddress, "TCD START")
		elif op == 0x2B: #PLB
			setPostComment(currAddress, "TCD END")
		elif op == 0xAB: #PLB
			setPreComment(currAddress, "DATA BANK CHANGE")
		else:
			newAddress = AddReferenceForInstructionAtAddress(currAddress,getDBRVal(currentAddress),getDPVal(currentAddress))
			if newAddress != -1:
				if newAddress not in targetAddressOffset:
					if newAddress not in doneAddresses:
						if not isAddressAlreadyCode(toAddr(newAddress)):
							targetAddressOffset.append(newAddress)
		currentInst = currentInst.getNext()