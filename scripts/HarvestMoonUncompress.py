#This takes an addrees in, and returns a list of bytes
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 

from  ghidra.program.model.symbol import RefType,FlowType
from SNESLib import getByteData, getWordData

def uncompress(startAddr):
	destList = []
	buffer = [0]*0x800
	bufferPos = 0x7de
	compressedSize = getWordData(startAddr)
	print( "uncompressed size : {0:04X}".format(compressedSize))
	currAddr = startAddr.add(2)
	unknown = getWordData(currAddr)
	print( "unknown : {0:04X}".format(unknown))
	currAddr = currAddr.add(2)

	controlBits = 0
	controlBitsCounter = 0

	while(compressedSize > 0):
		controlBitsCounter -= 1
		if controlBitsCounter < 0:
			controlBits = getByteData(currAddr)
			currAddr = currAddr.add(1)
			controlBitsCounter = 7
		flag = controlBits & 1
		controlBits = controlBits >> 1
		if flag:
			# read byte
			b = getByteData(currAddr)
			currAddr = currAddr.add(1)
			# write dest
			destList.append(b)
			compressedSize -= 1
			if compressedSize == 0:
				break
			buffer[bufferPos] = b
			# move Next Buffer Pos
			bufferPos += 1
			bufferPos &= 0x7ff
		else:
			#read byte
			w86 = getByteData(currAddr)
			currAddr = currAddr.add(1)
			b = getByteData(currAddr)
			currAddr = currAddr.add(1)
			#extract the size of buffer offset
			b88 =(b&0x1f)+3
			w86 =((b&0xe0)<<3)|w86
			while b88 > 0:
				b = buffer[w86]
				#write dest
				destList.append(b)
				compressedSize -= 1
				if compressedSize == 0:
					break
				buffer[bufferPos] = b
				# move Next Buffer Pos
				bufferPos += 1
				bufferPos &= 0x7ff

				w86 += 1
				w86 &= 0x7ff
				b88 -= 1
	compressedSize = currAddr.offset-startAddr.offset
	print( "final size : {0:04X}".format(len(destList)))
	print( "end of Compressed data : {0:06X}".format(currAddr.offset))
	print( "compressed size : {0:04X}".format(compressedSize))
	return (destList,compressedSize)
