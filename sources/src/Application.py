from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.fsm.FSM import FSM
from direct.gui.OnscreenImage import *
from direct.gui.OnscreenText import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.interval.IntervalGlobal import Sequence
from direct.interval.LerpInterval import LerpFunc
from direct.showbase.Transitions import Transitions
from direct.actor.Actor import Actor
from personnages import *
import os, sys


class Portail(CollisionBox):
	def __init__(self, center=(10, -130, 6), sx=3, sy=3, sz=3, newpos=(-36, 12, 6)):
		CollisionBox.__init__(self, center, sx, sy, sz)
		self.newpos = newpos
		self.setTangible(False)
		
class SetLevel(FSM):
	def __init__(self):
		FSM.__init__(self, "LevelManager")
		self.ok = False    
		self.reading = False    
		self.termine = True
		self.image = None
		self.map = None
		self.player = None
		self.debug = False
		self.music = None
		self.current_pnj = None #Variable nous indiquant quel pnj on touche
		self.currents_pnj = [] #Liste dans laquelle sont stockés ous les pnjs de la map
		#------------------Notre gestionnaire de collisions-------------------------
		self.antimur = CollisionHandlerPusher()
		self.antimur.addInPattern("into")
		self.antimur.addOutPattern("out")
		self.chapitre = 0
		self.coord = [0, 0, 0]
		self.current_map = "Village.bam"
		self.donnees = {"Village.bam":("../sounds/legende.ogg", ["Taya"], {})}
		self.texts = ["It's a secret to everybody."]
		self.dialogues_pnj = {"error":["I am Error.", "And you, what's your name ?"], "Taya":["Hello young boy !", "I am the bitch of this village.", "It will be 300$ the night !"]}
		self.text_index = 0
		self.letter_index = 0
		self.messages = []
		self.nom = "Link"
		self.read()
		self.transition = Transitions(loader)
		base.taskMgr.add(self.update_text, "update_text")
		self.accept("space", self.check_interact)
		self.accept("escape", sys.exit)
		
	#-----------------------Fonction de mises à jour (nécessaires pour l'affichage des textes...)----------------------------------	
	def check_interact(self):
		if not self.reading and not self.termine:
			self.reading = True
		elif self.reading:
			if self.letter_index >= len(self.texts[self.text_index]):
				self.text_index += 1
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
				else:
					self.letter_index = 0
			else:
				self.letter_index = len(self.texts[self.text_index])
		else:
			if self.current_pnj is not None:
				if self.current_pnj in self.dialogues_pnj:
					self.set_text(self.dialogues_pnj[self.current_pnj])	
					self.text_index = 0
					self.letter_index = 0	 
				
				
	def set_text(self, text, messages=[]):
		if not self.reading:
			self.reading = True
			self.termine = False
			self.texts = text
			self.messages = messages		
			
	def update_text(self, task):
		if self.reading:
			if self.ok:
				self.textObject.removeNode()
				self.dialog_box.removeNode()
				del self.textObject
				del self.dialog_box
			else:
				self.ok = True
			self.dialog_box = OnscreenImage("../pictures/dialog_box.png", scale=Vec3(1.2, 0, 0.15), pos=Vec3(0, 0, -0.75))
			self.dialog_box.setTransparency(TransparencyAttrib.MAlpha)
			self.textObject = OnscreenText(text=self.texts[self.text_index][0:self.letter_index], pos=(0, -0.75), scale=0.07)
			if self.letter_index < len(self.texts[self.text_index]):
				self.letter_index += 1
		return task.cont  
		
	#-------------Fonction de chargement de map--------------------------------
	
	
	def load_map(self, map="environment"):
		"""
		Fonction qui nous permet de charger une map
		-------------------------------------------
		map -> str
		return -> None
		"""
		for pnj in self.currents_pnj:
			pnj.cleanup()
			pnj.removeNode()
			del pnj
		self.current_pnj = None
		#-------Section de gestion de la map en elle-même-----
		self.current_map = map
		if self.map:
			self.map.removeNode()
			del self.map
		self.map = loader.loadModel(map)			
		self.map.reparentTo(render)	
		#-----Section de gestion de la musique------
		if self.music is not None:
			self.music.stop()
			self.music = None
		self.music = base.loader.loadSfx(self.donnees[self.current_map][0])
		self.music.setLoop(True)
		self.music.play()
		#--------------------LUMIERES--------------------------------------------
		"""alight = AmbientLight("alight")
		alnp = render.attachNewNode(alight)
		render.set_light(alnp)"""
		#---------------------NOTRE HEROS ET SA CAMERA-------------------------------------
		if self.player is None:
			self.player = Player()
			self.player.setPos(self.coord[0], self.coord[1], self.coord[2])
			self.player.reparentTo(render)
			self.player.set_active(True)
		#--------Section de gestion des pnjs--------
		for p in self.donnees[self.current_map][1]:
			if p == "Taya":
				t = Taya()
				t.reparentTo(render)
				self.currents_pnj.append(t)
			else:
				pnj = PNJ(p)
				pnj.setPos(10, -150, 3)
				pnj.reparentTo(render)
				self.currents_pnj.append(pnj)
		#---------------------------SECTION DE GESTION DES COLLISIONS------------------
		self.map.setCollideMask(BitMask32.bit(0))
		if self.debug:
			base.cTrav.showCollisions(render)
		self.antimur.addCollider(self.player.col_np, self.player)
		base.cTrav.addCollider(self.player.col_np, self.antimur)	
		#----------Les triggers-----------------------
		for portail in self.donnees[self.current_map][2]:
			noeud = CollisionNode(portail)
			solid = self.donnees[self.current_map][2][portail]
			noeud.addSolid(solid) 
			noeud.setCollideMask(BitMask32.bit(0)) 
			noeud_np = self.map.attachNewNode(noeud)
		if self.debug:
			self.player.set_active(False)
			base.enableMouse()
		else:
			self.player.set_active(True)
			base.disableMouse()		
		self.transition.fadeIn(2)	
					
	#---------------------------Ecran titre--------------------------------			
	def enterMenu(self):
		self.music = base.loader.loadSfx("../sounds/menu.ogg")
		self.music.setLoop(True)
		self.music.play()
		self.menu = True
		font = loader.loadFont("arial.bam")
		self.textObject1 = OnscreenText(text='The legend of Therenor 3D', pos=(0, 0.75), scale=0.07, fg=(255, 255, 255, 255))
		self.textObject1.setFont(font)
		self.textObject2 = OnscreenText(text='Appuyez sur F1 pour commencer', pos=(0, 0.5), scale=0.07, fg=(255, 255, 255, 255))
		self.textObject2.setFont(font)
		self.epee = loader.loadModel("sword.bam")
		self.epee.reparentTo(render)
		base.cam.lookAt(self.epee)
		self.epee.setPosHprScale(0.00, 5.00, 0.00, 0.00, 270, 90.00, 1.00, 1.00, 1.00)
		interval = self.epee.hprInterval(2, Vec3(0, 270, 90), startHpr = Vec3(0, 270, 0))
		interval2 = self.epee.hprInterval(2, Vec3(0, 270, 180), startHpr = Vec3(0, 270, 90))
		interval3 = self.epee.hprInterval(2, Vec3(0, 270, 270), startHpr = Vec3(0, 270, 180))
		interval4 = self.epee.hprInterval(2, Vec3(0, 270, 0), startHpr = Vec3(0, 270, 270))
		s = Sequence(interval, interval2, interval3, interval4)
		s.loop()	
		self.accept("f1", self.verify)
		self.accept("r", self.save, [True])
		
	def exitMenu(self):
		self.music.stop()
		self.textObject1.remove_node()	
		self.textObject2.remove_node()	
		self.epee.remove_node()	
	
	def verify(self):
		self.ignore("f1")
		self.ignore("r")
		if self.chapitre == 0:
			self.request("Init")
		elif self.chapitre == 1:
			self.request("Legende")	
		elif self.chapitre == 2:
			self.transition.fadeOut(2)
			Sequence(LerpFunc(self.music.setVolume, fromData = 1, toData = 0, duration = 2)).start()
			taskMgr.doMethodLater(2, self.on_change, "on change")
	#-------------------------------Paramètres en début de partie-----------------------------------
	def enterInit(self):
		self.music = base.loader.loadSfx("../sounds/para.ogg")
		self.music.setLoop(True)
		self.music.play()
		self.nameEnt = DirectEntry(scale = 0.08, pos = Vec3(-0.4, 0, 0.15), width = 10)
		self.nameLbl = DirectLabel(text = "Salutations jeune aventurier, quel est ton nom ?", pos = Vec3(0, 0, 0.4), scale = 0.1, textMayChange = 1, frameColor = Vec4(1, 1, 1, 1))
		self.helloBtn = DirectButton(text = "Confirmer", scale = 0.1, command = self.setName, pos = Vec3(0, 0, -0.1))
			
	def exitInit(self):
		self.music.stop()
		self.chapitre = 1
		self.save()

	def setName(self):
		self.acceptDlg = YesNoDialog(text = "C'est tout bon ?", command = self.acceptName)

	def acceptName(self, clickedYes):
		self.acceptDlg.cleanup()
		if clickedYes:
			self.nom = self.nameEnt.get()
			self.nameLbl.removeNode()        
			del self.nameLbl
			self.helloBtn.removeNode()        
			del self.helloBtn
			self.nameEnt.removeNode()        
			del self.nameEnt
			self.request("Legende")		
	#-------------------------------Introduction avec la légende--------------------------------------		
	def enterLegende(self):
		self.music = base.loader.loadSfx("../sounds/legende.ogg")
		self.music.setLoop(True)
		self.music.play()
		self.set_text(["Il existe une légende...", "Une légende racontant...", "...qu'il y a bien longtemps prospérait un royaume.", "Ce royaume légendaire vivait paisiblement.", "Jusqu'au jour où...", "...une hydre maléfique du nom de Zmeyevick arriva.",  "Elle terrorisa le bon peuple du royaume.", "Mais...alors que tout semblait perdu...", "Un jeune homme courageux apparu et terrassa l'hydre.",
		"Il la scella et repartit pour de lointaines contrées.", "Malgré le fait que le héros ait disparu, on murmure encore son nom...", "Et l'on dit qu'un jour...",  "il se réincarnera et protégera le monde d'un nouveau fléau."], ["Bz"])
		self.accept("Bz", self.change_legende)
		base.taskMgr.add(self.change_legende_image, "change_legende_image")
		
	def exitLegende(self):
		self.music.stop()	
		self.chapitre = 2
		
	def change_legende(self):
		self.transition.setFadeColor(0, 0, 0)
		self.transition.fadeOut(2)	
		taskMgr.doMethodLater(2, self.on_change, "on change")
		self.chapitre = 2
		self.save()
		
	def on_change(self, task):
		self.current_map = "Village.bam"
		self.request("Map")
		return task.done
	
	def fade_in(self, task):
		self.transition.fadeIn(2)
		return task.done	
		
	def change_legende_image(self, task):
		if self.text_index == 8:
			if not self.image:
				self.image = OnscreenImage("../pictures/la_legende.png", scale=Vec3(1.5, 0, 1), pos=Vec3(0, 0, 0))
		if self.text_index == 11:
			if self.image != None:
				self.image.removeNode()
				self.image = None	
		if self.text_index > 11:
			return task.done
		return task.cont	 
		
	#---------------------------------Boucle de jeu "normale"----------------------------------------------------------------	
	
	def enterMap(self):
		base.cTrav = CollisionTraverser()
		self.load_map(self.current_map)
		#------------------------GESTION DES INPUT----------------------------
		taskMgr.add(self.update, "update")
		self.accept("arrow_up", self.heroswalk)
		self.accept("arrow_up-up", self.herosstop)
		self.accept("arrow_down", self.heroswalki)
		self.accept("arrow_down-up", self.herosstopi)
		self.accept("arrow_left", self.beginleft)
		self.accept("arrow_left-up", self.endleft)
		self.accept("arrow_right", self.beginright)
		self.accept("arrow_right-up", self.endright)
		self.accept("b", self.augmente_vitesse)
		self.accept("b-up", self.diminue_vitesse)
		self.accept("a", self.player.followcam.change_vue)	
		self.accept("into", self.into)
		self.accept("out", self.out)
		
	def into(self, a):
		b = str(a.getIntoNodePath()).split("/")[len(str(a.getIntoNodePath()).split("/"))-1]
		if b[0:len(b)-7] in self.donnees[self.current_map][1]:
			self.current_pnj = b[0:len(b)-7]
		elif b in self.donnees[self.current_map][2]:
			self.transition.fadeOut(0.5)
			self.player.setPos(self.donnees[self.current_map][2][b].newpos)
			self.load_map(b)
			
	def out(self, a):
		self.current_pnj = None		
		
	def heroswalk(self):
		self.player.walk = True
		self.player.loop("walk")
		
	def herosstop(self):
		self.player.walk = False
		self.player.stop()	
		
	def heroswalki(self):
		self.player.reverse = True
		self.player.loop("walk")
		
	def herosstopi(self):
		self.player.reverse = False
		self.player.stop()	
		
	def beginleft(self):
		self.player.left = True
		
	def beginright(self):
		self.player.right = True	
		
	def endleft(self):
		self.player.left = False
	
	def endright(self):
		self.player.right = False				
			
	def augmente_vitesse(self):
		self.player.vitesse *= 2
		
	def diminue_vitesse(self):
		self.player.vitesse /= 2
					
	def update(self, task):
		if self.player.walk:
			self.player.setY(self.player, -self.player.vitesse)
		if self.player.reverse:
			self.player.setY(self.player, self.player.vitesse)
		if self.player.right:
			self.player.setH(self.player, -self.player.vitesse*2)
		if self.player.left:
			self.player.setH(self.player, self.player.vitesse*2)	
		return task.cont	
			   	
	def exitMap(self):
		print("Indéfini pour le moment")		
	#----------------------------------Partie pour le generique--------------------------------------------------------------------------
	def enterGenerique(self):
		self.music = loader.loadSfx("../sounds/generique.ogg")
		self.music.setLoop(True)
		self.music.play()
		self.texts_gen = [OnscreenText("Programming : ", pos=(0, -1.5), scale=(0.15, 0.15, 0.15), fg=(1, 0, 0, 1)),
		OnscreenText("Etienne Pacault       Rémi Martinot", pos=(0, -2), scale=(0.1, 0.1, 0.1), fg=(1, 1, 1, 1)),
		OnscreenText("Noé Mora              Tyméo Bonvicini-Renaud", pos=(0, -2.25), scale=(0.1, 0.1, 0.1), fg=(1, 1, 1, 1)),
		OnscreenText("Alexandrine Charette", pos=(0, -2.5), scale=(0.1, 0.1, 0.1), fg=(1, 1, 1, 1)),
		OnscreenText("3D models :", pos=(0, -3.5), scale=(0.15, 0.15, 0.15), fg=(0.65, 0.4, 0, 1)),
		OnscreenText("Etienne Pacault", pos=(0, -4), scale=(0.1, 0.1, 0.1), fg=(1, 1, 1, 1)),
		OnscreenText("Special thanks to :", pos=(0, -5), scale=(0.15, 0.15, 0.15), fg=(1, 1, 0, 1)),
		OnscreenText("Shigeru Miyamoto and Eiji Aonuma", pos=(0, -5.5), scale=(0.1, 0.1, 0.1), fg=(1, 1, 1, 1)),
		OnscreenText("for The legend of Zelda which has us inspired", pos=(0, -5.75), scale=(0.1, 0.1, 0.1), fg=(1, 1, 1, 1)),
		OnscreenText("Special thanks to Aimeline Cara", pos=(0, -6), scale=(0.1, 0.1, 0.1), fg=(1, 1, 1, 1)),
		OnscreenText("The Carnegie Mellon University who update the Panda 3D source code", pos=(0, -6.5), scale=(0.1, 0.1, 0.1), fg=(1, 1, 1, 1)),
		OnscreenText("Disney who has the great idea to create Panda 3D", pos=(0, -6.75), scale=(0.1, 0.1, 0.1), fg=(1, 1, 1, 1)),
		OnscreenText("...and to everyone we forgot...thank you ! :-)", pos=(0, -7), scale=(0.1, 0.1, 0.1), fg=(1, 1, 1, 1))]
		taskMgr.add(self.update_generique, "update generique")
		
	def exitGenerique(self):
		for text in self.texts_gen:
			text.removeNode()
			del text
		del self.texts_gen	
		self.music.stop()
		
	def change_to_menu(self, task):
		self.request("Menu")
		self.transition.fadeIn(2)
		Sequence(LerpFunc(self.music.setVolume, fromData = 0, toData = 1, duration = 2)).start()
		return task.done
		
	def update_generique(self, task):
		i = 0
		for text in self.texts_gen:
			i += 1
			text.setTextPos(text.getTextPos()[0], text.getTextPos()[1]+task.time/5000)
			if i == len(self.texts_gen) -1:
				if text.getTextPos()[1] > 2:
					taskMgr.doMethodLater(2, self.change_to_menu, "change to menu")
					self.transition.fadeOut(2)
					Sequence(LerpFunc(self.music.setVolume, fromData = 1, toData = 0, duration = 2)).start()
					return task.done
		return task.cont	
				
    #---------------------------------Fonctions de traitement des données de sauvegarde.--------------------------------------------------
	def save(self, reset=False):
		"""
		Fonction qui permet de sauvegarder les données de la partie.
		------------------------------------------------------------
		return -> None
		"""	
		if reset:
			self.chapitre = 0
			self.nom = "Link"
			self.current_map = "Village.bam"
			self.coord = [0, 0, 0]
		file = open("save.txt", "wt")
		info = [self.nom, str(self.chapitre), self.current_map]
		if self.player:
			info += [str(self.player.getX()), str(self.player.getY()), str(self.player.getZ())]
		else:
			info += ["0", "0", "0"]	
		file.writelines([donnee +"|" for donnee in info])
		file.close()
		

	
	def read(self):
		"""
		Fonction qui permet de lire les données préalablement enregistrées.
		-------------------------------------------------------------------
		return -> None
		"""	
		if os.path.exists("save.txt"):
			file = open("save.txt", "rt")
			i = 0
			for truc in file.read().split("|"):
				i += 1
				if i == 1:
					self.nom = truc
				elif i == 2:
					self.chapitre = int(truc)
				elif i == 3:
					self.current_map = truc
				elif i == 4:
					self.coord[0] = (float(truc))
				elif i == 5:
					self.coord[1] = (float(truc))
				elif i == 6:
					self.coord[2] = (float(truc))				
			file.close()
		else:
			file = open("save.txt", "wt")
			file.writelines(["Link|0|environment|0|0|0"])
			file.close()	

class Application(ShowBase):
	"""
	Classe principale, celle du jeu
	"""
	def __init__(self):
		loadPrcFile("config.prc")
		ShowBase.__init__(self)
		base.set_background_color(0, 0, 0, 0)
		self.set_level = SetLevel()
		base.disableMouse()
		self.set_level.request("Menu")
		
	
			
				
			
