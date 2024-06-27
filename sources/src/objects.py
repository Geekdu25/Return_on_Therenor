from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

class Lit():
	def __init__(self):
		self.object = loader.loadModel("../models/lit.bam")
		self.col = CollisionNode("lit")
		self.col.addSolid(CollisionBox((0, 0, 0), 40, 40, 10))
		self.col.setFromCollideMask(BitMask32.allOff())
		self.col.setIntoCollideMask(BitMask32.bit(0)) 
		self.col_np = self.object.attachNewNode(self.col)

