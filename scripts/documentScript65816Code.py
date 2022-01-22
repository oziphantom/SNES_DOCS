#TODO write a description for this script
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 

def getOpcodeByte(cA):
	b = getByte(cA)
	if b>=0:
		return b
	return b+256

buffer = []
cA = state.currentAddress
wA = cA
for i in range(32):
	buffer.append(getOpcodeByte(wA))
	wA = wA.add(1)

advanceOneBytes = [0xc2,0x30,0xA5,0xC9,0x18,0x69,0x01,0x00,0x85,0xC9]
advanceOneWords = [0xc2,0x30,0xA5,0xC9,0x18,0x69,0x02,0x00,0x85,0xC9]
readWord = [0xc2,0x20,0xA7,0xC9]
readByte = [0xe2,0x20,0xA7,0xC9]

print(buffer)
print(advanceOneBytes)
if buffer[0:len(advanceOneBytes)] == advanceOneBytes:
	setEOLComment(cA.add(2), "dummy") # remove the dumb ?? on a line
	setEOLComment(cA.add(8), "advance byte")

if buffer[0:len(advanceOneWords)] == advanceOneWords:
	setEOLComment(cA.add(2), "dummy") # remove the dumb ?? on a line
	setEOLComment(cA.add(8), "advance word")

if buffer[0:len(readWord)] == readWord:
	setEOLComment(cA.add(2), "read word")

if buffer[0:len(readByte)] == readByte:
	setEOLComment(cA.add(2), "read byte")



