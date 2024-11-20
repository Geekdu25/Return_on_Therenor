from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeoMipTerrain
base = ShowBase()
terrain = GeoMipTerrain("worldTerrain") # create a terrain
terrain.setHeightfield("heightmap.png") # set the height map
terrain.setColorMap("texturemap.png")   # set the colour map
terrain.setBruteforce(True)             # level of detail
root = terrain.getRoot()                # capture root
root.reparentTo(render)                 # render from root
root.setSz(60)                          # maximum height
terrain.generate()                      # generate terrain
root.writeBamFile('world.bam')  
base.run()
