#gets all refrences, if they are an R, looks them up and fixed them
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 

from  ghidra.program.model.symbol import RefType
from SNESLib import *

cA = state.currentAddress


refs = getReferencesTo(cA)

for r in refs:
	if r.getReferenceType() == RefType.READ:
		dest = r.getFromAddress()
		DP = getDPVal(dest)
		DBR = getDBRVal(dest)
		AddReferenceForInstructionAtAddress(dest, DBR, DP)
		


