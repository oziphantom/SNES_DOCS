#TODO write a description for this script
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 


#TODO Add User Code Here



data = ("enum eItemInHand {"
	"eHandItem_none = 0"
	",eHandItem_sickle = 1"
	",eHandItem_hoe = 2"
	",eHandItem_hammer = 3"
	",eHandItem_axe = 4"
	",eHandItem_cornSeeds =5"
	",eHandItem_tomatoSeeds = 6"
	",eHandItem_potatoeSeeds = 7"
	",eHandItem_turnipSeeds = 8"
	",eHandItem_cowMedicine = 9"
	",eHandItem_cowIcon = 10"
	",eHandItem_bell = 11"
	",eHandItem_grassSeeds = 12"
	",eHandItem_paint = 13"
	",eHandItem_milker = 14"
	",eHandItem_brush = 15"
	",eHandItem_wateringCan = 16"
	",eHandItem_goldSickle = 17"
	",eHandItem_goldHoe = 18"
	",eHandItem_goldHammer = 19"
	",eHandItem_goldAxe = 20"
	",eHandItem_sprinkler = 21"
	",eHandItem_bean = 22"
	",eHandItem_gem = 23"
	",eHandItem_blueFeather = 24"
	",eHandItem_chickenFeed = 25"
	",eHandItem_cowFeed = 26"
	"};")

from ghidra.app.util.cparser.C import CParser
from ghidra.program.model.data import DataTypeConflictHandler

dtm = currentProgram.getDataTypeManager()
parser = CParser(dtm)
new_dt = parser.parse(data)
new_dt.setLength(1); 
transaction = dtm.startTransaction("Adding new data")
dtm.addDataType(new_dt, None)
dtm.endTransaction(transaction, True)
