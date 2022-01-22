#TODO write a description for this script
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 
from ghidra.app.util.datatype import DataTypeSelectionDialog
from ghidra.framework.plugintool import PluginTool
from ghidra.program.model.data import DataType
from ghidra.program.model.data import DataTypeManager
from ghidra.util.data.DataTypeParser import AllowedDataTypes
from ghidra.util import Msg
from ghidra.program.model.symbol import RefType,FlowType

 
# tool = state.getTool()
# dtm = currentProgram.getDataTypeManager()
# selectionDialog = DataTypeSelectionDialog(tool, dtm, -1, AllowedDataTypes.FIXED_LENGTH)
# tool.showDialog(selectionDialog)
# dataType = selectionDialog.getUserChosenDataType()
dataTypes = getDataTypes("int3")
dataTypeInt3 = dataTypes[0]
dataTypes = getDataTypes("word")
dataTypeDWord = dataTypes[0]

# helper functions 
def getOpcodeByte(cA):
	b = getByte(cA)
	if b>=0:
		return b
	return b+256

def getOpcodeWord(cA):
	lo = getOpcodeByte(cA)
	hi = getOpcodeByte(cA.add(1))*256
	return hi+lo

def getOpcodeLong(cA):
	lo = getOpcodeByte(cA)
	hi = getOpcodeByte(cA.add(1))*256
	bank = getOpcodeByte(cA.add(2))*256*256
	return bank+hi+lo

def doSingleByte(address, desc):
	param1 = getOpcodeByte(address.add(1))
	setEOLComment(address, "{0}({1})".format(desc,param1))
	return address.add(2)

def doSingleWord(address, desc):
	param1 = getOpcodeWord(address.add(1))
	setEOLComment(address, "{0}({1})".format(desc,param1))
	data = createData(address.add(1),dataTypeDWord)
	return address.add(3)

def doSingleLong(address, desc):
	param1 = getOpcodeLong(address.add(1))
	setEOLComment(address, "{0}({1})".format(desc,param1))
	data = createData(address.add(1),dataTypeInt3)
	return address.add(4)

def doWordByte(address, desc):
	param1 = getOpcodeWord(address.add(1))
	param2 = getOpcodeByte(address.add(3))
	setEOLComment(address, desc+"({0},{1})".format(param1,param2))
	data = createData(address.add(1),dataTypeDWord)
	return address.add(4)

def doByteWordPtr(address, desc):
	param1 = getOpcodeByte(address.add(1))
	param2 = getOpcodeWord(address.add(2))
	setEOLComment(address, desc+"({0},{1:04X})".format(param1,param2))
	# set param2 to dword, add indirecton reference to Bank + value
	data = createData(address.add(2),dataTypeDWord)
	createMemoryReference(data, toAddr(param2+(address.offset&0xFF0000)), RefType.INDIRECTION)
	return address.add(4)

def doLongPtrByte(address, desc):
	param1 = getOpcodeLong(address.add(1))
	param2 = getOpcodeByte(address.add(4))
	setEOLComment(address, desc+"({0:06X},{1})".format(param1,param2))
	# set param1 to int3, add indirecton reference to Bank + value
	data = createData(address.add(1),dataTypeInt3)
	createMemoryReference(data, toAddr(param1), RefType.INDIRECTION)
	return address.add(5)

def doLongPtrWord(address, desc):
	param1 = getOpcodeLong(address.add(1))
	param2 = getOpcodeWord(address.add(4))
	setEOLComment(address, desc+"({0:06X},{1})".format(param1,param2))
	# set param1 to int3, add indirecton reference to Bank + value
	data = createData(address.add(1),dataTypeInt3)
	createMemoryReference(data, toAddr(param1), RefType.INDIRECTION)
	data = createData(address.add(4),dataTypeDWord)
	return address.add(6)	

def doLongPtrLong(address, desc):
	param1 = getOpcodeLong(address.add(1))
	param2 = getOpcodeLong(address.add(4))
	setEOLComment(address,desc+"({0:06X},{1}".format(param1,param2))
	# set param1 to int3, add indirecton reference to Bank + value
	data = createData(address.add(1),dataTypeInt3)
	createMemoryReference(data, toAddr(param1), RefType.INDIRECTION)
	data = createData(address.add(4),dataTypeInt3)
	return address.add(7)

#
# start of script functions
#

def script_setNextSong           (address):
	param1 = getOpcodeByte(address.add(1))
	param2 = getOpcodeByte(address.add(2))
	setEOLComment(address, "setNextSong({0},{1})".format(param1,param2))
	return address.add(3) # skip command + 2 byte params 	
  
def script_unknown1              (address):
	setEOLComment(address, "unknown1")
	return address.add(1) 
  
def script_unknown2              (address):
	setEOLComment(address, "unknown2")
	return address.add(1) 
  
def script_setHour               (address):
	param1 = getOpcodeByte(address.add(1))
	setEOLComment(address, "setHour({0})".format(param1))
	return address.add(2)
  
def script_NOP                   (address):
	setEOLComment(address, "NOP")
	return address.add(1) 
  
def script_SetPlayerPos          (address):
	param1 = getOpcodeWord(address.add(1))
	param2 = getOpcodeWord(address.add(3))
	setEOLComment(address, "setPlayerPos({0},{1})".format(param1,param2))
	return address.add(5)
  
def script_setNextScreen         (address):
	return doSingleByte(address,"setNextScreen")
  
def script_setMoveDirection      (address):
	return doSingleByte(address,"setMoveDirection")
  
def script_clearForcedInput      (address):
	setEOLComment(address, "clearForcedInput")
	return address.add(1) 
  
def script_spawnNewScript        (address):
	param1 = getOpcodeByte(address.add(1))
	param3 = getOpcodeWord(address.add(2))
	setEOLComment(address, "spwanNewScript({0},{1:04X})".format(param1,param3))
	# set param3 to dword, add indirecton reference to Bank + value
	data = createData(address.add(2),dataTypeDWord)
	createMemoryReference(data, toAddr(param3+(address.offset&0xFF0000)), RefType.INDIRECTION)
	return address.add(4)

def script_fadeInScreen          (address):
  	return doSingleByte(address,"fadeInScreen")

def script_setBit                (address):
	return doSingleByte(address,"setBit")
  
def script_testBit               (address):
	return doSingleByte(address,"testBit")
  
def script_unknownd              (address):
  	param1 = getOpcodeByte(address.add(1))
	param2 = getOpcodeByte(address.add(2))
	param3 = getOpcodeByte(address.add(3))
	param4 = getOpcodeByte(address.add(4))
	setEOLComment(address, "spwanNewScript({0},{1},{2},{3})".format(param1,param2,param3,param4))
	return address.add(5)

def script_checkPlayNewSong      (address):
	return doSingleByte(address,"checkPlayNewSong")
  
def script_fadeOut               (address):
	return doSingleByte(address,"fadeOut")
  
def script_unknowne              (address):
  	setEOLComment(address, "unknowne")
	return address.add(1) 

def script_unknownf              (address):
	setEOLComment(address, "unknownf")
	return address.add(1) 
  
def scipt_jumpLong               (address):
	param1 = getOpcodeWord(address.add(1))
	setEOLComment(address, "jumpLong({0:04X})".format(param1))
	# set param1 to dword, add indirecton reference to Bank + value
	data = createData(address.add(1),dataTypeDWord)
	createMemoryReference(data, toAddr(param1+(address.offset&0xFF0000)), RefType.INDIRECTION)
	return address.add(3)
  
def script_unknown11             (address):
	param1 = getOpcodeWord(address.add(1))
	setEOLComment(address, "unknown11({0:04X})".format(param1))
	return address.add(3)
  
def script_testFlagsAndBranch    (address):
	param1 = getOpcodeLong(address.add(1))
	param2 = getOpcodeByte(address.add(4))
	param3 = getOpcodeWord(address.add(5))
	setEOLComment(address, "testFlagsAndBranch({0:06X},{1},{2:04X})".format(param1,param2,param3))
	# set param1 address to int3, add read reference
	data = createData(address.add(1),dataTypeInt3)
	createMemoryReference(data, toAddr(param1), RefType.READ)
	# set param3 to dword, add indirecton reference to Bank + value
	data = createData(address.add(5),dataTypeDWord)
	createMemoryReference(data, toAddr(param3+(address.offset&0xFF0000)), RefType.INDIRECTION)
	return address.add(7)
  
def script_addrEqualsBranch      (address):
	param1 = getOpcodeLong(address.add(1))
	param2 = getOpcodeByte(address.add(4))
	param3 = getOpcodeWord(address.add(5))
	setEOLComment(address, "addrEqualsBranch({0:06X},{1},{2:04X})".format(param1,param2,param3))
	# set param1 address to int3, add read reference
	data = createData(address.add(1),dataTypeInt3)
	createMemoryReference(data, toAddr(param1), RefType.READ)
	# set param3 to dword, add indirecton reference to Bank + value
	data = createData(address.add(5),dataTypeDWord)
	createMemoryReference(data, toAddr(param3+(address.offset&0xFF0000)), RefType.INDIRECTION)
	return address.add(7)
  
def script_addrInRangeBranch     (address):
	param1 = getOpcodeLong(address.add(1))
	param2 = getOpcodeByte(address.add(4))
	param3 = getOpcodeByte(address.add(5))
	param4 = getOpcodeWord(address.add(6))
	setEOLComment(address, "addrInRangeBranch({0:06X},{1},{2},{3:04X})".format(param1,param2,param3,param4))
	# set param1 address to int3, add read reference
	data = createData(address.add(1),dataTypeInt3)
	createMemoryReference(data, toAddr(param1), RefType.READ)
	# set param4 to dword, add indirecton reference to Bank + value
	data = createData(address.add(6),dataTypeDWord)
	createMemoryReference(data, toAddr(param4+(address.offset&0xFF0000)), RefType.INDIRECTION)
	return address.add(8)
  
def script_getRandomNumberInRange(address):
	return doSingleByte(address,"getRandomNumberInRange")
  
def script_cmpSetValue           (address):
	return doByteWordPtr(address,"cmpSetValueBranch")
	
def script_setAnimAndFlip        (address):
	return doWordByte(address,"setAnimFlip")
  
def script_unknown18             (address):
	param1 = getOpcodeWord(address.add(1))
	param2 = getOpcodeWord(address.add(3))
	param3 = getOpcodeWord(address.add(5))
	param4 = getOpcodeByte(address.add(7))
	setEOLComment(address, "unknown18({0},{1},{2},{3})".format(param1,param2,param3,param4))
	return address.add(8)

def script_unknown19             (address):
	return doWordByte(address,"unknown19")
  
def script_showMSGBox            (address):
	return doWordByte(address,"showMsgBox_1a")
  
def script_showMSGBoxIncState    (address):
	return doWordByte(address,"showMsgBoz_incState")
  
def script_unknown1c             (address):
	param1 = getOpcodeWord(address.add(1))
	setEOLComment(address, "unknown1C({0:04X})".format(param1))
	return address.add(3)

def script_unknown1d             (address):
	param1 = getOpcodeWord(address.add(1))
	setEOLComment(address, "unknown1D({0:04X})".format(param1))
	return address.add(3)
  
def script_branchOnMsgBoxSel     (address):
	return doByteWordPtr(address, "branchOnMsgBoxSel")
  
def script_addSignedByteTo       (address):
	param1 = getOpcodeLong(address.add(1))
	param2 = getByte(address.add(4))
	setEOLComment(address, "addSignedByteTo({0:06X},{1})".format(param1,param2))
	return address.add(5)
  
def script_unknown1e             (address):
	param1 = getOpcodeByte(address.add(1))
	param2 = getOpcodeByte(address.add(2))
	param3 = getOpcodeByte(address.add(3))
	param4 = getOpcodeWord(address.add(4))
	param5 = getOpcodeByte(address.add(6))
	setEOLComment(address, "unkown1D({0},{1},{2},{3},{4})".format(param1,param2,param3,param4,param5))
	return address.add(7)
  
def script_setBitAt              (address):
	return doLongPtrByte(address,"setBitAt")
  
def script_setPalForHour         (address):
	return doSingleByte(address,"setPalForHour")
  
def script_unknown21             (address):
	return doByteWordPtr(address, "unknown21")
  
def script_clearBitAt            (address):
	return doLongPtrByte(address,"clearBitAt")
  
def script_setHVScrollDetla      (address):
	param1 = getOpcodeWord(address.add(1))
	param2 = getOpcodeWord(address.add(3))
	param3 = getOpcodeByte(address.add(5))
	setEOLComment(address, "unkown1D({0},{1},{2})".format(param1,param2,param3))
	return address.add(6)
  
def script_unknown26             (address):
	return doSingleWord(address,"unknown26")
  
def script_unknown27             (address):
	return doWordByte(address,"unknown27")
  
def script_unknown28             (address):
	param1 = getOpcodeByte(address.add(1))
	param2 = getOpcodeWord(address.add(2))
	param3 = getOpcodeByte(address.add(4))
	setEOLComment(address, "unkown28({0},{1},{2})".format(param1,param2,param3))
	return address.add(5)
  
def script_unknown29             (address):
	param1 = getOpcodeWord(address.add(1))
	param2 = getOpcodeWord(address.add(3))
	setEOLComment(address, "checkTalkorGiveItem({0},{1})".format(param1,param2))
	data = createData(address.add(1),dataTypeDWord)
	createMemoryReference(data, toAddr(param1+(address.offset&0xFF0000)), RefType.INDIRECTION)
	data = createData(address.add(3),dataTypeDWord)
	createMemoryReference(data, toAddr(param2+(address.offset&0xFF0000)), RefType.INDIRECTION)
	return address.add(5)
  
def sctipt_unknown2A                 (address):
	param1 = getOpcodeByte(address.add(1))
	param2 = getOpcodeWord(address.add(2))
	param3 = getOpcodeByte(address.add(4))
	setEOLComment(address, "unkown2A({0},{1},{2})".format(param1,param2,param3))
	return address.add(5)
  
def script_setChickenPosition    (address):
	return doSingleWord(address,"setChickenPosition")
  
def script_pickupOrHoldChicken   (address):
	setEOLComment(address, "pickupOrHoldChicken")
	return address.add(1) 
  
def somethingSetCowPosAndAction  (address):
	setEOLComment(address, "somethingSetCowPosAndAction")
	return address.add(1) 
  
def script_writeWordToAddress    (address):
	return doLongPtrWord(address, "writeWordToAddress")
  
def script_pickupMole            (address):
	setEOLComment(address, "pickupMole")
	return address.add(1) 
  
def script_pickupFish            (address):
	setEOLComment(address, "pickupFish")
	return address.add(1)
  
def script_unknown31             (address):
	return doSingleByte(address,"unknown31")
  
def script_hugDog                (address):
	return doSingleByte(address,"hugDog")
  
def script_playAnimFromStructData(address):
	setEOLComment(address, "playAnimFromStructData")
	return address.add(1)
  
def script_unknown34             (address):
	setEOLComment(address, "unknown34")
	return address.add(1)
  
def script_setForceMoveDirection (address):
	param1 = getOpcodeByte(address.add(1))
	param2 = getOpcodeByte(address.add(2))
	param3 = getOpcodeByte(address.add(3))
	param4 = getOpcodeByte(address.add(4))
	setEOLComment(address, "setForceMoveDirection({0},{1},{2},{3})".format(param1,param2,param3,param4))
	return address.add(5)
  
def setForceMovementWithBButton  (address):
	param1 = getOpcodeByte(address.add(1))
	param2 = getOpcodeByte(address.add(2))
	param3 = getOpcodeByte(address.add(3))
	param4 = getOpcodeByte(address.add(4))
	setEOLComment(address, "setForceMovementWithBButton({0},{1},{2},{3})".format(param1,param2,param3,param4))
	return address.add(5)

def script_setCarryItem          (address):
	return doSingleByte(address,"setCarryItem")
  
def script_setSamllHouseNext     (address):
	setEOLComment(address, "setSamllHouseNext")
	return address.add(1)
  
def script_setNextScreenToLoad   (address):
	return doSingleByte(address,"setNextScreenToLoad")
  
def script_pickUpItem            (address):
	return doSingleByte(address,"pickUpItem")
  
def script_setAnimStateToThrow   (address):
	setEOLComment(address, "setAnimStateToThrow")
	return address.add(1)
  
def script_unknown42             (address):
	setEOLComment(address, "unknown42")
	return address.add(1)
  
def script_addWordToLongClip0_999(address):
	return doLongPtrWord(address, "addWordToLongClip0_999")
  
def script_AddLongOfMoney        (address):
	return doLongPtrLong(address, "addLongOfMoney")
  
def script_BEQWord               (address):
	param1 = getOpcodeLong(address.add(1))
	param2 = getOpcodeWord(address.add(4))
	param3 = getOpcodeWord(address.add(6))
	setEOLComment(address, "BEQWord ({0:06X},{1},{2:04X})".format(param1,param2,param3))
	return address.add(8)
  
def script_BEQlong               (address):
	param1 = getOpcodeLong(address.add(1))
	param2 = getOpcodeLong(address.add(4))
	param3 = getOpcodeWord(address.add(7))
	setEOLComment(address, "BEQWord ({0:06X},{1},{2:04X})".format(param1,param2,param3))
	return address.add(9)
  
def script_inRangeWord           (address):
	param1 = getOpcodeLong(address.add(1))
	param2 = getOpcodeWord(address.add(4))
	param3 = getOpcodeWord(address.add(6))
	param4 = getOpcodeWord(address.add(8))
	setEOLComment(address, "inRangeWord ({0:06X},{1},{2},{3:04X})".format(param1,param2,param3,param4))
	# set param1 address to int3, add read reference
	data = createData(address.add(1),dataTypeInt3)
	createMemoryReference(data, toAddr(param1), RefType.READ)
	# set param4 to dword, add indirecton reference to Bank + value
	data = createData(address.add(4),dataTypeDWord)
	data = createData(address.add(6),dataTypeDWord)
	data = createData(address.add(8),dataTypeDWord)
	createMemoryReference(data, toAddr(param4+(address.offset&0xFF0000)), RefType.INDIRECTION)
	return address.add(10)
  
def script_inRangeLong           (address):
	param1 = getOpcodeLong(address.add(1))
	param2 = getOpcodeLong(address.add(4))
	param3 = getOpcodeLong(address.add(7))
	param4 = getOpcodeWord(address.add(10))
	setEOLComment(address, "inRangeWord ({0:06X},{1},{2},{3:04X})".format(param1,param2,param3,param4))
	# set param1 address to int3, add read reference
	data = createData(address.add(1),dataTypeInt3)
	createMemoryReference(data, toAddr(param1), RefType.READ)
	# set param4 to dword, add indirecton reference to Bank + value
	data = createData(address.add(4),dataTypeInt3)
	data = createData(address.add(7),dataTypeInt3)
	data = createData(address.add(10),dataTypeDWord)
	createMemoryReference(data, toAddr(param4+(address.offset&0xFF0000)), RefType.INDIRECTION)
	return address.add(12)
  
def script_writeByteTo           (address):
	return doLongPtrByte(address, "writeByteTo")
  
def script_writeLongTo           (address):
	return doLongPtrLong(address, "writeLongTo")
  
def script_jsrScripInBankB3      (address):
	param1 = getOpcodeWord(address.add(1))
	setEOLComment(address, "jsrScripInBankB3({0:04X})".format(param1))
	return address.add(3)
  
def script_pickupPowerBerry      (address):
	setEOLComment(address, "pickupPowerBerry")
	return address.add(1)
  
def script_plotTile              (address):
	param1 = getOpcodeByte(address.add(1))
	param2 = getOpcodeWord(address.add(2))
	param3 = getOpcodeWord(address.add(4))
	setEOLComment(address, "plotTile({0},{1},{2})".format(param1,param2,param3))
	return address.add(6)
  
def script_unknown4e             (address):
	setEOLComment(address, "unknown4e")
	return address.add(1)
  
def script_unknown4f             (address):
	param1 = getOpcodeWord(address.add(1))
	setEOLComment(address, "checkBlueFeather({0:04X})".format(param1))
	data = createData(address.add(1),dataTypeDWord)
	createMemoryReference(data, toAddr(param1+(address.offset&0xFF0000)), RefType.INDIRECTION)
	return address.add(3)
  
def script_unknown50             (address):
	setEOLComment(address, "unknown50")
	return address.add(1)
  
def script_unknown51             (address):
	setEOLComment(address, "unknown51")
	return address.add(1)
  
def script_unknown52             (address):
	setEOLComment(address, "unknown52")
	return address.add(1)
  
def script_unknown53             (address):
	setEOLComment(address, "unknown53")
	return address.add(1)
  
def script_unknown54             (address):
	setEOLComment(address, "unknown54")
	return address.add(1)
  
def script_unknown55             (address):
	setEOLComment(address, "unknown55")
	return address.add(1)
  
def script_unknown56             (address):
	return doWordByte(address,"unknown56")
  
def script_unknown57             (address):
	return doLongPtrByte(address, "unknown57")
  
def script_useToolInHand         (address):
	setEOLComment(address, "useToolInHand")
	return address.add(1)
  
def script_addStamina            (address):
	param1 = getByte(address.add(1))
	setEOLComment(address, "addStamina({0})".format(param1))
	return address.add(2)
  
def script_addTileToFarmAtXY     (address):
	param1 = getOpcodeByte(address.add(1))
	param2 = getOpcodeWord(address.add(2))
	param3 = getOpcodeWord(address.add(4))
	setEOLComment(address, "plotTile({0},{1},{2})".format(param1,param2,param3))
	return address.add(6)
  
def setAnimModeToShowToolInHand  (address):
	setEOLComment(address, "AnimModeToShowToolInHand")
	return address.add(1)
  
# CODE START
commentFuncs = [
	script_setNextSong           , #0 
	script_unknown1              , #1 
	script_unknown2              , #2 
	script_setHour               , #3 
	script_NOP                   , #4 
	script_SetPlayerPos          , #5 
	script_setNextScreen         , #6 
	script_setMoveDirection      , #7 
	script_clearForcedInput      , #8 
	script_spawnNewScript        , #9 
	script_fadeInScreen          , #A 
	script_setBit                , #B 
	script_testBit               , #C 
	script_unknownd              , #D 
	script_checkPlayNewSong      , #E 
	script_fadeOut               , #F 
	script_unknowne              , #10 
	script_unknownf              ,  
	scipt_jumpLong               ,  
	script_unknown11             ,  
	script_testFlagsAndBranch    ,  
	script_addrEqualsBranch      ,  
	script_addrInRangeBranch     ,  
	script_getRandomNumberInRange,  
	script_cmpSetValue           ,  
	script_setAnimAndFlip        ,  
	script_unknown18             , #1A 
	script_unknown19             ,  
	script_showMSGBox            ,  
	script_showMSGBoxIncState    ,  
	script_unknown1c             ,  
	script_unknown1d             ,  
	script_branchOnMsgBoxSel     , #20 
	script_addSignedByteTo       ,  
	script_unknown1e             ,  
	script_setBitAt              ,  
	script_setPalForHour         ,  
	script_unknown21             ,  
	script_clearBitAt            ,  
	script_clearBitAt            ,  
	script_clearBitAt            ,  
	script_setHVScrollDetla      ,  
	script_unknown26             , #2A 
	script_unknown27             ,  
	script_unknown28             ,  
	script_unknown29             ,  
	sctipt_unknown2A             ,  
	script_setChickenPosition    ,  
	script_pickupOrHoldChicken   , #30 
	somethingSetCowPosAndAction  ,  
	script_writeWordToAddress    ,  
	script_pickupMole            ,  
	script_pickupFish            ,  
	script_unknown31             ,  
	script_hugDog                ,  
	script_playAnimFromStructData,  
	script_unknown34             ,  
	script_setForceMoveDirection ,  
	setForceMovementWithBButton  ,  
	script_setCarryItem          ,  
	script_setSamllHouseNext     ,  
	script_setNextScreenToLoad   ,  
	script_pickUpItem            ,  
	script_setAnimStateToThrow   ,  
	script_unknown42             ,  
	script_addWordToLongClip0_999,  
	script_AddLongOfMoney        ,  
	script_BEQWord               ,  
	script_BEQlong               ,  
	script_inRangeWord           ,  
	script_inRangeLong           ,  
	script_writeByteTo           ,  
	script_writeLongTo           ,  
	script_jsrScripInBankB3      ,  
	script_pickupPowerBerry      ,  
	script_plotTile              ,  
	script_unknown4e             ,  
	script_unknown4f             ,  
	script_unknown50             ,  
	script_unknown51             ,  
	script_unknown52             ,  
	script_unknown53             ,  
	script_unknown54             ,  
	script_unknown55             ,  
	script_unknown56             ,  
	script_unknown57             ,  
	script_useToolInHand         ,  
	script_addStamina            ,  
	script_addTileToFarmAtXY     ,  
	setAnimModeToShowToolInHand  
]

start = state.currentSelection.minAddress
end = state.currentSelection.maxAddress

while start.offset < end.offset:
	command = getOpcodeByte(start)
	print("{0:06X},{1:02X}".format(start.offset,command))
	start = commentFuncs[command](start)
	
