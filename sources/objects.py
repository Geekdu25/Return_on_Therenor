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
        self.ouvert = False
        self.object = Actor("coffre.bam", {"anim":"coffre-ouverture.bam"})
        self.object.setScale(20)
        self.col = CollisionNode("coffre_"+str(id))
        self.col.addSolid(CollisionBox((0, 0, 2), 2, 4, 2))
        self.col.setFromCollideMask(BitMask32.allOff())
        self.col.setIntoCollideMask(BitMask32.bit(0))
        self.col_np = self.object.attachNewNode(self.col)

class Sapin:
    """
    Un sapin tout ce qu'il y a de plus normal.
    """
    def __init__(self):
        """
        Méthode constructeur.
        ----------------------
        return -> Sapin
        """
        self.object = loader.loadModel("sapin.bam")
        self.object.setScale(27)
        self.col = CollisionNode("sapin")
        self.col.addSolid(CollisionBox((0, 0, 3), 2.5, 2.5, 4))
        self.col.setFromCollideMask(BitMask32.allOff())
        self.col.setIntoCollideMask(BitMask32.bit(0))
        self.col_np = self.object.attachNewNode(self.col)
