#TODO write a description for this script
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 

from SwingLib import getJavaRGBFromRGB
from SNESLib import convert8x8_4bitToPalNums, convertSNESPaletteToRGB, getWordData
from HarvestMoonUncompress import uncompress


from javax.swing import JFrame, JPanel
from java.awt import Canvas, Color, BorderLayout
from java.awt.image import BufferedImage

tilesAddress = 0x98cc6b #0x9fef97
#base is a89400 then 200 each 
palAddresss = 0xa9da00+16

class SimpleComponent(Canvas):
	def create(self, tileData, palette):
		self.bi = BufferedImage(16*8,16*8,BufferedImage.TYPE_INT_ARGB)
		rows = len(tileData)/16
		for r in range(rows):
			for c in range(16):
					base = (r*16)+c
					tile = tiles[base]
					for y in range(8):
						for x in range(8):
							index = (y*8)+x
							p = tile[index]
							px = x+(c*8)
							py = y+(r*8)
							# print("settting ({0},{1}) to ".format(px,py))
							self.bi.setRGB(px,py,palette[p])
	
	def paint(self, graphics):
		#print("paint")
		graphics.drawImage(self.bi, 0,0, 16*8,16*8,Color.red, None)

bytes,size = uncompress(toAddr(tilesAddress))

palette = []
palAddr = toAddr(palAddresss)

for p in range(256):
	(r,g,b) = convertSNESPaletteToRGB(getWordData(palAddr))
	palAddr = palAddr.add(2)
	palette.append(int(getJavaRGBFromRGB(r,g,b)))

#for i in range(0, len(bytes), 16):
#	strings = ["{0:02X}".format(bytes[i+o]) for o in range(16)]
#	print(' '.join(strings))

numTiles = len(bytes)/32
tiles = []
for t in range(numTiles):
	offset = t*32
	tile = convert8x8_4bitToPalNums(bytes[offset:offset+32])
	tiles.append(tile)

#for i in range(0, 64, 8):
#	strings = ["{0:02X}".format(tile[i+o]) for o in range(8)]
#	print(' '.join(strings))

#print(palette)

frame = JFrame() # don't call constructor with "new"
frame.setSize(200,200+22)
frame.setLocation(200, 200)
frame.setTitle("test")

panel = JPanel(layout=BorderLayout())
sc = SimpleComponent()
sc.create(tiles,palette)
panel.add(sc, BorderLayout.CENTER)
frame.add(panel)

#frame.setLayout(None)
frame.setVisible(True)
#frame.getContentPane().repaint()

#print(str(Color.red.getRGB()))
