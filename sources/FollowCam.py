from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class ManetteCam():
	def __init__(self, camera, target):
		self.camera = camera
		self.target = target
		self.dummy = self.target.attachNewNode("cam" + target.getName())
		self.dummy.setZ(self.dummy, 1)
		self.dummy.setH(180)
		self.camera.reparentTo(self.dummy)
		self.camera.setPos(self.camera, Vec3(0, -2, 0))
		self.active = True
		self.vue = True
		camera.node().getLens().setFov(100)
		self.camera_col_node = CollisionNode("Camera_collision")
		self.camera_col_node.addSolid(CollisionSphere((0, 0.2, 0), 0.75))
		self.camera_col_node.setFromCollideMask(BitMask32.bit(0))
		self.camera_col_node.setIntoCollideMask(BitMask32.allOff()) 
		self.camera_col_np = self.camera.attachNewNode(self.camera_col_node)
		self.camera_col_manager = CollisionHandlerEvent()
		self.camera_col_manager.addInPattern("dedans")
		self.camera_col_manager.addOutPattern("dehors")
		self.camera_col_manager.addAgainPattern("encore")
		base.accept("dedans", self.into)
		base.accept("dehors", self.out)
		base.accept("encore", self.again)
		base.cTrav.addCollider(self.camera_col_np, self.camera_col_manager)
		taskMgr.add(self.update_camera, "updateCamera")
		
	def change_vue(self):
		if self.vue:
			self.vue = False
			self.dummy.setHpr(180, 0, 0)
			self.camera.setPos(self.dummy, Vec3(0, 0, 0))
		else:
			self.vue = True	
			self.dummy.setHpr(180, 0, 0)
			self.camera.setPos(self.camera, Vec3(0, -2, 0))	
			
			
	def into(self, a):
		"""
		Fonction qui se déclenche quand la caméra touche quelque chose.
		"""
		pass
				
	def again(self, a):
		"""
		Fonction qui se déclenche lorsque la caméra continue de toucher quelque chose. 
		"""		
		pass
		"""dt = globalClock.getDt()
		if self.vue:
			if self.dummy.getP() > -30:
				self.dummy.setP(self.dummy, -30*dt)
				self.camera.setY(self.camera, 0.2*dt)"""
	
	def out(self, a):
		"""
		Fonction qui se déclenche quand la caméra arrête une collision
		"""	
		pass
		"""if self.vue:
			self.descend = True"""
		
		
	def set_active(self, active=True):
		self.active = active
		if self.active:
			taskMgr.add(self.update_camera, "updateCamera")	
			self.camera.reparentTo(self.dummy)
			self.camera.node().getLens().setFov(120)
			self.camera.setPos(self.camera, Vec3(0, -2, 0))
		else:
			taskMgr.remove("updateCamera")
			self.camera.reparentTo(render)		
			
	def	update_camera(self, task):
		"""
		Fonction de mise à jour de la caméra.
		"""
		dt = globalClock.getDt()
		self.camera.lookAt(self.dummy)
		"""if self.vue:
			if hasattr(self, "descend"):
				if self.descend:
					if self.dummy.getP() < 0:
						self.dummy.setP(self.dummy, 30*dt)
						self.camera.setY(self.camera, -2*dt)
					if self.dummy.getP() > 0:
						self.dummy.setP(self.dummy, 0)
						self.camera.setY(-2)
						self.descend = False"""	
		return task.cont
		
	def recenter(self):
		if self.vue:
			self.dummy.setPos((0, 0, 0.25))
			self.dummy.setHpr((180, 0, 0))
			self.camera.setPos((0, -2, 0))	
			self.camera.setHpr((0, 0, 0))
		else:
			self.dummy.setPos((0, 0, 0.25))
			self.dummy.setHpr((180, 0, 0))
			self.camera.setPos((0, 0, 0))	
			self.camera.setHpr((0, 0, 0))	
		
	def move(self, direction="up", time=0.1):
		if self.vue:
			if direction == "up":
				if self.dummy.getP() > -25:
					self.dummy.setP(self.dummy, -time*50)
			elif direction == "down":
				if self.dummy.getP() < 15:
					self.dummy.setP(self.dummy, time*50)
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
