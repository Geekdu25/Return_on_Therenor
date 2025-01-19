from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from direct.task.Task import Task
from direct.actor.Actor import Actor
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.filter.CommonFilters import *
from direct.gui.OnscreenImage import *
import sys
import os

class Inventaire(DirectObject):
    """Classe gérant d'affichage à l'écran des deux inventaires: celui des armes et des items"""
    def __init__(self, joueur):
        DirectObject.__init__(self)
        self.joueur = joueur
        self.weapons = self.joueur.armes  #liste des armes que l'on possède
        self.arme_en_main = 0     #quand on a aucune arme équipée
        self.weapon_texts = []    #liste servant à afficher les armes
        self.visible = False  #état de l'inventaire (affiché ou non)
        self.invent = None #rectangle de l'inventaire armes
        self.titre = None #nom "ARMES"
        self.inventaire = self.joueur.inventaire   #liste des items de son inventaire avec leur quantité
        self.item_selectione = 0    #item selectionné dans l'inventaire
        self.inventaire_texts= []   #liste des textes à afficher
        self.inventaire_liste = []    #liste des objets, pour la methode consommer_item
        self.inventaire_visible = False   #état de l'inventaire (visible ou non)
        self.invent2 = None   #rectangle de l'inventaire items
        self.titre2 = None #nom "INVENTAIRE"
        self.creer_inventaire()


    def creer_inventaire(self):
        """Créer l'affichage des deux inventaires"""

        #Détruire le potentiel affichage d'un précédent inventaire
        if self.titre is not None:
            self.titre.removeNode()
        if self.titre2 is not None:
            self.titre2.removeNode()
        if self.invent is not None:
            self.invent.removeNode()
        if self.invent2 is not None:
            self.invent2.removeNode()
        for text in self.weapon_texts:
            text.removeNode()    
        self.weapon_texts = []
        self.invent = None
        self.inventaire = self.joueur.inventaire
        self.armes = self.joueur.armes
        self.titre = None
        for text in self.inventaire_texts:
            text.removeNode()    
        self.inventaire_texts= []
        self.inventaire_liste = []
        self.invent2 = None
        self.titre2 = None

        #créer les rectangle
        self.invent = self.creer_rectangle_inventaire(-0.71, -0.31, len(self.weapons))  #rectangle de l'inventaire des armes (limites en bas et en haut par défaut et la taille de l'inventaire
        self.invent2 = self.creer_rectangle_inventaire(0.5, 0.8, len(self.inventaire))  #rectangle de l'inventaire des items (' ' ' ' ')

        #créer les noms d'inventaires
        self.titre = OnscreenText(text="ARMES",
                                  pos=(-1.2, -0.6+len(self.weapons)*0.1 + 0.1),
                                  scale=0.07,
                                  fg=(1, 1, 1, 1),
                                  align=TextNode.ALeft,
                                  parent=aspect2d,
                                  mayChange=True)
        self.titre.hide()#on cache initialement le texte

        self.titre2 = OnscreenText(text="INVENTAIRE",
                                    pos=(-1.2, 0.7),
                                    scale=0.07,
                                    fg=(1,1,1,1),
                                    align=TextNode.ALeft,
                                    parent=aspect2d,
                                    mayChange=True)
        self.titre2.hide()#on cache initialement le texte

        #créer l'inventaire(liste des armes puis des items à afficher)
        for i, arme, in enumerate(self.weapons):
            texte_arme = OnscreenText( text=f"{arme}",
                                       pos=(-1.2, (-0.6 + len(self.weapons)*0.1)-0.1*(i+1)),
                                       scale=0.05,
                                       fg=(1,1,1,1),
                                       align=TextNode.ALeft,
                                       parent=aspect2d,
                                       mayChange=True)
            texte_arme.hide()#on cache initialement le texte
            self.weapon_texts.append(texte_arme)

        self.arme_surbrillance()#pour mettre l'arme selectionnée en surbrillance dés l'ouverture de l'inventaire

        for i, item in enumerate(self.inventaire.keys()):
            texte_item = OnscreenText( text=f"{item} x{self.inventaire[item]}",
                                        pos=(-1.2, 0.55 - i*0.1),
                                        scale=0.05,
                                        fg=(1,1,1,1),
                                        align=TextNode.ALeft,
                                        parent=aspect2d,
                                        mayChange=True)
            texte_item.hide()#on cache initialement le texte
            self.inventaire_texts.append(texte_item)
            self.inventaire_liste.append(item)

        self.item_surbrillance()#pour mettre l'objet selectionné en surbrillance dés l'ouverture de l'inventaire

    def creer_rectangle_inventaire(self, bas, haut, taille):
        """Méthode servant à créer les rectangles bleus servant de fond aux deux inventaires.
        bas: position de la limite en bas du rectangle, qui variera pour le rectangle INVENTAIRE
        haut: position de la limite en haut du rectangle, qui variera pour le rectangle ARMES
        taille: taille de l'inventaire (nb d'éléments) servant à faire varier sa taille
        """
        if bas == -0.71:
            haut = haut + 0.1*(taille-1)
        if haut == 0.8:
            bas = bas - 0.1*(taille-1)

        cm = CardMaker("inventaire") #création du premier rectangle (bleu marine)
        cm.setFrame(-1.24, -0.64, bas, haut)
        inventaire = aspect2d.attachNewNode(cm.generate())
        inventaire.setColor(0.1, 0.2, 0.5, 1)

        cm_border = CardMaker("inventaire_bordure") #création du deuxième rectangle (bleu clair) servant de bordure, donc un peu plus large
        cm_border.setFrame(-1.26, -0.62, bas-0.02, haut+0.02)
        inventaire_bordure = aspect2d.attachNewNode(cm_border.generate())
        inventaire_bordure.setColor(0.2, 0.4, 0.8, 1)
        inventaire_bordure.setZ(-0.001)

        #on rattache les deux rectangles ensembles
        inventaire.reparentTo(inventaire_bordure)
        inventaire_bordure.hide()#on cache initialement le rectangle
        return inventaire_bordure

    def arme_surbrillance(self):
        """Sert à mettre l'arme selectionnée en surbrillance dans l'inventaire ARMES"""
        for i, texte_arme in enumerate(self.weapon_texts):
            if i==self.arme_en_main:
                texte_arme.setFg((0,1,0,1))
            else:
                texte_arme.setFg((1,1,1,1))

    def item_surbrillance(self):
        """Sert à mettre l'item selectionné en surbrillance dans l'inventaire INVENTAIRE"""
        for i, texte_item in enumerate(self.inventaire_texts):
            if i==self.item_selectione:
                texte_item.setFg((0,1,0,1))
            else:
                texte_item.setFg((1,1,1,1))


    def arme_select(self, indiceArme):
        """Méthode qui modifie l'arme séléctionée et la met en surbrillance"""
        if 0 <= indiceArme < len(self.weapons):
            self.arme_en_main = indiceArme
            self.arme_surbrillance()
            #Arme sélectionnée : self.weapons[indiceArme]

    def item_select(self, indiceItem):
        """Méthode qui modifie l'item séléctionné et le met en surbrillance"""
        if 0 <= indiceItem < len(self.inventaire):
            self.item_selectione = indiceItem
            self.item_surbrillance()


    def affiche_inventaire_armes(self):
        """Méthode qui gère le changement d'état de l'inventaire des armes:
            l'affiche avec afficher_armes() s'il ne l'est pas
            le masque avec cacher_armes() s'il est affiché
        """
        if self.visible :
            self.cacher_armes()
            self.visible = False
        else:
            if self.inventaire_visible:
                self.affiche_inventaire_items()
            self.afficher_armes()
            self.visible = True

    def afficher_armes(self):
        """Méthode qui affiche les éléments consituant l'inventaire ARMES"""
        self.titre.show()
        self.invent.show()
        for arme in self.weapon_texts:
            arme.show()

    def cacher_armes(self):
        """Méthode qui masque les éléments consituant l'inventaire ARMES"""
        self.invent.hide()
        self.titre.hide()
        for arme in self.weapon_texts:
            arme.hide()

    def affiche_inventaire_items(self):
        """Méthode qui gère le changement d'état de l'inventaire des items:
            l'affiche avec afficher_items() s'il ne l'est pas
            le masque avec cacher_items() s'il est affiché
            """
        if self.inventaire_visible:
            self.cacher_items()
            self.inventaire_visible = False
        else:
            if self.visible:
                self.affiche_inventaire_armes()
            self.afficher_items()
            self.inventaire_visible = True

    def afficher_items(self):
        """Méthode qui affiche les éléments constituant l'inventaire INVENTAIRE"""
        self.titre2.show()
        self.invent2.show()
        for item in self.inventaire_texts:
            item.show()

    def cacher_items(self):
        """Méthode qui masque les éléments constituant l'inventaire INVENTAIRE"""
        self.titre2.hide()
        self.invent2.hide()
        for item in self.inventaire_texts:
            item.hide()

    def get_item(self):
        return self.inventaire_liste[self.item_selectione]
    
    def get_arme(self):
        return self.weapons[self.arme_en_main]


    def cacher(self):
        self.cacher_armes()
        self.cacher_items()





