#TODO write a description for this script
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 
from __main__ import * #bring in the ghidra flat

from SNESLib import getWordData, getLongData

def getStringFromPtr(start):

	easy = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'!.?\"/,()%-~&:"

	LUT = {}
	PRE_LUT = {}

	for a in range(len(easy)):
		LUT[a] = easy[a]
		PRE_LUT[a] = easy[a]


	LUT[0x42] = "<3"
	PRE_LUT[0x42] = "<3"
	# LUT[0x41] = ":"
	# PRE_LUT[0x41] = ":"
	LUT[0xa2] = "\\BR"
	PRE_LUT[0xa2] = "<b>\r\n"
	LUT[0xb1] = "' '"
	PRE_LUT[0xb1] = " "

	easy = "0123456789"
	for a in range(len(easy)):
		LUT[0xb2+a] = easy[a]
		PRE_LUT[0xb2+a] = easy[a]

	plateAddr = start
	full = ""
	fullCounter = 0
	while True:
		value = getWordData(start)
		if value == 0xffff:
			break
		if value == 0xFFFE: #menu selection
			start = start.add(2)
			value = getWordData(start)
			full += "<menu {0:04X}>".format(value)
			break
		# FFED = name string
			# 4 b = dog
			# 4 f = horse
		# FFEC = number string
			# 7 8 = current money or 7 9 hmm
		if value in LUT:
			setEOLComment(start, LUT[value])
			full += PRE_LUT[value]	
			fullCounter += 1
			if fullCounter == 28:
				full += "\n"
				fullCounter = 0
			if value == 0xa2:
				fullCounter = 0
		else:
			full +="<{0:04X}>".format(value)
		start = start.add(2)

	return full

def getStringFromNumber(num):
	ptr = toAddr(0x839bf6+(num*3))
	start = toAddr(getLongData(ptr))
	return getStringFromPtr(start)