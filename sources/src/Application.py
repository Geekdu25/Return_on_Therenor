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
from personnages import *
from monsters import *
from objects import *
import os, sys, json


class Portail(CollisionBox):
	"""
	Pour faire simple, un portail est un solide de collision invisible qui téléporte le joueur dès qu'il le touche.
	"""
	def __init__(self, center=(1320, -1000, 6), sx=40, sy=4, sz=150, newpos=(830, -470, 6)):
		CollisionBox.__init__(self, center, sx, sy, sz)
		self.newpos = newpos
		self.setTangible(False)
		
class Porte(CollisionBox):
	"""
	Contrairement à un portail, une porte doit être ouverte par le joueur en appuyant sur espace pour le téléporter.
	"""
	def __init__(self, center=(1320, -1000, 6), sx=50, sy=10, sz=150, newpos=(830, -460, 6)):
		CollisionBox.__init__(self, center, sx, sy, sz)
		self.newpos = newpos
		
class SetLevel(FSM):
	"""
	Partez du principe que cette classe sera le coeur du jeu.
	Tout le script principal s'y trouvera.
	"""
	def __init__(self):
		FSM.__init__(self, "LevelManager") #Initialisation de botre classe en initialisat la super classe.
		base.cTrav = CollisionTraverser() #Notre gestionnaire de collisions.
		base.cTrav.setRespectPrevTransform(True)
		#base.cTrav.showCollisions(render)
		self.ok = False    
		self.reading = False    
		self.termine = True
		self.image = None
		self.map = None
		self.player = None
		self.debug = False
		self.music = None #La musique d'ambiance
		self.son = None #Le son joué lors des dialogues.
		self.current_pnj = None #Variable nous indiquant quel pnj on touche
		self.pnjs = [] #Liste dans laquelle sont stockés ous les pnjs de la map
		self.current_porte = None #La porte actuellement touchée par le joueur
		self.portails = {} #Dictionnaure contenant les portails.
		self.triggers = []
		self.antimur = CollisionHandlerPusher() #Notre Collision Handler, qui empêchera le joueur de toucher les murs et d'autres choses.
		self.antimur.addInPattern("into")
		self.antimur.addOutPattern("out")
		self.chapitre = 0 #Où en sommes-nous dans l'histoire ?
		self.player = Player() #Trèèèèèèèèès important : notre joueur?
		self.player.reparentTo(render)
		self.current_map = "Village.bam"
		self.texts = ["It's a secret to everybody."]
		self.dialogues_pnj = {"error":["I am Error.", "And you, what's your name ?"], "Taya":["Je crois bien que je suis la seule habitante de ce village..."]}
		self.font = loader.loadFont("arial.bam") #Notre police
		self.text_index = 0
		self.letter_index = 0
		self.messages = []
		self.sons_messages = []
		self.current_point = 1
		self.read()
		self.transition = Transitions(loader)
		base.taskMgr.add(self.update_text, "update_text")
		self.accept("space", self.check_interact)
		self.accept("escape", sys.exit)
		
	#-----------------------Fonction de mises à jour (nécessaires pour l'affichage des textes...)----------------------------------	
	def check_interact(self):
		"""
		Fonction appelée chaque fois que le joueur appuie sur espace.
		Cela aura pour conséquences de vérifier les portes, les pnjs touchés, ou encore de passer les dialogues.
		----------------------------------------------------------------------------------------------
		return -> None
		"""
		self.check_interact_dial()
		if self.current_pnj is not None:
			if self.current_pnj in self.dialogues_pnj:
				self.set_text(self.dialogues_pnj[self.current_pnj])	
				self.text_index = 0
				self.letter_index = 0
		if self.current_porte is not None:	
			self.transition.fadeOut(0.5)
			taskMgr.remove("update")
			self.player.walk = False
			self.player.reverse = False
			self.player.left = False
			self.player.right = False
			taskMgr.doMethodLater(0.45, self.player.setPos, "new_player_pos", extraArgs=[self.portails[self.current_porte].newpos])
			taskMgr.doMethodLater(0.5, self.load_map, "loadmap", extraArgs=[self.current_porte])			 
	
	def set_player_pos_later(self, newpos = (0, 0, 0)):
		self.player.setPos(newpos)
		
	def check_interact_dial(self):
		"""
		"Petite" fonction qui permet de passer les dialogues.
		------------------------------------------------------
		return -> None
		"""
		if not self.reading and not self.termine:
			self.reading = True
		elif self.reading:
			if self.letter_index >= len(self.texts[self.text_index]):
				self.text_index += 1
				if self.son is not None:
					self.son.stop()
					if len(self.sons_messages) > self.text_index:
						try:	
							self.son = loader.loadSfx(f"../sounds/dialogues/{self.sons_messages[self.text_index]}.ogg")
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
				else:
					self.letter_index = 0
			else:
				self.letter_index = len(self.texts[self.text_index])			
				
	def set_text(self, text=["Navi, where are thou ?"], messages=[], sons=[]):
		"""
		Fonction qui permet d'afficher un texte.
		--------------------------------------------------
		text -> list[str]
		messages -> list[str]
		sons -> list[str]
		return -> None
		"""
		if not self.reading:
			self.reading = True
			self.termine = False
			self.texts = text
			self.sons_messages = sons
			self.messages = messages
			if len(sons) > 0:
				try:
					self.son = loader.loadSfx(f"../sounds/dialogues/{self.sons_messages[0]}.ogg")		
					self.son.play()
				except:
					print("Pas de fichier son valide.")	
			
	def update_text(self, task):
		"""
		Fonction qui met à jour le texte affiché à l'écran.
		-------------------------------------------------
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
			self.dialog_box = OnscreenImage("../pictures/dialog_box.png", scale=Vec3(1.2, 0, 0.15), pos=Vec3(0, 0, -0.75))
			self.dialog_box.setTransparency(TransparencyAttrib.MAlpha)
			self.textObject = OnscreenText(text=self.texts[self.text_index][0:self.letter_index], pos=(0, -0.75), scale=0.07)
			if self.letter_index < len(self.texts[self.text_index]):
				self.letter_index += 1
		return task.cont  
		
	#-------------Fonction de chargement de map--------------------------------	
	
	def load_map(self, map="maison_terenor.bam", task=None):
		"""
		Fonction qui nous permet de charger une map
		-------------------------------------------
		map -> str
		return -> None
		"""
		for pnj in self.pnjs:
			pnj.cleanup()
			pnj.removeNode()
			del pnj
		self.current_pnj = None
		self.current_porte = None
		self.pnjs = []
		self.portails = {}
		#-------Section de gestion de la map en elle-même-----
		self.current_map = map
		if self.map:
			self.map.removeNode()
			del self.map
		self.map = loader.loadModel(map)			
		self.map.reparentTo(render)	
		#-------------La skybox-----------------
		self.skybox = loader.loadModel("skybox.bam")
		self.skybox.setScale(10000)
		self.skybox.setBin('background', 1)
		self.skybox.setDepthWrite(0)
		self.skybox.setLightOff()
		self.skybox.reparentTo(render)
		#--------------------Chargement du fichier json-------------
		pnj_file = open("../json/data.json")
		data = json.load(pnj_file)
		pnj_file.close()	
		#-----Section de gestion de la musique------
		if self.music is not None:
			self.music.stop()
			self.music = None
		self.music = base.loader.loadSfx(data[self.current_map][0])
		self.music.setLoop(True)
		self.music.play()
		#---------------------NOTRE HEROS ET SA CAMERA-------------------------------------
		if self.player.followcam is None:
			self.player.create_camera()
		#---------------------------SECTION DE GESTION DES COLLISIONS------------------
		self.map.setCollideMask(BitMask32.bit(0))
		if self.debug:
			base.cTrav.showCollisions(render)
		self.antimur.addCollider(self.player.col_np, self.player)
		base.cTrav.addCollider(self.player.col_np, self.antimur)	
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
			if pnj == "Taya":
				a = Taya()
				a.setPos(info[0], info[1], info[2])
				self.pnjs.append(a)
			else:
				a = PNJ(pnj)
				a.setPos(info[0], info[1], info[2])
				self.pnjs.append(a)	
		self.load_triggers(map)		
		if self.debug:
			base.enableMouse()
		else:
			base.disableMouse()	
		self.accept("escape", sys.exit)	
		self.accept("arrow_up", self.touche_pave, extraArgs=["arrow_up"])
		self.accept("arrow_up-up", self.touche_pave, extraArgs=["arrow_up-up"])
		self.accept("arrow_down", self.touche_pave, extraArgs=["arrow_down"])
		self.accept("arrow_down-up", self.touche_pave, extraArgs=["arrow_down-up"])
		self.accept("arrow_left", self.touche_pave, extraArgs=["arrow_left"])
		self.accept("arrow_left-up", self.touche_pave, extraArgs=["arrow_left-up"])
		self.accept("arrow_right", self.touche_pave, extraArgs=["arrow_right"])
		self.accept("arrow_right-up", self.touche_pave, extraArgs=["arrow_right-up"])
		self.accept("a", self.player.followcam.change_vue)	
		self.accept("b", self.change_vitesse, extraArgs=["b"])
		self.accept("b-up", self.change_vitesse, extraArgs=["b-up"])
		self.accept("into", self.into)
		self.accept("out", self.out)
		self.accept("e", self.inventaire)	
		taskMgr.add(self.update, "update")	
		del data
		self.transition.fadeIn(2)
		if task is not None:
			return task.done	
					
	def load_triggers(self, map="Village.bam"):
		"""
		Fonction dans laquelle on rentre toutes les instructions sur nos triggers.
		C'est à dire les collisions "scénaristiques".
		------------------------------------------------------
		map -> str
		return -> None
		"""
		for trigger in self.triggers: 
			del trigger
		if map == "Village.bam":
			noeud = CollisionNode("1")
			solid = CollisionBox((1780, -5450, 10), 350, 25, 60)
			solid.setTangible(False)
			noeud.addSolid(solid)
			noeud.setIntoCollideMask(BitMask32.bit(0))
			self.triggers.append(noeud) 
			chemin_de_noeud = render.attachNewNode(noeud)				
			
	#---------------------------Ecran titre--------------------------------			
	def enterMenu(self):
		"""
		Fonction qui prépare l'écran titre.
		------------------------------------------
		return -> None
		"""
		self.music = base.loader.loadSfx("../sounds/menu.ogg")
		self.music.setLoop(True)
		self.music.play()
		self.menu = True
		self.textObject1 = OnscreenText(text='The legend of Therenor 3D', pos=(0, 0.75), scale=0.07, fg=(1, 1, 1, 1))
		self.textObject1.setFont(self.font)
		self.textObject2 = OnscreenText(text='Appuyez sur F1 pour commencer', pos=(0, 0.5), scale=0.07, fg=(1, 1, 1, 1))
		self.textObject2.setFont(self.font)
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
		"""
		Fonction qui s'acive quand on quitte l'écran titre.
		"""
		self.music.stop()
		self.textObject1.remove_node()	
		self.textObject2.remove_node()	
		self.epee.remove_node()	
	
	def verify(self):
		"""
		Quand on quitte l'écran titre, on vérifira notre avancement dans l'histoire.
		On agira de différentes manières selon le chapitre auquel le joueur est rendu.
		---------------------------------------------------------------------------
		return -> None
		"""
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
		"""
		Fonction qui s'active quand on entre dans les paramètres en début de partie.
		----------------------------------------------------------------------------
		return -> None
		"""
		self.music = base.loader.loadSfx("../sounds/para.ogg")
		self.music.setLoop(True)
		self.music.play()
		self.nameEnt = DirectEntry(scale = 0.08, pos = Vec3(-0.4, 0, 0.15), width = 10)
		self.nameLbl = DirectLabel(text = "Salutations jeune aventurier, quel est ton nom ?", pos = Vec3(0, 0, 0.4), scale = 0.1, textMayChange = 1, frameColor = Vec4(1, 1, 1, 1))
		self.helloBtn = DirectButton(text = "Confirmer", scale = 0.1, command = self.setName, pos = Vec3(0, 0, -0.1))
			
	def exitInit(self):
		"""
		Fonction qui s'active quand on quitte ces paramètres.
		--------------------------------------------------------
		return -> None
		"""
		self.music.stop()
		self.chapitre = 1
		self.save()

	def setName(self):
		"""
		Petit pop-up de vérification.
		--------------------------------
		return -> None
		"""
		self.acceptDlg = YesNoDialog(text = "C'est tout bon ?", command = self.acceptName)

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
			self.request("Legende")		
	#-------------------------------Introduction avec la légende--------------------------------------		
	def enterLegende(self):
		"""
		Fonction au début de l'histoire lorsqu'on raconte la légende.
		-----------------------------------------------------------------
		return -> None
		"""
		self.music = base.loader.loadSfx("../sounds/legende.ogg")
		self.music.setLoop(True)
		self.music.play()
		self.set_text(["Il existe une légende...", "Une légende racontant...", "...qu'il y a bien longtemps prospérait un royaume.", "Ce royaume légendaire vivait paisiblement.", "Jusqu'au jour où...", "...une hydre maléfique du nom de Zmeyevick arriva.",  "Elle terrorisa le bon peuple du royaume.", "Mais...alors que tout semblait perdu...", "Un jeune homme courageux apparu et terrassa l'hydre.",
		"Il la scella et repartit pour de lointaines contrées.", "Malgré le fait que le héros ait disparu, on murmure encore son nom...", "Et l'on dit qu'un jour...",  "il se réincarnera et protégera le monde d'un nouveau fléau."], ["Bz"], ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"])
		self.accept("Bz", self.change_legende)
		base.taskMgr.add(self.change_legende_image, "change_legende_image")
		
	def exitLegende(self):
		"""
		Fonction lorsque la légende est finie.
		-------------------------------------
		return -> None
		"""
		self.music.stop()	
		self.chapitre = 2
		
	def change_legende(self):
		"""
		Fonction s'acivant quand la légende est finie.
		-----------------------------------------------
		return -> None
		"""
		self.transition.setFadeColor(0, 0, 0)
		self.transition.fadeOut(2)	
		taskMgr.doMethodLater(2, self.on_change, "on change")
		self.chapitre = 2
		self.save()
		
	def on_change(self, task):
		"""
		Fonction appelée deux secondes près la fin de la légende qui charge la map.
		----------------------------------------------------
		task -> task
		return -> task.done
		"""
		self.current_map = "maison_terenor.bam"
		self.request("Map")
		return task.done
	
	def fade_in(self, task):
		"""
		Fonction qui permet de faire des fade in plus tard.
		----------------------------------------------------
		task -> task
		return -> task.done
		"""
		self.transition.fadeIn(2)
		return task.done	
		
	def change_legende_image(self, task):
		"""
		Fonction qui en fonction de l'avancement dans la légende change l'image en background.
		-----------------------------------------------------------------------------------
		task -> task
		return -> task.cont ou task.done
		"""
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
		"""
		Fonction s'activant quand on souhaite charger la map.
		-----------------------------------------------------
		return -> None
		"""
		self.coeurs_vides = []
		self.coeurs_moitie = []
		self.coeur_pleins = []
		x = -1.2
		for loop in range(10):
			self.coeurs_vides.append(OnscreenImage("../pictures/vie_lost.png", scale=Vec3(0.05, 0.05, 0.05), pos=Vec3(x, 1, 0.9)).setTransparency(TransparencyAttrib.MAlpha))
			x += 0.12
		x = -1.2	
		for loop in range(10):
			self.coeurs_pleins.append(OnscreenImage("../pictures/vie_full.png", scale=Vec3(0.05, 0.05, 0.05), pos=Vec3(x, 1, 0.9)).setTransparency(TransparencyAttrib.MAlpha))
			x += 0.12	
		x = -1.2
		for loop in range(10):
			self.coeurs_moitie.append(OnscreenImage("../pictures/vie_half.png", scale=Vec3(0.05, 0.05, 0.05), pos=Vec3(x, 1, 0.9)).setTransparency(TransparencyAttrib.MAlpha))
			x+= 0.12
		if self.player.vies > self.player.maxvies:
			self.player.vies = self.player.maxvies
		elif self.player.vies <= 0:
			self.transition.fadeOut(0.5)
			taskMgr.doMethodLater(1, self.launch_game_over, "request")	
		self.noai_text = OnscreenText(text=f"Noaïs : {int(self.player.noais)}", pos=(-1, 0.7), scale=0.07, fg=(1, 1, 1, 1))	
		self.noai_image = OnscreenImage("../pictures/noai.png", scale=Vec3(0.07, 0, 0.07), pos=Vec3(-1.23, 0, 0.72))
		self.noai_image.setTransparency(TransparencyAttrib.MAlpha)
		self.map_image = OnscreenImage("../pictures/carte_Terenor.png", scale=Vec3(0.8, 0, 0.8), pos=Vec3(0, 0, 0))
		self.croix_image = OnscreenImage("../pictures/croix.png", scale=Vec3(0.04, 0, 0.04), pos=Vec3(0, 0, 0))
		self.croix_image.setTransparency(TransparencyAttrib.MAlpha)
		self.lieu_text = OnscreenText(text="???", pos=(0, 0.65), scale=0.1, fg=(1, 1, 1, 1))
		self.load_map(self.current_map)
		
	def into(self, a):
		"""
		Fonction s'activant quand le joueur ou un autre objet from, touche un objet into.
		-------------------------------------------------------
		a -> entry (une info sur la collision)
		return -> None
		"""
		b = str(a.getIntoNodePath()).split("/")[len(str(a.getIntoNodePath()).split("/"))-1]
		if b in self.pnjs:
			self.current_pnj = b
		elif b in self.portails:
			if type(self.portails[b]) is Portail:
				self.transition.fadeOut(0.5)
				self.player.setPos(self.portails[b].newpos)
				taskMgr.doMethodLater(0.5, self.load_map, "loadmap", extraArgs=[b])
			elif type(self.portails[b]) is Porte:
				self.current_porte = b
		elif b.isdigit():
			b = int(b)
			if b == 1:
				if not "epee" in self.player.inventaire:
					taskMgr.remove("update")
					self.player.stop()
					s = Sequence(Func(self.player.loop, "walk"), self.player.posInterval(1.5, Vec3(self.player.getX(), self.player.getY()+30, self.player.getZ()), startPos=Vec3(self.player.getX(), self.player.getY(), self.player.getZ())), Func(self.player.stop), Func(taskMgr.add, self.update, "update"), Func(self.ignore, "finito"))
					self.set_text(["Non...", "Je n'ai pas encore d'épée.", "Je dois aller en acheter une chez le forgeron du village."], messages=["finito"])	
					self.accept("finito", s.start)	
	
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
		self.current_pnj = None	
		self.current_porte = None	
		
	def touche_pave(self, message="arrow_up"):
		if message == "arrow_up":
			self.player.walk = True
			self.player.loop("walk")
		elif message == "arrow_up-up":  
			self.player.walk = False
			self.player.stop()	
		elif message == "arrow_down":  
			self.player.reverse = True
			self.player.loop("walk")
		elif message == "arrow_down-up":	
			self.player.reverse = False
			self.player.stop()
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
                                        for loop in range(self.player.vies+1):
                                                self.coeurs_moitie[loop].show()
		for loop in range(self.player.vies):
                                        self.coeurs_pleins[loop].show()
		#-----------------------Section mouvements du joueur------------------------
		if self.player.getZ() > 50: 
		  self.player.setZ(self.player, -0.25)
		else:
		  self.player.setZ(10)  
		if self.player.walk:
			self.player.setY(self.player, -self.player.vitesse*globalClock.getDt())
		if self.player.reverse:
			self.player.setY(self.player, self.player.vitesse*globalClock.getDt())
		if self.player.right:
			self.player.setH(self.player, -self.player.vitesse*2*globalClock.getDt())
		if self.player.left:
			self.player.setH(self.player, self.player.vitesse*2*globalClock.getDt())	
		return task.cont	
			   	
	def exitMap(self):
		"""
		Fonction appelée quand on quitte la map
		"""
		self.map.removeNode()
		self.map = None	
		self.player.left = False
		self.player.right = False
		self.player.reverse = False
		self.player.walk = False
		taskMgr.remove("update")
		self.ignore("arrow_up")
		self.ignore("arrow_up-up")
		self.ignore("arrow_down")
		self.ignore("arrow_down-up")
		self.ignore("arrow_left")
		self.ignore("arrow_left-up")
		self.ignore("arrow_right")
		self.ignore("arrow_right-up")
		self.ignore("a")	
		self.ignore("b")
		self.ignore("b-up")
		self.ignore("into")
		self.ignore("out")
		self.player.stop()
	#-----------------------Section de gestion de l'inventaire (et d'autres fonctions d'ui)--------------		
	def inventaire(self):
		"""
		Fonction utilisée pour ouvrir l'inventaire
		-------------------------------------------
		return -> None
		"""
		self.index_invent = 0		
		self.accept("arrow_left", self.change_index_invent, extraArgs=["left"])
		self.accept("arrow_right", self.change_index_invent, extraArgs=["right"])
		self.accept("escape", self.exit_inventaire)
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
		if self.current_map == "Village.bam" or self.current_map == "maison_taya.bam" or self.current_map == "maison_terenor.bam":
			return	Vec3(-0.06, 0, -0.625), "Village Toal"
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
                                    for coeur in self.coeur_vides:
                                        coeur.hide()    
		if self.index_invent == 0:
			self.map_image.show()
			self.croix_image.show()
			self.lieu_text.show()
		elif self.index_invent == 1:
			self.noai_image.show()
			self.noai_text.show()			
		return task.cont
		
	def exit_inventaire(self):
		"""
		Fonction appelée lorsqu'on qitte l'inventaire
		--------------------------------------------------
		return -> None
		"""
		self.music.setVolume(1)
		taskMgr.remove("update_invent")
		taskMgr.add(self.update, "update")
		self.accept("escape", sys.exit)	
		self.accept("arrow_up", self.touche_pave, extraArgs=["arrow_up"])
		self.accept("arrow_up-up", self.touche_pave, extraArgs=["arrow_up-up"])
		self.accept("arrow_down", self.touche_pave, extraArgs=["arrow_down"])
		self.accept("arrow_down-up", self.touche_pave, extraArgs=["arrow_down-up"])
		self.accept("arrow_left", self.touche_pave, extraArgs=["arrow_left"])
		self.accept("arrow_left-up", self.touche_pave, extraArgs=["arrow_left-up"])
		self.accept("arrow_right", self.touche_pave, extraArgs=["arrow_right"])
		self.accept("arrow_right-up", self.touche_pave, extraArgs=["arrow_right-up"])
		self.accept("a", self.player.followcam.change_vue)	
		self.accept("b", self.change_vitesse, extraArgs=["b"])
		self.accept("b-up", self.change_vitesse, extraArgs=["b-up"])
		self.accept("into", self.into)
		self.accept("out", self.out)
		self.accept("e", self.inventaire)
	#----------------------------------Partie pour le generique--------------------------------------------------------------------------
	def enterGenerique(self):
		"""
		Fonction activée quand on entre dans le générique.
		-------------------------------------------------
		return -> None
		"""
		self.music = loader.loadSfx("../sounds/generique.ogg")
		self.music.setLoop(True)
		self.music.play()
		self.texts_gen_1 = [("Programming : ", True), ("Tyméo Bonvicini-Renaud     Alexandrine Charette", False), ("Rémi Martinot     Noé Mora", False), ("Etienne Pacault", False),
		("Music :", True),  ("Etienne Pacault", False),
		("Special thanks to :", True), ("Aimeline Cara", False), ("The Carnegie Mellon University who updates the Panda 3D source code", False),
		("And thank you to everyone we probably forgot ! :-)", False)]
		colors = [(1, 0, 0, 1), (0.65, 0.4, 0, 1), (1, 1, 0, 1), (0, 1, 0.2, 1), (0, 0.5, 0, 1), (0, 0.8, 1, 1), (0, 0, 0.9, 1), (1, 0, 1, 1)]
		i_color = 0
		y = -1
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
			text.setTextPos(text.getTextPos()[0], text.getTextPos()[1]+globalClock.getDt()/5000)
			if i == len(self.texts_gen) -1:
				if text.getTextPos()[1] > 2:
					taskMgr.doMethodLater(2, self.change_to_menu, "change to menu")
					self.transition.fadeOut(2)
					Sequence(LerpFunc(self.music.setVolume, fromData = 1, toData = 0, duration = 2)).start()
					return task.done
		return task.cont	
		
	#-------------------------Fonctions gérant le game over---------------------------------------
	def launch_game_over(self, task):
		self.request("Game_over")
		return task.done
		
	def enterGame_over(self):
		render.node().removeAllChildren()
		render2d.node().removeAllChildren()
		self.player.vies = 3
		self.transition.fadeIn(0.5)
		self.text_game_over = OnscreenText("Game over", pos=(0, 0), scale=(0.2, 0.2), fg=(0.9, 0, 0, 1))
		self.text_game_over_2 = OnscreenText("Appuyez sur A pour recommencer", pos=(0, -0.2), scale=(0.1, 0.1), fg=(0.9, 0, 0, 1))
		self.accept("a", self.change_to_map)
	
	def change_to_map(self):
		self.request("Map")
		
	def exitGame_over(self):		
		self.text_game_over.removeNode()
		self.text_game_over_2.removeNode()
				
    #---------------------------------Fonctions de traitement des données de sauvegarde.--------------------------------------------------
	def save(self, reset=False):
		"""
		Fonction qui permet de sauvegarder les données de la partie.
		------------------------------------------------------------
		return -> None
		"""	
		if reset:
			self.chapitre = 0
			self.player.nom = "Link"
			self.current_map = "maison_terenor.bam"
		file = open("save.txt", "wt")
		info = [self.player.nom, str(self.chapitre), self.current_point, str(self.player.vies), str(self.player.maxvies)]
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
					self.player.nom = truc
				elif i == 2:
					self.chapitre = int(truc)
				elif i == 3:
					self.current_point = truc				
				elif i == 4:
					self.player.vies = float(truc)
				elif i == 5:
					self.player.maxvies = int(truc)		
			file.close()
		else:
			file = open("save.txt", "wt")
			file.writelines(["Link|0|maison_terenor.bam|1|3|3"])
			file.close()	

class Application(ShowBase):
	"""
	Classe principale, celle du jeu
	"""
	def __init__(self):
		loadPrcFile("config.prc")
		ShowBase.__init__(self)
		#PStatClient.connect()
		base.set_background_color(0, 0, 0, 0)
		self.set_level = SetLevel()
		base.disableMouse()
		self.set_level.request("Menu")
		
	
			
				
			
