
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

#reads a LongParam (addr + 1,2,3)
def getLongParam(addr):
	return getUByte(addr.add(1)) | (getUByte(addr.add(2))<<8) | (getUByte(addr.add(3))<<16)

def getByteData(addr):
	return getUByte(addr)

#reads a wordParam (addr + 1,2)
def getWordData(addr):
	return getUByte(addr) | (getUByte(addr.add(1))<<8)

#reads a LongParam (addr + 1,2,3)
def getLongData(addr):
	return getUByte(addr) | (getUByte(addr.add(1))<<8) | (getUByte(addr.add(2))<<16)

#this will get the lo,hi,bank address for DP relative to the DPVal
def getDestForDP(cA,DPVal):
	lo = getUByte(cA.add(1))
	if DPVal != None:
		lo += DPVal
	hi = 0 #since this just | we can put the value in lo just fine
	if lo < 0x2000:
		bank = 0x7e
	else:
		bank = 0x00
	hi = lo >> 8
	lo = lo & 0xFF
	#print("DPVal {0:4X}, Bank {1:2X} Hi {2:2X} Lo {3:4X}".format(DPVal, bank, hi, lo))
	return (lo,hi,bank)

#this will expand a 16 bit address to 24bit
# <20 gets mapped to 7e
# <80 gets mapped to 00
#else mapped to bank/DBR
def getDestForABS(cA,DBRVal):
	lo = getUByte(cA.add(1))
	hi = getUByte(cA.add(2))
	if( hi < 0x20 ): #we are 7e ram mapped, I'm sure there are excpetions I will need to handle
		bank = 0x7e
	else:
		if( DBRVal != None ):
				bank = DBRVal
		else:
			if( hi < 0x80):
				bank = 0	# this maps the LO ROM shared registers
			else:
				bank = cA.getOffset()>>16
	return (lo,hi,bank)

#this just pulls all 3 bytes
def getDestForLong(cA):
	lo = getUByte(cA.add(1))
	hi = getUByte(cA.add(2))
	bank = getUByte(cA.add(3))
	return (lo,hi,bank)

#this will get the DBR val assigned at the address
# can return None
def getDBRVal(cA):
	pCon = getCurrentProgram().getProgramContext()
	DBRreg = pCon.getRegister("DBR")
	BRBigInt = pCon.getValue(DBRreg, cA, False)
	return BRBigInt

def getDPVal(cA):
	pCon = getCurrentProgram().getProgramContext()
	DPreg = pCon.getRegister("DP")
	DPBigInt = pCon.getValue(DPreg, cA, False)
	return DPBigInt

def getASize(cA):
	pCon = getCurrentProgram().getProgramContext()
	DBRreg = pCon.getRegister("ctx_MF")
	BRBigInt = pCon.getValue(DBRreg, cA, False)
	if( BRBigInt == 1):
		return 1
	return 2

def getXYSize(cA):
	pCon = getCurrentProgram().getProgramContext()
	DBRreg = pCon.getRegister("ctx_XF")
	BRBigInt = pCon.getValue(DBRreg, cA, False)
	if( BRBigInt == 1):
		return 1
	return 2

def transferAXYSizeFromTo(cA, dest):
	try:
		pCon = getCurrentProgram().getProgramContext()
		reg = pCon.getRegister("ctx_MF")
		mf = pCon.getRegisterValue(reg,cA)
		reg = pCon.getRegister("ctx_XF")
		xf = pCon.getRegisterValue(reg,cA)
		reg = pCon.getRegister("ctx_EF")
		ef = pCon.getRegisterValue(reg,cA)
		pCon.setRegisterValue(dest, dest.add(1), mf)
		pCon.setRegisterValue(dest, dest.add(1), xf)
		pCon.setRegisterValue(dest, dest.add(1), ef)
	except:
		print("already set")

def getOpCodeFields(opCode):
	A = (opCode & 0xE0) >> 5
	B = (opCode & 0x1C) >> 2
	C = opCode & 0x03
	return (A,B,C)

def AddReferenceForInstructionAtAddress(cA, DBRVal, DPVal ):
	returnAddress = -1
	opCode = getUByte(cA)
	# print("add ref")
	skipOpCodes = [00,0x40,0x60,0x8a,0x9a,0xaa,0xba,0xca,0xea,0x02,0x42,0x62,0x82,0xc2,0xe2,0x44,0x54,0xd4,0xf4,0x80,0x1A,0x3a,0x5a,0x7a,0xda,0xfa]
	if opCode in skipOpCodes:
		# print("skiped")
		return returnAddress
	if (opCode & 0x1F) == 0x10: # branch instructions
		# print("branch")
		return returnAddress
	if (opCode & 0x0F) == 0x08: # push/pull/transfer instructions
		# print("push/pull/trans")
		return returnAddress
	if (opCode & 0x0F) == 0x0B: # push/pull/transfer instructions 65816
		# print("push/pull/trans 65816")
		return returnAddress

	bankOffset = cA.getOffset() & 0xFF0000
	
	inst = getInstructionAt(cA)

	if opCode == 0x5c: # JMP XX:XXXX
		#removeAllRefs(refs)
		dest = getLongParam(cA)
		createMemoryReference(inst,0,toAddr(dest),FlowType.UNCONDITIONAL_JUMP)
		transferAXYSizeFromTo(cA, toAddr(dest))
		return dest
	if opCode == 0x22: # JSR XX:XXXX
		#removeAllRefs(refs)
		dest = getLongParam(cA)
		createMemoryReference(inst,0,toAddr(dest),FlowType.UNCONDITIONAL_CALL)
		transferAXYSizeFromTo(cA, toAddr(dest))
		return dest
	if opCode == 0x4c: # JMP XXXX
		#removeAllRefs(refs)
		dest = getWordParam(cA) | bankOffset
		createMemoryReference(inst,0,toAddr(dest),FlowType.UNCONDITIONAL_JUMP)
		transferAXYSizeFromTo(cA, toAddr(dest))
		return dest
	if opCode == 0x20: # JSR XXXX
		#removeAllRefs(refs)
		dest = getWordParam(cA) | bankOffset
		createMemoryReference(inst,0,toAddr(dest),FlowType.UNCONDITIONAL_CALL)
		transferAXYSizeFromTo(cA, toAddr(dest))
		return dest
	if opCode == 0x7c or opCode == 0x6C: # JMP (XXXX) (XXXX,X)
		#removeAllRefs(refs)
		dest = getWordParam(cA) | bankOffset
		createMemoryReference(inst,0,toAddr(dest),RefType.UNCONDITIONAL_JUMP)
		createMemoryReference(inst,0,toAddr(dest).add(1),RefType.UNCONDITIONAL_JUMP)
		transferAXYSizeFromTo(cA, toAddr(dest)) # usually the values are after it, so this sets for them due to order
		createBookmark(toAddr(dest),None,"JMP call table")
		return returnAddress
	if opCode ==  0xFC : # JSR (XXXX)
		#removeAllRefs(refs)
		dest = getWordParam(cA) | bankOffset
		createMemoryReference(inst,0,toAddr(dest),RefType.COMPUTED_CALL)
		createMemoryReference(inst,0,toAddr(dest).add(1),RefType.COMPUTED_CALL)
		transferAXYSizeFromTo(cA, toAddr(dest))
		createBookmark(toAddr(dest),None,"JSR call table")
		return returnAddress # this is a jump table not a valid address to continue
	
	ASize = getASize(cA)
	XYSize = getXYSize(cA)
	skip = False
	size = ASize
	if (opCode == 0x4) or (opCode == 0x14): # TSB/TRB ZP
		(lo,hi,bank) = getDestForDP(cA, DPVal)
		ref = RefType.READ_WRITE
	if (opCode == 0xc) or (opCode == 0x1C): # TSB/TRB ABS
		(lo,hi,bank) = getDestForABS(cA, DBRVal)
		ref = RefType.READ_WRITE
	if (opCode == 0x64) or (opCode == 0x74): # STZ ZP/ZP,x
		(lo,hi,bank) = getDestForDP(cA, DPVal)
		ref = RefType.WRITE
	if (opCode == 0x9c) or (opCode == 0x9E): # STZ ABS/ABS,x
		(lo,hi,bank) = getDestForABS(cA, DBRVal)
		ref = RefType.WRITE
	else:
		insA,insB,insC = getOpCodeFields(opCode)
		if insC == 0:
			# B
			ZP = [1,5]
			iABS = [3,7]
			# A
			iRead = [5,6,7]
			iWrite = [4]
			iReadWrite = [1]
			#index
			index = [4,5,6,7]
			
			size = ASize
			if insA in index:
				size = XYSize
			
			if insB in ZP:
				(lo,hi,bank) = getDestForDP(cA, DPVal)
			elif insB in iABS:
				(lo,hi,bank) = getDestForABS(cA, DBRVal)
			else:
				skip = True
			
			if insA in iRead:
				ref = RefType.READ
			elif insA in iWrite:
				ref = RefType.WRITE
			elif insA in iReadWrite:
				ref = RefType.READ_WRITE

			if (opCode == 0x4C) or (opCode == 0x6C): # handle jumps
				bank = cA.offset()>>16 #set bank to be program bank
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
				size = 2
				(lo,hi,bank) = getDestForDP(cA, DPVal)
			elif insB in ZP: # ZP
				print("ZP")
				size = ASize
				(lo,hi,bank) = getDestForDP(cA, DPVal)
			elif insB in iABS: # ABS
				size = ASize
				(lo,hi,bank) = getDestForABS(cA, DBRVal)
			else:
				skip = True

			if insA in iRead:
				ref = RefType.READ
			elif insA in iWrite:
				ref = RefType.WRITE
		elif insC == 2:
			if insB == 4: # 65C02 versions (ZP) A
				size = 2
				(lo,hi,bank) = getDestForDP(cA, DPVal)
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
				size = ASize
				if insA in iIndex:
					size = XYSize
				
				if insB in ZP:
					(lo,hi,bank) = getDestForDP(cA, DPVal)
				elif insB in iABS:
					(lo,hi,bank) = getDestForABS(cA, DBRVal)
				else:
					skip = True
				
				if insA in iRead:
					ref = RefType.READ
				elif insA in iWrite:
					ref = RefType.WRITE
				elif insA in iReadWrite:
					ref = RefType.READ_WRITE
		
		elif insC == 3:
			size = ASize
			# B
			iLong = [3,7]
			iLongIndirect = [1,5]
			# A
			iRead = [0,1,2,3,5,6,7]
			iWrite = [4]
			if insB in iLong:
				(lo,hi,bank) = getDestForLong(cA)
				ref = RefType.READ
				if insA in iWrite:
					ref = RefType.WRITE
			elif insB in iLongIndirect:
				# print("opcode {0:2X} to 3 ".format(opCode))
				size = 3
				(lo,hi,bank) = getDestForDP(cA, DPVal)
				ref = RefType.READ
			else:
				skip = True
	if not skip:
		if (bank != 0x7e) and (bank != 0x7f):
			if hi < 0x20:
				bank = 0x7e # sometimes longs will have XX:0000 but be for <$2000 so map to 7e
		bank = bank<<16
		hi = hi<<8
		dest = toAddr(bank|hi|lo)
		# print("{0:6X}".format(bank|hi|lo))
		# print(inst)
		createMemoryReference(inst,0,dest,ref)
		if size > 1:
			createMemoryReference(inst,0,dest.add(1),ref)
			if size > 2:
				createMemoryReference(inst,0,dest.add(2),ref)
	return returnAddress

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

def getSEPComment(value):
	SF = ['N','V',' A8 ',' XY8 ','D','I','Z','C']
	raw = value
	string = ''
	for b in range(8):
		if (raw & 0x80) == 0x80:
			string += SF[b]
		raw = raw << 1
	return string

def getREPComment(value):
	SF = ['N','V',' A16 ',' XY16 ','D','I','Z','C']
	raw = value
	string = ''
	for b in range(8):
		if (raw & 0x80) == 0x80:
			string += SF[b]
		raw = raw << 1
	return string

def convertSNESPaletteToRGB(snesPal):
	r = (snesPal & 0x001F)<<3
	g = ((snesPal & 0x03e0)>>(5-3))
	b = ((snesPal & 0x7c00)>>(10-3))
	return (r,g,b)

def convert8x8_4bitToPalNums(data):
	b0 = 0
	b1 = 1
	b2 = 16
	b3 = 17
	out = []
	for y in range(8):
		d0 = data[b0]
		d1 = data[b1]
		d2 = data[b2]
		d3 = data[b3]
		for x in range(8):
			p  = (d3 & 0x80)>>(7-3)
			p |= (d2 & 0x80)>>(7-2)
			p |= (d1 & 0x80)>>(7-1)
			p |= (d0 & 0x80)>>(7-0)
			out.append(p)
			d0 = d0 << 1
			d1 = d1 << 1
			d2 = d2 << 1
			d3 = d3 << 1
		b0 += 2
		b1 += 2
		b2 += 2
		b3 += 2
	return out