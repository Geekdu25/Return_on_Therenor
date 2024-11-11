from direct.actor.Actor import Actor
from panda3d.core import *
from FollowCam import *
import os
from direct.interval.IntervalGlobal import *

class Player(Actor):
	"""
	Classe gérant le joueur.
	"""
	def __init__(self):
		#-------------Initialisation--------------------------------------
		Actor.__init__(self, "../models/error.bam")
		#----------------------Noais et autres infos de jeu--------------------------------
		self.noais = 0
		self.nom = "Link"
		self.vies = 3
		self.maxvies = 3
		self.inventaire = []
		#--------------------Quelques paramètres simples-----------------------------------
		self.vitesse = 2.5
		self.walk = False
		self.reverse = False
		self.right = False
		self.left = False
		self.setHpr(90, 0, 0)
		self.setScale(70)
		#---------------Section de gestion des collisions------------------
		self.col = CollisionNode('player_sphere')
		self.col.addSolid(CollisionSphere((0, 0, 0.5), 0.65)) 
		self.col.setFromCollideMask(BitMask32.bit(0))
		self.col.setIntoCollideMask(BitMask32.allOff()) 
		self.col_np = self.attachNewNode(self.col)
	
	
	def create_camera(self):
		self.followcam = ManetteCam(base.cam, self)
		
		
class PNJ(Actor):
	"""
	Classe nous servant de base pour tous les pnjs du jeu.
	On peut bien sûr créer de nouvelles classes qui en héritent.
	"""
	def __init__(self, name="error", anims=[]):
		#On cherche l'existence des modèles 3D de notre personnage.
		dico = {}
		for anim in anims:
				dico[anim] = f"../models/{name}-{anim}.bam"
		Actor.__init__(self, f"../models/{name}.bam", dico)
		self.name = name		
		self.s = None
		self.texts = 0
		self.setScale(6)
		self.col = CollisionNode(name)
		self.col.addSolid(CollisionSphere((0, 0, 1.5), 1.25)) 
		self.col.setIntoCollideMask(BitMask32.bit(0)) 
		self.col_np = self.attachNewNode(self.col)

class Magicien(PNJ):
	def __init__(self):
		PNJ.__init__(self, name="magicien", anims=["Immobile"])
		self.setScale(60)
