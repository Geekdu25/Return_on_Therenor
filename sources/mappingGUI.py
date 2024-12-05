"""
Fichier tiré d'un exemple de Panda3D illustrant le paramétrage des touches par le joueur.
Nous n'avons pas codé ce programme, mais nous l'avons en partie modifié, c'est pourquoi nous
citons ses auteurs.
---------------------------------------------------------------------------------------------
Rendez-vous sur : https://docs.panda3d.org/1.10/python/more-resources/samples/gamepad
"""

from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from panda3d.core import *

loadPrcFileData("", "textures-auto-power-2 #t")
loadPrcFile("config.prc")
DEAD_ZONE = 0.33


class InputMapping(object):
    def __init__(self, keys_data):
        self.actions = keys_data.keys()
        self.__map = dict.fromkeys(self.actions)

    def mapButton(self, action, button):
        self.__map[action] = ("Bouton", str(button))

    def mapAxis(self, action, axis):
        self.__map[action] = ("Axe", axis)

    def unmap(self):
        self.__map[action] = None
        
    def get_map(self):
        dictionnaire = {}
        for machin in self.__map:
            dictionnaire[machin] = self.__map[machin][1]
        return dictionnaire 

    def formatMapping(self, action):
        mapping = self.__map.get(action)
        if not mapping:
            return "Sans évènement"
        label = mapping[1].replace('_', ' ').title()
        if mapping[0] == "Axe":
            return "Axe: " + label
        else:
            return "Bouton: " + label


class ChangeActionDialog(object):
    def __init__(self, action, command):
        self.action = action
        self.newInputType = ""
        self.newInput = ""
        self.setKeyCalled = False
        self.__command = command
        self.attachedDevices = []
        self.dialog = OkCancelDialog(
        dialogName="dlg_device_input",
        pos=(0, 0, 0.25),
        text="Veuillez sélectionner la nouvelle commande :",
        text_fg=VBase4(0.898, 0.839, 0.730, 1.0),
        text_shadow=VBase4(0, 0, 0, 0.75),
        text_shadowOffset=Vec2(0.05, 0.05),
        text_scale=0.05,
        text_align=TextNode.ACenter,
        fadeScreen=0.65,
        frameColor=VBase4(0.3, 0.3, 0.3, 1),
        button_scale=0.15,
        button_text_scale=0.35,
        button_text_align=TextNode.ALeft,
        button_text_fg=VBase4(0.898, 0.839, 0.730, 1.0),
        button_text_pos=Vec2(-0.9, -0.125),
        button_relief=1,
        button_pad=Vec2(0.01, 0.01),
        button_frameColor=VBase4(0, 0, 0, 0),
        button_frameSize=VBase4(-1.0, 1.0, -0.25, 0.25),
        button_pressEffect=False,
        command=self.onClose)
        self.dialog.setTransparency(True)
        self.dialog.configureDialog()

    def buttonPressed(self, button):
        if any(button.guiItem.getState() == 1 for button in self.dialog.buttonList):
            return

        text = str(button).replace('_', ' ').title()
        self.dialog["text"] = "Le nouvel évènement sera :\n\nLe bouton : " + text
        self.newInputType = "bouton"
        self.newInput = button

    def axisMoved(self, axis):
        text = axis.name.replace('_', ' ').title()
        self.dialog["text"] = "Le nouvel évènement sera :\n\nL'axe: " + text
        self.newInputType = "axe"
        self.newInput = axis

    def onClose(self, result):
        self.dialog.cleanup()
        if self.newInput and result == DGG.DIALOG_OK:
            self.__command(self.action, self.newInputType, self.newInput)
        else:
            self.__command(self.action, None, None)
