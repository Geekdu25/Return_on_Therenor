from direct.actor.Actor import Actor
from panda3d.core import *
from FollowCam import FollowCam
import os

class Player(Actor):
	def __init__(self):
		Actor.__init__(self, "../models/error.bam", {"walk": "../models/error-marche.bam"})
		self.vitesse = 0.20
		self.walk = False
		self.reverse = False
		self.right = False
		self.left = False
		self.setHpr(90, 0, 0)
		self.setScale(8)
		#----------------Notre caméra-------------------
		self.followcam = FollowCam(base.cam, self)
		#---------------Section de gestion de l'épée-------------------------
		self.rightHand = self.exposeJoint(None, 'modelRoot', 'hand.R')
		self.epee = loader.loadModel("../models/sword.bam")
		self.epee.setScale(0.3)
		self.epee.setHpr(270, 0, 0)
		self.epee.setX(self.epee, -1.5)
		self.epee.reparentTo(self.rightHand)
		#---------------Section de gestion des collisions------------------
		self.col = CollisionNode('player_sphere')
		self.col.addSolid(CollisionSphere((0, 0, 1.5), 1.25)) 
		self.col.setFromCollideMask(BitMask32.bit(0))
		self.col.setIntoCollideMask(BitMask32.allOff()) 
		self.col_np = self.attachNewNode(self.col)
	
	def set_active(self, active=False):
		self.followcam.set_active(active)
		
class PNJ(Actor):
	def __init__(self, name="error"):
		if os.path.exists(f"../models/{name}.bam"):
			if os.path.exists(f"../models/{name}-marche.bam"):
				Actor.__init__(self, f"../models/{name}.bam", {"marche" : f"../models/{name}-marche.bam"})
			else:
				Actor.__init__(self, f"../models/{name}.bam")
		else:
			Actor.__init__(self, name)	
		self.name = name		
		self.setScale(6)
		self.col = CollisionNode(f"{name}_sphere")
		self.col.addSolid(CollisionSphere((0, 0, 1.5), 1.25)) 
		self.col.setIntoCollideMask(BitMask32.bit(0)) 
		self.col_np = self.attachNewNode(self.col)
		
class Taya(PNJ):
	def __init__(self):
		PNJ.__init__(self, name="Taya")
		self.setScale(0.2)
		self.setPos(-150, 150, 0)		
