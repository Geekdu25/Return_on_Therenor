from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
"""
Fichier gérant la classe FollowCam, une classe qui fait en sorte que la caméra suiv toujours le joueur.
"""
class FollowCam():
	"""
	Notre classe FollowCam.
	"""
	def __init__(self, camera, target):
		self.dummy = render.attachNewNode("cam" + target.getName())
		self.turnRate = 2.2
		self.vue = 0
		self.camera = camera
		self.active = True
		camera.node().getLens().setFov(120)
		self.target = target
		taskMgr.add(self.updateCamera, "updateCamera" + target.getName())

	def change_vue(self):
		"""
		Fonction qui permet de passer de la vue à la première personne à une vue à la troisième personne (et vice-versa).
		---------------------------------------------
		return -> None
		"""
		if self.vue == 0:
			self.vue = 1
		else:
			self.vue = 0	
			
	def set_active(self, active=False):
		"""
		Fonction qui se met à suivre le joueur ou arrête de le suivre.
		----------------------------------------------------
		active -> bool
		return -> None
		"""
		if active:
			self.active = True
			base.cam.node().getLens().setFov(120)
			taskMgr.add(self.updateCamera, "updateCamera" + self.target.getName())
		else:
			self.active = False
			taskMgr.remove("updateCamera")			

	def updateCamera(self, task):
		"""
		Fonction qui met à jour l'emplacement de la caméra.
		-------------------------------------------------
		task -> task
		return -> task.cont
		"""
		if self.vue == 0:
			self.dummy.setPos(self.target.getPos())
			self.dummy.setZ(self.dummy, 20)
			self.dummy.setY(self.dummy, 15)
			heading = self.clampAngle(self.dummy.getH())
			turnDiff = self.target.getH() - heading
			turnDiff = self.clampAngle(turnDiff)
			dt = globalClock.getDt()
			turn = turnDiff * dt
			self.dummy.setH(heading + turn * self.turnRate)
			self.camera.setPos(self.dummy.getPos())
			self.camera.setY(self.dummy, 40)
			self.camera.setZ(self.dummy, 25)
			self.camera.lookAt(self.target.getPos() + Vec3(0, 0, 20))
		elif self.vue == 1:
			self.camera.setPos(self.target.getPos())
			self.camera.setY(self.camera, 5)
			self.camera.setZ(self.camera, 80)
			self.camera.lookAt(self.camera.getPos() + Vec3(0, -10, 0))
			self.camera.setH(self.target.getH()+180)
		return task.cont

	def clampAngle(self, angle):
		"""
		Fonction qui permet d'ajuster un angle de sorte à ce qu'il soit compris entre -180 et 180 degrés.
		------------------------------------------------------------------------------
		angle -> float
		return -> float
		"""
		while angle < -180:
			angle = angle + 360
		while angle > 180:
			angle = angle - 360
		return angle

class ManetteCam():
	def __init__(self, camera, target):
		self.camera = camera
		self.target = target
		self.dummy = self.target.attachNewNode("cam" + target.getName())
		self.dummy.setZ(self.dummy, 0.25)
		self.dummy.setH(270)
		self.camera.reparentTo(self.dummy)
		self.camera.setPos(self.camera, Vec3(-2, 0, 0))
		self.active = True
		self.vue = True
		camera.node().getLens().setFov(120)
		taskMgr.add(self.update_camera, "updateCamera")
		
	def change_vue(self):
		if self.vue:
			self.vue = False
			self.dummy.setH(270)
			self.camera.setPos(self.dummy, Vec3(0, 0, 0))
		else:
			self.vue = True	
			self.dummy.setH(180)
			self.camera.setPos(self.camera, Vec3(-2, 0, 0))	
			
	def set_active(self, active=True):
		self.active = active
		if self.active:
			taskMgr.add(self.update_camera, "updateCamera")	
		else:
			taskMgr.remove("updateCamera")		
			
	def	update_camera(self, task):
		"""
		Fonction de mise à jour de la caméra.
		"""
		self.camera.lookAt(self.dummy)
		return task.cont
		
	def recenter(self):
		if self.vue:
			self.dummy.setPos((0, 0, 0.25))
			self.dummy.setHpr((270, 0, 0))
			self.camera.setPos((-2, 0, 0))	
			self.camera.setHpr((0, 0, 0))
		else:
			self.dummy.setPos((0, 0, 0.25))
			self.dummy.setHpr((180, 0, 0))
			self.camera.setPos((0, 0, 0))	
			self.camera.setHpr((0, 0, 0))	
		
	def move(self, direction="up", time=0.1):
		if self.vue:
			if direction == "up":
				if self.dummy.getR() < 30:
					self.dummy.setR(self.dummy, time*50)
			elif direction == "down":
				if self.dummy.getR() > -30:
					self.dummy.setR(self.dummy, -time*50)
			elif direction == "left":
				save_r = self.dummy.getR()
				self.dummy.setR(0)
				self.dummy.setH(self.dummy, -time*50)
				self.dummy.setR(save_r)
			else:
				save_r = self.dummy.getR()
				self.dummy.setR(0)
				self.dummy.setH(self.dummy, time*50)
				self.dummy.setR(save_r)			
		else:
			if direction == "up":
				if self.dummy.getP() < 30:
					self.dummy.setP(self.dummy, time*50)
			elif direction == "down":
				if self.dummy.getP() > -30:
					self.dummy.setP(self.dummy, -time*50)
			elif direction == "left":
				self.target.setH(self.target, time*50)
			else:
				self.target.setH(self.target, -time*50)		
