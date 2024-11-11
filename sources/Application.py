#---------------Importation des différents modules-----------------------------
#-------------Section spécifique à panda3d---------------------
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
#-----------Section spécifique aux fichiers python du dossier-----------
from personnages import *
from monsters import *
from objects import *
from mappingGUI import *
#-------------Autres modules (nécessaires entre autres à la manipulation des fichiers)------------------
import os, sys, json, platform, random

class YesNoDialog(DirectDialog):
	"""
	Il s'agit de la même classe que celle présente avec Panda3d, mais on traduit Yes et No par Oui et Non.
	"""
	def __init__(self, parent = None, **kw):
		optiondefs = (('buttonTextList',  ['Oui', 'Non'],       DGG.INITOPT), ('buttonValueList', [DGG.DIALOG_YES, DGG.DIALOG_NO], DGG.INITOPT),)
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
		CollisionBox.__init__(self, (center[0], center[1], center[2]), 15, 15, 30)
		self.nom = nom #Un nom lui est attribué pour se repérer.


class SetLevel(FSM):
	"""
	Partez du principe que cette classe sera le coeur du jeu.
	Tout le script principal s'y trouvera.
	"""
	def __init__(self):
		"""
		Métohde constructeur.
		----------------------
		return -> SetLevel
		"""
		FSM.__init__(self, "LevelManager") #Initialisation de notre classe en initialisant la super classe.
		self.debug = False #Le mode debug pourra être activé lors de certains tests (on peut y voir les collisions)
		#-----------------Variables nécessaires au fonctionnement de la boîte de dialogue----------------
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
		base.cTrav = CollisionTraverser() #Le CollisionTraverser, gestionnaire de toutes les collisions.
		if self.debug:
			base.cTrav.showCollisions(render)
		self.skybox = None
		self.portails = {}
		self.triggers = []
		self.save_statues = {}
		self.antimur = CollisionHandlerPusher() #Notre Collision Handler, qui empêchera le joueur de toucher les murs et d'autres choses.
		#-----------------Autres variables-----------------------
		self.chapitre = 0
		self.player = Player()
		self.player.reparentTo(render)
		self.player.hide()
		self.current_map = "village_pecheurs_maison_heros.glb"
		self.texts = ["It's a secret to everybody."]
		self.text_index = 0
		self.letter_index = 0
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
		#----------------Fonctions--------------------------
		base.taskMgr.add(self.update_text, "update_text")
		self.accept("escape", self.all_close)
		base.win.setCloseRequestEvent("escape")


	#---------------Fonctions de manipulation de la GUI------------------------------
	def load_gui(self):
		"""
		Fonction qui nous permet de charger les éléments 2D (car on n'a besoin de les charger qu'une fois)
		--------------------------------------------------
		return -> None
		"""
		self.myOkDialog = None
		self.coeurs_vides = []
		self.coeurs_moitie = []
		self.coeurs_pleins = []
		#------------------------Les coeurs vides-------------------------------------
		x = -1.2
		for loop in range(10):
			a = OnscreenImage("vie_lost.png", scale=Vec3(0.05, 0.05, 0.05), pos=Vec3(x, 1, 0.9))
			a.setTransparency(TransparencyAttrib.MAlpha)
			self.coeurs_vides.append(a)
			x += 0.12
		#-------------------------Les coeurs pleins---------------------------------	
		x = -1.2
		for loop in range(10):
			a = OnscreenImage("vie_full.png", scale=Vec3(0.05, 0.05, 0.05), pos=Vec3(x, 1, 0.9))
			a.setTransparency(TransparencyAttrib.MAlpha)
			self.coeurs_pleins.append(a)
			x += 0.12
		#--------------------Les coeurs à moitié pleins-------------------------------------	
		x = -1.2
		for loop in range(10):
			a = OnscreenImage("vie_half.png", scale=Vec3(0.05, 0.05, 0.05), pos=Vec3(x, 1, 0.9))
			a.setTransparency(TransparencyAttrib.MAlpha)
			self.coeurs_moitie.append(a)
			x+= 0.12
		self.noai_text = OnscreenText(text=f"Noaïs : {int(self.player.noais)}", pos=(-1, 0.7), scale=0.07, fg=(1, 1, 1, 1))
		self.noai_image = OnscreenImage("noai.png", scale=Vec3(0.07, 0, 0.07), pos=Vec3(-1.23, 0, 0.72))
		self.noai_image.setTransparency(TransparencyAttrib.MAlpha)
		self.map_image = OnscreenImage("carte_Terenor.png", scale=Vec3(0.8, 0, 0.8), pos=Vec3(0, 0, 0))
		self.croix_image = OnscreenImage("croix.png", scale=Vec3(0.04, 0, 0.04), pos=Vec3(0, 0, 0))
		self.croix_image.setTransparency(TransparencyAttrib.MAlpha)
		self.lieu_text = OnscreenText(text="???", pos=(0, 0.65), scale=0.1, fg=(1, 1, 1, 1))
		self.hide_gui()

	def hide_gui(self):
		"""
  		Fonction permettant de cacher la GUI (utile lors des cinématiques, ou lors d'un tuto).
    	--------------------------------------------------------------------------------------
      	return -> None
  		"""
		for a in self.coeurs_pleins:
			a.hide()
		for a in self.coeurs_moitie:
			a.hide()
		for a in self.coeurs_vides:
			a.hide()
		self.noai_text.hide()
		self.noai_image.hide()
		self.map_image.hide()
		self.croix_image.hide()
		self.lieu_text.hide()

	#-----------------------Autres fonctions----------------------------------
	def init_fichiers(self):
		"""
		Fonction qui permet de créer les fichiers de jeu.
		-------------------------------------------------
		return -> None
		"""
		#-----------Section qui permet de déterminer si l'ordinateur est au lycée----------------------
		self.augustins = False
		if platform.system() == "Windows":
			if os.path.exists(f"C://users/{os.getlogin()}.AUGUSTINS"):
				self.augustins = True
		self.langue = "francais"		
		path = self.get_path()
		#----------Création du dossier---------------------------
		if not os.path.exists(path):
			os.mkdir(path)
		#-----------------Création des 3 fichiers individuels----------------	
		for loop in range(3):
			if not os.path.exists(path+f"/save_{loop+1}.txt"):
				file = open(path+f"/save_{loop+1}.txt", "wt")
				file.writelines(["_|0|1|3|3"])
				file.close()
		#--------------Création du fichier de mappage de touches-------------------------------		
		if not os.path.exists(path+"/keys.json"):
			file = open(path+"/keys.json", "wt")
			file.writelines(['[{"Avancer":"arrow_up", "Monter la camera":"i", "Descendre la camera":"k", "Camera a droite":"l", "Camera a gauche":"j", "Courir":"b", "Interagir":"space", "Inventaire":"e", "Changer le point de vue":"a", "Recentrer":"l"}]'])
			file.close()
		#----------------Création du fichier pour enregistrer les vriables communes à tous les joueurs (ex : langue)---------------------	
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
			self.langue = "francais"
		file = open(self.get_path()+"/global.txt", "wt")
		info = [self.langue]
		file.writelines([donnee +"|" for donnee in info])
		file.close()
			
		
	def check_interact(self):
		"""
		Fonction appelée chaque fois que le joueur appuie sur espace.
		Cela aura pour conséquences de vérifier les portes, les pnjs touchés, ou encore de passer les dialogues.
		----------------------------------------------------------------------------------------------
		return -> None
		"""
		print(self.player.getPos())
		reussi = self.check_interact_dial()
		if self.current_pnj is not None:
			if not self.reading and not reussi:
				self.text_index = 0
				self.letter_index = 0
				self.set_text(self.pnjs[self.current_pnj].texts)
		if self.current_porte is not None:
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
			taskMgr.doMethodLater(0.45, self.player.setPos, "new_player_pos", extraArgs=[self.portails[self.current_porte].newpos])
			taskMgr.doMethodLater(0.5, self.load_map, "loadmap", extraArgs=[self.current_porte])
		if self.actual_statue is not None:
			taskMgr.remove("update")
			properties = WindowProperties()
			properties.setCursorHidden(False)
			base.win.requestProperties(properties)
			self.ignore("escape")
			self.saveDlg = YesNoDialog(text = self.story["gui"][0], command = self.will_save)

	def check_interact_dial(self):
		"""
		"Petite" fonction qui permet de passer les dialogues.
		------------------------------------------------------
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
							print("Pas de fichier son valide.")
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
		Fonction qui permet d'afficher un texte.
		--------------------------------------------------
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
			self.texts = self.story[str(numero)]
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
				print(self.sons_messages)
				try:
					self.son = loader.loadSfx(self.sons_messages[0])
					self.son.play()
				except:
					print("Pas de fichier son valide.")

	def update_text(self, task):
		"""
		Fonction qui met à jour le texte affiché à l'écran.
		(Il y a sans doute une meilleure solution, mais comme celle-ci fonctionne on la garde)
		---------------------------------------------------------------------------------------
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

	def fade_out(self, state="Menu"):
		"""
		Fonction qui permet au FSM de changer de state avec un fade out visuel et sonore.
		----------------------------------------------------------------------------------
		state -> str
		return None
		"""
		self.transition.fadeOut(1)
		self.ignore("f1")
		Sequence(LerpFunc(self.music.setVolume, fromData = 1, toData = 0, duration = 1)).start()
		taskMgr.doMethodLater(1, self.change_state, "requete", extraArgs=[state])

	def change_state(self, state):
		"""
		Fonction qui fonctionne avec la fonction fade_out.
		------------------------------------------------------
		state -> str
		return -> None
		"""
		self.request(state)

	def all_close(self):
		"""
		Fonction pour fermer la fenêtre et quitter le programme.
		----------------------------------------------------------
		return -> None
		"""
		base.destroy()
		os._exit(0)

	def get_path(self):
		"""
		Fonction permettant de donner le chemin d'accès aux données de sauvegarde.
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
			
	#---------------------------Ecran titre--------------------------------
	def enterMenu(self):
		"""
		Fonction qui prépare l'écran titre.
		------------------------------------------
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
		#-----------------------On charge les textes------------------------------------
		self.textObject1 = OnscreenText(text='Return on Therenor', pos=(0, 0.75), scale=0.07, fg=(1, 1, 1, 1))
		self.textObject2 = OnscreenText(text=self.story["gui"][1], pos=(0, 0.5), scale=0.07, fg=(1, 1, 1, 1))
		#--------------------L'épée--------------------------------------
		self.epee = loader.loadModel("sword.bam")
		self.epee.reparentTo(base.cam)
		#--------------On modifie la caméra (position, lentille)-------------
		base.cam.setPos(0, 0, 0)
		base.cam.node().getLens().setFov(70)
		base.cam.lookAt(self.epee)
		#-------------On fait tourner cette épée---------------------------
		self.epee.setPosHprScale(0.00, 5.00, 0.00, 0.00, 270, 90.00, 1.00, 1.00, 1.00)
		interval = self.epee.hprInterval(2, Vec3(0, 270, 90), startHpr = Vec3(0, 270, 0))
		interval2 = self.epee.hprInterval(2, Vec3(0, 270, 180), startHpr = Vec3(0, 270, 90))
		interval3 = self.epee.hprInterval(2, Vec3(0, 270, 270), startHpr = Vec3(0, 270, 180))
		interval4 = self.epee.hprInterval(2, Vec3(0, 270, 0), startHpr = Vec3(0, 270, 270))
		s = Sequence(interval, interval2, interval3, interval4)
		s.loop()
		#--------------------Gestion des touches----------------------------
		self.accept("escape", self.all_close)
		self.acceptOnce("f1", self.fade_out, extraArgs=["Trois_fichiers"])



	def exitMenu(self):
		"""
		Fonction qui s'acive quand on quitte l'écran titre.
		-----------------------------------------------------
		return -> None
		"""
		self.textObject1.remove_node()
		self.textObject2.remove_node()
		self.epee.removeNode()
		del self.epee

	#-----------------Section de gestion des trois fichiers de sauvegarde--------------------------------
	def enterTrois_fichiers(self):
		"""
		Fonction qui s'active lorsqu'on entre dans le gestionnaire de fichiers de sauvegarde.
		------------------------------------------------------------------------------------
		return -> None
		"""
		self.ignoreAll()
		self.accept("escape", self.all_close)
		self.music = loader.loadSfx("para.ogg")
		self.music.setLoop(True)
		self.music.play()
		Sequence(LerpFunc(self.music.setVolume, fromData = 0, toData = 1, duration = 1)).start()
		#-------------------On met la skybox en arrière-plan (on pourra mettre d'autres modèles 3d plus tard)----------------------
		self.skybox = loader.loadModel("skybox.bam")
		self.skybox.setScale(10000)
		self.skybox.setBin('background', 1)
		self.skybox.setDepthWrite(0)
		self.skybox.setLightOff()
		self.skybox.reparentTo(render)
		#--------------On charge une image pour chaque fichier--------------------------------
		self.files = [OnscreenImage("file.png", scale=Vec3(0.3, 1, 0.3), pos=Vec3(-0.8+i*0.8, 1, 0)) for i in range(3)]
		noms = []
		path = self.get_path()
		for loop in range(3):
			self.read(file=loop+1)
			if self.player.nom != "_":
				noms.append(self.player.nom)
			else:
				noms.append(self.story["gui"][2])	
		self.player.nom = "Link"
		file = open(path+"/keys.json", "rt")
		self.keys_data = json.load(file)[0]
		file.close()
		self.buttons_continue = [DirectButton(text=self.story["gui"][3], scale=0.07, pos=(-0.8+0.8*i, 1, -0.08), command=self.verify, extraArgs=[i+1]) for i in range(3)]
		self.buttons_erase = [DirectButton(text=self.story["gui"][4], scale=0.07, pos=(-0.8+0.8*i, 1, -0.18), command=self.confirm_erase, extraArgs=[i+1]) for i in range(3)]
		self.names = [OnscreenText(text=noms[i], pos=(-0.8+0.8*i, 0.08), scale=0.07) for i in range(3)]
		self.button_mapping = DirectButton(text=self.story["gui"][5], scale=0.07, pos=(0.8, 1, -0.7), command=self.fade_out, extraArgs=["Mapping"])
		self.button_langue = DirectButton(text=self.story["gui"][6], scale=0.07, pos=(-0.8, 1, -0.7), command=self.fade_out, extraArgs=["Language"])		
		self.transition.fadeIn(1)

	def confirm_erase(self, file=1):
		"""
		Fonction qui crée un petit pop-up qui permet de s'assurer que l'utilisateur veut effacer ses données.
		----------------------------------------------------------------------------------------------------
		file -> int
		return -> None
		"""
		self.eraseDlg = YesNoDialog(text=self.story["gui"][7], command=self.erase_file, extraArgs=[file])


	def erase_file(self, clickedYes, file):
		"""
		Fonction qui s'active lorsque l'utilisateur répond au pop-up pour l'effacement de fichier.
		---------------------------------------------------------------------------------------------
		clickedYes -> bool
		file -> int
		return -> None
		"""
		self.eraseDlg.cleanup()
		if clickedYes:
			fichier = open(self.get_path()+f"/save_{file}.txt", "wt")
			fichier.writelines(["_|0|1|3|3"])
			fichier.close()
			for button in self.buttons_erase:
				button.removeNode()
			for button in self.buttons_continue:
				button.removeNode()
			self.fade_out()



	def exitTrois_fichiers(self):
		"""
		Fonction qui s'active lorsque l'on quitte l'état trois_fichiers.
		----------------------------------------------------------------------
		return -> None
		"""
		self.music.stop()
		self.accept(self.keys_data["Interagir"], self.check_interact)
		self.accept("escape", self.all_close)
		base.win.setCloseRequestEvent("escape")
		self.skybox.removeNode()
		for file in self.files:
			file.removeNode()
		del self.files
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

	def verify(self, file):
		"""
		Quand on quitte l'écran titre, on vérifira notre avancement dans l'histoire.
		On agira de différentes manières selon le chapitre auquel le joueur est rendu.
		---------------------------------------------------------------------------
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
		elif self.chapitre == 2:
			Sequence(LerpFunc(self.music.setVolume, fromData = 1, toData = 0, duration = 2)).start()
			self.fade_out("Map")
		elif self.chapitre == 3:
			self.fade_out("Cinematique")
		#------------Générique---------------------------
		else:
			self.request("Generique")
	#--------------------------------Gestion du changement de langue-----------------------------------------------
	def enterLanguage(self):
		"""
		Fonction qui s'active lorsque l'on entre dans l'état de changement de langue.
		-------------------------------------------------------------------------------
		return -> None
		"""
		self.transition.fadeIn(1)
		self.skybox = loader.loadModel("skybox.bam")
		self.skybox.setScale(10000)
		self.skybox.setBin('background', 1)
		self.skybox.setDepthWrite(0)
		self.skybox.setLightOff()
		self.skybox.reparentTo(render)
		dico = {"francais":0, "deutsch":1}
		self.textObject = OnscreenText(text="Veuillez choisir votre langue.", pos=(0, 0.7), scale=0.07, fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter, mayChange=1)
		self.menu = DirectOptionMenu(text="options", scale=0.15, pos=(-0.5, 0, 0), initialitem=dico[self.langue], items=["francais", "deutsch"], highlightColor=(0.65, 0.65, 0.65, 1), command=self.itemSel, textMayChange=1)
		self.exit_button = DirectButton(text="Retour", scale=0.07, pos=(-0.8, 1, -0.7), command=self.fade_out, extraArgs=["Trois_fichiers"])
		if self.langue == "deutsch":
			self.textObject.setText("Bitte wählen Sie Ihre Sprache.")
			self.exit_button.setText("Zurück")

	def itemSel(self, arg):
		"""
		Fonction qui s'active dès que l'utilisateur change de langue.
		----------------------------------------------------------------
		arg -> str
		return -> None
		"""
		self.langue = arg
		if self.langue == "francais":
			self.textObject.setText("Veuillez choisir votre langue.")
			self.exit_button.setText("Retour")
		elif self.langue == "deutsch":
			self.textObject.setText("Bitte wählen Sie Ihre Sprache.")
			self.exit_button.setText("Zurück")	

	
	def exitLanguage(self):
		"""
		Fonction qui s'active lorsque l'on quitte l'état pour changer de langue.
		---------------------------------------------------------------------------
		return -> None
		"""
		self.save_global()
		with open("../data/json/texts.json", encoding="utf-8") as texts:
			self.story = json.load(texts)[self.langue]
		self.skybox.removeNode()
		del self.skybox
		self.textObject.removeNode()
		del self.textObject
		self.menu.removeNode()
		del self.menu
		self.exit_button.removeNode()
		del self.exit_button
		
	#-------------------------------Gestion du mappage de touches--------------------------------------------------
	def enterMapping(self):
		"""
		Fonction inspirée du script mappingGUI des samples de panda3d.
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
        #On charge la géométrie des boutons
		maps = loader.loadModel("gui/button_map")
		self.buttonGeom = (maps.find("**/ready"), maps.find("**/click"), maps.find("**/hover"), maps.find("**/disabled"))
        #Ici, on crée un titre
		self.textscale = 0.1
		self.title = DirectLabel(
		scale=self.textscale,
		pos=(base.a2dLeft + 0.05, 0.0, base.a2dTop - (self.textscale + 0.05)),
		frameColor=VBase4(0, 0, 0, 0),
		text="Paramétrage des touches",
		text_align=TextNode.ALeft,
		text_fg=VBase4(1, 1, 1, 1),
		text_shadow=VBase4(0, 0, 0, 0.75),
		text_shadowOffset=Vec2(0.05, 0.05))
		self.title.setTransparency(1)
		#---------------------------------------------------
		thumbMaps = loader.loadModel("gui/thumb_map")
		thumbGeom = (
		thumbMaps.find("**/thumb_ready"),
		thumbMaps.find("**/thumb_click"),
		thumbMaps.find("**/thumb_hover"),
		thumbMaps.find("**/thumb_disabled"))
		incMaps = loader.loadModel("gui/inc_map")
		incGeom = (
		incMaps.find("**/inc_ready"),
		incMaps.find("**/inc_click"),
		incMaps.find("**/inc_hover"),
		incMaps.find("**/inc_disabled"))
		decMaps = loader.loadModel("gui/dec_map")
		decGeom = (
		decMaps.find("**/dec_ready"),
		decMaps.find("**/dec_click"),
		decMaps.find("**/dec_hover"),
		decMaps.find("**/dec_disabled"))
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
		verticalScroll_thumb_geom=thumbGeom,
		verticalScroll_thumb_pressEffect=False,
		verticalScroll_thumb_frameColor=VBase4(0, 0, 0, 0),
		verticalScroll_incButton_relief=1,
		verticalScroll_incButton_geom=incGeom,
		verticalScroll_incButton_pressEffect=False,
		verticalScroll_incButton_frameColor=VBase4(0, 0, 0, 0),
		verticalScroll_decButton_relief=1,
		verticalScroll_decButton_geom=decGeom,
		verticalScroll_decButton_pressEffect=False,
		verticalScroll_decButton_frameColor=VBase4(0, 0, 0, 0),)
		#On crée notre liste
		idx = 0
		self.listBGEven = base.loader.loadModel("gui/list_item_even")
		self.listBGOdd = base.loader.loadModel("gui/list_item_odd")
		self.actionLabels = {}
		for action in self.mapping.actions:
			mapped = self.mapping.formatMapping(action)
			item = self.__makeListItem(action, mapped, idx)
			item.reparentTo(self.lstActionMap.getCanvas())
			idx += 1
		#On recalcule la taille du canevas pour ajouter une barre de défilement si nécessaire.
		self.lstActionMap["canvasSize"] = (base.a2dLeft+0.05, base.a2dRight-0.05, -(len(self.mapping.actions)*0.1), 0.09)
		self.lstActionMap.setCanvasSize()
		self.button_retour = DirectButton(text=self.story["gui"][8], pos=(0.8, 1, -0.7), scale=0.07, command=self.fade_out, extraArgs=["Trois_fichiers"])
		#Petit fade in (sinon on n'y voit rien)
		self.transition.fadeIn(2)

	def closeDialog(self, action, newInputType, newInput):
		"""
		Fonction qui s'active lorsque l'on a répondu à la boîte de dialogue
		qui s'affiche quand on change les touches.
		-------------------------------------------------------------
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
		Fonction qui permet d'afficher le dialogue pour changer les touches.
		----------------------------------------------------------------------
		action -> str
		return -> None
		"""
		liste_interdite = ["Avancer", "Monter la camera", "Descendre la camera", "Camera a droite", "Camera a gauche"]
		if self.manette and action in liste_interdite:
			return None
		else:
			#On crée notre fenêtre de dialogue.
			self.dlgInput = ChangeActionDialog(action, button_geom=self.buttonGeom, command=self.closeDialog)
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
		Fonction qui vérifie si l'on touche à quelque chose.
		-------------------------------------------------------
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
		Fonction appelée pour créer un contenu.
		------------------------------------------
		action -> str
		event -> str
		index -> int
		return -> DrectFrame
		"""
		def dummy(): pass
		if index % 2 == 0:
			bg = self.listBGEven
		else:
			bg = self.listBGOdd
		item = DirectFrame(
		text=action,
		geom=bg,
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
		text="Modifier",
		geom=self.buttonGeom,
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

	def exitMapping(self):
		"""
		Fonction qui s'active lorsque l'on quitte le mappage de touches.
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
			dico["Avancer"], dico["Monter la camera"], dico["Descendre la camera"], dico["Camera a gauche"], dico["Camera a droite"] = data["Avancer"], data["Reculer"], data["Aller a gauche"], data["Aller a droite"], data["Monter la camera"], data["Descendre la camera"], data["Camera a gauche"], data["Camera a droite"]
			file = open(self.get_path()+"/keys.json", "wt")
			file.writelines([json.dumps([dico])])
			file.close()
		else:
			file = open(self.get_path()+"/keys.json", "wt")
			file.writelines([json.dumps([self.mapping.get_map()])])
			file.close()
		self.listBGEven.removeNode()
		self.listBGOdd.removeNode()
		del self.listBGEven
		del self.listBGOdd
		self.title.removeNode()
		self.lstActionMap.removeNode()
		del self.lstActionMap
		del self.title
		self.button_retour.removeNode()
		del self.button_retour

	#-------------------------------Paramètres en début de partie (Nom du joueur)-----------------------------------
	def enterInit(self):
		"""
		Fonction qui s'active quand on entre dans les paramètres en début de partie.
		----------------------------------------------------------------------------
		return -> None
		"""
		self.nameEnt = DirectEntry(scale = 0.08, pos = Vec3(-0.4, 0, 0.15), width = 10)
		self.nameLbl = DirectLabel(text = self.story["gui"][9], pos = Vec3(0, 0, 0.4), scale = 0.1, textMayChange = 1, frameColor = Vec4(1, 1, 1, 1))
		self.helloBtn = DirectButton(text =self.story["gui"][10], scale = 0.1, command = self.setName, pos = Vec3(0, 0, -0.1))

	def exitInit(self):
		"""
		Fonction qui s'active quand on quitte ces paramètres.
		--------------------------------------------------------
		return -> None
		"""
		self.music.stop()
		self.chapitre = 1

	def setName(self):
		"""
		Petit pop-up de vérification.
		--------------------------------
		return -> None
		"""
		self.acceptDlg = YesNoDialog(text =self.story["gui"][11], command = self.acceptName)

	def acceptName(self, clickedYes):
		"""
		Fonction qui en fonction de la rééponse du joueur commence le jeu ou reste dans les paramètres.
		--------------------------------------------------------------------------------------------
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
			self.request("Cinematique")
			
	#-------------------------------Introduction avec la légende--------------------------------------
	def enterCinematique(self):
		"""
		Fonction au début de l'histoire lorsqu'on raconte la légende.
		-----------------------------------------------------------------
		return -> None
		"""
		self.actuals_light = []
		#------------------------Légende-------------------------------------------------------
		if self.chapitre == 1:
			self.music = base.loader.loadSfx("legende.ogg")
			self.music.setLoop(True)
			self.music.play()
			self.set_text(0, ["Fini"])
			self.accept("Fini", self.fade_out, extraArgs=["Map"])
		#---------------------------Cinématique du magicien----------------------------------
		elif self.chapitre == 3:
			if hasattr(self.player, "followcam"):
				self.player.followcam.set_active(False)
			self.player.show()
			self.player.setPos(200, -400, 0)
			self.player.setH(180)
			self.player.setScale(110)
			if hasattr(self, "map"):
				self.map.removeNode()
			self.move_camera = 0
			#-------------------Lumières-------------------------------------------
			point_light = PointLight("point_light")
			point_light.setColor((0.85, 0.8, 0.5, 1))
			point_light_np = render.attachNewNode(point_light)
			point_light_np.setPos(200, 0, 50)
			self.actuals_light.append(point_light_np)
			render.setLight(point_light_np)
			render.setShaderAuto()
			#-----------------Modèles------------------------------------------
			self.map = loader.loadModel("salle_du_sacrifice.bam")
			self.map.reparentTo(render)
			self.map.setPos(500, 500, 0)
			self.map.setHpr(270, 0, 0)
			self.magicien = Magicien()
			self.magicien.setPos(200, 200, 0)
			self.magicien.loop("Immobile")
			self.magicien.reparentTo(render)
			base.cam.setPos(200, -550, 250)
			#-----------------------Musique-------------------------------
			self.music.stop()
			self.music = base.loader.loadSfx("Le_magicien_démoniaque.ogg")
			self.music.setLoop(True)
			self.music.play()
			#------------Petit fade in---------------------------------------------
			self.transition.fadeIn(2)
			self.set_text(1, ["Fini"])
			self.accept("Fini", self.fade_out, extraArgs=["Map"])
		taskMgr.add(self.update_cinematique, "update_cinematique")

	def update_cinematique(self, task):
		"""
		Fonction qui en fonction de l'avancement dans la légende change l'image en background.
		-----------------------------------------------------------------------------------
		task -> task
		return -> task.cont ou task.done
		"""
		dt = globalClock.getDt()
		if self.chapitre == 1:
			if self.text_index == 8:
				if not hasattr(self, "image"):
					self.image = OnscreenImage("la_legende.png", scale=Vec3(1.5, 0, 1), pos=Vec3(0, 0, 0))
			if self.text_index == 11:
				if hasattr(self, "image"):
					self.image.removeNode()
					del self.image
			if self.text_index > 11:
				return task.done
		elif self.chapitre == 3:
			if self.text_index	<= 4:
				if base.cam.getY() < 200:
					base.cam.setY(base.cam, dt*60)
			elif self.text_index <= 6:
				if self.move_camera == 0:
					self.move_camera = 1
					base.cam.setPosHpr(200, 200, 200, 180, 0, 0)
				if base.cam.getY() > -100:
					base.cam.setY(base.cam, dt*25)
		return task.cont

	def exitCinematique(self):
		"""
		Fonction lorsque la cinématique est finie.
		------------------------------------------
		return -> None
		"""
		for light in self.actuals_light:
			render.clearLight(light)
			light.removeNode()	
		del self.actuals_light
		taskMgr.remove("update_cinematique")
		self.ignore("Fini")
		if self.chapitre == 1:
			self.music.stop()
			self.chapitre = 2
		if self.chapitre == 3:
			self.magicien.delete()
			del self.magicien
			base.cam.setPosHpr(0, 0, 0, 0, 0, 0)
			self.player.setScale(70)
			self.music.stop()
			self.chaptre = 2
			
	#-------------Fonction de chargement de map--------------------------------
	def load_map(self, map="village_pecheurs_maison_heros.glb", task=None):
		"""
		Fonction qui nous permet de charger une map
		-------------------------------------------
		map -> str
		task -> None (ou task)
		return -> None
		"""
		for pnj in self.pnjs:
			self.pnjs[pnj].cleanup()
			self.pnjs[pnj].removeNode()
		for objet in self.objects:
			objet.object.removeNode()
		self.objects = []
		self.current_pnj = None
		self.current_porte = None
		self.pnjs = {}
		self.portails = {}
		self.save_statues = {}
		if hasattr(self, "actuals_light"):
			for light in self.actuals_light:
				render.clearLight()
				light.removeNode()
		self.actuals_light = []
		#-------Section de gestion de la map en elle-même-----
		self.current_map = map
		if hasattr(self, "map"):
			if self.map is not None:
				self.map.removeNode()
			del self.map
		self.map = loader.loadModel(map)
		self.map.setHpr(0, 90, 0)
		self.map.reparentTo(render)
		#---------------------------Collisions de la map------------------
		self.antimur.addInPattern("into")
		self.antimur.addOutPattern("out")
		self.map.setCollideMask(BitMask32.bit(0))
		if self.debug:
			base.cTrav.showCollisions(render)
		self.antimur.addCollider(self.player.col_np, self.player)
		base.cTrav.addCollider(self.player.col_np, self.antimur)
		#-------------La skybox-----------------
		if self.skybox is not None:
			self.skybox.removeNode()
		self.skybox = loader.loadModel("skybox.bam")
		self.skybox.setScale(10000)
		self.skybox.setBin('background', 1)
		self.skybox.setDepthWrite(0)
		self.skybox.setLightOff()
		self.skybox.reparentTo(render)
		#--------------------Chargement du premier fichier json (objets)---------------
		objects_file = open("../data/json/objects.json")
		data = json.load(objects_file)
		objects_file.close()
		if self.current_map in data:
			for object in data[self.current_map]:
				if object == "lit.bam":
					objet = Lit()
				objet.object.reparentTo(render)
				objet.object.setPos((data[self.current_map][object][0][0], data[self.current_map][object][0][1], data[self.current_map][object][0][2]))
				objet.object.setHpr((data[self.current_map][object][1][0], data[self.current_map][object][1][1], data[self.current_map][object][1][2]))
				self.objects.append(objet)
		#--------------------Chargement du deuxième fichier json-------------
		pnj_file = open("../data/json/data.json")
		data = json.load(pnj_file)
		pnj_file.close()
		#-----Section de gestion de la musique------
		if self.music is not None:
			self.music.stop()
			self.music = None
		self.music = base.loader.loadSfx(data[self.current_map][0])
		self.music.setLoop(True)
		self.music.play()
		#---------------------Gestion de la caméra du joueur----------------
		if not hasattr(self.player, "followcam"):
				self.player.create_camera()
		if not self.player.followcam.active:
			self.player.followcam.set_active(True)
		self.player.followcam.dummy.setHpr(180, 0, 0)
		self.player.followcam.camera.setHpr(0, 0, 0)	
		self.player.followcam.camera.setPos(0, 0, 0)	
		self.player.followcam.camera.setPos(0, -2, 0)	
		#----------Les portes-----------------------
		for portail in data[self.current_map][2]:
			noeud = CollisionNode(portail)
			info = data[self.current_map][2][portail]
			if info[0] == "porte":
				solid = Porte(center=(info[1][0], info[1][1], info[1][2]), sx=info[2], sy=info[3], sz=info[4], newpos=(info[5][0], info[5][1], info[5][2]))
			else:
				solid = Portail(center=(info[1][0], info[1][1], info[1][2]), sx=info[2], sy=info[3], sz=info[4], newpos=(info[5][0], info[5][1], info[5][2]))
			noeud.addSolid(solid)
			self.portails[portail] = solid
			noeud.setCollideMask(BitMask32.bit(0))
			noeud_np = self.map.attachNewNode(noeud)
		#------------------Les pnjs--------------------------------
		for pnj in data[self.current_map][1]:
			info = data[self.current_map][1][pnj]
			a = PNJ(pnj)
			a.setPos(info[0], info[1], info[2])
			self.pnjs[pnj] = a
		for pnj in self.pnjs:
			self.pnjs[pnj].reparentTo(render)
        #-------------Les sauvegardes------------------------
		for save in data[self.current_map][3]:
			noeud = CollisionNode(save)
			noeud.addSolid(Save_bloc(save, data[self.current_map][3][save]))
			self.save_statues[save] = noeud
			noeud.setCollideMask(BitMask32.bit(0))
			noeud_np = self.map.attachNewNode(noeud)
		self.load_triggers(map)
		self.map.setScale(data[self.current_map][4])
		del data
		#------------Mode debug------------------------
		if self.debug:
			base.enableMouse()
		else:
			base.disableMouse()
		#-------------Lumière----------------------------
		light = AmbientLight("a")
		light_np = render.attachNewNode(light)
		self.actuals_light.append(light_np)
		render.setLight(light_np)
		#--------------Attribution des touches à des fonctions-------------------------------
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
		taskMgr.add(self.update, "update")
		self.transition.fadeIn(2)
		if task is not None:
			return task.done

	def load_triggers(self, map="village_pecheurs_maison_heros.glb"):
		"""
		Fonction dans laquelle on rentre toutes les instructions sur nos triggers.
		C'est à dire les collisions "scénaristiques".
		------------------------------------------------------
		map -> str
		return -> None
		"""
		if hasattr(self, "triggers"):
			for trigger in self.triggers:
				trigger.removeNode()
		self.triggers = []


	#---------------------------------Boucle de jeu "normale"----------------------------------------------------------------
	def enterMap(self):
		"""
		Fonction s'activant quand on souhaite charger la map.
		-----------------------------------------------------
		return -> None
		"""
		#On montre le joueur.
		self.player.show()
		#On cache le curseur de la souris.
		properties = WindowProperties()
		properties.setCursorHidden(True)
		base.win.requestProperties(properties)
		self.load_save()
		#Petit fade in et on charge la map.
		self.transition.fadeIn(1)
		self.load_map(self.current_map)

	def load_save(self, task=None):
		"""
		Fonction qui permet de charger la nouvelle position du joueur quand on charge une map.
		--------------------------------------------------------------------------------------
		task -> task
		return -> None
		"""
		if self.current_point == "1":
			self.current_map = "village_pecheurs_maison_heros.glb"
			self.player.setPos(200, -110, 6)
		#------------Par défaut, le joueur se retrouve chez lui-------------	
		else:
			self.current_map = "village_pecheurs_maison_heros.glb"
			self.player.setPos(200, -110, 6)
		if task != None:
			return task.done

	def into(self, a):
		"""
		Fonction s'activant quand le joueur ou un autre objet from, touche un objet into.
		-----------------------------------------------------------------------------------
		a -> entry (une info sur la collision)
		return -> None
		"""
		b = str(a.getIntoNodePath()).split("/")[len(str(a.getIntoNodePath()).split("/"))-1] #L'objet Into
		c = str(a.getFromNodePath()).split("/")[len(str(a.getFromNodePath()).split("/"))-1] #L'objet From
		#--------------Si c'est le joueur qui touche--------------------------
		if c == "player_sphere":
			#-----------Si on touche un pnj--------------------------
			if b in self.pnjs:
				self.current_pnj = b
				self.pnjs[b].s.pause()
			elif b in self.portails:
				if type(self.portails[b]) is Portail:
					self.transition.fadeOut(0.5)
					self.player.setPos(self.portails[b].newpos)
					taskMgr.doMethodLater(0.5, self.load_map, "loadmap", extraArgs=[b])
				elif type(self.portails[b]) is Porte:
					self.current_porte = b
			#--------------Si on touche un trigger------------------------------
			elif b.isdigit():
				b = int(b)
				if b == 1:
					if not "epee" in self.player.inventaire:
						taskMgr.remove("update")
						self.player.stop()
						s = Sequence(self.player.posInterval(1.5, Vec3(self.player.getX(), self.player.getY()+30, self.player.getZ()), startPos=Vec3(self.player.getX(), self.player.getY(), self.player.getZ())), Func(taskMgr.add, self.update, "update"), Func(self.ignore, "finito"))
						self.set_text(2, messages=["finito"])
						self.accept("finito", s.start)
			#--------------Si on touche une statue de sauvegarde----------------------------------
			elif b in self.save_statues:
				self.actual_statue = b		


	def change_vitesse(self, touche="b"):
		"""
		Fonction qui change la vitesse du joueur si on appuie sur la touche b ou si on la relâche.
		-------------------------------------------------
		touche -> str
		return -> None
		"""
		if touche == "b":
			self.player.vitesse *= 2
		else:
			self.player.vitesse /=2

	def out(self, a):
		"""
		Fonction s'activant quand un objet from qitte un objet into.
		----------------------------------------------------------------
		a -> entry (info sur la collision)
		return -> None
		"""
		b = str(a.getIntoNodePath()).split("/")[len(str(a.getIntoNodePath()).split("/"))-1]
		c = str(a.getFromNodePath()).split("/")[len(str(a.getFromNodePath()).split("/"))-1]
		if c == "player_sphere":
			if b in self.pnjs:
				self.pnjs[b].s.resume()
				self.current_pnj = None
			elif b in self.portails:
				self.current_porte = None
			elif b in self.save_statues:
				self.actual_statue = None

	def touche_pave(self, message="arrow_up"):
		"""
  		Fonction s'activant quand on appuie sur ou qu'on relache une touche du pavé de flèches.
  		Cette fonction pourrait être supprimée, vu que le joueur se dirige maintenant avec la souris.
  		Mais on la garde pour ne pas avoir de bugs.
  		----------------------------------------------------------------------------------------------
  		message -> str
  		return -> None
  		"""
		if message == "arrow_up":
			self.player.walk = True
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

	def update(self, task):
		"""
		Fonction appelée à chaque frame pour mettre certaines choses à jour.
		---------------------------------------------------------
		task -> task
		return -> task.cont
		"""
		dt = globalClock.getDt()
		#---------------Section éléments 2D-------------------------------------------
		self.noai_text.show()
		self.noai_image.show()
		self.croix_image.hide()
		self.lieu_text.hide()
		self.map_image.hide()
		for coeur in self.coeurs_vides:
			coeur.hide()
		for coeur in self.coeurs_moitie:
			coeur.hide()
		for coeur in self.coeurs_pleins:
			coeur.hide()
		for loop in range(self.player.maxvies):
			self.coeurs_vides[loop].show()
		if self.player.vies%1 != 0:
			self.coeurs_moitie[int(self.player.vies)].show()
		for loop in range(int(self.player.vies)):
			self.coeurs_pleins[loop].show()
		#-----------------------Section gestion de la manette-----------------
		if self.manette:
			base.devices.update()
			if not base.devices.getDevices(InputDevice.DeviceClass.gamepad):
				self.music.setVolume(0)
				self.hide_gui()
				self.transition.fadeScreenColor((0, 0, 0, 0.6))
				self.transition.letterboxOn()
				self.gamepad_text = OnscreenText(text=self.story["gui"][12], pos=(0, 0), scale=(0.15, 0.15), fg=(1, 1, 1, 1))
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
		if self.player.getZ() > 6:
		  self.player.setZ(self.player, -0.25)
		else:
		  self.player.setZ(6)
		if self.player.walk:
			self.player.setY(self.player, -self.player.vitesse*globalClock.getDt())
		if self.player.reverse:
			self.player.setY(self.player, self.player.vitesse*globalClock.getDt())
		if self.player.right:
			self.player.setH(self.player, -self.player.vitesse*10*globalClock.getDt())
		if self.player.left:
			self.player.setH(self.player, self.player.vitesse*10*globalClock.getDt())
		#--------------------Sections gestion des vies-----------------------------
		if self.player.vies <= 0:
			self.transition.fadeOut(0.5)
			taskMgr.doMethodLater(0.5, self.launch_game_over, "launch game over")
			return task.done
		return task.cont

	def exitMap(self):
		"""
		Fonction appelée quand on quitte la map.
		----------------------------------------
		return -> None
		"""
		self.music.stop()
		self.map.removeNode()
		self.skybox.removeNode()
		self.player.hide()
		for pnj in self.pnjs:
			self.pnjs[pnj].cleanup()
			self.pnjs[pnj].removeNode()
		for objet in self.objects:
			objet.object.removeNode()
		for statue in self.save_statues:
			self.save_statues[statue].clearSolids()
		self.save_statues = {}
		self.antimur.clearInPatterns()
		self.antimur.clearOutPatterns()
		self.objects = []
		self.pnjs = {}
		self.map = None
		self.player.left = False
		self.player.right = False
		self.player.reverse = False
		self.player.walk = False
		taskMgr.remove("update")
		self.ignoreAll()
		self.accept("escape", self.all_close)
		self.player.stop()
		self.player.followcam.set_active(False)

	def confirm_quit(self):
		"""
		Fonction qui s'active quand on joue, et que l'on appuie sur échap.
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
		  self.quitDlg = YesNoDialog(text = self.story["gui"][13], command = self.quit_confirm)

	def quit_confirm(self, clickedYes):
		"""
		Fonction qui se met en marche une fois que le joueur 
		a répondu à la boîte de dialogue pour quitter le jeu.
		-----------------------------------------------------
		clickedYes -> bool
		return -> None
		"""
		self.quitDlg.cleanup()
		self.quitDlg = None
		taskMgr.add(self.update, "update")
		if clickedYes:
			self.read(file=self.actual_file)
			self.fade_out()
		else:
			properties = WindowProperties()
			properties.setCursorHidden(True)
			base.win.requestProperties(properties)
			self.accept("escape", self.confirm_quit)
			self.accept(self.keys_data["Inventaire"], self.inventaire)

		
	#-----------------------Section de gestion de l'inventaire (et d'autres fonctions d'ui)--------------
	def inventaire(self):
		"""
		Fonction utilisée pour ouvrir l'inventaire
		-------------------------------------------
		return -> None
		"""
		self.player.stop()
		taskMgr.remove("update")
		self.player.walk, self.player.reverse, self.player.left, self.player.right = False, False, False, False
		self.index_invent = 0
		self.ignore("out")
		self.ignore("into")
		self.ignore("escape")
		self.accept("escape", self.exit_inventaire)
		self.ignore(self.keys_data["Avancer"])
		self.ignore(self.keys_data["Avancer"]+"-up")
		self.ignore(self.keys_data["Changer le point de vue"])
		self.ignore(self.keys_data["Courir"])
		self.ignore(self.keys_data["Courir"]+"-up")
		self.ignore(self.keys_data["Inventaire"])
		self.accept(self.keys_data["Inventaire"], self.exit_inventaire)
		taskMgr.add(self.update_invent, "update_invent")
		self.music.setVolume(0.6)
		self.croix_image.setPos(self.get_pos_croix()[0])
		self.lieu_text.setText(self.get_pos_croix()[1])

	def get_pos_croix(self):
		"""
		Fonction qui retourne la position de la croix qui indique notre position sur la carte de l'inventaire.
		-----------------------------------------------------------------------
		return -> Vec3
		"""
		if self.current_map == "village_pecheurs.glb" or self.current_map == "village_pecheurs_maison_chef.glb" or self.current_map == "village_pecheurs_maison_heros.glb":
			return	Vec3(0.5, 0, 0), "Village des pêcheurs"
		return Vec3(0, 0, 0), "???"

	def change_index_invent(self, dir="left"):
		"""
		Fonction qui permet de changer de menu d'inventaire
		-------------------------------------------------
		dir -> str
		return -> None
		"""
		if dir == "left":
			if self.index_invent > 0:
				self.index_invent -= 1
			else:
				self.index_invent = 1
		elif dir == "right":
			if self.index_invent < 1:
				self.index_invent += 1
			else:
				self.index_invent = 0

	def update_invent(self, task):
		"""
		Fonction appelée à chaque frame dans l'inventaire pour mettre à jour le contenu
		-----------------------------------------------------------------------------
		task -> task
		return -> task.cont
		"""
		self.map_image.hide()
		self.croix_image.hide()
		self.noai_image.hide()
		self.noai_text.hide()
		self.lieu_text.hide()
		for coeur in self.coeurs_pleins:
			coeur.hide()
		for coeur in self.coeurs_moitie:
			coeur.hide()
		for coeur in self.coeurs_vides:
			coeur.hide()
		if self.index_invent == 0:
			self.map_image.show()
			self.croix_image.show()
			self.lieu_text.show()
		elif self.index_invent == 1:
			self.noai_image.show()
			self.noai_text.show()
		base.win.movePointer(0, int(base.win.getProperties().getXSize()/2), int(base.win.getProperties().getYSize()/2))
		return task.cont

	def exit_inventaire(self):
		"""
		Fonction appelée lorsqu'on quitte l'inventaire
		--------------------------------------------------
		return -> None
		"""
		self.music.setVolume(1)
		taskMgr.remove("update_invent")
		taskMgr.add(self.update, "update")
		self.accept("escape", self.confirm_quit)
		if not self.manette:
			self.accept(self.keys_data["Avancer"], self.touche_pave, extraArgs=["arrow_up"])
			self.accept(self.keys_data["Avancer"]+"-up", self.touche_pave, extraArgs=["arrow_up-up"])
		self.accept(self.keys_data["Changer le point de vue"], self.player.followcam.change_vue)
		self.accept(self.keys_data["Courir"], self.change_vitesse, extraArgs=["b"])
		self.accept(self.keys_data["Courir"]+"-up", self.change_vitesse, extraArgs=["b-up"])
		self.accept(self.keys_data["Inventaire"], self.inventaire)
		self.accept("into", self.into)
		self.accept("out", self.out)
	#----------------------------------Partie pour le generique--------------------------------------------------------------------------
	def enterGenerique(self):
		"""
		Fonction activée quand on entre dans le générique.
		-------------------------------------------------
		return -> None
		"""
		self.music = loader.loadSfx("Thème_de_Therenor.ogg")
		self.music.setLoop(True)
		self.music.play()
		self.texts_gen_1 = [("Music :", True),  ("Etienne Pacault", False), ("PNJ Design :", True), ("Alexandrine Charette", False), ("Player and Item Design :", True), ("Rémy Martinot", False),
		("Enemy program : ", True), ("Noé Mora", False), ("Map and dungeon creation :", True), ("Etienne Pacault", False), ("Website and movies :", True), ("Tyméo Bonvicini-Renaud", False),
		("Special thanks to :", True), ("Aimeline Cara", False), ("The Carnegie Mellon University who updates the Panda 3D source code", False), ("Disney Online", False),
		("And thank you to everyone we probably forgot ! :-)", False)]
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
		Fonction activée quand on quitte le générique.
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
		Fonction qui après le générique permet d'accéder à l'écran titre.
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
		Fonction qui met à jour le générique.
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
		Fonction pour lancer le game over.
		-----------------------------------
		task -> task
		return -> task.done
		"""
		self.request("Game_over")
		return task.done

	def enterGame_over(self):
		"""
		Fonction qui s'active quand on entre dans le game over.
		--------------------------------------------------------
		return -> None
		"""
		render.hide()
		self.noai_text.hide()
		self.noai_image.hide()
		for coeur in self.coeurs_pleins:
			coeur.hide()
		for coeur in self.coeurs_moitie:
			coeur.hide()
		for coeur in self.coeurs_vides:
			coeur.hide()
		self.music.stop()
		self.music = loader.loadSfx("game_over.ogg")
		self.music.play()
		self.player.vies = 3
		self.transition.fadeIn(0.5)
		self.text_game_over = OnscreenText("Game over", pos=(0, 0), scale=(0.2, 0.2), fg=(0.9, 0, 0, 1))
		self.text_game_over_2 = OnscreenText(self.story["gui"][14], pos=(0, -0.2), scale=(0.1, 0.1), fg=(0.9, 0, 0, 1))
		self.accept("f1", self.fade_out, extraArgs=["Map"])

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
		Fonction qui permet de masquer les textes 
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
		Fonction qui permet de sauvegarder les données de la partie.
		------------------------------------------------------------
		return -> None
		"""
		if reset:
			self.chapitre = 0
			self.player.nom = "Link"
			self.player.noais = 0
			self.current_map = "village_pecheurs_maison_heros.glb"
		file = open(self.get_path()+f"/save_{file}.txt", "wt")
		info = [self.player.nom, str(self.chapitre), str(self.current_point), str(self.player.vies), str(self.player.maxvies), str(self.player.noais)]
		file.writelines([donnee +"|" for donnee in info])
		file.close()

	def will_save(self, clickedYes):
		"""
		Fonction qui s'active si on touche une statue de sauvegarde.
		--------------------------------------------------------------
		return -> None
		"""
		self.saveDlg.cleanup()
		if clickedYes:
			self.save(file=self.actual_file)
			self.myOkDialog = OkDialog(text=self.story["gui"][15], command = self.reupdate)

	def reupdate(self, inutile):
		"""
		Fonction pour remettre la fonction de mise à jour en éxécution.
		---------------------------------------------------------------
		inutile -> bool
		return -> None
		"""
		properties = WindowProperties()
		properties.setCursorHidden(True)
		base.win.requestProperties(properties)
		self.myOkDialog.cleanup()
		self.accept("escape", self.confirm_quit)
		taskMgr.add(self.update, "update")

	def read(self, file=1):
		"""
		Fonction qui permet de lire les données préalablement enregistrées.
		-------------------------------------------------------------------
		return -> None
		"""
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
		fichier.close()

	def wait_for_gamepad(self, task):
		"""
		Fonction qui vérifie si la manette
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
