from panda3d.core import *
from direct.actor.Actor import Actor
import os
"""
Fichier qui va gérer toutes les stats des monstres
"""

class Monster(Actor):
	def __init__(self, name="slime", vies=3):
		if os.path.exists(f"../models/{name}.bam"):
			if os.path.exists(f"../models/{name}-attaque.bam"):
				Actor.__init__(self, f"../models/{name}.bam", {"attaque" : f"../models/{name}-attaque.bam"})
			else:
				Actor.__init__(self, f"../models/{name}.bam")
		else:
			Actor.__init__(self, name)	
		self.name = name		
		self.setScale(6)
		self.col = CollisionNode(name)
		self.col.addSolid(CollisionSphere((0, 0, 1.5), 1.25)) 
		self.col.setIntoCollideMask(BitMask32.bit(0)) 
		self.col_np = self.attachNewNode(self.col)
		self.vies = vies
		
class Slime(Monster):
	def __init__(self):
		Monster.__init__(self, name="slime")	
		
class Ours(Monster):
	def __init__(self):
		Monster.__init__(self, name="ours", vies=6)	
		
class Arachnide(Monster):
	def __init__(self):
		Monster.__init__(self, name="arachnide", vies=4)
		
class Gobelin(Monster):
	def __init__(self):
		Monster.__init__(self, name="gobelin", vies=4)										
		
class Esprit(Monster):
	def __init__(self):
		Monster.__init__(self, name="esprit", vies=5)
		
class Requin(Monster):
	def __init__(self):
		Monster.__init__(self, name="requin", vies=6)

class Homme_poisson(Monster):
	def __init__(self):
		Monster.__init__(self, name="homme_poisson", vies=5)
		
class Crabe_geant(Monster):
	def __init__(self):
		Monster.__init__(self, name="crabe_geant", vies=4)
		
class Serpent_des_mers(Monster):
	def __init__(self):
		Monster.__init__(self, name="serpents_des_mers", vies=8)
		
class Golem_marin(Monster):
	def __init__(self):
		Monster.__init__(self, name="golem_marin", vies=8)	
		
class Yeti(Monster):
	def __init__(self):
		Monster.__init__(self, name="yeti", vies=10)																		

class Loup_des_neiges(Monster):
	def __init__(self):
		Monster.__init__(self, name="loup_des_neiges", vies=6)
		
class Zombie_de_glace(Monster):
	def __init__(self):
		Monster.__init__(self, name="zombie_de_glace", vies=6)
		
class Sorcier_des_montagnes(Monster):
	def __init__(self):
		Monster.__init__(self, name="sorcier_des_montagnes", vies=12)
		
class Golem_de_glace(Monster):
	def __init__(self):
		Monster.__init__(self, name="golem_de_glace", vies=12)
		
class Gibdo(Monster):
	def __init__(self):
		Monster.__init__(self, name="gibdo", vies=10)
		
class Squelette(Monster):
	def __init__(self):
		Monster.__init__(self, name="squelette", vies=8)

class Scorpion_geant(Monster):
	def __init__(self):
		Monster.__init__(self, name="scorpion_geant", vies=10)
		
class Cobra(Monster):
	def __init__(self):
		Monster.__init__(self, name="cobra", vies=5)
		
class Ver_du_sable(Monster):
	def __init__(self):
		Monster.__init__(self, name="ver_du_sable", vies=5)
		
class Dragon(Monster):
	def __init__(self):
		Monster.__init__(self, name="dragon", vies=15)
		
class Spectre_brulant(Monster):
	def __init__(self):
		Monster.__init__(self, name="spectre_brulant", vies=10)
		
class Diablotin(Monster):
	def __init__(self):
		Monster.__init__(self, name="diablotin", vies=12)

class Phoenix(Monster):
	def __init__(self):
		Monster.__init__(self, name="phoenix", vies=13)	
		
class Homme_des_cendres(Monster):
	def __init__(self):
		Monster.__init__(self, name="homme_des_cendres", vies=10)
		
class Zmeyevick(Monster):
	def __init__(self):
		Monster.__init__(self, name="zmeyevick", vies=20)
		
class Sorcier(Monster):
	def __init__(self):
		Monster.__init__(self, name="sorcier", vies=15)																																											
