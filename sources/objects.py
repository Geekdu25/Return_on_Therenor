from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor

class Objet:
    """
    Un objet classique utilisé par défaut.
    """
    def __init__(self, name):
        """
        Méthode constructeur.
        ----------------------
        return -> Objet
        """
        self.name = name
        self.object = loader.loadModel(name)

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

class Manoir:
    """
    Le manoir que l'on retrouve à Verdantia.
    """
    def __init__(self):
        """
        Méthode constructeur.
        ---------------------
        return -> Manoir
        """
        self.object = loader.loadModel("Manoir.bam")
        self.object.setScale(9)
        self.col = CollisionNode("Manoir")
        self.col.addSolid(CollisionBox((-10, -20, 10), 100, 40, 50))
        self.col.setFromCollideMask(BitMask32.allOff())
        self.col.setIntoCollideMask(BitMask32.bit(0))
        self.col_np = self.object.attachNewNode(self.col)

class Palmier:
    """
    Les palmiers se trouvant à Arduny.
    """
    def __init__(self):
        """
        Méthode constructeur.
        ----------------------
        return -> Palmier
        """
        self.object = loader.loadModel("Palmier.bam")
        self.object.setScale(13)
        self.col = CollisionNode("palmier")
        self.col.addSolid(CollisionBox((0, 0, 3), 3, 3, 10))
        self.col.setFromCollideMask(BitMask32.allOff())
        self.col.setIntoCollideMask(BitMask32.bit(0))
        self.col_np = self.object.attachNewNode(self.col)

class Maison_aurelia:
    """
    La maison abandonnée se trouvant à Ignirift.
    """
    def __init__(self):
        """
        Méthode constructeur.
        ------------------------
        return -> Maison_aurelia
        """
        self.object = loader.loadModel("maison_aurelia.bam")
        self.object.setScale(3)
