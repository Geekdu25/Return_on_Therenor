#Projet : Return on Therenor
#Auteurs : Tyméo Bonvicini-Renaud, Alexandrine Charette, Rémy Martinot, Noé Mora, Etienne Pacault
from direct.actor.Actor import Actor
from panda3d.core import *
from FollowCam import *
import os
from direct.interval.IntervalGlobal import *

#-------------------------Le joueur----------------------------------------------
class Player(Actor):
    """
    Classe gérant le joueur.
    """
    def __init__(self):
        #-------------Initialisation--------------------------------------
        Actor.__init__(self, "../models/base_prota.bam")
        #----------------------Noais et autres infos de jeu--------------------------------
        self.noais = 0
        self.nom = "Link"
        self.vies = 30
        self.maxvies = 30
        self.mana = 15
        self.mana_max = 15
        self.armes = []
        self.current_arme = None
        self.inventaire = {}
        self.coffres = [0, 0]
        self.sexe = "masculin"
        #--------------------Quelques paramètres simples-----------------------------------
        self.vitesse = 20
        self.walk = False
        self.reverse = False
        self.right = False
        self.left = False
        self.setHpr(90, 0, 0)
        self.setScale(3)
        self.gravite = 15
        self.loop("attaque")
        #---------------Section de gestion des collisions------------------
        self.col = CollisionNode('player_sphere')
        self.col.addSolid(CollisionSphere((0, 0, 7.5), 7))
        self.col.setFromCollideMask(BitMask32.bit(0))
        self.col.setIntoCollideMask(BitMask32.allOff())
        self.col_np = self.attachNewNode(self.col)
        self.main_droite = self.exposeJoint(None, "modelRoot", "Bone.006")
        self.epee = loader.loadModel("../data/models/epee.bam")
        self.epee.reparentTo(self.main_droite)
        self.epee.setScale(0.05)
        self.epee.setPos((0, 0, 0.575))
        self.epee.setHpr((-55, 270, 0))
        self.epee.hide()
        self.setPlayRate(5.0, 'Attaque')
        self.setPlayRate(3.0, 'Marche.001(real)')

    def change_etat_coffres(self, map="village_pecheurs.bam", numero=0):
        """
        Méthode permettant de changer l'état d'un coffre.
        -------------------------------------------------
        return -> None
        """
        if map == "village_pecheurs.bam" and numero == 0:
            self.coffres[0] = 1
        elif map == "pyramide.bam" and numero == 0:
            self.coffres[1] = 1

    def ajoute_item(self, item="Vodka"):
        """
        Méthode permettant d'ajouter un item dans l'inventaire.
        --------------------------------------------------------
        item -> str
        return -> None
        """
        if item in self.inventaire:
            self.inventaire[item] += 1
        else:
            self.inventaire[item] = 1

    def ajoute_arme(self, item="Epée"):
        """
        Méthode permettant d'ajouter un item dans les armes.
        -----------------------------------------------------
        item -> str
        return -> None
        """
        self.armes.append(item)

    def create_camera(self):
        """
        Méthode permettant de créer la caméra du joueur.
        --------------------------------------------------
        return -> None
        """
        self.followcam = ManetteCam(base.cam, self)

#-------------------------------Les pnjs---------------------------------------
class PNJ(Actor):
    """
    Classe nous servant de base pour tous les pnjs du jeu.
    On peut bien sûr créer de nouvelles classes qui en héritent.
    """
    def __init__(self, name="error", anims=[]):
        #On cherche l'existence des modèles 3D de notre personnage.
        dico = {}
        for anim in anims:
                dico[anim] = f"{name}-{anim}.bam"
        Actor.__init__(self, f"{name}.bam", dico)
        self.name = name
        self.s = None
        self.nom = "Tingle"
        self.texts = None
        self.commercant = False
        self.texts = 2
        self.setScale(6)
        self.col = CollisionNode(name)
        self.col_np = self.attachNewNode(self.col)

    def __str__(self):
        return self.nom+" est un PNJ."

    """def optention(self):
        if "collier" in self.inventaire:
            self.texts = "Tu as retrouver mon collier merci","Mais maintenant j'en ai plus besoin, garde le. Et prend un peu d'argent pour te rembourser le trajet"
        elif "amulette" in inventaire:
            self.texts= "Prend ceci est fout le camp d'ici"
        elif "poisson" in self.inventaire:
            self.texts = "Merci je peux enfin finir mon antidote pour le cholera","Prend ca, mais ne dit rien à mon papa"
        else:
            self.texts="Tu n'as pas l'object adéquat repasse plus tard"
        return self.texts"""

class Assassin_repenti(PNJ):
    def __init__(self):
        PNJ.__init__(self, name="pnjs/assassin")
        self.texts= 4
        self.setScale(20)
        self.setSz(26)
        self.setP(180)
        self.quetes= 13
        self.object= "collier"
        self.nom = "Phoolan Devi"
        self.col.setName("assassin")
        self.col.addSolid(CollisionSphere((0, 0, -1.5), 1.25))
        self.col.setIntoCollideMask(BitMask32.bit(0))

class Mage_cache(PNJ):
    def __init__(self):
        PNJ.__init__(self,name="pnjs/mage")
        self.texts= 5
        self.setScale(20)
        self.setSz(26)
        self.object= "amulette"#amulette qui permet d'ouvrir un portail pour aller dans la forteresse plus rapidement
        self.nom = "Axil"
        self.col.setName("mage")
        self.col.addSolid(CollisionSphere((0, 0, 1.5), 1.25))
        self.col.setIntoCollideMask(BitMask32.bit(0))

class Inventeur(PNJ):
    def __init__(self):
        PNJ.__init__(self, name="pnjs/inventeur")
        self.texts = 6
        self.setScale(20)
        self.setSz(28)
        self.setH(270)
        self.nom = "Elia"
        self.col.setName("inventeur")
        self.col.addSolid(CollisionSphere((0, 0, 1.5), 1.25))
        self.col.setIntoCollideMask(BitMask32.bit(0))

class Enfant_prodige(PNJ):
    def __init__(self):
        PNJ.__init__(self, name="pnjs/enfant")
        self.texts = 7
        self.setScale(15)
        self.setSz(22)
        self.object = "Vodka"
        self.textquest = 14
        self.nom = "Maryanne"
        self.col.setName("enfant_prodige")
        self.col.addSolid(CollisionSphere((0, 0, 1.5), 1.25))
        self.col.setIntoCollideMask(BitMask32.bit(0))

    """def poisson(self):
        self.ajoute_item(item="poisson") -=1
        self.ajoute_item(item="Vodka") +=1
        return self.optention"""

class Archer(PNJ):
    def __init__(self):
        PNJ.__init__(self, name="pnjs/archer")
        self.texts = 8
        self.setScale(20)
        self.setSz(27)
        #self.loop(self.getAnimNames()[0])
        self.setP(180)
        self.setH(90)
        self.nom = "Robin"
        self.col.setName("archer")
        self.col.addSolid(CollisionSphere((0, 0, -1.5), 1.25))
        self.col.setIntoCollideMask(BitMask32.bit(0))

class Etudiant_amoureux(PNJ):
    def __init__(self):
        PNJ.__init__(self, name="magicien")
        self.texts = 9
        self.anecdotes = 11
        self.aide = 12
        self.setScale(40)
        self.nom = "Rodef"
        self.lieu = "tentes des nomades"
        self.col.setName("etudiant")
        self.col.addSolid(CollisionSphere((0, 0, 1.5), 1.25))
        self.col.setIntoCollideMask(BitMask32.bit(0))

class Etudiante_amoureuse(PNJ):
    def __init__(self):
        PNJ.__init__(self, name="magicien")
        self.texts = 10
        self.setScale(40)
        self.nom = "Alfi"
        self.lieu = "tentes des nomades"
        self.col.setName("etudiante")
        self.col.addSolid(CollisionSphere((0, 0, 1.5), 1.25))
        self.col.setIntoCollideMask(BitMask32.bit(0))

class Pecheur(PNJ):
    def __init__(self):
        PNJ.__init__(self, name="magicien")
        self.texts = 10
        self.setScale(40)
        self.nom = "Michel"
        self.col.setName("pecheur")
        self.col.addSolid(CollisionSphere((0, 0, 1.5), 1.25))
        self.col.setIntoCollideMask(BitMask32.bit(0))

class Marchand(PNJ):
    def __init__(self):
        PNJ.__init__(self, name="pnjs/marchand")
        self.texts = 10
        self.setScale(20)
        self.setSz(28)
        self.setP(180)
        self.setH(90)
        self.texts = None
        self.commercant = True
        self.texts_vente = 2
        self.articles = {"Vodka":30, "Tsar Bomba":300, "Epée":50}
        self.col.addSolid(CollisionSphere((0, 0, -1.5), 1.25))
        self.col.setIntoCollideMask(BitMask32.bit(0))
        #self.loop(self.getAnimNames()[0])

class Golem_pnj(PNJ):
  def __init__(self):
    PNJ.__init__(self, name="golem")
    self.setScale(25)
    self.setH(180)
    light = PointLight("lumiere_golem")
    light.setColor((0.1, 2, 0.2, 1))
    light_np = self.attachNewNode(light)
    light_np.setPos((0, 0, 1))
    self.setLight(light_np)
    self.col = CollisionNode("golem_pnj")
    self.col.addSolid(CollisionSphere((0, 0, 4.5), 6))
    self.col.setIntoCollideMask(BitMask32.bit(0))
    self.col_np = self.attachNewNode(self.col)
#-----------------------------------------PNJ de test--------------------------------------

class Magicien(PNJ):
    def __init__(self):
        PNJ.__init__(self, name="magicien", anims=["Immobile"])
        self.setScale(40)
        self.col.addSolid(CollisionSphere((0, 0, 1.5), 1.25))
        self.col.setIntoCollideMask(BitMask32.bit(0))
