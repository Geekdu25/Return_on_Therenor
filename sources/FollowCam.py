from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class SimpleThirdPersonCamera():
	"""
	MIT License
	Copyright (c) 2021 Ian Eborn (Thaumaturge)
	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:
	The above copyright notice and this permission notice shall be included in all
	copies or substantial portions of the Software.
	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
	SOFTWARE.
	"""
	def __init__(self, tilt, intendedDistance, shoulderSideDistance, height, adjustmentSpeed, sideSwitchSpeed, ownerNodePath, camera):
		self.camera = camera
		self.ownerNodePath = ownerNodePath
		self.shoulderSideDistance = shoulderSideDistance
		self.intendedDistance = intendedDistance
		self.height = height
		self.tilt = tilt
		self.sideSwitchSpeed = sideSwitchSpeed
		self.adjustmentSpeed = adjustmentSpeed
		self.cameraBase = ownerNodePath.attachNewNode(PandaNode("third-person camera-base"))
		self.cameraHolder = self.cameraBase.attachNewNode(PandaNode("third-person camera-holder"))
		self.colliderRadius = 0.5
		camera.reparentTo(self.cameraHolder)
		self.cameraBase.setZ(height)
		self.cameraBase.setP(tilt)
		self.cameraHolder.setY(-intendedDistance)
		self.setupCollision()

	def setupCollision(self):
		self.traverser = CollisionTraverser()
		self.collisionQueue = CollisionHandlerQueue()
		self.colliderNode = CollisionNode("camera collider")
		self.colliderNode.addSolid(CollisionSegment(-self.colliderRadius, -self.colliderRadius, 0,
                                                    -self.colliderRadius, -self.intendedDistance, 0))
		self.colliderNode.addSolid(CollisionSegment(self.colliderRadius, -self.colliderRadius, 0,
                                                    self.colliderRadius, -self.intendedDistance, 0))
		self.colliderNode.addSolid(CollisionSegment(0, -self.colliderRadius, -self.colliderRadius,
                                                    0, -self.intendedDistance, -self.colliderRadius))
		self.colliderNode.addSolid(CollisionSegment(0, -self.colliderRadius, self.colliderRadius,
                                                    0, -self.intendedDistance, self.colliderRadius))
		self.colliderNode.setIntoCollideMask(0)
		self.colliderNode.setFromCollideMask(1)
		self.collider = self.cameraBase.attachNewNode(self.colliderNode)
		self.traverser.addCollider(self.collider, self.collisionQueue)

	def getNearestCollision(self, sceneRoot):
		self.traverser.traverse(sceneRoot)
		if self.collisionQueue.getNumEntries() > 0:
			self.collisionQueue.sortEntries()
			entry = self.collisionQueue.getEntry(0)
			pos = entry.getSurfacePoint(sceneRoot)
			diff = self.cameraBase.getPos(sceneRoot) - pos
			return diff.length()
		return self.intendedDistance


	def update(self, dt, sceneRoot):
		currentDistance = abs(self.cameraHolder.getY())
		targetY = self.intendedDistance
		collisionDistance = self.getNearestCollision(sceneRoot)
		if targetY > collisionDistance:
			targetY = collisionDistance
		yDiff = targetY - currentDistance
		offsetVal = self.adjustmentSpeed*dt
		if offsetVal > 1:
			offsetVal = 1
		offset = yDiff*offsetVal
		self.cameraHolder.setY(-currentDistance -offset)
		currentSideDistance = self.cameraBase.getX()
		sideDiff = self.shoulderSideDistance*0 - currentSideDistance
		if abs(sideDiff) < 0.001:
			currentSideDistance = 0
		else:
			offsetVal = self.sideSwitchSpeed*dt
			if offsetVal > 1:
				offsetVal = 1
			offset = sideDiff*offsetVal
			currentSideDistance += offset
		self.cameraBase.setX(currentSideDistance)

	def cleanup(self):
		if self.camera is not None:
			self.camera.detachNode()
			self.camera = None
		if self.ownerNodePath is not None:
			self.ownerNodePath = None
		self.cleanupCollision()
		if self.cameraBase is not None:
			self.cameraBase.removeNode()
			self.cameraBase = None
            
	def cleanupCollision(self):
		if self.collider is not None:
			self.traverser.removeCollider(self.collider)
			self.collider.removeNode()
			self.collider = None
			self.colliderNode = None
		self.traverser = None
		self.collisionQueue = None

class ManetteCam(SimpleThirdPersonCamera):
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
		camera.node().getLens().setFov(120)
		#super().__init__(0, 0, 0.5, 2, 7, 10, self.dummy, self.camera)
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
		#self.update(dt, render)
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
