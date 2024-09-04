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
			self.camera.setZ(self.camera, 45)
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
