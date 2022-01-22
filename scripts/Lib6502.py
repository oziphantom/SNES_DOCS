from __main__ import * #bring in the ghidra flat

from  ghidra.program.model.symbol import RefType,FlowType
from java.math import BigInteger

#reads a byte from an address
# converts it to unsigned
def getUByte(addr):
	val = getByte(addr)
	if val <0:
		val = 256+val
	return val

def getByteParam(addr):
	return getUByte(addr.add(1))

#reads a wordParam (addr + 1,2)
def getWordParam(addr):
	return getUByte(addr.add(1)) | (getUByte(addr.add(2))<<8)

def getByteData(addr):
	return getUByte(addr)

#reads a wordParam (addr + 1,2)
def getWordData(addr):
	return getUByte(addr) | (getUByte(addr.add(1))<<8)

def getOpCodeFields(opCode):
	A = (opCode & 0xE0) >> 5
	B = (opCode & 0x1C) >> 2
	C = opCode & 0x03
	return (A,B,C)

def AddReferenceForInstructionAtAddress(cA):
	opCode = getUByte(cA)
	print("add ref")
	skipOpCodes = [00,0x40,0x60,0x8a,0x9a,0xaa,0xba,0xca,0xea,0x02,0x42,0x62,0x82,0xc2,0xe2,0x44,0x54,0xd4,0xf4,0x80,0x1A,0x3a,0x5a,0x7a,0xda,0xfa]
	if opCode in skipOpCodes:
		print("skiped")
		return
	if (opCode & 0x1F) == 0x10: # branch instructions
		print("branch")
		return
	if (opCode & 0x0F) == 0x08: # push/pull/transfer instructions
		print("push/pull/trans")
		return
	if (opCode & 0x0F) == 0x0B: # push/pull/transfer instructions 65816
		print("push/pull/trans 65816")
		return

	inst = getInstructionAt(cA)

	if opCode == 0x4c: # JMP XXXX
		#removeAllRefs(refs)
		dest = getWordParam(cA)
		createMemoryReference(inst,0,toAddr(dest),FlowType.UNCONDITIONAL_JUMP)
		return
	if opCode == 0x20: # JSR XXXX
		#removeAllRefs(refs)
		dest = getWordParam(cA)
		createMemoryReference(inst,0,toAddr(dest),FlowType.UNCONDITIONAL_CALL)
		return
	if opCode == 0x7c or opCode == 0x6C: # JMP (XXXX) (XXXX,X)
		#removeAllRefs(refs)
		dest = getWordParam(cA)
		createMemoryReference(inst,0,toAddr(dest).add(1),RefType.UNCONDITIONAL_JUMP)
		return
	if opCode ==  0xFC : # JSR (XXXX)
		#removeAllRefs(refs)
		dest = getWordParam(cA)
		createMemoryReference(inst,0,toAddr(dest),RefType.COMPUTED_CALL)
		createMemoryReference(inst,0,toAddr(dest).add(1),RefType.COMPUTED_CALL)
		transferAXYSizeFromTo(cA, toAddr(dest))
		return
	
	skip = False
	insA,insB,insC = getOpCodeFields(opCode)
	if insC == 0:
		print("c0")
		# B
		ZP = [1,5]
		iABS = [3,7]
		# A
		iRead = [5,6,7]
		iWrite = [4]
		iReadWrite = [1]
		#index
		index = [4,5,6,7]
		
		if insB in ZP:
			lo = getUByte(cA.add(1))
			hi = 0
		elif insB in iABS:
			lo = getUByte(cA.add(1))
			hi = getUByte(cA.add(2))
		else:
			skip = True
		
		if insA in iRead:
			ref = RefType.READ
		elif insA in iWrite:
			ref = RefType.WRITE
		elif insA in iReadWrite:
			ref = RefType.READ_WRITE

		if (opCode == 0x4C) or (opCode == 0x6C): # handle jumps
			ref = FlowType.COMPUTED_JUMP
			if opcode == 0x4C: #JUMP
				ref = FlowType.UNCONDITIONAL_JUMP
		
	elif insC == 1:
		print("insC = 1")
		# B
		iZP = [0,4]
		ZP = [1,5]
		iABS = [3,6,7]
		# A
		iRead = [0,1,2,3,5,6,7]
		iWrite = [4]
		if insB in iZP: #(ZP,X)
			lo = getUByte(cA.add(1))
			hi = 0
		elif insB in ZP: # ZP
			lo = getUByte(cA.add(1))
			hi = 0
		elif insB in iABS: # ABS
			lo = getUByte(cA.add(1))
			hi = getUByte(cA.add(2))
		else:
			skip = True

		if insA in iRead:
			ref = RefType.READ
		elif insA in iWrite:
			ref = RefType.WRITE
	elif insC == 2:
		print("c2")
		if insB == 4: # 65C02 versions (ZP) A
			lo = getUByte(cA.add(1))
			hi = 0
			ref = RefType.READ
			if opCode == 0x92:
				ref = RefType.WRITE
		else: #6502 versions
			# B
			ZP = [1,5]
			iABS = [3,7]
			# A
			iRead = [5]
			iWrite = [4]
			iReadWrite = [0,1,2,3,6,7]
			# index
			iIndex = [4,5]			
			if insB in ZP:
				lo = getUByte(cA.add(1))
				hi = 0
			elif insB in iABS:
				lo = getUByte(cA.add(1))
				hi = getUByte(cA.add(2))
			else:
				skip = True
			
			if insA in iRead:
				ref = RefType.READ
			elif insA in iWrite:
				ref = RefType.WRITE
			elif insA in iReadWrite:
				ref = RefType.READ_WRITE

	elif insC == 3:
		print("c3")
		# B
		iLong = [3,7]
		iLongIndirect = [1,5]
		# A
		iRead = [0,1,2,3,5,6,7]
		iWrite = [4]
		skip = True

	if not skip:
		refs = getReferencesFrom(inst.getAddress())
		for r in refs:
			removeReference(r)
		hi = hi<<8
		dest = toAddr(hi|lo)
		createMemoryReference(inst,0,dest,ref)

#i.e no jmp, branches, jsr, pea etc
def isOpcodeR_W_Abs(opcode):
	A,B,C = getOpCodeFields(opCode)
	if C == 1:
		if B == 3 or B == 6 or B == 7:
			return True
	if C == 2 or C == 0:
		if B == 3 or B == 7:
			return True
	exceptions = [0x1c,0x9c,0x9e]
	return opcode in exceptions