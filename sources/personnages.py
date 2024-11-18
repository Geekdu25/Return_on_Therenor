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
		self.sexe = "masculin"
		#--------------------Quelques paramètres simples-----------------------------------
		self.vitesse = 2.5
		self.walk = False
		self.reverse = False
		self.right = False
		self.left = False
		self.setHpr(90, 0, 0)
		self.setScale(70)
		self.gravite = 0.3
		self.cache = True
		if self.cache:
			self.setAlphaScale(0.5)
		#---------------Section de gestion des collisions------------------
		self.col = CollisionNode('player_sphere')
		self.col.addSolid(CollisionSphere((0, 0, 0.5), 0.65)) 
		self.col.setFromCollideMask(BitMask32.bit(0))
		self.col.setIntoCollideMask(BitMask32.allOff()) 
		self.col_np = self.attachNewNode(self.col)
	
	def degats(self, degats=1):
		"""
		Méthode permettant d'ajouter des dégâts au joueur.
		---------------------------------------------------
		return -> None
		"""
		self.vies -= degats
		
		
	def create_camera(self):
		"""
		Méthode permettant de créer la caméra du joueur.
		--------------------------------------------------
		return -> None
		"""
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
		self.texts = None
		self.commercant = False
		self.texts = 2
		self.setScale(6)
		self.col = CollisionNode(name)
		self.col.addSolid(CollisionSphere((0, 0, 1.5), 1.25)) 
		self.col.setIntoCollideMask(BitMask32.bit(0)) 
		self.col_np = self.attachNewNode(self.col)

class Magicien(PNJ):
	def __init__(self):
		PNJ.__init__(self, name="magicien", anims=["Immobile"])
		self.setScale(40)
		self.texts = None
		self.commercant = True
		self.texts_vente = 2
		self.articles = {"Vodka":30, "Tsar Bomba":300, "Cigare cubain":50,"Machins":5}
