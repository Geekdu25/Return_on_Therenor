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
        self.hp = affichageTexte(0.6, 0.06, 0.05, 'HP')  #affichage à l'écran de "HP"
        self.mn = affichageTexte(0.6, 0.131, 0.05, 'MANA')  #affichage à l'écran de "MANA"
        self.no = OnscreenImage(image="noai.png", pos=(-0.9,0,0.73), scale=(0.05,0,0.05))
        self.no.setTransparency(TransparencyAttrib.MAlpha)
        self.ag = affichageTexte(0.6, 0.25, 0.1, str(self.joueur.noais))  #affichage à l'écran de la quantité d'argent
        self.barre_pv_root = NodePath("BarrePVRoot")
        self.barre_pv_root.reparentTo(aspect2d)
        self.barre_mana_root = NodePath("BarreManaRoot")
        self.barre_mana_root.reparentTo(aspect2d)
        self.barre_pv_background = self.create("background_pv",scale=(0.5,0,0.05),color=LVector4(0.2,0.2,0.2,1),pos=(-1,0,0.92))
        self.barre_pv = self.create("Barredevie",scale=(0.5,0,0.05),color=LVector4(0.8,0,0,1),pos=(-1,0,0.92))
        self.barre_mana_background = self.create("background_mana",scale=(0.5,0,0.05), color=LVector4(0.2,0.2,0.2,1),pos=(-1,0,0.85))
        self.barre_mana = self.create("Barredemana",scale=(0.5,0,0.05), color=LVector4(0,0.8,0,1),pos=(-1,0,0.85))



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




    def enlever_hp(self, enmoins):
        """Méthode qui diminue la quantité de la barre d'hp quand le joueur en perd"""
        if self.joueur.vies - enmoins >= 0:
            self.joueur.vies -= enmoins
            ratio = self.joueur.vies/self.joueur.maxvies
            self.barre_pv.setScale(ratio*0.5,0,0.05)

    def ajouter_hp(self, enplus):
        """Méthode qui augmente la quantité de la barre d'hp quand le joueur en gagne"""
        if self.joueur.vies + enplus <= self.pv_max:
            self.joueur.vies += enplus
            ratio = self.joueur.vies/self.joueur.maxvies
            self.barre_pv.setScale(ratio*0.5,0,0.05)
        else:
            self.joueur.vies = self.joueur.maxvies
            ratio = self.joueur.vies/self.joueur.maxvies
            self.barre_pv.setScale(ratio*0.5,0,0.05)

    def ajouter_mana(self, enplus):
        """Méthode qui augmente la quantité de la barre de mana quand le joueur en gagne"""
        if self.joueur.mana + enplus<= self.joueur.mana_max:
            self.joueur.mana += enplus
            ratio = self.joueur.mana/self.joueur.mana_max
            self.barre_mana.setScale(ratio*0.5,0,0.05)

    def enlever_mana(self, enlever):
        """Méthode qui diminue la quantité de la barre de mana quand le joueur en perd"""
        if self.joueur.mana - enlever >= 0:
            self.joueur.mana -= enlever
            ratio = self.joueur.mana/self.joueur.mana_max
            self.barre_mana.setScale(ratio*0.5,0,0.05)

    def enlever_argent(self, somme):
        """Méthode qui diminue la quantité d'argent affichée quand le joueur en perd"""
        if self.joueur.noais -1 >= 0:
            self.joueur.noais -= somme
            self.ag.destroy()
            self.ag = affichageTexte(0.2, 0.25, 0.1, str(self.joueur.noais))

    def ajouter_argent(self, somme):
        """Méthode qui augmente la quantité d'argent affichée quand le joueur de gagne"""
        self.joueur.noais += somme
        self.ag.destroy()
        self.ag = affichageTexte(0.2, 0.25, 0.1, str(self.joueur.noais))

    def changer(self, quoi="hp", combien=0):
        """
        Méthode permettant de changer un paramètre.
        -------------------------------------------
        quoi -> str
        combien -> int
        return -> None
        """     
        if quoi == "hp":
            if combien > self.player.vies:
                self.ajouter_hp(combien-self.player.vies)
            elif combien < self.player.vies:
                self.enlever_hp(self.player.vies-combien)
        elif quoi == "mana":
            if combien > self.player.mana:
                self.ajouter_mana(combien-self.player.mana)
            elif combien < self.player.mana:
                self.enlever_mana(self.player.mana-combien)
        else:
            if combien > self.player.noais:
                self.ajouter_argent(combien-self.player.noais)
            elif combien < self.player.noais:
                self.enlever_argent(self.player.noais-combien)                





    def cacher(self):
        """
        Méthode pour cacher l'interface.
        """
        self.ag.hide()
        self.no.hide()
        self.barre_mana.hide()
        self.barre_pv.hide()
        self.barre_pv_background.hide()
        self.barre_mana_background.hide()
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
        self.barre_pv_background.show()
        self.barre_mana_background.show()
        self.hp.show()
        self.mn.show()

def affichageTexte(x, y, t, texte):
    """Fonction pour mettre du texte à l'écran
    x, y coordonnées du texte, et t la taille"""
    return OnscreenText(text=texte, style=1, fg=(1, 1, 1, 1), scale=t,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(x, -y - 0.04), align=TextNode.ALeft)


