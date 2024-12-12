from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task.Task import Task
from direct.actor.Actor import Actor
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.filter.CommonFilters import *
from direct.gui.OnscreenImage import *
from direct.showbase.DirectObject import DirectObject
import sys
import os



class InterfaceJoueur(DirectObject):
    """Classe gérant l'interface des stats du joueur: barre de HP, de mana, et bourse"""
    def __init__(self, joueur):
        DirectObject.__init__(self)
        self.joueur = joueur
        self.accept("mouse1", self.enlever_hp)  # Bouton gauche souris
        self.accept("mouse3", self.ajouter_hp) # Bouton droit souris
        self.accept("a", self.ajouter_mana)    #touche a
        self.accept("z", self.enlever_mana)    #touche z
        self.accept("r", self.enlever_argent)  #touche r
        self.accept("e", self.ajouter_argent)  #touche e
        #stats du joueur(on pourra les modifier si elles sont sensées être stockées ailleurs)
        self.pv = 50
        self.pv_max = 50
        self.mana = 25
        self.mana_max = 25
        self.bourse = 100
        self.hp = affichageTexte(0.6, 0.06, 0.05, 'HP')  #affichage à l'écran de "HP"
        self.mn = affichageTexte(0.6, 0.131, 0.05, 'MANA')  #affichage à l'écran de "MANA"
        self.no = OnscreenImage(image="noai.png", pos=(-1.2,0,0.73), scale=(0.05,0,0.05))
        self.no.setTransparency(TransparencyAttrib.MAlpha)
        self.ag = affichageTexte(0.2, 0.25, 0.1, str(self.bourse))  #affichage à l'écran de la quantité d'argent
        self.barre_pv_root = NodePath("BarrePVRoot")
        self.barre_pv_root.reparentTo(aspect2d)
        self.barre_mana_root = NodePath("BarreManaRoot")
        self.barre_mana_root.reparentTo(aspect2d)
        self.create("background_pv",scale=(0.5,0,0.05),color=LVector4(0.2,0.2,0.2,1),pos=(-1.25,0,0.92))
        self.barre_pv = self.create("Barredevie",scale=(0.5,0,0.05),color=LVector4(0.8,0,0,1),pos=(-1.25,0,0.92))
        self.create("background_mana",scale=(0.5,0,0.05), color=LVector4(0.2,0.2,0.2,1),pos=(-1.25,0,0.85))
        self.barre_mana = self.create("Barredemana",scale=(0.5,0,0.05), color=LVector4(0,0.8,0,1),pos=(-1.25,0,0.85))



    def create(self, name, scale, color, pos):
        """
        Créer une barre rectangulaire"""
        cm = CardMaker(name)
        cm.setFrame(0,1,-0.5,0.5)
        barre = NodePath(cm.generate())
        barre.setScale(scale)
        barre.setPos(pos)
        barre.setColor(color)
        barre.reparentTo(self.barre_pv_root)
        return barre




    def enlever_hp(self):
        """Méthode qui diminue la quantité de la barre d'hp quand le joueur en perd"""
        if self.pv -1 >= 0:
            self.pv -= 1
            ratio = self.pv/self.pv_max
            self.barre_pv.setScale(ratio*0.5,0,0.05)

    def ajouter_hp(self):
        """Méthode qui augmente la quantité de la barre d'hp quand le joueur en gagne"""
        if self.pv + 1 <= self.pv_max:
            self.pv += 1
            ratio = self.pv/self.pv_max
            self.barre_pv.setScale(ratio*0.5,0,0.05)

    def ajouter_mana(self):
        """Méthode qui augmente la quantité de la barre de mana quand le joueur en gagne"""
        if self.mana+1 <= self.mana_max:
            self.mana += 1
            ratio = self.mana/self.mana_max
            self.barre_mana.setScale(ratio*0.5,0,0.05)

    def enlever_mana(self):
        """Méthode qui diminue la quantité de la barre de mana quand le joueur en perd"""
        if self.mana -1 >= 0:
            self.mana -= 1
            ratio = self.mana/self.mana_max
            self.barre_mana.setScale(ratio*0.5,0,0.05)

    def enlever_argent(self):
        """Méthode qui diminue la quantité d'argent affichée quand le joueur en perd"""
        if self.bourse -1 >= 0:
            self. bourse -= 1
            self.ag.destroy()
            self.ag = affichageTexte(0.2, 0.25, 0.1, str(self.bourse))

    def ajouter_argent(self):
        """Méthode qui augmente la quantité d'argent affichée quand le joueur de gagne"""
        self.bourse += 1
        self.ag.destroy()
        self.ag = affichageTexte(0.2, 0.25, 0.1, str(self.bourse))

    def cacher(self):
        """
        Méthode pour cacher l'interface.
        """
        self.ag.hide()
        self.no.hide()
        self.barre_mana.hide()
        self.barre_pv.hide()
        self.hp.hide()
        self.mn.hide()

    def montrer(self):
        """
        Méthode pour montrer l'interface.
        """
        self.ag.show()
        self.no.show()
        self.barre_mana.show()
        self.barre_pv.show()
        self.hp.show()
        self.mn.show()

def affichageTexte(x, y, t, texte):
    """Fonction pour mettre du texte à l'écran
    x, y coordonnées du texte, et t la taille"""
    return OnscreenText(text=texte, style=1, fg=(1, 1, 1, 1), scale=t,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(x, -y - 0.04), align=TextNode.ALeft)


