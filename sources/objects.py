from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor

class Lit:
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

class Bateau:
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

class Coffre:
	"""
	Un coffre avec une animation.
	"""
	def __init__(self, id=0):
		"""
		Méthode constructeur.
		-------------------------
		return -> Coffre
		"""
		self.nom = "coffre"
		self.id = id
		self.object = Actor("coffre.egg", {"anim":"coffre-Coffre_ouverture.egg"})
		self.object.setScale(20)
		self.col = CollisionNode("coffre_"+str(id))
		self.col.addSolid(CollisionBox((0, 0, 2), 2, 4, 2))
		self.col.setFromCollideMask(BitMask32.allOff())
		self.col.setIntoCollideMask(BitMask32.bit(0)) 
		self.col_np = self.object.attachNewNode(self.col)
