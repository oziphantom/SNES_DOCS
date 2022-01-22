def getJavaRGBFromRGB(r,g,b):
	val = 0xff000000|(r<<16)|(g<<8)|b
	val = -0x100000000 + val
	return val
