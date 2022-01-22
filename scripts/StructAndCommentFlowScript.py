#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 



def ReadFunction(address):
    op = getShort(address)
    p1 = getShort(address.add(2))
    p2 = getInt(address.add(4))
    return op,p1,p2
    
def MoveNextFunction(address):
    return address.add(8)

def GetLabelFor(address):
    return str(getSymbolAt(toAddr(address)))

currAddress = state.currentAddress
print("start " + str(currAddress))

justIntDataType = dataTypes = getDataTypes("sFlowScriptInt")[0]
justIntDataPointer = dataTypes = getDataTypes("sFlowScriptPointer")[0]
while(True):
            code,sparam,iparam = ReadFunction(currAddress)
            if   code == 0:
                 createData(currAddress,justIntDataType)
                 setEOLComment(currAddress, "FinishScript()")
                 break
            elif code == 1:
                 createData(currAddress,justIntDataType)
                 setEOLComment(currAddress, "setField0x10ToInt({0:08X})".format(iparam))
            elif code == 2:
                 createData(currAddress,justIntDataPointer)
                 setEOLComment(currAddress, "{0}(nextPosInScript,{1:04X})".format(GetLabelFor(iparam),sparam))
            elif code == 3:
                 createData(currAddress,justIntDataPointer)
                 setEOLComment(currAddress, "setSubFunction(nextPosInScript,{0})".format(GetLabelFor(iparam)))
            elif code == 4:
                 createData(currAddress,justIntDataPointer)
                 setEOLComment(currAddress, "setField0x8ToInt({0:08X})".format(iparam))
            elif code == 5:
                 createData(currAddress,justIntDataType)
                 setEOLComment(currAddress, "attachNewScript({0:08X})".format(iparam))
                 print("sub script found : "+"{0:08X}".format(iparam))
            elif code == 6:
                 createData(currAddress,justIntDataType)
                 setEOLComment(currAddress, "runScript({0:08X})".format(iparam))
                 print("sub script found : "+"{0:08X}".format(iparam))
            elif code == 7:
                 createData(currAddress,justIntDataType)
                 setEOLComment(currAddress, "runScriptInSlot({0:08X}, {1:d})".format(iparam, sparam))
                 print("sub script found : "+"{0:08X}".format(iparam))
            elif code == 8:
                 createData(currAddress,justIntDataType)
                 setEOLComment(currAddress, "haltUntilScriptStarts({0:08X})".format(iparam))
                 print("sub script found : "+"{0:08X}".format(iparam))
            elif code == 9:
                 createData(currAddress,justIntDataType)
                 setEOLComment(currAddress, "removeAllInstancesOf({0:08X})".format(iparam))
                 print("sub script found : "+"{0:08X}".format(iparam))
            elif code == 10:
                 createData(currAddress,justIntDataType)
                 setEOLComment(currAddress, "clearSubFunctionOnScript({0:08X})".format(iparam))
                 print("sub script found : "+"{0:08X}".format(iparam))
            elif code == 11:
                 createData(currAddress,justIntDataType)
                 setEOLComment(currAddress, "Label:"+str(sparam))
            elif code == 12:
                 createData(currAddress,justIntDataType)
                 setEOLComment(currAddress, "Goto Label:"+str(sparam))
            elif code == 13:
                 createData(currAddress,justIntDataType)
                 setEOLComment(currAddress, "Goto Address, clear subFuc:"+"{0:08X}".format(iparam))
            elif code == 14:
                 createData(currAddress,justIntDataType)
                 setEOLComment(currAddress, "Wait "+str(sparam)+ "frames")
            elif code == 15:
		 createData(currAddress,justIntDataType)
                 setEOLComment(currAddress, "SetScriptID "+str(sparam))
	    elif code == 16:
                 createData(currAddress,justIntDataType)
                 setEOLComment(currAddress,"return 0")
            elif code == 17:
                 createData(currAddress,justIntDataType)
                 setEOLComment(currAddress, "If2OrMoreOfCullMe({0:08X})".format(iparam))
                 print("sub script found : "+"{0:08X}".format(iparam))
            elif code == 18:
                 createData(currAddress,justIntDataType)
                 setEOLComment(currAddress, "SetBit2OfField0x27")
            elif code == 19:
                 createData(currAddress,justIntDataType)
                 setEOLComment(currAddress, "NOP 2")
            elif code == 20:
                 createData(currAddress,justIntDataPointer)
                 setEOLComment(currAddress, "waitUntilReturnTrue(nextPosInScript,{0}".format(GetLabelFor(iparam)))
            elif code == 21:
                 createData(currAddress,justIntDataType)
                 setEOLComment(currAddress, "NOP 3")
            elif code == 22:
                 createData(currAddress,justIntDataPointer)
                 setEOLComment(currAddress,"{0}_withReturn(nextPosInScript,{1:04X})".format(GetLabelFor(iparam),sparam))
            elif code == 23:
                 createData(currAddress,justIntDataType)
                 setEOLComment(currAddress, "removeOtherInstance({0:08X})".format(iparam))
                 print("sub script found : "+"{0:08X}".format(iparam))
            elif code == 24:
                 createData(currAddress,justIntDataPointer)
                 setEOLComment(currAddress, "{0}_withReturn({1:04X},scriptStruct,nextPosInScript)".format(GetLabelFor(iparam),sparam))
            elif code == 25:
                 createData(currAddress,justIntDataType)
                 setEOLComment(currAddress, "NOP 4")

            currAddress = MoveNextFunction(currAddress)

