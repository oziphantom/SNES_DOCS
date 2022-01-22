#TODO write a description for this script
#@author oziphantom
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 


#TODO Add User Code Here

addr = state.currentAddress

while True:
	local = addr
	print(local)
	thisValue = getUndefinedDataAt(local)
	local = local.next()
	nextValue = getUndefinedDataAt(local)
	local = local.next()
	nextNextValue = getUndefinedDataAt(local)
	if (nextNextValue == None) and (thisValue.getValue().getValue() == 0x0) and (nextValue.getValue().getValue() == 0x0):
		createWord(addr)
		print("made word")
		addr = local
		while True:
			local = local.next()
			if local is None:
				addr = None
				break
			else:
				if getUndefinedDataAt(local) is not None:
					addr = local
					break
	else:
		break

		
	
