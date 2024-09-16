from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3

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
