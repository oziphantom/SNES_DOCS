#TODO write a description for this script
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 

from javax.swing import JFrame, JPanel
from java.awt import Color

from SNESLib import convertSNESPaletteToRGB, getWordData
blockSize = 25

currAddr = state.currentAddress


frame = JFrame() # don't call constructor with "new"
frame.setSize(blockSize*17,(blockSize*17)+22)
frame.setLocation(200, 200)
frame.setTitle("SNES Pallete - 256 @{0:06X}".format(currAddr.offset))



for y in range(16):
	for x in range(16):
		pal = getWordData(currAddr)
		r,g,b = convertSNESPaletteToRGB(pal)
				
		panel = JPanel();
		panel.setBounds(x*blockSize,y*blockSize,blockSize,blockSize)
		panel.setBackground(Color(r,g,b))
		frame.add(panel)
		currAddr = currAddr.add(2)

frame.setLayout(None)
frame.setVisible(True)