import ghidra.program.util.ProgramSelection
import ghidra.app.cmd.data.CreateArrayCmd
# this will work out and turn a GBA compressed type 0x10 into a byte array
#@author oziphantom
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 


#TODO Add User Code Here
def makeSureUnsinged(value):
    if value < 0 :
        return value + 256
    return value

def decompress(start):
    # Determine how much decompressed data to expect.
    header = []
    header.append(makeSureUnsinged(getByte(toAddr(start))))
    header.append(makeSureUnsinged(getByte(toAddr(start+1))))
    header.append(makeSureUnsinged(getByte(toAddr(start+2))))
    header.append(makeSureUnsinged(getByte(toAddr(start+3))))
    assert header[0] == 0x10
    size = (header[3] << 16) | (header[2] << 8) | header[1]
    result = bytearray(b'')
    position = start + 4
    # Main loop.
    flags = []
    while len(result) < size:
        if not flags:
            flag_byte = getByte(toAddr(position))
            position += 1
            flags = [bool((flag_byte << i) & 0x80) for i in range(8)]
        # Check the next flag and handle it accordingly.
        flag = flags[0]
        flags = flags[1:]
        if flag:
            # Interpret a compression code.
            first = makeSureUnsinged(getByte(toAddr(position)))
            second = makeSureUnsinged(getByte(toAddr(position+1)))
            position += 2
            match_length = (first >> 4) + 3
            encoded_distance = (first & 0xF) << 8 | second
            match_location = len(result) - encoded_distance - 1
            # Doing indexing math here in order to be able to handle
            # the 'wrap-around' behaviour elegantly.
            for i in range(match_length):
                result.append(result[match_location + i])
        else:
            # Interpret a literal byte.
            value = makeSureUnsinged(getByte(toAddr(position)))
            # print(str(value))
            result.append(value)
            position += 1
    if len(result) != size:
        print("got "+str(len(result))+" expected "+str(size))
    assert len(result) == size
    # Position may be less than len(data) due to padding.
    # In general, we won't know how much data to read anyway.
    return result,(position-start)

offset = state.currentAddress.getOffset()
print("{0:08X}".format(offset))
uncomp, end = decompress(offset)
print("end {0:08X}".format(end+offset))

addr = state.currentAddress

clearListing(addr, toAddr(offset+end))

for i in range(end):
    createByte(addr)
    addr = addr.next()

state.setCurrentSelection(ghidra.program.util.ProgramSelection(toAddr(offset), toAddr(offset+end) ))
arr = ghidra.app.cmd.data.CreateArrayCmd(toAddr(offset),end, getDataTypes("byte")[0],1)
arr.applyTo(getCurrentProgram())
