from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
base = ShowBase()
model = loader.loadModel("Village.bam")
#mon_modèle.setHpr(0, 270, 180)
a = model.find("**/stems_3_713_1")
a.node().removeAllChildren()
a.removeNode()
model.reparentTo(render)
render.setLight(render.attachNewNode(AmbientLight("alight")))
model.writeBamFile("Village.bam")
base.run()

