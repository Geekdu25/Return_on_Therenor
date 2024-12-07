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
        Actor.__init__(self, "../models/error.bam")
        #----------------------Noais et autres infos de jeu--------------------------------
        self.noais = 0
        self.nom = "Link"
        self.vies = 3
        self.maxvies = 3
        self.inventaire = {}
        self.sexe = "masculin"
        #--------------------Quelques paramètres simples-----------------------------------
        self.vitesse = 2.5
        self.walk = False
        self.reverse = False
        self.right = False
        self.left = False
        self.setHpr(90, 0, 0)
        self.setScale(70)
        self.gravite = 2
        #---------------Section de gestion des collisions------------------
        self.col = CollisionNode('player_sphere')
        self.col.addSolid(CollisionSphere((0, 0, 0.65), 0.65)) 
        self.col.setFromCollideMask(BitMask32.bit(0))
        self.col.setIntoCollideMask(BitMask32.allOff()) 
        self.col_np = self.attachNewNode(self.col)
        self.mode = True
        
    def degats(self, degats=1):
        """
        Méthode permettant d'ajouter des dégâts au joueur.
        ---------------------------------------------------
        return -> None
        """
        self.vies -= degats
    
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
class Assasin_repenti(PNJ):
    def __init__(self):
        PNJ.__init__(self, name="assasin repenti", anims=["immobile"])
        self.texts= ["Salut. moi c'est Phoolan.","Je cherche mon colier porte bohneur, je la'i perdu en me battant dans la forteresse de la reine"]
        self.quetes= ["Phoolan semble avoir perdu son colier porte bonheur, essayer de le trouver et de lui ramener qui sait il vous donnera peut etre quelque chose"]
        self.object= "error"
        self.name = "Phoolan Devi"
        self.lieu= "Ignirift"

class Mage_cache(PNJ):
    def __init__(self):
        PNJ.__init__(self,name="Mage caché", anims["immobile"])
        self.textes= ["Axil, tel est mon nom.","Mais ne dis a personne que je suis la sinon il pourrais m'arriver des ennuis","Prend ceci est fout le camp d'ici"]
        self.object= "montre"#montre qui permet de ralentir le temps pour les combat
        self.name= "Axil"
        self.lieu = "Maison d'aurélia"

class Inventeur(PNJ):
    def __init___(self):
        PNJ.__init__(self,name="Inventeur",anims["immobile"])
        self.texts = ["Hey, je suis désolé mais je peux pas trop m'attarder sur toi","Je dois continuer a travailler mais reviens plus tard"]
        self.name= "Elia"
        self.lieu = "vilage des chasseurs"

class Enfant_prodige(PNJ):
    def __init__(self):
        PNJ.__init__(self,names="enfant prodige", anims["immobile"])
        self.texts=["Un ingredients, il me faut un ingredients pour finir ma potion, est que tu voudrais bien aller me le chercher?"]
        self.quest= ["Elle était tellement dans son experience qu'elle ne vous même pas dit ce qu'elle voulait, laisser moi vous aider","Maryanne voudrait un poisson"]
        self.object= "Vodka"
        self.textquest="Ne le dis pas a Papa s'il te plait"
        self.name="Maryanne"
        self.lieu="village des pecheurs"
class Archer(PNJ):
    def __init__(self):
        PNJ.__init__(self,names="Archer", anims["immobile"])
        self.texts= ["Bonjour, avez-vous rencontrer ma fille, Maryanne", "bien que cela m'etonnerais vu qu'elle passse son temps dans son labo c'est temps si","Elle recherche a faire un remede pour une maladie, comme elle l'appelait deja le cholera, il me semble"]
        self.name= "Robin"
        self.lieu= "Village des pecheurs"
class Etudiant_amoureux(PNJ):
    def __init__(self):
        PNJ.__init__(self,names="Etudiant amoureux", anims["immobile"])
        self.texts=["Salut ma belle.","As-tu besoin d'aide dans ton aventure","Peut- être que je pourrais t'être utiles", "Ou peut être voudrait tu une anecdotes sur nos créateurs?"]
        self.anecdotes=["Remy est un grand musciens de renom","Noé c'est voué une passion au modelage 3d","Tyméo adore les trains ca en devient suspiceux","Etienne a l'air d'être un génie de l'informatique","Et Alex, bah elle existe"]
        self.aide=["Le magicien et Zweyvick doivent etre dans l'ancien Forteresse de la Reine", "mais je ne vois pas pourquoi tu veux y aller"]
        self.name="Rodef"
        self.lieu= "tentes des nomades"
class Etudiante_amoureuse(PNJ):
    def __init__(self):
        PNJ.__init__(self, name="Etudiante amoureuse",anims["immobile"])
        self.texts=["Salut mon chou.","Apparament, nos créateurs ne se reveront peut être plus","Je trouve sa vraiment dommage","mais bon ils ne doivent pas avoir le choix on va dire"]
        self.name="Alfi"
        self.lieu="tentes des nomades"

#-----------------------------------------PNJ de test--------------------------------------

class Magicien(PNJ):
    def __init__(self):
        PNJ.__init__(self, name="magicien", anims=["Immobile"])
        self.setScale(40)
        self.texts = None
        self.commercant = True
        self.texts_vente = 2
        self.articles = {"Vodka":30, "Tsar Bomba":300, "Cigare cubain":50,"Machins":5}
