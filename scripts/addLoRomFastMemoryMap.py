#TODO write a description for this script
#@author 
#@category SNES
#@keybinding 
#@menupath 
#@toolbar 


memory = currentProgram.getMemory()
# add WRAM and PPU
memory.createUninitializedBlock("WRAM",toAddr(0x7e0000),0x20000,False)
memory.createUninitializedBlock("PPU1", toAddr(0x2000),0x200, False)
memory.createUninitializedBlock("PPU2", toAddr(0x2400),0x300, False)
memory.createUninitializedBlock("CPU1", toAddr(0x4000),0x18, False)
memory.createUninitializedBlock("CPU2", toAddr(0x4200),0x20, False)
memory.createUninitializedBlock("DMAR", toAddr(0x4300),0x80, False)

fb = memory.getAllFileBytes()

#for fast
#for bank in range(0,0x80):
#    name = "Bank{0:2X}".format(bank+0x80);
#    offset = bank * 0x8000
#    memory.createInitializedBlock(name, toAddr((bank*0x10000)+0x808000), fb[0], offset, 0x8000, False)

#for slow   
for bank in range(0,64):
    name = "Bank{0:2X}".format(bank);
    offset = bank * 0x8000
    memory.createInitializedBlock(name, toAddr((bank*0x10000)+0x008000), fb[0], offset, 0x8000, False)
