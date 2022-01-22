#Set DBR to 00 for SNES
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 

from java.math import BigInteger
val = BigInteger.valueOf(0x00);

if state.currentSelection == None:
	start = state.currentAddress
	end = state.currentAddress
else:
	start = state.currentSelection.getMinAddress()
	end = state.currentSelection.getMaxAddress()
pCon = getCurrentProgram().getProgramContext()
reg = pCon.getRegister("DBR")
pCon.setValue(reg,start,end,val);


