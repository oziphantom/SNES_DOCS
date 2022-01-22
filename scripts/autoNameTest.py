#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 


#TODO Add User Code Here
def convertUnsigned(val):
    if val < 0:
       val = 256+val
    return val

def getAddress(s):
   b = s.getBytes()
   b1 = convertUnsigned(b[0])
   b2 = convertUnsigned(b[1])
   b3 = convertUnsigned(b[2])
   b4 = convertUnsigned(b[3])
   return b1 | (b2 << 8) | (b3 << 16) | (b4<<24)

struct = state.getCurrentProgram().listing.getDataAt(state.getCurrentAddress())
first =  struct.getComponentAt(0)
second = struct.getComponentAt(4)
third = struct.getComponentAt(8)

firstTargetAddr = getAddress(first)
secondTargetAddr = getAddress(second)
thirdTargetAddr = getAddress(third)

print(format(firstTargetAddr, '08X'))
print(format(secondTargetAddr, '08X'))
print(format(thirdTargetAddr, '08X'))

base = "Back_Shrine"

createLabel(toAddr(firstTargetAddr), base+"_Tiles", False)
createLabel(toAddr(secondTargetAddr), base+"_TileMap", False)
createLabel(toAddr(thirdTargetAddr), base+"_Palette", False)