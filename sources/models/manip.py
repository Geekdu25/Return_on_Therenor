from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
def write():
	model.writeBamFile("lit.bam")
loadPrcFileData("", "want-directtools #t")
loadPrcFileData("", "want-tk #t")
base = ShowBase()
model = loader.loadModel("maison_terenor.bam")
#------------------Changer l'orientation d'un modèle----------------------
"mon_modèle.setHpr(0, 270, 180)"
#--------------------Trouver un objet du modèle et le supprimer-------------
"""a = model.find("**/chaussette_128_226_1")
a.node().removeAllChildren()
a.removeNode()
a = model.find("**/Plane_321_183_1")
a.node().removeAllChildren()
a.removeNode()"""
#----------------Changer la taille d'un modèle------------------
"model.setScale(22)"
model.reparentTo(render)
#render.setLight(render.attachNewNode(AmbientLight("alight")))
base.accept("a", write)
base.run()

