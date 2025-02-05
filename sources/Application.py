#Projet : Return on Therenor
#Auteurs : Tyméo Bonvicini-Renaud, Alexandrine Charette, Rémy Martinot, Noé Mora, Etienne Pacault
#---------------Importation des différents modules-----------------------------
#-------------Section spécifique à panda3d-------------------------------------
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.fsm.FSM import FSM
from direct.gui.OnscreenImage import *
from direct.gui.OnscreenText import *
from direct.gui.DirectGui import *
from direct.gui.DirectFrame import DirectFrame
from direct.interval.IntervalGlobal import *
from direct.interval.LerpInterval import LerpFunc
from direct.showbase.Transitions import Transitions
from direct.actor.Actor import Actor
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
#-----------Section spécifique aux fichiers python du dossier-----------
from personnages import *
from monsters import *
from objects import *
from mappingGUI import *
from Inventaire import *
from Interface_joueur import *
#-------------Autres modules (nécessaires entre autres à la manipulation des fichiers)------------------
import os, sys, json, platform, random, time


#----------------------------Création de certaines classes dont nous aurons besoin (en particulier des solide de collisions.)--------------------------
class YesNoDialog(DirectDialog):
    """
    Il s'agit de la même classe que celle présente avec Panda3d, mais on traduit Yes et No par Oui et Non.
    """
    def __init__(self, parent = None, **kw):
        optiondefs = (('buttonTextList',  ['Oui', 'Non'], DGG.INITOPT), ('buttonValueList', [DGG.DIALOG_YES, DGG.DIALOG_NO], DGG.INITOPT),)
        self.defineoptions(kw, optiondefs)
        DirectDialog.__init__(self, parent)
        self.initialiseoptions(YesNoDialog)

class Portail(CollisionBox):
    """
    Pour faire simple, un portail est un solide de collision invisible qui téléporte le joueur dès qu'il le touche.
    """
    def __init__(self, center=(1320, -1000, 6), sx=40, sy=4, sz=150, newpos=(830, -470, 6)):
        """
        Méthode constructeur.
        -------------------------
        center -> tuple
        sx -> int
        sy -> int
        sz -> int
        newpos -> int
        return -> Portail
        """
        CollisionBox.__init__(self, center, sx, sy, sz)
        self.newpos = newpos
        self.orientation = None
        self.setTangible(False) #On peut traverser un portail


class Porte(CollisionBox):
    """
    Contrairement à un portail, une porte doit être ouverte par le joueur en appuyant sur espace pour le téléporter.
    """
    def __init__(self, center=(1320, -1000, 6), sx=50, sy=10, sz=150, newpos=(830, -460, 6)):
        """
        Méthode constructeur.
        -------------------------
        center -> tuple
        sx -> int
        sy -> int
        sz -> int
        newpos -> int
        return -> Porte
        """
        CollisionBox.__init__(self, center, sx, sy, sz)
        self.newpos = newpos
        self.orientation = None

class Save_bloc(CollisionBox):
    """
    Ce type de collision sera utilisé pour sauvegarder.
    """
    def __init__(self, nom=1, center=(0, 0, 0)):
        """
        Méthode constructeur.
        ------------------------
        nom -> int
        center -> tuple
        return -> Save_bloc
        """
        CollisionBox.__init__(self, (center[0], center[1], center[2]), 1.5, 1.5, 3)
        self.nom = nom #Un nom lui est attribué pour se repérer.


class SetLevel(FSM):
    """
    Partez du principe que cette classe sera le coeur du jeu.
    Tout le script principal s'y trouvera.
    -------------------------------------------------------------
    Catégories dans lesquelles sont classées les méthodes :
    - Méthodes spéciales
    - GUI
    - Méthodes d'interactions
    - Changement de states
    - Hors catégorie
    - Ecran titre
    - Section de gestion des trois fichiers de sauvegarde
    - Gestion du menu pour changer la langue
    - Gestion du mappage de touches
    - Début de partie
    - Cinémtiques
    - Map
    - Collisions
    - Mise à jour
    - Pop-ups
    - Inventaire
    - Générique
    - Game over
    - Sauvegardes
    - Manette
    """
    #-----------------------Méthodes spéciales----------------------------------
    def __init__(self):
        """
        Métohde constructeur.
        ----------------------
        return -> SetLevel
        """
        FSM.__init__(self, "LevelManager") #Initialisation de notre classe en initialisant la super classe.
        self.debug = False #Le mode debug pourra être activé lors de certains tests (on peut y voir les collisions)
        #-----------------Variables nécessaires au Méthodenement de la boîte de dialogue----------------
        self.ok = False
        self.reading = False
        self.termine = True
        self.messages = []
        self.sons_messages = []
        #------------Section sons (musique, dialogues...)--------------------
        self.music = None
        self.son = None
        #-----------------------Varibles de collisions (pnj touché, liste de pnjs, porte touchée...)-------------------
        self.current_pnj = None
        self.pnjs = {}
        self.current_porte = None
        self.actual_trigger = None
        self.current_panneau = None
        self.actual_coffre = None
        base.cTrav = CollisionTraverser() #Le CollisionTraverser, gestionnaire de toutes les collisions.
        if self.debug:
            base.cTrav.showCollisions(render)
        self.skybox = None
        self.portails = {}
        self.triggers = []
        self.murs = []
        self.monstres = {}
        self.save_statues = {}
        self.particles_effects = []
        self.hack = False
        self.antimur = CollisionHandlerPusher() #Notre Collision Handler, qui empêchera le joueur de toucher les murs et d'autres choses.
        #-----------------Autres variables-----------------------
        self.chapitre = 0
        self.player = Player()
        self.player.reparentTo(render)
        self.player.hide()
        self.current_map = "village_pecheurs_maison_heros.bam"
        self.texts = ["It's a secret to everybody."]
        self.text_index = 0
        self.letter_index = 0
        self.first_time = False
        self.objects = []
        self.keys_data = {}
        self.current_point = 1
        self.actual_statue = None
        self.actual_file = 1
        self.manette = False
        if base.devices.getDevices(InputDevice.DeviceClass.gamepad):
            self.manette = True
            base.attachInputDevice(base.devices.getDevices(InputDevice.DeviceClass.gamepad)[0], prefix="manette")
        self.quitDlg = None
        self.load_gui()
        self.transition = Transitions(loader)
        self.clavier_rep = base.win.get_keyboard_map()
        self.init_fichiers()
        self.read_global()
        with open("../data/json/texts.json", encoding="utf-8") as texts:
                self.story = json.load(texts)[self.langue]
        base.taskMgr.add(self.update_text, "update_text")
        self.accept("escape", self.all_close)
        base.win.setCloseRequestEvent("escape")

    #--------------------------------------GUI------------------------------
    def load_gui(self):
        """
        Méthode qui nous permet de charger les éléments 2D.
        ----------------------------------------------------
        return -> None
        """
        self.myOkDialog = None
        self.inventaire_mgr = Inventaire(self.player)
        self.player_interface = InterfaceJoueur(self.player)
        self.map_image = OnscreenImage("carte_Terenor.png", scale=Vec3(0.8, 0, 0.8), pos=Vec3(0, 0, 0))
        self.croix_image = OnscreenImage("croix.png", scale=Vec3(0.04, 0, 0.04), pos=Vec3(0, 0, 0))
        self.croix_image.setTransparency(TransparencyAttrib.MAlpha)
        self.lieu_text = OnscreenText(text="???", pos=(0, 0.65), scale=0.1, fg=(1, 1, 1, 1))
        self.hide_gui()

    def hide_gui(self):
        """
        Méthode permettant de cacher la GUI (utile lors des cinématiques, ou lors d'un tuto).
        --------------------------------------------------------------------------------------
        return -> None
        """
        self.inventaire_mgr.cacher()
        self.player_interface.cacher()
        self.map_image.hide()
        self.croix_image.hide()
        self.lieu_text.hide()

    def genere_liste_defilement(self):
        """
        Méthode permettant de générer une liste de défilement, ce qui est utile pour la vente et l'inventaire.
        ------------------------------------------------------------------------------------------------------
        return -> DirectScrolledList
        """
        a = DirectScrolledList(
        decButton_pos=(0, 0, 0.7),
        decButton_text="+",
        decButton_text_scale=0.07,
        decButton_borderWidth=(0.005, 0.005),
        incButton_pos=(0, 0, -0.7),
        incButton_text="-",
        incButton_text_scale=0.07,
        incButton_borderWidth=(0.005, 0.005),
        frameSize=(-0.7, 0.7, -0.8, 0.8),
        frameColor=(0.1, 0.1, 0.1, 0.8),
        pos=(0, 0, 0),
        items=[],
        numItemsVisible = 7,
        forceHeight = 0.15,
        itemFrame_frameSize=(-0.6, 0.6, -0.5, 0.5),
        itemFrame_pos=(0, 0, 0))
        return a

    #-----------------------Méthodes d'interactions (triggers, PNJS, vente...)----------------------------------
    def check_interact(self):
        """
        Méthode appelée chaque fois que le joueur appuie sur espace.
        Cela aura pour conséquences de vérifier les portes,
        les pnjs touchés, ou encore de passer les dialogues.
        -------------------------------------------------------------
        return -> None
        """
        reussi = self.check_interact_dial()
        if self.current_pnj is not None:
            if not self.reading and not reussi:
                taskMgr.remove("update")
                self.ignore("out")
                self.ignore("into")
                self.ignore("escape")
                self.ignore(self.keys_data["Inventaire"])
                self.ignore("h")
                if self.pnjs[self.current_pnj].texts is not None: #Dans le cas où le pnj aurait quelque chose à dire
                    self.text_index = 0
                    self.letter_index = 0
                    self.music.setVolume(0.3)
                    if self.chapitre > 3 and self.current_pnj == "mage":
                      self.set_text(["..."], messages=["reupdate"])
                    elif self.current_pnj == "etudiant":
                        self.set_text(self.pnjs[self.current_pnj].texts, messages=["boutons"])
                        self.acceptOnce("boutons", self.show_etudiant_options)
                    elif self.current_pnj == "golem_pnj" and self.chapitre == 5:
                        self.current_pnj = None
                        self.chapitre = 6
                        self.fade_out("Cinematique")
                    elif self.current_pnj == "golem_pnj" and self.chapitre > 6:
                        self.set_text(["Où désires-tu aller ?"], messages=["boutons"])
                        self.acceptOnce("boutons", self.show_golem_options)
                    else:
                      self.set_text(self.pnjs[self.current_pnj].texts, messages=["reupdate"])
                    self.acceptOnce("reupdate", self.reupdate)
                elif self.pnjs[self.current_pnj].commercant:
                    self.music.setVolume(0.3)
                    self.set_text(self.pnjs[self.current_pnj].texts_vente, messages=["vente"])
                    self.accept("vente", self.vente, extraArgs=[self.pnjs[self.current_pnj].articles])
        elif self.current_porte is not None:
            self.transition.fadeOut(0.5)
            taskMgr.remove("update")
            self.player.walk = False
            self.player.reverse = False
            self.player.left = False
            self.player.right = False
            for event in self.keys_data:
                self.ignore(self.keys_data[event])
            self.ignore("into")
            self.ignore("out")
            if self.chapitre == 2:
                self.chapitre = 3
                self.fade_out("Cinematique")
            else:
              taskMgr.doMethodLater(0.5, self.load_map, "loadmap", extraArgs=[self.current_porte, self.portails[self.current_porte][1].newpos])
              if self.portails[self.current_porte][1].orientation is not None:
                taskMgr.doMethodLater(0.5, self.player.setH, "change orientation joueur", extraArgs=self.portails[self.current_porte][1].orientation)
        elif self.actual_statue is not None:
            taskMgr.remove("update")
            properties = WindowProperties()
            properties.setCursorHidden(False)
            base.win.requestProperties(properties)
            self.ignore("escape")
            self.current_point = self.actual_statue
            self.saveDlg = YesNoDialog(text = self.story["gui"][0], command = self.will_save) #Voulez-vous sauvegarder ?
        elif self.actual_trigger is not None:
            taskMgr.remove("update")
            properties = WindowProperties()
            properties.setCursorHidden(False)
            base.win.requestProperties(properties)
            self.ignore("escape")
            self.triggerDlg = YesNoDialog(text = self.story["trigger"][self.actual_trigger], command = self.accept_trigger)
            self.ignore("out")
        elif self.current_panneau is not None:
            for objet in self.objects:
                if "panneau" in objet.nom and str(objet.numero) == str(self.current_panneau):
                    if not self.reading and not reussi:
                      taskMgr.remove("update")
                      self.ignore("out")
                      self.ignore("into")
                      self.ignore("escape")
                      self.ignore(self.keys_data["Inventaire"])
                      self.ignore("h")
                      self.set_text([objet.text], messages=["reupdate"])
                      self.acceptOnce("reupdate", self.reupdate)
        elif self.actual_coffre is not None:
            a = False
            for objet in self.objects:
                if objet.nom == "coffre" and str(objet.id) == self.actual_coffre:
                    if not objet.ouvert:
                            self.player.change_etat_coffres(self.current_map, objet.id)
                            objet.ouvert = True
                            a = True
                            objet.object.play("anim")
                            taskMgr.remove("update")
                            properties = WindowProperties()
                            properties.setCursorHidden(False)
                            base.win.requestProperties(properties)
            if a:
                item = ""
                money = 0
                if self.current_map == "pyramide.bam" and self.actual_coffre == "0":
                    item = "Vodka"
                elif self.current_map == "village_pecheurs.bam" and self.actual_coffre == "0":
                    money = 100
                if item != "":
                  self.player.ajoute_item(item)
                  self.dialog = OkDialog(text=self.story["items"][6]+item, command=self.cleanup_dialog_tresor)
                  self.dialog.hide()
                  taskMgr.doMethodLater(1.5, self.dialog.show, "show dialog", extraArgs=[])
                elif money > 0:
                  self.player.noais += money
                  self.dialog = OkDialog(text=self.story["items"][6]+str(money)+" noaïs.", command=self.cleanup_dialog_tresor)
                  self.dialog.hide()
                  taskMgr.doMethodLater(1.5, self.dialog.show, "show dialog", extraArgs=[])

    def show_etudiant_options(self):
        """
        Méthode permettant à l'étudiant de présenter des options au joueur.
        -------------------------------------------------------------------
        return -> None
        """
        properties = WindowProperties()
        properties.setCursorHidden(False)
        base.win.requestProperties(properties)
        self.bouton1 = DirectButton(text=(self.story["trigger"][5]), pos=Vec3(0.5, 0, 0), scale=0.1, command=self.active_etudiant, extraArgs=[1])
        self.bouton2 = DirectButton(text=(self.story["trigger"][4]), scale=0.1, pos=Vec3(-0.5, 0, 0), command=self.active_etudiant, extraArgs=[2])
        self.bouton3 = DirectButton(text=(self.story["trigger"][3]), pos=Vec3(0, 0, -0.5), scale=0.1, command=self.active_etudiant, extraArgs=[3])

    def active_etudiant(self, info=1):
        """
        Méthode permettant d'afficher les dialogues de l'étudiant.
        -----------------------------------------------------------
        return -> None
        """
        properties = WindowProperties()
        properties.setCursorHidden(True)
        base.win.requestProperties(properties)
        self.bouton1.destroy()
        self.bouton2.destroy()
        self.bouton3.destroy()
        del self.bouton1, self.bouton2, self.bouton3
        if info == 1 or info == 2:
          self.music.setVolume(0.2)
          if info == 1:
              n = 11
          else:
              n = 12
          self.set_text(n, messages=["reupdate"])
        else:
          self.reupdate()

    def show_golem_options(self):
        """
        Méthode permettant à l'étudiant de présenter des options au joueur.
        -------------------------------------------------------------------
        return -> None
        """
        self.ignore(self.keys_data["Interagir"])
        properties = WindowProperties()
        properties.setCursorHidden(False)
        base.win.requestProperties(properties)
        self.bouton1 = DirectButton(text=(self.story["trigger"][7]), pos=Vec3(0.5, 0, 0), scale=0.1, command=self.active_golem, extraArgs=[1])
        self.bouton2 = DirectButton(text=(self.story["trigger"][6]), scale=0.1, pos=Vec3(-0.5, 0, 0), command=self.active_golem, extraArgs=[2])
        self.bouton3 = DirectButton(text=(self.story["trigger"][3]), pos=Vec3(0, 0, -0.5), scale=0.1, command=self.active_golem, extraArgs=[3])

    def active_golem(self, info=1):
        """
        Méthode permettant d'afficher les dialogues de l'étudiant.
        -----------------------------------------------------------
        return -> None
        """
        properties = WindowProperties()
        properties.setCursorHidden(True)
        base.win.requestProperties(properties)
        self.bouton1.destroy()
        self.bouton2.destroy()
        self.bouton3.destroy()
        del self.bouton1, self.bouton2, self.bouton3
        if info == 1 or info == 2:
          if info == 1:
            self.current_point = "save_desert"
          else:
            self.current_point = "save_crest"
          self.fade_out("Map")
        else:
          self.reupdate()

    def accept_trigger(self, clickedYes):
        """
        Méthode permettant d'exécuter l'action d'un trigger.
        ----------------------------------------------------
        clickedYes -> bool
        return -> None
        """
        self.triggerDlg.cleanup()
        properties = WindowProperties()
        properties.setCursorHidden(True)
        base.win.requestProperties(properties)
        self.accept("out", self.out)
        if self.actual_trigger == 0: #Voulez-vous vous rendre à Marelys ?
            if clickedYes:
                self.transition.fadeOut(1)
                taskMgr.doMethodLater(0.95, self.player.setPos, "new_player_pos", extraArgs=[(-1000, 650, 50)])
                taskMgr.doMethodLater(1, self.load_map, "loadmap", extraArgs=["Marelys.bam"])
        elif self.actual_trigger == 1: #Voulez-vous vous rendre au village des pêcheurs ?
            if clickedYes:
                self.transition.fadeOut(1)
                taskMgr.doMethodLater(1, self.player.setPos, "new_player_pos", extraArgs=[(0, -1075, 250)])
                taskMgr.doMethodLater(0.95, self.load_map, "loadmap", extraArgs=["village_pecheurs.bam"])
        elif self.actual_trigger == 2: #Tuez Zmeyevick ?
            if clickedYes:
                self.chapitre = 8
                self.fade_out("Cinematique")
        self.accept("escape", self.confirm_quit)
        taskMgr.add(self.update, "update")


    def vente(self, articles={"Vodka":30, "Tsar bomba":300, "Epée":50}):
        """
        Méthode qui s'active lorsqu'un pnj commerçant est interrogé.
        ------------------------------------------------------------
        articles -> dict
        return -> None
        """
        self.ignore("space")
        self.d_actif = False
        self.hide_gui()
        taskMgr.add(self.update_vente, "update vente")
        properties = WindowProperties()
        properties.setCursorHidden(False)
        base.win.requestProperties(properties)
        self.accept("escape", self.exit_vente)
        self.ignore(self.keys_data["Inventaire"])
        self.articles = self.genere_liste_defilement()
        for article in articles:
            bouton = DirectButton(text=article + " : " + str(articles[article]) + " noaïs",  text_scale=0.1, borderWidth=(0.01, 0.01), relief=2, command=self.add_article, extraArgs=[article, articles[article]])
            self.articles.addItem(bouton)

    def add_article(self, article="Vodka", prix=30):
        """
        Méthode permettant d'ajouter à l'inventaire du joueur un article acheté.
        ------------------------------------------------------------------------
        article -> str
        return -> None
        """
        armes = ["Epée"]
        if not self.d_actif:
            self.d_actif = True
            if self.player.noais >= prix:
                if article in armes:
                    if article in self.player.armes:
                       self.dialog = OkDialog(text=self.story["items"][4], command=self.cleanup_dialog_vente)
                       return None
                    else:
                      self.player.noais -= prix #On retire de l'argent au joueur $$$$
                      self.player.ajoute_arme(article)
                else:
                  self.player.noais -= prix #On retire de l'argent au joueur $$$$
                  self.player.ajoute_item(article)
                self.dialog = OkDialog(text=self.story["items"][2], command=self.cleanup_dialog_vente)
            else:
                self.dialog = OkDialog(text=self.story["items"][3], command=self.cleanup_dialog_vente)


    def cleanup_dialog_vente(self, inutile):
        """
        Méthode permettant d'effacer un pop-up de la vente.
        ---------------------------------------------------
        inutile -> bool
        return -> None
        """
        self.dialog.cleanup()
        self.d_actif = False

    def cleanup_dialog_tresor(self, inutile):
        """
        Méthode permettant d'enlever le dialogue de découverte d'un trésor.
        -------------------------------------------------------------------
        inutile -> bool
        return -> None
        """
        self.dialog.cleanup()
        properties = WindowProperties()
        properties.setCursorHidden(True)
        base.win.requestProperties(properties)
        taskMgr.add(self.update, "update")

    def exit_vente(self):
        """
        Méthode s'activant quand la transaction avec un pnj est finie.
        --------------------------------------------------------------
        return -> None
        """
        if not self.d_actif:
            properties = WindowProperties()
            properties.setCursorHidden(True)
            base.win.requestProperties(properties)
            taskMgr.add(self.update, "update")
            self.ignore("escape")
            self.accept("escape", self.confirm_quit)
            self.accept(self.keys_data["Inventaire"], self.inventaire)
            self.accept(self.keys_data["Interagir"], self.check_interact)
            self.articles.removeNode()
            self.accept("into", self.into)
            self.accept("out", self.out)
            self.accept("h", self.help)
            self.accept("space", self.check_interact)
            self.music.setVolume(1)
            self.current_pnj = None

    def update_vente(self, task=None):
        """
        Méthode permettant de mettre à jour la vente.
        ---------------------------------------------
        task -> task
        return -> task.cont
        """
        self.player_interface.ag.setText(f"{str(self.player.noais)}")
        return task.cont


    def reupdate(self):
        """
        Méthode permettant de réactiver la méthode update.
        --------------------------------------------------
        return -> None
        """
        if self.current_pnj == "mage" and self.chapitre == 3:
          self.ignore("space")
          self.chapitre = 4
          self.fade_out("Cinematique")
        self.music.setVolume(1)
        taskMgr.add(self.update, "update")
        self.accept("out", self.out)
        self.accept("escape", self.confirm_quit)
        self.accept(self.keys_data["Inventaire"], self.inventaire)
        self.accept("into", self.into)
        self.accept("h", self.help)

    def check_interact_dial(self):
        """
        "Petite" méthode qui permet de passer les dialogues.
        -----------------------------------------------------
        return -> bool
        """
        if not self.reading and not self.termine:
            self.reading = True
            return False
        elif self.reading:
            if self.letter_index >= len(self.texts[self.text_index]):
                self.text_index += 1
                if self.son is not None:
                    self.son.stop()
                    if len(self.sons_messages) > self.text_index:
                        try:
                            self.son = loader.loadSfx(self.sons_messages[self.text_index])
                            self.son.play()
                        except:
                            pass
                if self.text_index >= len(self.texts):
                    self.reading = False
                    self.termine = True
                    self.ok = False
                    self.text_index = 0
                    self.textObject.removeNode()
                    self.dialog_box.removeNode()
                    del self.textObject
                    del self.dialog_box
                    for message in self.messages:
                        base.messenger.send(message)
                    return True
                else:
                    self.letter_index = 0
                    return False
            else:
                self.letter_index = len(self.texts[self.text_index])
                return False

    def set_text(self, numero=0, messages=[]):
        """
        Méthode qui permet d'afficher un texte.
        ----------------------------------------
        numero -> int
        messages -> list[str]
        return -> None
        """
        if not hasattr(self, "story"):
            with open("../data/json/texts.json", encoding="utf-8") as texts:
                self.story = json.load(texts)[self.langue]
        if not self.reading:
            self.reading = True
            self.termine = False
            #On va chercher dans le fichier json, à la langue séléctionnée, le numéro de dialogue demandé
            if type(numero) is int:
                self.texts = self.story[str(numero)]
            else:
                self.texts = numero
            self.text_index = 0
            self.letter_index = 0
            self.sons_messages = []
            if os.path.exists(f"../data/sounds/dialogues/{numero}"):
                r = os.listdir(f"../data/sounds/dialogues/{numero}").copy()
                r.sort()
                for truc in r:
                    if truc.endswith(".ogg"):
                        self.sons_messages.append(f"../data/sounds/dialogues/{numero}/"+truc)
                    if len(self.sons_messages) == len(self.story[str(numero)]):
                        break
                if len(self.sons_messages) < len(self.story[str(numero)]):
                    while len(self.sons_messages) < len(self.story[str(numero)]):
                        self.sons_messages.append("../data/sounds/dialogues/blank.ogg")
            self.messages = messages
            #-------------Partie de chargement des fichiers audios de dialogue------------
            if len(self.sons_messages) > 0:
                try:
                    self.son = loader.loadSfx(self.sons_messages[0])
                    self.son.play()
                except:
                    pass

    def update_text(self, task):
        """
        Méthode qui met à jour le texte affiché à l'écran.
        (Il y a sans doute une meilleure solution, mais comme celle-ci Méthodene on la garde)
        --------------------------------------------------------------------------------------
        task -> task
        return -> task.cont
        """
        if self.reading:
            if self.ok:
                self.textObject.removeNode()
                self.dialog_box.removeNode()
                del self.textObject
                del self.dialog_box
            else:
                self.ok = True
            self.dialog_box = OnscreenImage("dialog_box.png", scale=Vec3(1.2, 0, 0.15), pos=Vec3(0, 0, -0.75))
            self.dialog_box.setTransparency(TransparencyAttrib.MAlpha)
            self.textObject = OnscreenText(text=self.texts[self.text_index][0:self.letter_index], pos=(0, -0.75), scale=0.07)
            if self.letter_index < len(self.texts[self.text_index]):
                self.letter_index += 1
        return task.cont

    #---------------------------Méthodes de changement de state--------------------------------------
    def fade_out(self, state="Menu"):
        """
        Méthode qui permet au FSM de changer de state avec un fade out visuel et sonore.
        ---------------------------------------------------------------------------------
        state -> str
        return None
        """
        self.transition.fadeOut(1)
        self.ignore("f1")
        Sequence(LerpFunc(self.music.setVolume, fromData = 1, toData = 0, duration = 1)).start()
        taskMgr.doMethodLater(1, self.change_state, "requete", extraArgs=[state])

    def change_state(self, state):
        """
        Méthode qui fonctionne avec la fonction fade_out.
        --------------------------------------------------
        state -> str
        return -> None
        """
        self.request(state)

    #------------------------Méthodes n'entrant dans aucune catégorie--------------------------
    def all_close(self):
        """
        Méthode pour fermer la fenêtre et quitter le programme.
        --------------------------------------------------------
        return -> None
        """
        base.destroy()
        os._exit(0)

    #---------------------------Ecran titre--------------------------------
    def enterMenu(self):
        """
        Méthode qui prépare l'écran titre.
        -----------------------------------
        return -> None
        """
        #--------------Petit fade in visuel et sonore-----------------
        self.transition.fadeIn(1)
        self.music = base.loader.loadSfx("menu.ogg")
        self.music.setLoop(True)
        self.music.play()
        Sequence(LerpFunc(self.music.setVolume, fromData = 0, toData = 1, duration = 1)).start()
        if hasattr(self, "player"):
            if hasattr(self.player, "followcam"):
                self.player.followcam.set_active(False)
        self.hide_gui()
        self.menu = True
        #-----------------------On charge le modèle du fond-----------------------------
        self.model = loader.loadModel("salle_du_sacrifice.bam")
        self.model.reparentTo(render)
        self.model.setPos((500, 500, 0))
        self.model.setHpr((270, 0, 0))
        base.cam.setPos((0, 0, 0))
        base.cam.setHpr((0, 0, 0))
        light = PointLight("Lumière d'un point")
        light.setColor((4, 4.5, 0.5, 1))
        light_np = render.attachNewNode(light)
        render.setLight(light_np)
        #-----------------------On définit notre séquence-----------------------------
        self.boucle = Sequence(base.cam.posInterval(10, Vec3(200, -200, 250), startPos=Vec3(200, -500, 250)), base.cam.posInterval(5, Vec3(300, -50, 275), startPos=Vec3(325, -50, 275)),
         base.cam.posInterval(5, Vec3(-125, -50, 200), startPos=Vec3(-150, -50, 200)))
        self.boucle.loop()
        #-----------------------On charge les textes------------------------------------
        self.textObject2 = OnscreenText(text=self.story["gui"][1], pos=(0, -0.8), scale=0.07, fg=(1, 1, 1, 1)) #Appuyez sur F1 pour commencer.
        self.image_logo = OnscreenImage("../data/pictures/Logo_Final_RoT.png", pos=Vec3(0, 0, 0.35), scale=(0.35, 1, 0.35))
        #--------------On modifie la caméra (position, lentille)-------------
        base.cam.node().getLens().setFov(70)
        #--------------------Gestion des touches----------------------------
        self.accept("escape", self.all_close)
        self.acceptOnce("f1", self.fade_out, extraArgs=["Trois_fichiers"])

    def exitMenu(self):
        """
        Méthode qui s'acive quand on quitte l'écran titre.
        ---------------------------------------------------
        return -> None
        """
        self.boucle.finish()
        del self.boucle
        render.clearLight()
        self.model.removeNode()
        del self.model
        self.textObject2.remove_node()
        self.image_logo.removeNode()
        del self.image_logo
        del self.textObject2

    #-----------------Section de gestion des trois fichiers de sauvegarde--------------------------------
    def enterTrois_fichiers(self):
        """
        Méthode qui s'active lorsqu'on entre dans le gestionnaire de fichiers de sauvegarde.
        -------------------------------------------------------------------------------------
        return -> None
        """
        self.ignoreAll()
        self.accept("escape", self.all_close)
        self.music.stop()
        self.music = loader.loadSfx("para.ogg")
        self.music.setLoop(True)
        self.music.play()
        Sequence(LerpFunc(self.music.setVolume, fromData = 0, toData = 1, duration = 1)).start()
        #-------------------On met un arrière-plan----------------------
        light = AmbientLight("ambient light")
        light_np = render.attachNewNode(light)
        render.setLight(light_np)
        self.actuals_light = [light_np]
        base.cam.setPosHpr(0, 10, 90, 55, 0, 0)
        self.player.setScale(8)
        self.map = loader.loadModel("village_pecheurs_maison_heros.bam")
        self.map.reparentTo(render)
        self.map.setScale(10)
        self.lit = loader.loadModel("lit.bam")
        self.lit.reparentTo(render)
        self.lit.setPos((-290, 95, 5))
        self.lit.setHpr((270, 0, 0))
        self.lit.setScale(15)
        self.player.setPosHpr(-280, 25, 45, 270, 0, 270)
        self.player.pose("Marche.001(real)", 17)
        self.player.show()
        base.cam.setPos((0, 0, 100))
        self.sequence = Sequence(base.cam.hprInterval(8, Vec3(80, 0, 0), startHpr=Vec3(0, 0, 0)), Func(base.cam.setHpr, (0, -55, 0)), base.cam.posInterval(10, Vec3(-280, 90, 120), Vec3(-280, 85, 140)), Func(base.cam.setPos, (0, 0, 100)))
        self.sequence.loop()
        #--------------On charge une image pour chaque fichier--------------------------------
        self.files = [OnscreenImage("file.png", scale=Vec3(0.3, 1, 0.3), pos=Vec3(-0.8+i*0.8, 1, 0)) for i in range(3)]
        for f in self.files:
            f.setTransparency(TransparencyAttrib.MAlpha)
        noms = []
        path = self.get_path()
        for loop in range(3):
            self.read(file=loop+1)
            if self.player.nom != "_":
                noms.append(self.player.nom)
            else:
                noms.append(self.story["gui"][2]) #Fichier vide
        self.player.nom = "Link"
        file = open(path+"/keys.json", "rt")
        self.keys_data = json.load(file)[0]
        file.close()
        self.buttons_continue = [DirectButton(text=self.story["gui"][3], scale=0.07, pos=(-0.8+0.8*i, 1, -0.08), command=self.verify, extraArgs=[i+1]) for i in range(3)] #Commencer
        self.buttons_erase = [DirectButton(text=self.story["gui"][4], scale=0.07, pos=(-0.8+0.8*i, 1, -0.18), command=self.confirm_erase, extraArgs=[i+1]) for i in range(3)] #Effacer
        self.names = [OnscreenText(text=noms[i], pos=(-0.8+0.8*i, 0.08), scale=0.07) for i in range(3)]
        self.button_mapping = DirectButton(text=self.story["gui"][5], scale=0.07, pos=(0.8, 1, -0.7), command=self.fade_out, extraArgs=["Mapping"]) #Mappage de touches
        self.button_langue = DirectButton(text=self.story["gui"][6], scale=0.07, pos=(-0.8, 1, -0.7), command=self.fade_out, extraArgs=["Language"]) #Changer la langue
        self.transition.fadeIn(1)

    def confirm_erase(self, file=1):
        """
        Méthode qui crée un petit pop-up qui permet de s'assurer que l'utilisateur veut effacer ses données.
        -----------------------------------------------------------------------------------------------------
        file -> int
        return -> None
        """
        self.eraseDlg = YesNoDialog(text=self.story["gui"][7], command=self.erase_file, extraArgs=[file]) #Voulez-vous vraiment effacer les données de sauvegarde ?


    def erase_file(self, clickedYes, file):
        """
        Méthode qui s'active lorsque l'utilisateur répond au pop-up pour l'effacement de fichier.
        ------------------------------------------------------------------------------------------
        clickedYes -> bool
        file -> int
        return -> None
        """
        self.eraseDlg.cleanup()
        if clickedYes:
            self.save(file=file, reset=True)
            for button in self.buttons_erase:
                button.removeNode()
            for button in self.buttons_continue:
                button.removeNode()
            self.fade_out()



    def exitTrois_fichiers(self):
        """
        Méthode qui s'active lorsque l'on quitte l'état trois_fichiers.
        ----------------------------------------------------------------
        return -> None
        """
        self.music.stop()
        self.player.setPos((0, 0, 0))
        self.player.setHpr((0, 0, 0))
        base.cam.setPos((0, 0, 0))
        base.cam.setHpr((0, 0, 0))
        self.accept(self.keys_data["Interagir"], self.check_interact)
        self.accept("escape", self.all_close)
        base.win.setCloseRequestEvent("escape")
        for file in self.files:
            file.removeNode()
        del self.files
        for light in self.actuals_light:
            light.removeNode()
        render.clearLight()
        self.player.hide()
        self.map.removeNode()
        self.lit.removeNode()
        del self.lit, self.map
        for button in self.buttons_continue:
            button.removeNode()
        del self.buttons_continue
        for button in self.buttons_erase:
            button.removeNode()
        del self.buttons_erase
        for name in self.names:
            name.removeNode()
        del self.names
        self.button_mapping.removeNode()
        del self.button_mapping
        self.button_langue.removeNode()
        del self.button_langue
        self.sequence.finish()
        del self.sequence

    def verify(self, file):
        """
        Quand on quitte l'écran titre, on vérifira notre avancement dans l'histoire.
        On agira de différentes manières selon le chapitre auquel le joueur est rendu.
        ------------------------------------------------------------------------------
        return -> None
        """
        self.actual_file = file
        self.read(file=file)
        with open("../data/json/texts.json", encoding="utf-8") as texts:
            self.story = json.load(texts)
        self.story = self.story[self.langue]
        #--------------Initialisation-----------------
        if self.chapitre == 0:
            self.request("Init")
        #----------------La légende------------------------
        elif self.chapitre == 1:
            self.request("Cinematique")
        #-----------------On charge la map-----------------------------------
        elif self.chapitre >= 2 and self.chapitre <= 7:
            Sequence(LerpFunc(self.music.setVolume, fromData = 1, toData = 0, duration = 2)).start()
            self.fade_out("Map")
        #------------Générique---------------------------
        else:
            self.request("Generique")


    #--------------------------------Gestion du changement de langue-----------------------------------------------
    def enterLanguage(self):
        """
        Méthode qui s'active lorsque l'on entre dans l'état de changement de langue.
        -----------------------------------------------------------------------------
        return -> None
        """
        self.transition.fadeIn(1)
        dico = {"français":0, "deutsch":1, "português":2, "english":3}
        self.textObject = OnscreenText(text="Veuillez choisir votre langue.", pos=(0, 0.7), scale=0.07, fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter, mayChange=1)
        self.menu = DirectOptionMenu(text="options", scale=0.15, pos=(-0.5, 0, 0), initialitem=dico[self.langue], items=["français", "deutsch", "português", "english"], highlightColor=(0.65, 0.65, 0.65, 1), command=self.itemSel, textMayChange=1)
        self.exit_button = DirectButton(text="Retour", scale=0.07, pos=(-0.8, 1, -0.7), command=self.fade_out, extraArgs=["Trois_fichiers"])
        if self.langue == "deutsch":
            self.textObject.setText("Bitte wählen Sie Ihre Sprache.")
            self.exit_button.setText("Zurück")
        elif self.langue == "português":
            self.textObject.setText("Favor escolhe o seu idioma.")
            self.exit_button.setText("Voltar")
        elif self.langue == "english":
            self.textObject.setText("Please, choose your language.")
            self.exit_button.setText("Back")

    def itemSel(self, arg):
        """
        Méthode qui s'active dès que l'utilisateur change de langue.
        ----------------------------------------------------------------
        arg -> str
        return -> None
        """
        self.langue = arg
        if self.langue == "français":
            self.textObject.setText("Veuillez choisir votre langue.")
            self.exit_button.setText("Retour")
        elif self.langue == "deutsch":
            self.textObject.setText("Bitte wählen Sie Ihre Sprache.")
            self.exit_button.setText("Zurück")
        elif self.langue == "português":
            self.textObject.setText("Favor escolhe o seu idioma ")
            self.exit_button.setText("Voltar")
        elif self.langue == "english":
            self.textObject.setText("Please, choose your language.")
            self.exit_button.setText("Back")

    def exitLanguage(self):
        """
        Méthode qui s'active lorsque l'on quitte l'état pour changer de langue.
        ---------------------------------------------------------------------------
        return -> None
        """
        self.save_global()
        with open("../data/json/texts.json", encoding="utf-8") as texts:
            self.story = json.load(texts)[self.langue]
        self.textObject.removeNode()
        del self.textObject
        self.menu.removeNode()
        del self.menu
        self.exit_button.removeNode()
        del self.exit_button

    #-------------------------------Gestion du mappage de touches--------------------------------------------------
    """
    Attention ! Cette partie, comme le fichier mappingGui.py n'a pas été
    entièrement codé par nous, mais seulement en partie modifié.
    Il fait partie d'un exemple de Panda3D.
    -------------------------------------------------------------------------------------
    Rendez-vous sur : https://docs.panda3d.org/1.10/python/more-resources/samples/gamepad
    """
    def enterMapping(self):
        """
        Méthode inspirée du script mappingGUI des samples de panda3d.
        ----------------------------------------------------------------
        Elle se déclenche lorsque l'on entre dans l'état Mapping.
        -------------------------------------------------------------
        return -> None
        """
        file = open(self.get_path()+"/keys.json", "rt")
        keys_data = json.load(file)
        file.close()
        keys_data = keys_data[0]
        liste_axe = ["left y 1", "right y 1", "right y -1", "right x 1", "right x -1"]
        self.mapping = InputMapping(keys_data) #On crée une instnce de la classe InputMapping.
        i = 0
        for key in keys_data:
            if not self.manette:
                self.mapping.mapButton(key, keys_data[key])
            else:
                if i < 5:
                    self.mapping.mapAxis(key, liste_axe[i])
                else:
                    self.mapping.mapButton(key, keys_data[key])
            i += 1
        #Ici, on crée un titre
        self.textscale = 0.1
        self.title = DirectLabel(
        scale=self.textscale,
        pos=(base.a2dLeft + 0.05, 0.0, base.a2dTop - (self.textscale + 0.05)),
        frameColor=VBase4(0, 0, 0, 0),
        text=self.story["gui"][18],
        text_align=TextNode.ALeft,
        text_fg=VBase4(1, 1, 1, 1),
        text_shadow=VBase4(0, 0, 0, 0.75),
        text_shadowOffset=Vec2(0.05, 0.05))
        self.title.setTransparency(1)
        #On crée le menu qui contiendra notre liste
        self.lstActionMap = DirectScrolledFrame(
        #On lui fait prendre toute la taille de la fenêtre
        frameSize=VBase4(base.a2dLeft, base.a2dRight, 0.0, 1.55),
        #On fait en sorte que le canevas soit aussi grand que le menu
        canvasSize=VBase4(base.a2dLeft, base.a2dRight, 0.0, 0.0),
        #Et on change la couleur du menu en blanc.
        frameColor=VBase4(0, 0, 0.25, 0.75),
        pos=(0, 0, -0.8),
        verticalScroll_scrollSize=0.2,
        verticalScroll_frameColor=VBase4(0.02, 0.02, 0.02, 1),
        verticalScroll_thumb_relief=1,
        verticalScroll_thumb_pressEffect=False,
        verticalScroll_thumb_frameColor=VBase4(0, 0, 0, 0),
        verticalScroll_incButton_relief=1,
        verticalScroll_incButton_pressEffect=False,
        verticalScroll_incButton_frameColor=VBase4(0, 0, 0, 0),
        verticalScroll_decButton_relief=1,
        verticalScroll_decButton_pressEffect=False,
        verticalScroll_decButton_frameColor=VBase4(0, 0, 0, 0),)
        idx = 0
        self.actionLabels = {}
        for action in self.mapping.actions:
            mapped = self.mapping.formatMapping(action)
            item = self.__makeListItem(action, mapped, idx)
            item.reparentTo(self.lstActionMap.getCanvas())
            idx += 1
        self.lstActionMap["canvasSize"] = (base.a2dLeft+0.05, base.a2dRight-0.05, -(len(self.mapping.actions)*0.1), 0.09)
        self.lstActionMap.setCanvasSize()
        self.button_retour = DirectButton(text=self.story["gui"][8], pos=(0.8, 1, -0.7), scale=0.07, command=self.fade_out, extraArgs=["Trois_fichiers"]) #Retour
        self.transition.fadeIn(2)

    def closeDialog(self, action, newInputType, newInput):
        """
        Méthode qui s'active lorsque l'on a répondu à la boîte de dialogue
        qui s'affiche quand on change les touches.
        -------------------------------------------------------------------
        action -> str
        newInputType -> str
        newInput -> str
        return -> None
        """
        self.dlgInput = None
        if newInputType is not None:
            #On change l'évènement pour l'action donnée.
            if newInputType == "axis":
                self.mapping.mapAxis(action, newInput)
            else:
                self.mapping.mapButton(action, newInput)
            #On met à jour la taille du texte dns la liste.
            self.actionLabels[action]["text"] = self.mapping.formatMapping(action)
        #On efface ce qui n'est pas nécessaire.
        for bt in base.buttonThrowers:
            bt.node().setSpecificFlag(True)
            bt.node().setButtonDownEvent("")
        for bt in base.deviceButtonThrowers:
            bt.node().setSpecificFlag(True)
            bt.node().setButtonDownEvent("")
        taskMgr.remove("checkControls")

    def changeMapping(self, action):
        """
        Méthode qui permet d'afficher le dialogue pour changer les touches.
        ----------------------------------------------------------------------
        action -> str
        return -> None
        """
        liste_interdite = ["Avancer", "Monter la camera", "Descendre la camera", "Camera a droite", "Camera a gauche"]
        if self.manette and action in liste_interdite:
            return None
        else:
            #On crée notre fenêtre de dialogue.
            self.dlgInput = ChangeActionDialog(action, command=self.closeDialog)
            #On attache les périphériques d'entrée
            devices = base.devices.getDevices()
            self.attachedDevices = devices
            # Disable regular button events on all button event throwers, and
            # instead broadcast a generic event.
            for bt in base.buttonThrowers:
                bt.node().setSpecificFlag(False)
                bt.node().setButtonDownEvent("keyListenEvent")
            for bt in base.deviceButtonThrowers:
                bt.node().setSpecificFlag(False)
                bt.node().setButtonDownEvent("deviceListenEvent")
            self.accept("keyListenEvent", self.dlgInput.buttonPressed)
            self.accept("deviceListenEvent", self.dlgInput.buttonPressed)
            self.axisStates = {None: {}}
            for device in devices:
                for axis in device.axes:
                    if device not in self.axisStates.keys():
                        self.axisStates.update({device: {axis.axis: axis.value}})
                    else:
                        self.axisStates[device].update({axis.axis: axis.value})
            taskMgr.add(self.watchControls, "checkControls")

    def watchControls(self, task):
        """
        Méthode qui vérifie si l'on touche à quelque chose.
        ----------------------------------------------------
        task -> task
        return -> task.cont
        """
        for device in self.attachedDevices:
            if device.device_class == InputDevice.DeviceClass.mouse:
                continue
            for axis in device.axes:
                if self.axisStates[device][axis.axis] + DEAD_ZONE < axis.value or \
                    self.axisStates[device][axis.axis] - DEAD_ZONE > axis.value:
                    self.axisStates[device][axis.axis] = axis.value
                    if axis.axis != InputDevice.Axis.none:
                        self.dlgInput.axisMoved(axis.axis)

        return task.cont

    def __makeListItem(self, action, event, index):
        """
        Méthode appelée pour créer un contenu.
        ---------------------------------------
        action -> str
        event -> str
        index -> int
        return -> DrectFrame
        """
        def dummy(): pass
        item = DirectFrame(
        text=action,
        geom_scale=(base.a2dRight-0.05, 1, 0.1),
        frameSize=VBase4(base.a2dLeft+0.05, base.a2dRight-0.05, -0.05, 0.05),
        frameColor=VBase4(1,0,0,0),
        text_align=TextNode.ALeft,
        text_scale=0.05,
        text_fg=VBase4(1,1,1,1),
        text_pos=(base.a2dLeft + 0.3, -0.015),
        text_shadow=VBase4(0, 0, 0, 0.35),
        text_shadowOffset=Vec2(-0.05, -0.05),
        pos=(0.05, 0, -(0.10 * index)))
        item.setTransparency(True)
        lbl = DirectLabel(
        text=event,
        text_fg=VBase4(1, 1, 1, 1),
        text_scale=0.05,
        text_pos=Vec2(0, -0.015),
        frameColor=VBase4(0, 0, 0, 0),
        )
        lbl.reparentTo(item)
        lbl.setTransparency(True)
        self.actionLabels[action] = lbl

        buttonScale = 0.15
        btn = DirectButton(
        text=self.story["gui"][19],
        scale=buttonScale,
        text_scale=0.25,
        text_align=TextNode.ALeft,
        text_fg=VBase4(0.898, 0.839, 0.730, 1.0),
        text_pos=Vec2(-0.9, -0.085),
        relief=1,
        pad=Vec2(0.01, 0.01),
        frameColor=VBase4(0, 0, 0, 0),
        frameSize=VBase4(-1.0, 1.0, -0.25, 0.25),
        pos=(base.a2dRight-(0.898*buttonScale+0.3), 0, 0),
        pressEffect=False,
        command=self.changeMapping,
        extraArgs=[action])
        btn.setTransparency(True)
        btn.reparentTo(item)
        return item

    """
    Fin de l'avertissement. A partir de maintenant, ce code est original est crée entièrement par nous.
    ---------------------------------------------------------------------------------------------------
    """
    def exitMapping(self):
        """
        Méthode qui s'active lorsque l'on quitte le mappage de touches.
        ---------------------------------------------------------------
        return -> None
        """
        if self.manette:
            file = open(self.get_path()+"/keys.json", "rt")
            data = json.load(file)[0]
            file.close()
            dico = self.mapping.get_map()
            for action in dico:
                if "face" in dico[action] or "shoulder" in dico[action]:
                    if not dico[action].startswith("manette"):
                        dico[action] = "manette-" + dico[action]
            dico["Avancer"], dico["Monter la camera"], dico["Descendre la camera"], dico["Camera a gauche"], dico["Camera a droite"] = data["Avancer"], data["Monter la camera"], data["Descendre la camera"], data["Camera a gauche"], data["Camera a droite"]
            file = open(self.get_path()+"/keys.json", "wt")
            file.writelines([json.dumps([dico])])
            file.close()
        else:
            file = open(self.get_path()+"/keys.json", "wt")
            file.writelines([json.dumps([self.mapping.get_map()])])
            file.close()
        self.title.removeNode()
        self.lstActionMap.removeNode()
        del self.lstActionMap
        del self.title
        self.button_retour.removeNode()
        del self.button_retour

    #-------------------------------Paramètres en début de partie (Nom du joueur)-----------------------------------
    def enterInit(self):
        """
        Méthode qui s'active quand on entre dans les paramètres en début de partie.
        ----------------------------------------------------------------------------
        return -> None
        """
        self.nameEnt = DirectEntry(scale = 0.08, pos = Vec3(-0.4, 0, 0.15), width = 10)
        self.nameLbl = DirectLabel(text = self.story["gui"][9], pos = Vec3(0, 0, 0.4), scale = 0.1, textMayChange = 1, frameColor = Vec4(1, 1, 1, 1)) #Salutations jeune aventurier, quel est ton nom ?
        self.helloBtn = DirectButton(text =self.story["gui"][10], scale = 0.1, command = self.setName, pos = Vec3(0, 0, -0.1)) #Confirmer

    def exitInit(self):
        """
        Méthode qui s'active quand on quitte ces paramètres.
        -----------------------------------------------------
        return -> None
        """
        self.music.stop()
        self.chapitre = 1

    def setName(self):
        """
        Petit pop-up de vérification.
        -----------------------------
        return -> None
        """
        self.acceptDlg = YesNoDialog(text =self.story["gui"][11], command = self.acceptName) #C'est tout bon ?

    def acceptName(self, clickedYes):
        """
        Méthode qui en fonction de la rééponse du joueur commence le jeu ou reste dans les paramètres.
        -----------------------------------------------------------------------------------------------
        clickedYes -> bool
        return -> None
        """
        self.acceptDlg.cleanup()
        if clickedYes:
            self.player.nom = self.nameEnt.get()
            self.nameLbl.removeNode()
            del self.nameLbl
            self.helloBtn.removeNode()
            del self.helloBtn
            self.nameEnt.removeNode()
            del self.nameEnt
            self.request("Mini_tuto")

    def enterMini_tuto(self):
        """
        Méthode qui permet d'afficher le tuto du début sur l'utilisation de la touche d'interaction.
        --------------------------------------------------------------------------------------------
        return -> None
        """
        self.tuto = OnscreenText(self.story["gui"][27]+self.keys_data["Interagir"].capitalize()+self.story["gui"][28], pos=(0, 0.4), scale=(0.13, 0.13), fg=(1, 1, 1, 1))
        self.ignore(self.keys_data["Interagir"])
        self.acceptOnce(self.keys_data["Interagir"], self.fade_out, extraArgs=["Cinematique"])

    def exitMini_tuto(self):
        """
        Méthode permettant de quitter le tuto.
        --------------------------------------
        return -> None
        """
        self.tuto.removeNode()
        self.ignore(self.keys_data["Interagir"])
        self.accept(self.keys_data["Interagir"], self.check_interact)

    #-------------------------------Cinématiques--------------------------------------
    def enterCinematique(self):
        """
        Méthode d'entrée dans le state Cinématique.
        -----------------------------------------------------------------
        return -> None
        """
        self.actuals_light = []
        #------------------------Légende-------------------------------------------------------
        if self.chapitre == 1:
            self.transition.fadeIn(1)
            self.chapitre_step = 0
            cm = CardMaker("plan")
            cm.setFrame(-1, 1, -1, 1)
            self.text_erreur = OnscreenText(text='*"Et on ne le revit jamais." (Toutes nos excuses pour les \npersonnes qui sont passionnées par la conjugaison)', pos=(0, -0.6), scale=(0.1, 0.1), fg=(1, 1, 1, 1))
            self.text_erreur.hide()
            self.plane = render2d.attachNewNode(cm.generate())
            self.texture = loader.loadTexture("test.mp4")
            self.son = loader.loadSfx("test.mp4")
            self.plane.setTexture(self.texture)
            self.plane.setTexScale(TextureStage.getDefault(), self.texture.getTexScale())
            self.texture.setLoop(0)
            self.texture.synchronizeTo(self.son)
            self.son.play()
            self.ignore(self.keys_data["Interagir"])
            self.acceptOnce(self.keys_data["Interagir"], self.texture.setTime, extraArgs=[64])
        elif self.chapitre == 3:
            self.load_map("village_pecheurs.bam")
            render.clearFog()
            fummee = Fog("Brume")
            fummee.setColor(0.5, 0.5, 0.55)
            fummee.setExpDensity(0.0005)
            render.setFog(fummee)
            self.pnj_bonus = Pecheur()
            self.pnj_bonus.reparentTo(render)
            self.pnj_bonus.setPos((-470, 175, 275))
            self.player.followcam.set_active(False)
            taskMgr.remove("update")
            self.player.show()
            self.player.col_np.removeNode()
            self.player.setPos((-490, 500, 275))
            self.player.setHpr((270, 0, 0))
            base.cam.setPos((-200, 500, 500))
            base.cam.setHpr((180, 0, 0))
            self.ignore_touches()
            self.accept(self.keys_data["Interagir"], self.check_interact)
            self.inventaire_mgr.cacher()
            self.player_interface.cacher()
            s = Sequence(Parallel(base.cam.posInterval(4, Vec3(-200, 200, 500)), base.cam.hprInterval(4, Vec3(90, -30, 0))), Func(self.player.loop, "Marche.001(real)"), Parallel(self.player.posInterval(2, Vec3(-480, 300, 275)), base.cam.posInterval(2, Vec3(-240, 200, 475))), Func(self.player.stop), Func(self.set_text, 15, ["texte_ok"]))
            s.start()
            self.accept("texte_ok", self.change_cine, extraArgs=[5])
            self.transition.fadeIn(2)
        elif self.chapitre == 4:
            taskMgr.remove("update")
            self.inventaire_mgr.cacher()
            self.player_interface.cacher()
            self.ignore_touches()
            self.accept("space", self.check_interact)
            a_light = AmbientLight("aa")
            a_light_np = render.attachNewNode(a_light)
            self.actuals_light.append(a_light_np)
            render.setLight(a_light_np)
            point_light = PointLight("point_light")
            point_light.setColor((8.5, 8, 5, 1))
            point_light_np = render.attachNewNode(point_light)
            point_light_np.setPos(0, 0, 0)
            self.actuals_light.append(point_light_np)
            render.setLight(point_light_np)
            base.cam.setPos(0, 0, 0)
            base.cam.setHpr(0, 0, 0)
            self.amulette = loader.loadModel("amulette.bam")
            self.amulette.reparentTo(render)
            self.amulette.setPos(0, 0, -10)
            self.amulette.setHpr(180, 90, 0)
            self.amulette.setScale(2)
            self.s = Sequence(self.amulette.hprInterval(5, Vec3(360, 270, 10), startHpr=Vec3(270, 90, 30)), self.amulette.hprInterval(5, Vec3(270, 89, 30), startHpr=Vec3(360, 270, 10)))
            self.s.loop()
            base.cam.lookAt(self.amulette)
            self.set_text(21, messages=["texte_ok"])
            self.accept("texte_ok", self.fade_out, extraArgs=["Map"])
            self.transition.fadeIn(2)
        elif self.chapitre == 5:
          taskMgr.remove("update")
          point_light = PointLight("point_light")
          point_light.setColor((0.7, 0.6, 0, 0.5))
          point_light_np = self.player.attachNewNode(point_light)
          point_light_np.setPos(0, 0, 20)
          self.actuals_light.append(point_light_np)
          render.setLight(point_light_np)
          self.inventaire_mgr.cacher()
          self.player_interface.cacher()
          self.load_map("pyramide.bam")
          self.player.show()
          self.player.setPos((-30, -20, 0))
          self.player.setHpr((270, 0, 0))
          base.cam.setPos((-6, 30, 30))
          base.cam.lookAt(self.player)
          self.ignore_touches()
          self.s = base.cam.posInterval(5, Vec3(-6, 30, 10))
          self.s.start()
          self.set_text(20, messages=["texte_ok"])
          self.current_point = "save_pyramide"
          self.accept("texte_ok", self.fade_out, extraArgs=["Map"])
          self.accept("space", self.check_interact)
          self.transition.fadeIn(2)
        elif self.chapitre == 6:
          self.music.stop()
          self.music = base.loader.loadSfx("Pyramide.ogg")
          self.music.setLoop(True)
          self.music.play()
          taskMgr.remove("update")
          a_light = AmbientLight("aa")
          a_light_np = render.attachNewNode(a_light)
          self.actuals_light.append(a_light_np)
          render.setLight(a_light_np)
          point_light = PointLight("point_light")
          point_light.setColor((7, 7, 0.5, 1))
          point_light_np = self.player.attachNewNode(point_light)
          point_light_np.setPos((1722, -3300, 0))
          self.actuals_light.append(point_light_np)
          render.setLight(point_light_np)
          self.inventaire_mgr.cacher()
          self.player_interface.cacher()
          self.ignore_touches()
          self.accept(self.keys_data["Interagir"], self.check_interact)
          self.pyramide = loader.loadModel("pyramide.bam")
          self.pyramide.reparentTo(render)
          self.pyramide.setScale(9)
          self.player.show()
          self.golem = Golem_pnj()
          self.golem.reparentTo(render)
          self.golem.setPos((1722, -3350, 0))
          self.player.setPos((1722, -3275, 40))
          self.player.setHpr((270, 0, 0))
          base.cam.setPos((1722, -2900, 340))
          base.cam.setHpr((180, -20, 0))
          self.s = Sequence(base.cam.hprInterval(10, (180, -30, 0), startHpr=(180, -20, 0)), base.cam.hprInterval(10, (180, -20, 0), startHpr=(180, -30, 0)))
          self.s.loop()
          self.set_text([self.story["24"][0]+self.player.nom+"."]+self.story["24"][1:], messages=["fin_discours"])
          self.acceptOnce("fin_discours", self.change_cine, extraArgs=[11])
          self.transition.fadeIn(2)
        elif self.chapitre == 8:
            self.chapitre_step = 0
            self.inventaire_mgr.cacher()
            self.player_interface.cacher()
            self.ignore_touches()
            self.actual_trigger = None
            self.accept(self.keys_data["Interagir"], self.check_interact)
            taskMgr.remove("update")
            if hasattr(self.player, "followcam"):
                self.player.followcam.set_active(False)
            self.player.show()
            self.player.pose("Marche.001(real)", 1)
            self.player.setPos(200, -400, 0)
            self.player.setH(90)
            self.player.setScale(10)
            if hasattr(self, "map"):
                if self.map is not None:
                    self.map.removeNode()
            self.move_camera = 0
            point_light = PointLight("point_light")
            point_light.setColor((0.85, 0.8, 0.5, 1))
            point_light_np = render.attachNewNode(point_light)
            point_light_np.setPos(200, 0, 50)
            self.actuals_light.append(point_light_np)
            render.setLight(point_light_np)
            self.map = loader.loadModel("salle_du_sacrifice.bam")
            self.map.reparentTo(render)
            self.map.setPos(500, 500, 0)
            self.map.setHpr(270, 0, 0)
            self.magicien = Magicien()
            self.magicien.setScale(60)
            self.magicien.setPos(200, 200, 0)
            self.magicien.loop("Immobile")
            self.magicien.reparentTo(render)
            base.cam.setPos(200, -550, 250)
            base.cam.setHpr((0, 0, 0))
            self.music.stop()
            self.music = base.loader.loadSfx("Le_magicien_démoniaque.ogg")
            self.music.setTime(7.6)
            self.music.setLoop(True)
            self.music.play()
            self.music.setVolume(0.3)
            self.set_text(1, messages=["Fini"])
            self.acceptOnce("Fini", self.change_cine, extraArgs=[13])
            self.transition.fadeIn(2)
        elif self.chapitre == 949:
            taskMgr.remove("update")
            a_light = AmbientLight("aa")
            a_light_np = render.attachNewNode(a_light)
            self.actuals_light.append(a_light_np)
            render.setLight(a_light_np)
            point_light = PointLight("point_light")
            point_light.setColor((7, 7, 7, 1))
            point_light_np = self.player.attachNewNode(point_light)
            point_light_np.setPos(0, 0, 20)
            self.actuals_light.append(point_light_np)
            render.setLight(point_light_np)
            self.inventaire_mgr.cacher()
            self.player_interface.cacher()
            self.ignore_touches()
            self.accept(self.keys_data["Interagir"], self.check_interact)
            base.cam.setPos(0, -15, 2)
            base.cam.setHpr((0, 0, 0))
            self.tsar_bomba = loader.loadModel("tsar_bomba.bam")
            self.tsar_bomba.reparentTo(render)
            self.tsar_bomba.hprInterval(4, (270, 0, 0), startHpr=(0, 0, 0)).loop()
            self.set_text(23, messages=["launch_generique"])
            self.accept("launch_generique", self.request, extraArgs=["Generique"])
            self.transition.fadeIn(2)
        taskMgr.add(self.update_cinematique, "update_cinematique")


    def change_cine(self, cine=0, task=None):
        """
        Méthode permettant de faire apparaître la cinématique du magicien.
        ------------------------------------------------------------------
        task -> task ou None
        return -> None
        """
        if cine == 0:
            self.son.stop()
            self.plane.removeNode()
            del self.plane
            if hasattr(self.player, "followcam"):
                self.player.followcam.set_active(False)
            self.player.show()
            self.player.pose("Marche.001(real)", 1)
            self.player.setPos(200, -400, 0)
            self.player.setH(90)
            self.player.setScale(10)
            if hasattr(self, "map"):
                if self.map is not None:
                    self.map.removeNode()
            self.move_camera = 0
            point_light = PointLight("point_light")
            point_light.setColor((0.85, 0.8, 0.5, 1))
            point_light_np = render.attachNewNode(point_light)
            point_light_np.setPos(200, 0, 50)
            self.actuals_light.append(point_light_np)
            render.setLight(point_light_np)
            self.map = loader.loadModel("salle_du_sacrifice.bam")
            self.map.reparentTo(render)
            self.map.setPos(500, 500, 0)
            self.map.setHpr(270, 0, 0)
            self.magicien = Magicien()
            self.magicien.setScale(60)
            self.magicien.setPos(200, 200, 0)
            self.magicien.loop("Immobile")
            self.magicien.reparentTo(render)
            base.cam.setPos(200, -550, 250)
            base.cam.setHpr((0, 0, 0))
            self.music.stop()
            self.music = base.loader.loadSfx("Le_magicien_démoniaque.ogg")
            self.music.setLoop(True)
            self.music.play()
            self.music.setVolume(0.3)
            self.transition.fadeIn(2)
            self.set_text(1, ["Fini"])
            self.accept("Fini", self.change_cine, extraArgs=[1])
        elif cine == 1:
            self.transition.fadeOut(2)
            self.son.stop()
            self.map.removeNode()
            del self.map
            self.magicien.delete()
            del self.magicien
            taskMgr.doMethodLater(2, self.change_cine, "change cine", extraArgs=[2])
        elif cine == 2:
            for light in self.actuals_light:
                render.clearLight(light)
                light.removeNode()
            light = AmbientLight("ambient light")
            light_np = render.attachNewNode(light)
            render.setLight(light_np)
            self.actuals_light = [light_np]
            base.cam.setPosHpr(0, 10, 90, 55, 0, 0)
            self.player.setScale(8)
            self.map = loader.loadModel("village_pecheurs_maison_heros.bam")
            self.map.reparentTo(render)
            self.map.setScale(10)
            self.lit = loader.loadModel("lit.bam")
            self.lit.reparentTo(render)
            self.lit.setPos((-290, 95, 5))
            self.lit.setHpr((270, 0, 0))
            self.lit.setScale(15)
            self.player.setPosHpr(-280, 25, 45, 270, 0, 270)
            self.player.pose("Marche.001(real)", 17)
            self.transition.fadeIn(2)
            self.chapitre_step = 2
            s = Sequence(Parallel(base.cam.posInterval(7, Vec3(-270, 120, 150), startPos=Vec3(0, 10, 90)), base.cam.hprInterval(7, Vec3(0, -70, 0), startHpr=Vec3(55, 0, 0))), Func(self.set_text, 3, ["texte_ok"]))
            s.start()
            self.accept("texte_ok", self.change_cine, extraArgs=[3])
        elif cine == 3:
            texts = self.story["0"]
            texts[0] = texts[0] + self.player.nom + " !"
            self.s = Sequence(base.cam.hprInterval(4, Vec3(-140, 0, 0), startHpr=Vec3(0, -70, 0)), Func(self.set_text, texts, ["texte_ok"]))
            self.s.start()
            self.ignore("texte_ok")
            self.accept("texte_ok", self.change_cine, extraArgs=[4])
        elif cine == 4:
            self.ignore("texte_ok")
            self.fade_out("Map")
            self.first_time = True
        elif cine == 5:
            self.ignore("texte_ok")
            self.accept("texte_ok", self.change_cine, extraArgs=[6])
            self.s = Parallel(base.cam.hprInterval(1, Vec3(15, 0, 0)), base.cam.posInterval(1, Vec3(-430, 250, 400)))
            self.s.start()
            self.set_text(16, ["texte_ok"])
        elif cine == 6:
            self.ignore("texte_ok")
            self.accept("texte_ok", self.change_cine, extraArgs=[7])
            self.s.finish()
            self.s = base.cam.hprInterval(1, Vec3(165, 0, 0))
            self.s.start()
            self.set_text(17, ["texte_ok"])
        elif cine == 7:
            self.ignore("texte_ok")
            self.accept("texte_ok", self.change_cine, extraArgs=[8])
            self.s.finish()
            self.s = base.cam.hprInterval(1, Vec3(15, 0, 0))
            self.s.start()
            self.set_text(18, ["texte_ok"])
        elif cine == 8:
            self.ignore("texte_ok")
            self.accept("texte_ok", self.fade_out, extraArgs=["Map"])
            self.travel = 0
            self.s.finish()
            self.set_text(19, ["texte_ok"])
        elif cine == 9:
            self.s.finish()
            self.music.stop()
            base.cam.node().getLens().setFov(70)
            self.music = base.loader.loadSfx("Le_magicien_démoniaque.ogg")
            self.music.setTime(7.6)
            self.music.setLoop(True)
            self.music.play()
            self.pyramide.hide()
            self.golem.hide()
            self.player.hide()
            self.model = loader.loadModel("salle_du_sacrifice.bam")
            self.model.reparentTo(render)
            self.model.setPos((500, 500, 0))
            self.model.setHpr((270, 0, 0))
            base.cam.setPos((0, 0, 100))
            base.cam.setHpr((0, 0, 0))
            render.clearLight()
            light = PointLight("Lumière d'un point")
            light.setColor((4, 4.5, 0.5, 1))
            light_np = render.attachNewNode(light)
            render.setLight(light_np)
            self.actuals_light.append(light_np)
            #-----------------------On définit notre séquence-----------------------------
            self.boucle = Sequence(base.cam.posInterval(10, Vec3(200, -200, 250), startPos=Vec3(200, -500, 250)), base.cam.posInterval(5, Vec3(300, -50, 275), startPos=Vec3(325, -50, 275)),
             base.cam.posInterval(5, Vec3(-125, -50, 200), startPos=Vec3(-150, -50, 200)))
            self.boucle.loop()
            self.set_text(25, messages=["fin_discours"])
            self.acceptOnce("fin_discours", self.change_cine, extraArgs=[12])
            self.transition.fadeIn(2)
        elif cine == 10:
            for light in self.actuals_light:
              render.clearLight(light)
              light.removeNode()
            self.actuals_light = []
            self.music.stop()
            base.cam.node().getLens().setFov(100)
            self.music = base.loader.loadSfx("menu.ogg")
            self.music.setLoop(True)
            self.music.play()
            self.player.show()
            self.golem.show()
            self.pyramide.show()
            base.cam.setPos((1722, -3000, 400))
            base.cam.setHpr((180, -30, 0))
            self.s = Sequence(base.cam.hprInterval(10, (180, -40, 0), startHpr=(180, -30, 0)), base.cam.hprInterval(10, (180, -30, 0), startHpr=(180, -40, 0)))
            self.s.loop()
            self.set_text(26, messages=["fin_discours"])
            self.acceptOnce("fin_discours", self.fade_out, extraArgs=["Map"])
            light = PointLight("lanterne")
            light.color = (2, 2, 0.25, 1)
            light_np = self.player.attachNewNode(light)
            light_np.setPos((0, 1, 1))
            render.setLight(light_np)
            self.actuals_light.append(light_np)
            light = PointLight("lanterne")
            light.color = (0.25, 3, 0.25, 1)
            light_np = self.golem.attachNewNode(light)
            light_np.setPos((0, 1, 1))
            render.setLight(light_np)
            self.actuals_light.append(light_np)
            self.transition.fadeIn(2)
        elif cine == 11:
            self.transition.fadeOut(2)
            taskMgr.doMethodLater(2.5, self.change_cine, "changement de cinématique", extraArgs=[9])
        elif cine == 12:
            self.boucle.finish()
            del self.boucle
            self.transition.fadeOut(2)
            self.model.removeNode()
            del self.model
            taskMgr.doMethodLater(2.5, self.change_cine, "changement de cinématique", extraArgs=[10])
        elif cine == 13:
            self.transition.fadeOut(2)
            self.chapitre_step = 1
            taskMgr.doMethodLater(2, self.change_cine, "changement de cinématique", extraArgs=[14])
        elif cine == 14:
            for light in self.actuals_light:
              render.clearLight(light)
              light.removeNode()
            self.actuals_light = []
            l = AmbientLight("ambiante")
            l_np = render.attachNewNode(l)
            render.setLight(l_np)
            self.actuals_light.append(l_np)
            fummee = Fog("neige")
            fummee.setColor(1, 1, 1)
            fummee.setExpDensity(0.0004)
            render.setFog(fummee)
            self.player.hide()
            self.magicien.hide()
            self.skybox = loader.loadModel("skybox.bam")
            self.skybox.setScale(10000)
            self.skybox.setBin('background', 1)
            self.skybox.setDepthWrite(0)
            self.skybox.setLightOff()
            self.skybox.reparentTo(render)
            self.crest = loader.loadModel("Crest.bam")
            self.crest.reparentTo(render)
            self.crest.setScale(750)
            self.forteresse = loader.loadModel("Forteresse.bam")
            self.forteresse.setScale(100)
            self.forteresse.reparentTo(render)
            self.forteresse.setPos((0, 100, 0))
            self.map.setHpr((0, 0, 0))
            self.map.setPos((-1000, 400, 270))
            base.cam.setPos((1000, 150, 300))
            base.cam.setHpr((90, 0, 0))
            self.s1 = self.map.posInterval(7, Vec3(-1000, 400, -100), startPos=Vec3(-1000, 400, 270))
            self.s1.start()
            taskMgr.doMethodLater(8, self.change_cine, "changement de cinématique", extraArgs=[15])
            self.transition.fadeIn(2)
        elif cine == 15:
            self.s1.finish()
            self.transition.fadeOut(1)
            del self.s1
            taskMgr.doMethodLater(2, self.change_cine, "changement", extraArgs=[16])
        elif cine == 16:
            for light in self.actuals_light:
              render.clearLight(light)
              light.removeNode()
            self.actuals_light = []
            l = AmbientLight("ambiante")
            l.color = (0.4, 1.2, 0.4, 1)
            l_np = render.attachNewNode(l)
            render.setLight(l_np)
            self.actuals_light.append(l_np)
            self.forteresse.removeNode()
            render.clearFog()
            self.map.removeNode()
            self.crest.removeNode()
            self.skybox.removeNode()
            del self.map, self.crest, self.forteresse, self.skybox
            self.arene = loader.loadModel("arene.bam")
            self.arene.reparentTo(render)
            self.player.show()
            self.magicien.show()
            self.player.setPos((0, 0, 55))
            self.magicien.setPos((0, -30, 60))
            base.cam.setPos(self.player, Vec3(20, 0, 30))
            base.cam.setHpr((180, -45, 0))
            self.arene.setScale(10)
            self.music.stop()
            self.music = base.loader.loadSfx("Zmeyevick,_l'antique_terreur_phase_1.ogg")
            self.music.setLoop(True)
            self.music.play()
            self.transition.fadeIn(2)
            self.set_text(["Le processus de résurection \nde l'hydre est presque terminé !", "Tu seras la première victime de\n la folie meurtrière de Zmeyevick.", "Profite-bien !\n Hahahahaha !"], messages=["fini"])
            self.acceptOnce("fini", self.change_cine, extraArgs=[17])
        elif cine == 17:
            self.magicien.cleanup()
            self.magicien.removeNode()
            del self.magicien
            self.chapitre_step = 2
            self.hydre = Actor("Zmeyevick_fin.bam")
            self.hydre.reparentTo(render)
            self.hydre.loop("Armature.002Action")
            self.hydre.setPos(Vec3(0, 0, -100))
            self.hydre.posInterval(10, Vec3(0, 0, -100), startPos=Vec3(0, 0, 0)).start()
        if task is not None:
            return task.done


    def update_cinematique(self, task):
        """
        Méthode qui permet de mettre à jour la cinématique.
        -----------------------------------------------------------------------------------
        task -> task
        return -> task.cont ou task.done
        """
        dt = globalClock.getDt()
        if self.chapitre == 1:
            if self.texture.getTime() > 51 and self.texture.getTime() < 55 and self.chapitre_step == 0:
                self.text_erreur.show()
            elif self.texture.getTime() > 55 and self.texture.getTime() < 63:
                self.text_erreur.hide()
            elif self.texture.getTime() > 64 and self.chapitre_step == 0:
                self.chapitre_step = 1
                self.text_erreur.removeNode()
                del self.text_erreur
                self.transition.fadeOut(2)
                self.ignore(self.keys_data["Interagir"])
                self.accept(self.keys_data["Interagir"], self.check_interact)
                taskMgr.doMethodLater(2, self.change_cine, "magic_cine", extraArgs=[0], appendTask=True)
            elif self.chapitre == 1 and self.chapitre_step == 1:
                if self.text_index  <= 4:
                    if base.cam.getY() < 200:
                        base.cam.setY(base.cam, dt*60)
                elif self.text_index <= 6:
                    if self.move_camera == 0:
                        self.move_camera = 1
                        base.cam.setPosHpr(200, 200, 200, 180, 0, 0)
                    if base.cam.getY() > -100:
                        base.cam.setY(base.cam, dt*25)
        elif self.chapitre == 3:
            if hasattr(self, "travel"):
                if self.text_index == 0 and self.travel == 0:
                    self.travel = 1
                    base.cam.setHpr(180, 0, 0)
                    self.s = base.cam.posInterval(3, Vec3(-450, 50, 350), startPos=Vec3(-450, 150, 350))
                    self.s.start()
                elif self.text_index == 1 and self.travel == 1:
                    self.travel = 2
                    self.s.finish()
                    self.s = base.cam.posInterval(3, Vec3(0, -250, 350), startPos=Vec3(0, -50, 350))
                    self.s.start()
        elif self.chapitre == 8 and self.chapitre_step == 0:
          if self.text_index  <= 4:
            if base.cam.getY() < 200:
              base.cam.setY(base.cam, dt*60)
          elif self.text_index <= 6:
            if self.move_camera == 0:
              self.move_camera = 1
              base.cam.setPosHpr(200, 200, 200, 180, 0, 0)
            if base.cam.getY() > -100:
              base.cam.setY(base.cam, dt*25)
        elif self.chapitre == 8 and self.chapitre_step == 2:
            """if self.magicien.getTransparency() > 0.1:
                t = self.magicien.getTransparency()
                t -= dt*0.01
                self.magicien.setTransparency(t)
            else:
                if hasattr(self, "magicien"):
                    self.magicien.removeNode()
                    del self.magicien"""
            pass
        return task.cont


    def exitCinematique(self):
        """
        Méthode de sortie du state cinématique.
        ------------------------------------------
        return -> None
        """
        self.ignore("texte_ok")
        for light in self.actuals_light:
            render.clearLight(light)
            light.removeNode()
        del self.actuals_light
        taskMgr.remove("update_cinematique")
        if self.chapitre == 1:
            self.lit.removeNode()
            self.music.stop()
            self.player.setHpr(0, 0, 0)
            base.cam.setPosHpr(0, 0, 0, 0, 0, 0)
            self.chapitre = 2
        elif self.chapitre == 3:
            self.s.finish()
            del self.s
            self.current_point = "save_village"
            del self.travel
            self.player.col_np = self.player.attachNewNode(self.player.col)
            self.pnj_bonus.cleanup()
            self.pnj_bonus.removeNode()
            taskMgr.doMethodLater(1.1, self.music.setVolume, "volume", extraArgs=[1])
        elif self.chapitre == 4:
          self.current_point = "save_ignirift"
          self.amulette.removeNode()
          self.player.inventaire["Amulette"] = 1
        elif self.chapitre == 5:
          self.s.finish()
          taskMgr.doMethodLater(1.1, self.music.setVolume, "volume", extraArgs=[1])
        elif self.chapitre == 6:
            self.music.stop()
            self.s.finish()
            del self.s
            self.chapitre = 7
            self.hack = True
            self.golem.removeNode()
            self.pyramide.removeNode()
            del self.golem, self.pyramide
        elif self.chapitre == 949:
            self.tsar_bomba.removeNode()

    #-----------------------------Map (chargement et state)--------------------------------
    def load_map(self, map="village_pecheurs_maison_heros.bam", position=None, task=None):
        """
        Méthode qui nous permet de charger une map.
        --------------------------------------------
        map -> str
        task -> None (ou task)
        return -> None
        """
        render.clearFog()
        for pnj in self.pnjs:
            self.pnjs[pnj].cleanup()
            self.pnjs[pnj].removeNode()
        for pnj in self.monstres:
            self.monstres[pnj].cleanup()
            self.monstres[pnj].removeNode()
        for objet in self.objects:
            if objet.nom == "coffre":
                objet.object.cleanup()
            objet.object.removeNode()
        for mur in self.murs:
            mur.removeNode()
        for porte in self.portails:
            self.portails[porte][0].removeNode()
        for statue in self.save_statues:
            self.save_statues[statue][0].removeNode()
            self.save_statues[statue][1].removeNode()
        self.objects = []
        self.murs = []
        self.monstres = {}
        self.current_pnj = None
        self.current_porte = None
        self.pnjs = {}
        self.portails = {}
        self.save_statues = {}
        base.win.movePointer(0, int(base.win.getProperties().getXSize()/2), int(base.win.getProperties().getYSize()/2))
        if hasattr(self, "actuals_light"):
            for light in self.actuals_light:
                render.clearLight()
                light.removeNode()
        self.actuals_light = []
        #-------Chargement du modèle de la map------------
        self.current_map = map
        if hasattr(self, "map"):
            if self.map is not None:
                self.map.removeNode()
            del self.map
        self.map = loader.loadModel(map)
        self.map.reparentTo(render)
        #---------------------------Collisions de la map------------------
        self.antimur.addInPattern("into")
        self.antimur.addOutPattern("out")
        self.map.setCollideMask(BitMask32.bit(0))
        if self.debug:
            base.cTrav.showCollisions(render)
        self.antimur.addCollider(self.player.col_np, self.player)
        base.cTrav.addCollider(self.player.col_np, self.antimur)
        #-----------------------Fumée---------------------
        self.load_fog()
        #--------------La skybox----------------------------
        if self.skybox is not None:
            self.skybox.removeNode()
        self.skybox = loader.loadModel("skybox.bam")
        self.skybox.setPos(self.skybox, (0, 0, -50000))
        self.skybox.setScale(5000)
        self.skybox.setBin('background', 1)
        self.skybox.setDepthWrite(0)
        self.skybox.setLightOff()
        self.skybox.reparentTo(render)
        #--------------------Chargement du premier fichier json (objets)---------------
        objects_file = open("../data/json/objects.json")
        data = json.load(objects_file)
        objects_file.close()
        n_coffre = 0
        numero_panneau = 0
        if self.current_map in data:
            i = 0
            for cle in data[self.current_map]:
                if cle[0] == "lit":
                    objet = Lit()
                elif cle[0] == "bateau":
                    objet = Bateau()
                elif cle[0] == "coffre":
                    objet = Coffre(n_coffre, ouvert=self.get_ouvert(self.current_map, n_coffre))
                    n_coffre += 1
                elif cle[0] == "sapin":
                    objet = Sapin()
                elif cle[0] == "manoir":
                    objet = Manoir()
                elif cle[0] == "palmier":
                    objet = Palmier()
                elif cle[0] == "maison_aurelia":
                    objet = Maison_aurelia()
                elif cle[0] == "Forteresse":
                    objet = Forteresse()
                elif cle[0] == "armoire":
                    objet = Armoire()
                elif cle[0] == "panneau":
                    objet = Panneau(text=self.get_text_panneau(numero_panneau), numero=numero_panneau)
                    numero_panneau += 1
                elif cle[0] == "Salle":
                    objet = Salle()
                elif cle[0] == "collier":
                    objet = Collier()
                else:
                    objet = Objet(cle[0])
                objet.object.reparentTo(render)
                objet.object.setPos((data[self.current_map][i][1][0][0], data[self.current_map][i][1][0][1], data[self.current_map][i][1][0][2]))
                objet.object.setHpr((data[self.current_map][i][1][1][0], data[self.current_map][i][1][1][1], data[self.current_map][i][1][1][2]))
                self.objects.append(objet)
                i += 1
        #--------------------Chargement du deuxième fichier json-------------
        pnj_file = open("../data/json/data.json")
        data = json.load(pnj_file)
        pnj_file.close()
        #-----Section de gestion de la musique------
        if not hasattr(self, "music_name"):
            self.music_name = data[self.current_map][0]
            self.music = base.loader.loadSfx(data[self.current_map][0])
            self.music.setLoop(True)
            self.music.play()
        if self.music is not None and self.music_name != data[self.current_map][0]:
            self.music.stop()
            self.music = None
        if self.music_name != data[self.current_map][0]:
            self.music_name = data[self.current_map][0]
            self.music = base.loader.loadSfx(data[self.current_map][0])
            self.music.setLoop(True)
            self.music.play()
        self.music.setVolume(1)
        #---------------------Gestion de la caméra du joueur----------------
        if not hasattr(self.player, "followcam"):
                self.player.create_camera()
        if not self.player.followcam.active:
            self.player.followcam.set_active(True)
        self.player.followcam.dummy.setHpr(270, 0, 0)
        self.player.followcam.camera.setHpr(0, 0, 0)
        self.player.followcam.camera.setPos(0, -16, 0)
        #----------Les portes-----------------------
        for portail in data[self.current_map][2]:
            noeud = CollisionNode(portail)
            info = data[self.current_map][2][portail]
            if info[0] == "porte":
                solid = Porte(center=(info[1][0], info[1][1], info[1][2]), sx=info[2], sy=info[3], sz=info[4], newpos=(info[5][0], info[5][1], info[5][2]))
            else:
                solid = Portail(center=(info[1][0], info[1][1], info[1][2]), sx=info[2], sy=info[3], sz=info[4], newpos=(info[5][0], info[5][1], info[5][2]))
            noeud.addSolid(solid)
            noeud.setCollideMask(BitMask32.bit(0))
            noeud_np = self.map.attachNewNode(noeud)
            if len(info) > 6:
                solid.orientation = info[6]
            self.portails[portail] = (noeud_np, solid)
            #noeud_np.show() #Décommentez pour voir les portes et les portails.
        #------------------Les pnjs--------------------------------
        for pnj in data[self.current_map][1]:
            info = data[self.current_map][1][pnj]
            a = self.return_pnj(pnj)
            a.setPos(info[0], info[1], info[2])
            self.pnjs[pnj] = a
        for pnj in self.pnjs:
            self.pnjs[pnj].reparentTo(render)
        #------------------Les monstres--------------------------------
        for pnj in data[self.current_map][7]:
            info = data[self.current_map][7][pnj]
            a = self.return_monstre(pnj)
            a.setPos(info[0], info[1], info[2])
            self.monstres[pnj] = a
        for pnj in self.monstres:
            self.monstres[pnj].reparentTo(render)
        #-------------Les points de sauvegardes------------------------
        for save in data[self.current_map][3]:
            noeud = CollisionNode(save)
            noeud.addSolid(Save_bloc(save, data[self.current_map][3][save][0:3]))
            noeud.setCollideMask(BitMask32.bit(0))
            noeud_np = self.map.attachNewNode(noeud)
            if self.current_map == "Ignirift.bam":
                noeud_np.setScale(0.25)
                noeud_np.setY(noeud_np, -6.25)
            #noeud_np.show() #Décommentez pour voir les solides de collision de sauvegardes.
            model_save = loader.loadModel("save_point.bam")
            model_save.reparentTo(render)
            model_save.setPos((data[self.current_map][3][save][0]*data[self.current_map][4], data[self.current_map][3][save][1]*data[self.current_map][4], data[self.current_map][3][save][2]*data[self.current_map][4]))
            if len(data[self.current_map][3][save]) > 3:
                if data[self.current_map][3][save][3] == "gauche":
                    model_save.setH(90)
                elif data[self.current_map][3][save][3] == "devant":
                    model_save.setH(180)
                else:
                    model_save.setH(270)
            model_save.setScale(18.5)
            self.save_statues[save] = [noeud_np, model_save]
        self.load_triggers(map)
        self.map.setScale(data[self.current_map][4])
        #-----------------Eau--------------------------------------
        if data[self.current_map][5] == "Vrai" and not hasattr(self, "eau"):
            self.eau = loader.loadModel("eau.bam")
            self.eau.reparentTo(render)
            self.eau.setScale(3)
            self.eau.setSx(10000)
            self.eau.setSy(10000)
            self.eau.setZ(self.eau, 10)
        else:
            if hasattr(self, "eau"):
                self.eau.removeNode()
                del self.eau
        #--------------------Les murs (invisibles)-------------------------
        i = 0
        for mur in data[self.current_map][6]:
            i += 1
            noeud = CollisionNode("mur"+str(i))
            a = (mur[0][0], mur[0][1], mur[0][2])
            noeud.addSolid(CollisionBox(a, mur[1][0], mur[1][1], mur[1][2]))
            noeud.setCollideMask(BitMask32.bit(0))
            noeud_np = self.map.attachNewNode(noeud)
            #noeud_np.show() #Décommentez pour voir les murs.
            self.murs.append(noeud_np)
        if self.current_map == "Marelys.bam":
            plane = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0.8)))
            plane_n = CollisionNode("Sol")
            plane_n.addSolid(plane)
            plane_n.setCollideMask(BitMask32.bit(0))
            plane_np = self.map.attachNewNode(plane_n)
            self.murs.append(plane_np)
        del data, i
        #------------Mode debug------------------------
        if self.debug:
            base.enableMouse()
        else:
            base.disableMouse()
        #-------------Lumière----------------------------
        if hasattr(self, "actuals_light"):
            for light in self.actuals_light:
                render.clearLight(light)
                light.removeNode()
        self.actuals_light = []
        self.load_light()
        if position is not None:
            self.player.setPos(position)
        self.transition.fadeIn(2)
        self.accept_touches()
        if task is not None:
            return task.done

    def quit_crest(self):
        """
        Méthode permettant de sortir de Crest.
        --------------------------------------
        return -> None
        """
        self.current_point = "save_desert"
        self.fade_out("Map")

    def get_ouvert(self, map="village_pecheurs.bam", numero=0):
        """
        Méthode permettant de retourner l'état d'un coffre.
        ---------------------------------------------------
        map -> str
        numero -> int
        return -> bool
        """
        if map == "pyramide.bam" and numero == 0:
            return bool(self.player.coffres[1])
        else:
            return bool(self.player.coffres[0])

    def get_text_panneau(self, numero=0):
        """
        Méthode permettant de retourner le texte d'un panneau.
        ------------------------------------------------------
        numero -> int
        return -> str
        """
        if self.current_map == "Marelys.bam" and numero == 0:
            return "Arduny"
        elif self.current_map == "Marelys.bam" and numero == 1:
            return "Verdantia"
        elif self.current_map == "Verdantia.bam" and numero == 0:
            return "Marelys"
        elif self.current_map == "Verdantia.bam" and numero == 1:
            return "Ignirift"
        elif self.current_map == "Ignirift.bam" and numero == 0:
            return "Verdantia"
        elif self.current_map == "Ignirift.bam" and numero == 1:
            return "Arduny"
        elif self.current_map == "Arduny.bam" and numero == 0:
            return "Ignirift"
        elif self.current_map == "Arduny.bam" and numero == 1:
            return "Marelys"
        return "You've met with a terrible fate, haven't you ?"

    def load_light(self):
        """
        Méthode permettant de générer une lumière spécifique pour chaque map.
        ----------------------------------------------------------------------
        return -> None
        """
        light = AmbientLight("Lumière ambiante")
        light_np = render.attachNewNode(light)
        self.actuals_light.append(light_np)
        render.setLight(light_np)
        if self.current_map == "Arduny.bam":
            light = DirectionalLight("dlight")
            light.color = (9, 9, 7, 1)
            light_np = render.attachNewNode(light)
            light_np.setHpr((0, 300, 0))
            render.setLight(light_np)
            self.actuals_light.append(light_np)
        elif self.current_map == "village_pecheurs.bam":
            light = DirectionalLight("dlight")
            light.color = (1, 1, 1, 1)
            light_np = render.attachNewNode(light)
            light_np.setHpr((0, 300, 0))
            render.setLight(light_np)
            self.actuals_light.append(light_np)
        elif self.current_map == "village_pecheurs_maison_chef.bam" or self.current_map == "village_pecheurs_maison_heros.bam" or self.current_map == "village_pecheurs_maison_pote.bam" or self.current_map == "village_pecheurs_port.bam":
            light = DirectionalLight("dlight")
            light.color = (0.21, 0.21, 0.11, 1)
            light_np = render.attachNewNode(light)
            light_np.setHpr((180, 300, 0))
            render.setLight(light_np)
            self.actuals_light.append(light_np)
        elif self.current_map == "Verdantia.bam":
            light = DirectionalLight("dlight")
            light.color = (2, 2, 1.5, 1)
            light_np = render.attachNewNode(light)
            light_np.setHpr((0, 300, 0))
            render.setLight(light_np)
            self.actuals_light.append(light_np)
        elif self.current_map == "Ignirift.bam":
            light = DirectionalLight("dlight")
            light.color = (8, 5, 5, 1)
            light_np = render.attachNewNode(light)
            light_np.setHpr((0, 200, 0))
            render.setLight(light_np)
            self.actuals_light.append(light_np)
        elif self.current_map == "pyramide.bam":
            light = PointLight("lanterne")
            light.color = (2, 2, 0.25, 1)
            light_np = self.player.attachNewNode(light)
            light_np.setPos((0, 1, 1))
            render.setLight(light_np)
            self.actuals_light.append(light_np)


    def load_fog(self):
        """
        Méthode permettant de générer une fummée spécifique pour chaque map.
        -----------------------------------------------------------------------
        return -> None
        """
        for p in self.particles_effects:
          p.removeNode()
        self.particles_effects = []
        if self.current_map == "village_pecheurs.bam":
            fummee = Fog("Brume")
            fummee.setColor(0.5, 0.5, 0.55)
            d = random.randint(2, 150)/10000
            fummee.setExpDensity(d)
            render.setFog(fummee)
        elif self.current_map == "Arduny.bam" and random.randint(1, 2) == 1:
            fummee = Fog("Sable")
            fummee.setColor(0.4, 0.4, 0.05)
            fummee.setExpDensity(0.005)
            render.setFog(fummee)
        elif self.current_map == "Crest.bam":
            fummee = Fog("neige")
            fummee.setColor(1, 1, 1)
            fummee.setExpDensity(0.01)
            render.setFog(fummee)
        elif self.current_map == "Ignirift.bam" :
            """base.enableParticles()
            particles = Particles()
            particles.setPoolSize(5)
            particles.setBirthRate(0.5)
            particles.setLitterSize(100)
            particles.setLitterSpread(15)
            particles.setFactory("PointParticleFactory")
            particles.setRenderer("GeomParticleRenderer")
            particles.setEmitter("SphereVolumeEmitter")
            smiley = loader.loadModel("smiley")
            smiley.setScale(6)
            particles.getRenderer().setGeomNode(smiley.node())
            particles.enable()
            effect = ParticleEffect("peffect", particles)
            effect.reparentTo(render)
            effect.setPos((0, 0, 50))
            effect.enable()
            self.particles_effects.append(effect)"""
            fummee = Fog("Cendres")
            fummee.setColor(0.7, 0.2, 0.2)
            fummee.setExpDensity(random.randint(0, 150)/10000)
            render.setFog(fummee)
        else:
            pass


    def return_pnj(self, pnj="magicien"):
        """
        Méthode permettant de renvoyer la bonne classe en fonction du PNJ choisi.
        ----------------------------------------------------------------------
        pnj -> str
        return -> PNJ (ou classe qui en hérite)
        """
        if pnj == "magicien":
            return Magicien()
        elif pnj == "inventeur":
            return Inventeur()
        elif pnj == "archer":
            return Archer()
        elif pnj == "enfant_prodige":
            return Enfant_prodige()
        elif pnj == "mage":
            return Mage_cache()
        elif pnj == "etudiant":
            return Etudiant_amoureux()
        elif pnj == "etudiante":
            return Etudiante_amoureuse()
        elif pnj == "assassin":
            return Assassin_repenti()
        elif pnj == "marchand":
            return Marchand()
        elif pnj == "golem_pnj":
            return Golem_pnj()
        return PNJ()

    def return_monstre(self, pnj="golem"):
        """
        Méthode permettant de renvoyer la bonne classe en fonction du Monstre choisi.
        ------------------------------------------------------------------------------
        pnj -> str
        return -> Monster (ou classe qui en hérite)
        """
        if pnj == "golem":
            return Golem()
        elif pnj == "Zmeyevick":
            return Zmeyevick()
        elif pnj == "bonhomme_de_neige":
            return Bonhomme_de_neige()
        return Monster()

    def load_triggers(self, map="village_pecheurs_maison_heros.bam"):
        """
        Méthode dans laquelle on rentre toutes les instructions sur nos triggers.
        C'est à dire les collisions "scénaristiques".
        -------------------------------------------------------------------------
        map -> str
        return -> None
        """
        if hasattr(self, "triggers"):
            for trigger in self.triggers:
                trigger.removeNode()
        self.triggers = []
        temp = []
        self.actual_trigger = None
        if map == "village_pecheurs.bam":
            trigger = CollisionNode("0")
            trigger.addSolid(CollisionBox((5, -1280, 300), 80, 100, 100))
            temp.append(trigger)
        elif map == "Marelys.bam":
            trigger = CollisionNode("1")
            trigger.addSolid(CollisionBox((-1000, 730, 0), 100, 100, 200))
            temp.append(trigger)
        elif map == "Crest.bam":
            trigger = CollisionNode("2")
            trigger.addSolid(CollisionBox((135, 70, 150), 200, 200, 400))
            temp.append(trigger)
        for trigger in temp:
            trigger.setFromCollideMask(BitMask32.allOff())
            trigger.setIntoCollideMask(BitMask32.bit(0))
            trigger_chemin_de_noeud = render.attachNewNode(trigger)
            #trigger_chemin_de_noeud.show() #Décommentez pour voir les triggers
            self.triggers.append(trigger_chemin_de_noeud)
        del temp

    def enterMap(self):
        """
        Méthode d'entrée dans le state map.
        -----------------------------------------------------
        return -> None
        """
        #On montre le joueur.
        self.player.show()
        self.player.pose("Marche.001(real)", 1)
        self.player.setScale(8)
        self.accept("t", self.player_interface.enlever_hp, extraArgs=[5])
        #On cache le curseur de la souris.
        properties = WindowProperties()
        properties.setCursorHidden(True)
        base.win.requestProperties(properties)
        self.load_save()
        self.load_map(self.current_map)
        if self.first_time:
            self.help()

    def accept_touches(self):
        """
        Méthode permettant d'accepter les évènements liés à des touches.
        ----------------------------------------------------------------
        return -> None
        """
        self.accept("escape", self.confirm_quit)
        if not self.manette:
            self.accept(self.keys_data["Avancer"], self.touche_pave, extraArgs=["arrow_up"])
            self.accept(self.keys_data["Avancer"]+"-up", self.touche_pave, extraArgs=["arrow_up-up"])
        self.accept(self.keys_data["Changer le point de vue"], self.player.followcam.change_vue)
        self.accept(self.keys_data["Courir"], self.change_vitesse, extraArgs=["b"])
        self.accept(self.keys_data["Courir"]+"-up", self.change_vitesse, extraArgs=["b-up"])
        self.accept(self.keys_data["Inventaire"], self.inventaire)
        self.accept(self.keys_data["Interagir"], self.check_interact)
        self.accept("into", self.into)
        self.accept("out", self.out)
        self.accept("h", self.help)
        self.accept(self.keys_data["Attaquer"], self.attaque)
        taskMgr.remove("update")
        taskMgr.add(self.update, "update")

    def ignore_touches(self):
        """
        Méthode permettant d'ignorer les évènements liés à des touches.
        ----------------------------------------------------------------
        return -> None
        """
        self.ignore("escape")
        self.ignore(self.keys_data["Avancer"])
        self.ignore(self.keys_data["Avancer"]+"-up")
        self.ignore(self.keys_data["Changer le point de vue"])
        self.ignore(self.keys_data["Courir"])
        self.ignore(self.keys_data["Courir"]+"-up")
        self.ignore(self.keys_data["Inventaire"])
        self.ignore(self.keys_data["Interagir"])
        self.ignore(self.keys_data["Attaquer"])
        self.ignore("into")
        self.ignore("out")
        self.ignore("h")
        taskMgr.remove("update")

    def attaque(self):
        """
        Méthode permettant au joueur de donner un coup d'épée.
        -------------------------------------------------------
        return -> None
        """
        if self.player.current_arme is not None:
          taskMgr.remove("apres attaque")
          self.player.play("Attaque")
          self.player.epee.setHpr((-90, 270, 0))
          taskMgr.doMethodLater(1, self.apres_attaque, "apres attaque")

    def apres_attaque(self, task):
        """
        Méthode permettant de remettre le joueur
        dans une pose normale après une attaque.
        -----------------------------------------
        task -> task
        return -> task.done
        """
        if not self.player.getAnimControl('Marche.001(real)').isPlaying():
          self.player.pose("Marche.001(real)", 1)
        self.player.epee.setHpr((-55, 270, 0))
        return task.done

    def load_save(self, task=None):
        """
        Méthode qui permet de charger la nouvelle position du joueur quand on charge une map.
        --------------------------------------------------------------------------------------
        task -> task
        return -> None
        """
        if self.hack:
            self.hack = False
            self.current_map = "pyramide.bam"
            self.player.setPos((1722, -3200, 20))
        else:
          if self.current_point == "save_heros":#Maison du joueur.
              self.current_map = "village_pecheurs_maison_heros.bam"
              self.player.setPos(0, 30, 6)
          elif self.current_point == "save_village": #Dans le village des pecheurs
              self.current_map = "village_pecheurs.bam"
              self.player.setPos(-380, 220, 250)
          elif self.current_point == "save_pyramide": #Dans la pyramide
              self.current_map = "pyramide.bam"
              self.player.setPos(150, -50, 0)
          elif self.current_point == "save_maison_chasseurs":
              self.current_map = "Manoir.bam"
              self.player.setPos(0, -20, 0)
          elif self.current_point == "save_ignirift":
              self.current_map = "Ignirift.bam"
              self.player.setPos(10, 10, 25)
          elif self.current_point == "save_desert":
              self.current_map = "Arduny.bam"
              self.player.setPos(2125, -2000, 20)
          elif self.current_point == "save_crest":
              self.current_map = "Crest.bam"
              self.player.setPos((3500, 0, 500))
          else:#Le joueur se retrouve chez lui par défaut
              self.current_map = "village_pecheurs_maison_heros.bam"
              self.player.setPos(0, 30, 6)
        if task != None:
            return task.done

    def exitMap(self):
        """
        Méthode pour sortir du state map.
        ----------------------------------------
        return -> None
        """
        for light in self.actuals_light:
            render.clearLight(light)
            light.removeNode()
        self.actuals_light = []
        render.clearFog()
        self.music.stop()
        self.map.removeNode()
        self.skybox.removeNode()
        self.player.hide()
        for t in self.triggers:
            t.removeNode()
        for porte in self.portails:
            self.portails[porte][0].removeNode()
        for pnj in self.pnjs:
            self.pnjs[pnj].cleanup()
            self.pnjs[pnj].removeNode()
        for pnj in self.monstres:
            self.monstres[pnj].cleanup()
            self.monstres[pnj].removeNode()
        for objet in self.objects:
            if objet.nom == "coffre":
                objet.object.cleanup()
            objet.object.removeNode()
        for statue in self.save_statues:
            self.save_statues[statue][0].removeNode()
            self.save_statues[statue][1].removeNode()
        if hasattr(self, "eau"):
            self.eau.removeNode()
            del self.eau
        for p in self.particles_effects:
          p.removeNode()
        self.particles_effects = []
        self.save_statues = {}
        self.antimur.clearInPatterns()
        self.antimur.clearOutPatterns()
        self.objects = []
        self.pnjs = {}
        self.portails = {}
        self.map = None
        self.current_panneau = None
        self.player.left = False
        self.player.right = False
        self.player.reverse = False
        self.current_pnj = None
        self.player.walk = False
        taskMgr.remove("update")
        del self.music_name
        self.ignoreAll()
        self.accept("escape", self.all_close)
        self.player.stop()
        self.player.followcam.set_active(False)
        del self.player.followcam
        base.cam.setPos((0, 0, 0))
        base.cam.setHpr((0, 0, 0))

    #----------------------Méthodes de collisions-----------------------------------------
    def into(self, a):
        """
        Méthode s'activant quand le joueur ou un autre objet from, touche un objet into.
        -----------------------------------------------------------------------------------
        a -> entry (une info sur la collision)
        return -> None
        """
        b = str(a.getIntoNodePath()).split("/")[len(str(a.getIntoNodePath()).split("/"))-1] #L'objet Into
        c = str(a.getFromNodePath()).split("/")[len(str(a.getFromNodePath()).split("/"))-1] #L'objet From
        if c == "player_sphere":#Si c'est le joueur qui touche
            if b in self.pnjs:#PNJ
                self.current_pnj = b
                if self.pnjs[b].s is not None:
                    self.pnjs[b].s.pause()
            elif b in self.portails:
                if type(self.portails[b][1]) is Portail:
                    if b == "pyramide.bam" and not "Amulette" in self.player.inventaire:
                      taskMgr.remove("update")
                      self.set_text(22, messages=["ja"])
                      self.acceptOnce("ja", taskMgr.add, extraArgs=[self.update, "update"])
                    elif b == "pyramide.bam" and self.chapitre == 4:
                      self.chapitre = 5
                      self.fade_out("Cinematique")
                    else:
                      self.transition.fadeOut(0.5)
                      taskMgr.doMethodLater(0.5, self.load_map, "loadmap", extraArgs=[b, self.portails[b][1].newpos])
                      if self.portails[b][1].orientation is not None:
                        taskMgr.doMethodLater(0.5, self.player.setH, "change orientation joueur", extraArgs=[self.portails[b][1].orientation])
                elif type(self.portails[b][1]) is Porte:
                    self.current_porte = b
            elif b.isdigit(): #Trigger
                b = int(b)
                if b >= 0 or b <= 2:
                    self.actual_trigger = b
            elif b in self.save_statues: #Statue de sauvegarde
                self.actual_statue = b
            elif "coffre" in b:
                self.actual_coffre = b.split("_")[len(b.split("_"))-1]
            elif "panneau" in b:
                self.current_panneau = b.split("_")[len(b.split("_"))-1]

    def out(self, a):
        """
        Méthode s'activant quand un objet from qitte un objet into.
        ----------------------------------------------------------------
        a -> entry (info sur la collision)
        return -> None
        """
        b = str(a.getIntoNodePath()).split("/")[len(str(a.getIntoNodePath()).split("/"))-1]
        c = str(a.getFromNodePath()).split("/")[len(str(a.getFromNodePath()).split("/"))-1]
        if c == "player_sphere":
            if b in self.pnjs:
                if self.pnjs[b].s is not None:
                    self.pnjs[b].s.resume()
                self.current_pnj = None
            elif b in self.portails:
                self.current_porte = None
            elif b in self.save_statues:
                self.actual_statue = None
            elif b.isdigit():
                self.actual_trigger = None
            elif "coffre" in b:
                self.actual_coffre = None
            elif "panneau" in b or self.current_panneau is not None:
                self.current_panneau = None


    def change_vitesse(self, touche="b"):
        """
        Méthode qui change la vitesse du joueur si on appuie sur la touche b ou si on la relâche.
        -------------------------------------------------
        touche -> str
        return -> None
        """
        if touche == "b":
            self.player.vitesse *= 2
        else:
            self.player.vitesse /=2



    def touche_pave(self, message="arrow_up"):
        """
        Méthode s'activant quand on appuie sur ou qu'on relache une touche du pavé de flèches.
        Cette Méthode pourrait être supprimée, vu que le joueur se dirige maintenant avec la souris.
        Mais on la garde pour ne pas avoir de bugs.
        ----------------------------------------------------------------------------------------------
        message -> str
        return -> None
        """
        if message == "arrow_up":
            self.player.walk = True
            self.player.loop('Marche.001(real)')
        elif message == "arrow_up-up":
            self.player.walk = False
            self.player.stop()
        elif message == "arrow_down":
            self.player.reverse = True
        elif message == "arrow_down-up":
            self.player.reverse = False
        elif message == "arrow_left":
            self.player.left = True
        elif message == "arrow_right":
            self.player.right = True
        elif message == "arrow_left-up":
            self.player.left = False
        elif message == "arrow_right-up":
            self.player.right = False

    #-------------------Méthode de mise à jour----------------------------------
    def update(self, task):
        """
        Méthode appelée à chaque frame pour mettre certaines choses à jour.
        ---------------------------------------------------------
        task -> task
        return -> task.cont
        """
        dt = globalClock.getDt() #L'horloge, le chronomètre...appelez ça comme
        #vous voulez c'est ce qui permet de mesurer le temps écoulé entre chaque frame.
        #---------------Section éléments 2D-------------------------------------------
        self.croix_image.hide()
        self.lieu_text.hide()
        self.map_image.hide()
        self.player_interface.montrer()
        #-----------------------Section gestion de la manette-----------------
        if self.manette:
            base.devices.update()
            if not base.devices.getDevices(InputDevice.DeviceClass.gamepad):
                self.music.setVolume(0)
                self.hide_gui()
                self.transition.fadeScreenColor((0, 0, 0, 0.6))
                self.transition.letterboxOn()
                self.gamepad_text = OnscreenText(text=self.story["gui"][12], pos=(0, 0), scale=(0.15, 0.15), fg=(1, 1, 1, 1)) #Veuillez reconnecter votre manette.
                self.gamepad_text.setBin("gui-popup", 80)
                taskMgr.remove("update")
                taskMgr.add(self.wait_for_gamepad, "wait_for_gamepad")
                return None
            gamepad = base.devices.getDevices(InputDevice.DeviceClass.gamepad)[0]
            left_x = gamepad.findAxis(InputDevice.Axis.left_x)
            left_y = gamepad.findAxis(InputDevice.Axis.left_y)
            right_x = gamepad.findAxis(InputDevice.Axis.right_x)
            right_y = gamepad.findAxis(InputDevice.Axis.right_y)
            if left_x.value > 0.5:
                self.touche_pave(message="arrow_right")
            elif left_x.value < -0.5:
                self.touche_pave(message="arrow_left")
            else:
                self.touche_pave(message="arrow_right-up")
                self.touche_pave(message="arrow_left-up")
            if left_y.value > 0.5:
                self.touche_pave(message="arrow_up")
            elif left_y.value < -0.5:
                self.touche_pave(message="arrow_down")
            else:
                self.touche_pave(message="arrow_up-up")
                self.touche_pave(message="arrow_down-up")
            if right_y.value > 0.5:
                self.player.followcam.move("up", globalClock.getDt())
            elif right_y.value < -0.5:
                self.player.followcam.move("down", globalClock.getDt())
            if right_x.value > 0.5:
                self.player.followcam.move("right", globalClock.getDt())
            elif right_x.value < -0.5:
                self.player.followcam.move("left", globalClock.getDt())
        #----------------------Section de gestion de la caméra si pas de manette----------------------
        else:
            haut_button = self.clavier_rep.get_mapped_button(self.keys_data["Monter la camera"])
            if base.mouseWatcherNode.is_button_down(haut_button):
                self.player.followcam.move("up", globalClock.getDt())
            bas_button = self.clavier_rep.get_mapped_button(self.keys_data["Descendre la camera"])
            if base.mouseWatcherNode.is_button_down(bas_button):
                self.player.followcam.move("down", globalClock.getDt())
            gauche_button = self.clavier_rep.get_mapped_button(self.keys_data["Camera a gauche"])
            if base.mouseWatcherNode.is_button_down(gauche_button):
                self.player.followcam.move("left", globalClock.getDt())
            droite_button = self.clavier_rep.get_mapped_button(self.keys_data["Camera a droite"])
            if base.mouseWatcherNode.is_button_down(droite_button):
                self.player.followcam.move("right", globalClock.getDt())
        #-----------------------Section souris---------------------------------------
        if not self.manette:
            if base.mouseWatcherNode.hasMouse():
                self.player.setH(self.player.getH() - base.mouseWatcherNode.getMouseX() * globalClock.getDt() * 3000)
        base.win.movePointer(0, int(base.win.getProperties().getXSize()/2), int(base.win.getProperties().getYSize()/2))
        #-----------------------Section mouvements du joueur------------------------
        self.player.setZ(self.player, -self.player.gravite*dt)
        if self.player.walk:
            self.player.setX(self.player, self.player.vitesse*globalClock.getDt())
        if self.player.reverse:
            self.player.setX(self.player, -self.player.vitesse*globalClock.getDt())
        if self.player.right:
            self.player.setH(self.player, -self.player.vitesse*20*globalClock.getDt())
        if self.player.left:
            self.player.setH(self.player, self.player.vitesse*20*globalClock.getDt())
        #--------------------Section gestion des vies-----------------------------
        if self.player.vies <= 0:
            self.transition.fadeOut(0.5)
            taskMgr.doMethodLater(0.5, self.launch_game_over, "launch game over")
            return task.done
        return task.cont

    #--------------------------Pop-ups----------------------------------------
    def confirm_quit(self):
        """
        Méthode qui s'active quand on joue, et que l'on appuie sur échap.
        Une boîte de dialogue apparaît et nous demande si l'on est sûr de quitter.
        ------------------------------------------------------------------------------
        return -> None
        """
        taskMgr.remove("update")
        properties = WindowProperties()
        properties.setCursorHidden(False)
        base.win.requestProperties(properties)
        self.ignore(self.keys_data["Inventaire"])
        self.ignore("escape")
        if self.quitDlg is None:
          self.quitDlg = YesNoDialog(text = self.story["gui"][13], command = self.quit_confirm) #Voulez-vous vraiment quitter ?

    def quit_confirm(self, clickedYes):
        """
        Méthode qui se met en marche une fois que le joueur
        a répondu à la boîte de dialogue pour quitter le jeu.
        -----------------------------------------------------
        clickedYes -> bool
        return -> None
        """
        self.quitDlg.cleanup()
        self.quitDlg = None
        taskMgr.add(self.update, "update")
        if clickedYes:
            self.fade_out()
        else:
            properties = WindowProperties()
            properties.setCursorHidden(True)
            base.win.requestProperties(properties)
            self.accept("escape", self.confirm_quit)
            self.accept(self.keys_data["Inventaire"], self.inventaire)


    #-----------------------Section de gestion de l'inventaire (et d'autres fonctions d'ui)-------------------
    def help(self):
        """
        Méthode permettant d'afficher un message d'aide.
        ------------------------------------------------
        return -> None
        """
        self.hide_gui()
        if self.first_time:
            self.first_time = False
        taskMgr.remove("update")
        self.ignore_touches()
        self.bg_picture = OnscreenImage("file.png", pos=Vec3(0, 0, 0), scale=Vec3(1.2, 1, 0.75))
        self.bg_picture.setTransparency(TransparencyAttrib.MAlpha)
        self.title = OnscreenText("Aide :", scale=0.15, pos=(-0.85, 0.46), align=TextNode.ALeft)
        liste_textes = [self.story["gui"][20]+self.keys_data["Avancer"].capitalize(), self.story["gui"][21]+self.keys_data["Changer le point de vue"].capitalize(),
                            self.story["gui"][22]+self.keys_data["Courir"].capitalize(), self.story["gui"][23]+self.keys_data["Inventaire"].capitalize(), self.story["gui"][24]+self.keys_data["Interagir"].capitalize(),
                            self.story["gui"][25], self.story["gui"][26], self.story["gui"][30]]
        z = 0.35
        self.real_liste = []
        for element in liste_textes:
            self.real_liste.append(OnscreenText(element, scale=0.1, pos=(-0.85, z), align=TextNode.ALeft))
            z -= 0.1
        del liste_textes
        self.ignore("h")
        self.accept("h", self.exit_help)
        self.ignore("escape")
        self.accept("escape", self.exit_help)

    def exit_help(self):
        """
        Méthode permettant de quitter l'aide.
        ---------------------------------------
        return -> None
        """
        taskMgr.add(self.update, "update")
        self.bg_picture.removeNode()
        self.title.removeNode()
        for element in self.real_liste:
            element.removeNode()
        self.ignore("h")
        self.ignore("escape")
        self.accept_touches()

    def inventaire(self):
        """
        Méthode utilisée pour ouvrir l'inventaire
        -------------------------------------------
        return -> None
        """
        self.player.stop()
        self.ignore_touches()
        self.activing = False
        self.player_interface.cacher()
        self.player.walk, self.player.reverse, self.player.left, self.player.right = False, False, False, False
        self.index_invent = 0
        self.accept("escape", self.exit_inventaire)
        self.accept(self.keys_data["Inventaire"], self.exit_inventaire)
        self.accept("arrow_right", self.change_index_invent, extraArgs=["right"])
        self.accept("arrow_left", self.change_index_invent)
        self.accept("arrow_down", self.change_index_invent, extraArgs=["down"])
        self.accept("arrow_up", self.change_index_invent, extraArgs=["up"])
        self.indication = OnscreenText(text=self.story["gui"][29], scale=0.1, pos=(0, -0.8), fg=(1, 1, 1, 1))
        self.indication.hide()
        taskMgr.add(self.update_invent, "update_invent")
        self.accept("enter", self.active_article)
        self.inventaire_show = self.genere_liste_defilement()
        for article in self.player.inventaire:
            if self.player.inventaire[article] > 0:
                bouton = DirectButton(text=article+" : "+str(self.player.inventaire[article]),  text_scale=0.1, borderWidth=(0.01, 0.01), relief=2, command=self.active_article, extraArgs=[article])
                self.inventaire_show.addItem(bouton)
        self.music.setVolume(0.6)
        self.croix_image.setPos(self.get_pos_croix()[0])
        self.lieu_text.setText(self.get_pos_croix()[1])
        self.inventaire_mgr.weapons = self.player.armes
        self.inventaire_mgr.creer_inventaire()
        properties = WindowProperties()
        properties.setCursorHidden(False)
        base.win.requestProperties(properties)

    def active_article(self):
        """
        Méthode s'activant quand on consomme un article.
        -------------------------------------------------
        return -> None
        """
        if self.index_invent == 2 and not self.activing and len(self.player.inventaire) > 0:
          self.activing = True
          article = self.inventaire_mgr.get_item()
          taskMgr.remove("update_invent")
          if article == "Amulette":
            self.OkDialog = OkDialog(text=self.story["items"][1], command=self.inutile)
          else:
            self.player.inventaire[article] -= 1
            if self.player.inventaire[article] < 1:
                del self.player.inventaire[article]
            a_dire = "Utilisation d'un(e) "+ article
            if article == "Vodka":
              a_dire = self.story["items"][0]
              self.player_interface.ajouter_hp(5)
            elif article == "Tsar Bomba":
                a_dire = self.story["items"][5]
                self.solution_finale = True
            self.OkDialog = OkDialog(text=a_dire, command=self.inutile)
        elif self.index_invent == 1 and len(self.player.armes) > 0:
          vieille_arme = self.player.current_arme
          self.player.current_arme = self.inventaire_mgr.get_arme()
          if self.player.current_arme == vieille_arme:
              if self.player.current_arme == "Epée":
                self.player.epee.hide()
              self.player.current_arme = None
          else:
            if self.player.current_arme == "Epée":
              self.player.epee.show()


    def inutile(self, inutile=None):
        """
        Méthode qui permet d'effacer le diaogue ok.
        --------------------------------------------
        inutile -> bool
        return -> None
        """
        self.OkDialog.cleanup()
        taskMgr.add(self.update_invent, "update_invent")
        self.inventaire_mgr.creer_inventaire()
        self.activing = False


    def get_pos_croix(self):
        """
        Méthode qui retourne la position de la croix qui indique notre position sur la carte de l'inventaire.
        -----------------------------------------------------------------------
        return -> Vec3
        """
        if self.current_map == "village_pecheurs.bam" or self.current_map == "village_pecheurs_maison_chef.bam" or self.current_map == "village_pecheurs_maison_heros.bam":
            return  Vec3(0.6, 0, 0), self.story["map"][2]
        elif self.current_map == "Marelys.bam":
            return Vec3(0.2, 0, 0), self.story["map"][1]
        elif self.current_map == "pyramide.bam":
            return Vec3(0, 0, 0.6), self.story["map"][0]
        elif self.current_map == "Verdantia.bam":
            return Vec3(-0.05, 0, -0.3), self.story["map"][3]
        elif self.current_map == "Manoir.bam":
            return Vec3(-0.1, 0, -0.05), self.story["map"][4]
        elif self.current_map == "Ignirift.bam":
            return Vec3(-0.3, 0, 0.2), self.story["map"][5]
        elif self.current_map == "maison_aurelia.bam":
            return Vec3(-0.3, 0, 0), self.story["map"][6]
        elif self.current_map == "Arduny.bam":
            return Vec3(0.1, 0, 0.5), self.story["map"][7]
        elif self.current_map == "Crest.bam":
            return Vec3(-0.05, 0, 0.4), self.story["map"][8]
        return Vec3(0, 0, 0), "???"

    def change_index_invent(self, dir="left"):
        """
        Méthode qui permet de changer de menu d'inventaire
        -------------------------------------------------
        dir -> str
        return -> None
        """
        if dir == "left":
            if self.index_invent > 0:
                self.index_invent -= 1
            else:
                self.index_invent = 2
        elif dir == "right":
            if self.index_invent < 2:
                self.index_invent += 1
            else:
                self.index_invent = 0
        elif dir == "up" or dir == "down":
            if len(self.player.inventaire) > 0:
              if self.index_invent == 1:
                if dir == "up":
                    self.inventaire_mgr.arme_select(self.inventaire_mgr.arme_en_main-1)
                elif dir == "down":
                    self.inventaire_mgr.arme_select(self.inventaire_mgr.arme_en_main+1)
              elif self.index_invent == 2:
                if dir == "up":
                    self.inventaire_mgr.item_select(self.inventaire_mgr.item_selectione-1)
                elif dir == "down":
                    self.inventaire_mgr.item_select(self.inventaire_mgr.item_selectione+1)


    def update_invent(self, task):
        """
        Méthode appelée à chaque frame dans l'inventaire pour mettre à jour le contenu
        -----------------------------------------------------------------------------
        task -> task
        return -> task.cont
        """
        self.inventaire_show.hide()
        self.indication.hide()
        self.map_image.hide()
        self.croix_image.hide()
        self.lieu_text.hide()
        self.inventaire_mgr.cacher_armes()
        self.inventaire_mgr.cacher_items()
        if self.index_invent == 0:
            self.map_image.show()
            self.croix_image.show()
            self.lieu_text.show()
        elif self.index_invent == 1:
            self.inventaire_mgr.afficher_armes()
        elif self.index_invent == 2:
            self.inventaire_mgr.afficher_items()
            self.indication.show()
        if hasattr(self, "solution_finale"):
            self.chapitre = 949
            self.indication.hide()
            self.inventaire_mgr.cacher_items()
            self.fade_out("Cinematique")
            return task.done
        return task.cont

    def exit_inventaire(self):
        """
        Méthode appelée lorsqu'on quitte l'inventaire
        --------------------------------------------------
        return -> None
        """
        self.indication.removeNode()
        self.ignore("enter")
        self.ignore("arrow_down")
        self.ignore("arrow_up")
        self.ignore("arrow_right")
        self.ignore("arrow_left")
        self.inventaire_mgr.cacher_items()
        self.inventaire_mgr.cacher_armes()
        properties = WindowProperties()
        properties.setCursorHidden(True)
        base.win.requestProperties(properties)
        self.inventaire_show.removeNode()
        del self.inventaire_show
        self.player_interface.montrer()
        self.music.setVolume(1)
        taskMgr.remove("update_invent")
        self.accept_touches()

    #----------------------------------Partie pour le generique--------------------------------------------------------------------------
    def enterGenerique(self):
        """
        Méthode activée quand on entre dans le générique.
        -------------------------------------------------
        return -> None
        """
        self.music = loader.loadSfx("Thème_de_Therenor.ogg")
        self.music.setLoop(True)
        self.music.play()
        self.texts_gen_1 = [("PNJ Design :", True), ("Alexandrine Charette", False), ("Player and GUI Design :", True), ("Rémy Martinot", False),
        ("Enemy program : ", True), ("Noé Mora", False), ("Map and dungeon creation :", True), ("Etienne Pacault", False), ("Website and movies :", True), ("Tyméo Bonvicini-Renaud", False),
        ("Special thanks to :", True), ("Aimeline Cara", False), ("The Carnegie Mellon University", False), ("Disney Online", False), ("The blender foundation", False), ("Emmanuel Puybaret (Sweet Home 3D)", False), ("And you !", False)]
        colors = [(1, 0, 0, 1), (0.65, 0.4, 0, 1), (1, 1, 0, 1), (0, 1, 0.2, 1), (0, 0.5, 0, 1), (0, 0.8, 1, 1), (0, 0, 0.9, 1), (1, 0, 1, 1)]
        i_color = 0
        y = -0.9
        self.texts_gen = []
        s = (0.15, 0.15, 0.15)
        c = (1, 0, 0, 1)
        for text in self.texts_gen_1:
            if text[1]:
                s = (0.15, 0.15, 0.15)
                c = colors[i_color]
                i_color += 1
                y -= 0.5
            else:
                s = (0.1, 0.1, 0.1)
                c = (1, 1, 1, 1)
                y -= 0.25
            self.texts_gen.append(OnscreenText(text[0], pos=(0, y), scale=s , fg=(c)))
        self.texts_gen.append(OnscreenText("Fin", pos=(0, y-0.5), scale=(0.2, 0.2, 0.2), fg=(1, 1, 1, 1)))
        taskMgr.add(self.update_generique, "update generique")

    def exitGenerique(self):
        """
        Méthode activée quand on quitte le générique.
        -------------------------------------------------
        return -> None
        """
        for text in self.texts_gen:
            text.removeNode()
            del text
        del self.texts_gen
        self.music.stop()

    def change_to_menu(self, task):
        """
        Méthode qui après le générique permet d'accéder à l'écran titre.
        ------------------------------------------------------------------
        task -> task
        return -> task.done
        """
        self.request("Menu")
        self.transition.fadeIn(2)
        Sequence(LerpFunc(self.music.setVolume, fromData = 0, toData = 1, duration = 2)).start()
        return task.done

    def update_generique(self, task):
        """
        Méthode qui met à jour le générique.
        --------------------------------------
        task -> task
        return -> task.cont ou task.done
        """
        i = 0
        for text in self.texts_gen:
            i += 1
            text.setTextPos(text.getTextPos()[0], text.getTextPos()[1]+globalClock.getDt()/20)
            if i == len(self.texts_gen) -1:
                if text.getTextPos()[1] > 1.5:
                    taskMgr.doMethodLater(2, self.change_to_menu, "change to menu")
                    self.transition.fadeOut(2)
                    Sequence(LerpFunc(self.music.setVolume, fromData = 1, toData = 0, duration = 2)).start()
                    return task.done
        return task.cont

    #-------------------------Fonctions gérant le game over---------------------------------------
    def launch_game_over(self, task):
        """
        Méthode pour lancer le game over.
        -----------------------------------
        task -> task
        return -> task.done
        """
        self.request("Game_over")
        return task.done

    def enterGame_over(self):
        """
        Méthode qui s'active quand on entre dans le game over.
        --------------------------------------------------------
        return -> None
        """
        self.player_interface.cacher()
        render.hide()
        self.music.stop()
        self.music = loader.loadSfx("game_over.ogg")
        self.music.play()
        self.player.vies = 15
        self.transition.fadeIn(0.5)
        self.text_game_over = OnscreenText("Game over", pos=(0, 0), scale=(0.2, 0.2), fg=(0.9, 0, 0, 1))
        self.text_game_over_2 = OnscreenText(self.story["gui"][14], pos=(0, -0.2), scale=(0.1, 0.1), fg=(0.9, 0, 0, 1)) #Appuyez sur F1 pour recommencer.
        self.acceptOnce("f1", self.fade_out, extraArgs=["Map"])

    def exitGame_over(self):
        """
        Fonciton qui s'active quand on quitte l'état game over.
        ----------------------------------------------------------
        return -> None
        """
        self.music.stop()
        self.text_game_over.removeNode()
        self.text_game_over_2.removeNode()
        del self.text_game_over
        del self.text_game_over_2
        render.show()

    def apparaitre_render(self, task):
        """
        Méthode qui permet de masquer les textes
        de game over et faire apparaître le rendu
        ------------------------------------------
        task -> task
        return -> task.done
        """
        render.show()
        self.text_game_over.hide()
        self.text_game_over_2.hide()
        return task.done

    #---------------------------------Fonctions de traitement des données de sauvegarde.--------------------------------------------------
    def save(self, reset=False, file=1):
        """
        Méthode qui permet de sauvegarder les données de la partie.
        ------------------------------------------------------------
        return -> None
        """
        if reset:
            self.chapitre = 0
            self.player.nom = "_"
            self.player.noais = 0
            self.player.inventaire = {}
            self.player.armes = []
            self.player.sexe = "masculin"
            self.current_point = "save_heros"
        fichier = open(self.get_path()+f"/save_{file}.txt", "wt")
        info = [self.player.nom, str(self.chapitre), str(self.current_point), str(self.player.vies), str(self.player.maxvies), str(self.player.noais), self.player.sexe]
        fichier.writelines([donnee +"|" for donnee in info])
        fichier.close()
        string = "["
        i = 0
        for item in self.player.armes:
            i += 1
            string += f'"{item}"'
            if i < len(self.player.armes):
                string += ", "
        del i
        string += "]"
        string2 = "["
        i = 0
        for item in self.player.coffres:
            i += 1
            string2 += f'{item}'
            if i < len(self.player.coffres):
                string2 += ", "
        del i
        string2 += "]"
        fichier = open(self.get_path()+f'/invent_{file}.json', "wt")
        fichier.writelines(['{"Armes":'+string+', "Objets":'+json.dumps(self.player.inventaire)+', "Coffres":'+string2+'}'])
        fichier.close()

    def will_save(self, clickedYes):
        """
        Méthode qui s'active si on touche une statue de sauvegarde.
        --------------------------------------------------------------
        return -> None
        """
        self.saveDlg.destroy()
        if clickedYes:
            self.save(file=self.actual_file)
            self.myOkDialog = OkDialog(text=self.story["gui"][15], command = self.update_after_save) #Sauvegarde effectuée.
        else:
            self.update_after_save(True)

    def update_after_save(self, inutile):
        """
        Méthode pour remettre la Méthode de mise à jour en éxécution.
        ---------------------------------------------------------------
        inutile -> bool
        return -> None
        """
        properties = WindowProperties()
        properties.setCursorHidden(True)
        base.win.requestProperties(properties)
        if hasattr(self, "myOkDialog"):
            if self.myOkDialog is not None:
                self.myOkDialog.cleanup()
                del self.myOkDialog
        self.accept("escape", self.confirm_quit)
        taskMgr.add(self.update, "update")

    def read(self, file=1):
        """
        Méthode qui permet de lire les données préalablement enregistrées.
        -------------------------------------------------------------------
        return -> None
        """
        self.player.epee.hide()
        self.player.current_arme = None
        fichier = open(self.get_path()+f"/save_{file}.txt", "rt")
        i = 0
        for truc in fichier.read().split("|"):
            i += 1
            if i == 1:
                self.player.nom = truc
            elif i == 2:
                self.chapitre = int(truc)
            elif i == 3:
                self.current_point = truc
            elif i == 4:
                self.player.vies = float(truc)
                if self.player.vies < 3:
                    self.player.vies = 3
            elif i == 5:
                self.player.maxvies = int(truc)
            elif i == 6:
                self.player.noais = int(truc)
            elif i == 7:
                self.player.sexe = truc
        fichier.close()
        fichier = open(self.get_path()+f"/invent_{file}.json", "rt")
        data = json.loads(fichier.read())
        fichier.close()
        self.player.inventaire = data["Objets"]
        self.player.armes = data["Armes"]
        self.player.coffres = data["Coffres"]
        del data

    def init_fichiers(self):
        """
        Méthode qui permet de créer les fichiers de jeu.
        -------------------------------------------------
        return -> None
        """
        #-----------Section qui permet de déterminer si l'ordinateur est au lycée----------------------
        self.augustins = False
        if platform.system() == "Windows":
            if os.path.exists(f"C://users/{os.getlogin()}.AUGUSTINS"):
                self.augustins = True
        self.langue = "français"
        path = self.get_path()
        #----------Création du dossier---------------------------
        if not os.path.exists(path):
            os.mkdir(path)
        #-----------------Création des 3 fichiers individuels----------------
        for loop in range(3):
            if not os.path.exists(path+f"/save_{loop+1}.txt"):
                file = open(path+f"/save_{loop+1}.txt", "wt")
                file.writelines(["_|0|save_heros|15|15|0|masculin"])
                file.close()
        #------------------Création des 3 fichiers de l'inventaire-----------------------
        for loop in range(3):
            if not os.path.exists(path+f"/invent_{loop+1}.json"):
                file = open(path+f"/invent_{loop+1}.json", "wt")
                file.writelines('{"Armes":[], "Objets":{}, "Coffres":[0, 0]}')
                file.close()
        #--------------Création du fichier de mappage de touches-------------------------------
        if not os.path.exists(path+"/keys.json"):
            file = open(path+"/keys.json", "wt")
            file.writelines(['[{"Avancer":"z", "Monter la camera":"i", "Descendre la camera":"k", "Camera a droite":"l", "Camera a gauche":"j", "Courir":"lshift", "Interagir":"space", "Inventaire":"e", "Changer le point de vue":"a", "Attaquer":"c"}]'])
            file.close()
        #----------------Création du fichier pour enregistrer les variables communes à tous les joueurs (ex : langue)---------------------
        if not os.path.exists(path+"/global.txt"):
            self.save_global(reset=True)
        #On lit ce fichier pour mettre à jour toutes les variables.
        self.read_global()

    def read_global(self):
        """
        Méthode de lecture du fichier contenant les variables globales.
        ---------------------------------------------------------------
        return -> None
        """
        file = open(self.get_path()+"/global.txt", "rt")
        i = 0
        for machin in file.read().split("|"):
            i += 1
            if i == 1:
                self.langue = machin
        file.close()

    def save_global(self, reset=False):
        """
        Méthode pour enregistrer le fichier de sauvegarde commun aux différents joueurs.
        --------------------------------------------------------------------------------
        reset -> bool
        return -> None
        """
        if reset:
            self.langue = "français"
        file = open(self.get_path()+"/global.txt", "wt")
        info = [self.langue]
        file.writelines([donnee +"|" for donnee in info])
        file.close()

    def get_path(self):
        """
        Méthode permettant de donner le chemin d'accès aux données de sauvegarde.
        --------------------------------------------------------------------------
        return -> str
        """
        if platform.system() == "Windows":
            if self.augustins:
                return f"C://users/{os.getlogin()}.AUGUSTINS/AppData/Roaming/Therenor"
            else:
                return f"C://users/{os.getlogin()}/AppData/Roaming/Therenor"
        else:
            return f"/home/{os.getlogin()}/.Therenor"

    #-------------------------------Méthodes spécifiques à la manette (je ne pense pas qu'il y en aura beaucoup)---------------------------
    def wait_for_gamepad(self, task):
        """
        Méthode qui vérifie si la manette
        qui a été déconnectée est rebranchée.
        --------------------------------------------
        task -> task
        return -> task.cont ou task.done
        """
        base.devices.update()
        if base.devices.getDevices(InputDevice.DeviceClass.gamepad):
            base.attachInputDevice(base.devices.getDevices(InputDevice.DeviceClass.gamepad)[0], prefix="manette")
            self.transition.noTransitions()
            self.gamepad_text.removeNode()
            del self.gamepad_text
            self.transition.letterboxOff()
            taskMgr.add(self.update, "update")
            self.music.setVolume(1)
            return task.done
        return task.cont


#-----------------------------------------------------------------------------------------------------------
class Application(ShowBase):
    """
    Classe "principale", celle du jeu.
    """
    def __init__(self):
        """
        Méthode constructeur.
        -----------------------
        return -> Application
        """
        loadPrcFile("config.prc")
        ShowBase.__init__(self)
        #PStatClient.connect() #Décommentez si vous voulez voir les stats du PC
        base.set_background_color(0, 0, 0, 0)
        self.set_level = SetLevel()
        base.disableMouse()
        #messenger.toggleVerbose() #Décommentez si vous voulez voir les messages d'input
        self.set_level.request("Menu")
