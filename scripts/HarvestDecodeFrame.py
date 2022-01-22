#TODO write a description for this script
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 

from math import floor
import threading

from SwingLib import getJavaRGBFromRGB
from SNESLib import convert8x8_4bitToPalNums, convertSNESPaletteToRGB, getWordData, getByteData, getLongData
from HarvestMoonUncompress import uncompress


from javax.swing import JFrame, JPanel, JButton, JLabel
from java.awt import Canvas, Color, BorderLayout
from java.awt.image import BufferedImage

class MyThread(threading.Thread):
	def __init__(self, event, owner):
		threading.Thread.__init__(self)
		self.stopped = event
		self.owner = owner

	def run(self):
		timeValue = (1.0/60.0)*30.0
		#print("timeValue = " + str(timeValue))
		while not self.stopped.wait(timeValue):
			#print("my thread")
			self.owner.nextFrame(None)


class Logic:
	def create(self):
		palRaw = [0xEF,0x29,0xFA,0x26,0x56,0x1A,0xB0,0x0D,0xBB,0x00,0x94,0x52,0xA0,0x69,0xC0,0x4C,
				  0x6E,0x1D,0x2C,0x11,0x7F,0x5B,0x1E,0x47,0x17,0x22,0x08,0x21,0xC6,0x14,0xBD,0x77]
		palette = []

		for p in range(16):
			(r,g,b) = convertSNESPaletteToRGB(palRaw[p*2]+(palRaw[(p*2)+1]<<8))
			palette.append(int(getJavaRGBFromRGB(r,g,b)))
		self.palette = palette

		self.animNum = 0x90
		self.frameNum = 0
		self.maxFrames = 0

		frame = JFrame() # don't call constructor with "new"
		frame.setSize(600,600+22)
		frame.setLocation(300, 300)
		frame.setTitle("test")

		self.panel = JPanel(layout=BorderLayout())
		self.sc = SimpleComponent()
		self.sc.create(0x86a57f,self.palette)
		self.panel.add(self.sc, BorderLayout.CENTER)
		frame.add(self.panel)

		button = JButton("next anim", actionPerformed=self.nextAnim)
		frame.add(button, BorderLayout.SOUTH)
		button = JButton("next frame", actionPerformed=self.nextFrame)
		frame.add(button, BorderLayout.NORTH)
		label = JLabel("test")
		frame.add(label, BorderLayout.LINE_END)
		self.label = label
		
		self.stopFlag = threading.Event()
		self.stopFlag.clear()
		thread = MyThread(self.stopFlag, self)
		thread.start()
		self.worker = thread
		#frame.setLayout(None)
		frame.setVisible(True)
		self.frame = frame
		frame.windowClosing = self.windowClosing

	def windowClosing(self, event):
		self.stopFlag.set()
		self.worker.join()
		print("window closed")

	def getAnimPointer(self):
		if self.animNum > 0x262:
			offset = ((self.animNum-0x262)*2) + 0x878080
		else:
			offset = (self.animNum*2) + 0x868080
		

		print("to anim pointer = {0:06X}".format(offset))
		ptr = getWordData(toAddr(offset))
		ptr += 0x860000
		if self.animNum > 0x262:
			ptr += 0x010000
		print("anim pointer = {0:06X}".format(ptr))
		return ptr 

	def getFramePointer(self):
		ptr = self.getAnimPointer()
		aPtr = getWordData(toAddr(ptr+(self.frameNum*3)))
		if aPtr != 0:
			aPtr += 0x860000
			if self.animNum > 0x262:
				aPtr += 0x010000
		print("frame pointer = {0:06X}".format(aPtr))
		return aPtr

	def updateFrame(self, pointer):
		self.sc.create(pointer,self.palette)
		self.label.text = "{0},{1}".format(self.animNum, self.frameNum)
		#self.sc.size = (self.sc.imageWidth+1,self.sc.imageHeight+1)
		#self.panel.size = (600,622)
		#self.sc.size = (self.sc.imageWidth,self.sc.imageHeight)
		self.sc.repaint()

	def actionPerformed(self, action):
		self.nextFrame(None)

	def nextAnim(self, event):
		self.animNum += 1
		self.frameNum = 0
		self.updateFrame(self.getFramePointer())

	def nextFrame(self, event):
		print("frame = "+str(self.frameNum))
		# first get the pointer for the anim data
		self.frameNum += 1
		pFrame = self.getFramePointer()
		if pFrame == 0:
			self.frameNum = 0
			pFrame = self.getFramePointer()
		print("frame = "+str(self.frameNum))
		self.updateFrame(pFrame)

class SimpleComponent(Canvas):
	def create(self, metaSprite, palette):
		self.imageWidth = 16*8*4
		self.imageHeight = 16*8*4
		self.bi = BufferedImage(self.imageWidth,self.imageHeight,BufferedImage.TYPE_INT_ARGB)
		self.setToFrame(metaSprite, palette)

	def setToFrame(self, metaSprite, palette):
		for y in range(self.imageHeight):
			for x in range(self.imageHeight):
				self.bi.setRGB(x,y,palette[0])
		offset = 64
		parts = getByteData(toAddr(metaSprite))
		metaSprite += 1
		subSpriteOffsts = [0,0x20,0x200,0x220]
		subSpriteX = [0,8,0,8]
		subSpriteY = [0,0,8,8]
		for r in range(parts):
			tileNum = getWordData(toAddr(metaSprite))
			xDelta = getByte(toAddr(metaSprite+2)) #I want these signed bytes
			yDelta = getByte(toAddr(metaSprite+3)) #I want these signed bytes
			print("tile num {0}, xDelta {1}, yDelta {2}".format(tileNum, xDelta, yDelta))
			metaSprite += 5
			bankOffset = int(floor(tileNum/256))
			r = int(floor((tileNum % 256) / 8))
			c = (tileNum % 8)
			print("bank offset {0}, r {1}, c {2}".format(bankOffset, r, c))
			# 8x8 = 32 bytes
			# 16x16 = 128 bytes
			# stored in rows of 8 16x16 = 1024bytes or 0x400
			# to get next row its 0x200
			base = 0x888000
			for sub in range(4):
				tileAddr = toAddr(base + (bankOffset<<16) + (r*0x400) + (c*64)+subSpriteOffsts[sub])
				print("tile address {0:06X}".format(tileAddr.offset))
				tileData = []
				for d in range(32):
					tileData.append(getByteData(tileAddr))
					tileAddr = tileAddr.add(1)
				tile = convert8x8_4bitToPalNums(tileData)
				for y in range(8):
					for x in range(8):
						index = (y*8)+x
						p = tile[index]
						if p > 0:
							px = (x+offset+xDelta+subSpriteX[sub])*4
							py = (y+offset+yDelta+subSpriteY[sub])*4
							# print("settting ({0},{1}) to ".format(px,py))
							for spy in range(4):
								for spx in range(4):
									self.bi.setRGB(px+spx,py+spy,palette[p])
	
	def paint(self, graphics):
		#print("paint")
		graphics.drawImage(self.bi, 0,0, 16*8*4,16*8*4,Color.red, None)

logic = Logic()
logic.create()
