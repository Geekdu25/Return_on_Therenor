from direct.showbase.ShowBase import ShowBase




base = ShowBase()
model = loader.loadModel("Village.bam")
#model.setHpr(0, 270, 180)
model.setScale(0.25)
model.reparentTo(render)
model.writeBamFile("Village.bam")
base.run()

