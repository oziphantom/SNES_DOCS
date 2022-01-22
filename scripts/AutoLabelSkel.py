#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 

BaseName = "InvPal_{0}"
Delta = 1

start = state.currentSelection.minAddress
end = state.currentSelection.maxAddress

print("{0}-{1}".format(start, end))

counter = 0
while start.getOffset() <= end.getOffset():
	createLabel(start,BaseName.format(counter), True)
	start = start.add(Delta)
	print(start)
	counter += 1

