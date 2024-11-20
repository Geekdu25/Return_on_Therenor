from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

class Lit():
	"""
	Un lit.
	"""
	def __init__(self):
		"""
		Méthode constructeur.
		----------------------
		return -> Lit
		"""
		self.object = loader.loadModel("lit.bam")
		self.object.setScale(15)
		self.col = CollisionNode("lit")
		self.col.addSolid(CollisionBox((0, 0, 0), 4, 3.5, 1))
		self.col.setFromCollideMask(BitMask32.allOff())
		self.col.setIntoCollideMask(BitMask32.bit(0)) 
		self.col_np = self.object.attachNewNode(self.col)

class Bateau():
	"""
	Un bateau.
	"""
	def __init__(self):
		"""
		Méthode constructeur.
		----------------------
		return -> Bateau
		"""
		self.object = loader.loadModel("bateau.bam")
		self.object.setScale(30)
		self.col = CollisionNode("bateau")
		self.col.addSolid(CollisionBox((0, 0, 0), 4, 3.5, 1))
		self.col.setFromCollideMask(BitMask32.allOff())
		self.col.setIntoCollideMask(BitMask32.bit(0)) 
		self.col_np = self.object.attachNewNode(self.col)
