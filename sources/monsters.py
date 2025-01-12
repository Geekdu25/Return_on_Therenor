from panda3d.core import *
from direct.actor.Actor import Actor
import os
"""
Fichier qui va gérer toutes les stats des monstres
"""

#--------------------------Classe de base-----------------------------------------
class Monster(Actor):
    """
    Classe d'un monstre on ne peut plus basique.
    """
    def __init__(self, name="slime", vies=3, actions=["move"]):
        """
        Méthode constructeur.
        ------------------------
        name -> str
        vies -> int
        actions -> list
        return -> Monster
        """
        dico = {}
        for anim in actions:
            if os.path.exists(f"../data/models/{name}-{anim}.bam"):
                dico[anim] = f"../data/models/{name}-{anim}.bam"
        Actor.__init__(self, name+".bam", dico)
        self.name = name        
        self.vies = vies

#------------------------------Tous les monstres-------------------------------
class Slime(Monster):
    def __init__(self):
        Monster.__init__(self)
        self.setScale(6)
        self.col = CollisionNode(name)
        self.col.addSolid(CollisionSphere((0, 1.5, 4.5), 2.5))
        self.col.setIntoCollideMask(BitMask32.bit(0))
        self.col_np = self.attachNewNode(self.col)
        self.col_np.show()

class Golem(Monster):
  def __init__(self):
    Monster.__init__(self, name="golem", vies = 10)
    self.setScale(25)
    light = PointLight("lumiere_golem")
    light.setColor((0.1, 0.9, 0.3, 0.9)) 
    light_np = self.attachNewNode(light)
    self.setLight(light_np) 
    self.col = CollisionNode("golem")
    self.col.addSolid(CollisionSphere((0, 0, 4.5), 5))
    self.col.setIntoCollideMask(BitMask32.bit(0))
    self.col_np = self.attachNewNode(self.col)
    

class Zmeyevick(Monster):
    def __init__(self):
        Monster.__init__(self, name="zmeyevick", vies=20)

class Sorcier(Monster):
    def __init__(self):
        Monster.__init__(self, name="sorcier", vies=15)
