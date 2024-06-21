from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
s = ShowBase()
a = Actor("../models/error.bam")
b = Actor("panda")
a.reparentTo(render)
a.setScale(10)
b.reparentTo(render)
s.run()
