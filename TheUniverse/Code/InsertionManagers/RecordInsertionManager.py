'''

----SUMMARY----
This option displays a submenu to the user for all of
the more specific insertions they can do.

----IMPORTS----
OptionBase:

Used to obtain base option functionality
since this is an option for record insertions

Various insertion Managers (...InsertionManager):

Each is used to load and manage
a more specific insertion option (as
indicated by the name of the class), so
for example, NewGalaxyInsertionManager manages
the behavior for inserting a galaxy, etc.
These are presented to the user upon their
clicking of the corresponding button.

'''

from Code.OptionBase import OptionBase
from Code.InsertionManagers.InvidualInsertionManagers.NewGalaxyInsertionManager import NewGalaxyInsertionManager
from Code.InsertionManagers.InvidualInsertionManagers.NewGalaxyTypeInsertionManager import NewGalaxyTypeInsertionManager
from Code.InsertionManagers.InvidualInsertionManagers.NewEvolutionaryStageInsertionManager import NewEvolutionaryStageInsertionManager
from Code.InsertionManagers.InvidualInsertionManagers.NewPlanetInsertionManager import NewPlanetInsertionManager
from Code.InsertionManagers.InvidualInsertionManagers.NewPlanetarySystemInsertionManager import NewPlanetarySystemInsertionManager
from Code.InsertionManagers.InvidualInsertionManagers.NewStarInsertionManager import NewStarInsertionManager
from Code.InsertionManagers.InvidualInsertionManagers.NewMoonInsertionManager import NewMoonInsertionManager
from tkinter import *

class RecordInsertionManager(OptionBase):

    def insertNewGalaxy(self):
        self.mainFrame.grid_forget()
        newGalaxyInsertionFrameManager = NewGalaxyInsertionManager(self.localMySqlInstancePassword)
        newGalaxyInsertionFrameManager.manageInsertion(self.window, self, "Galaxy Insertion")

    def insertNewEvolutionaryStage(self):
        self.mainFrame.grid_forget()
        evolutionaryStageManager = NewEvolutionaryStageInsertionManager(self.localMySqlInstancePassword)
        evolutionaryStageManager.manageInsertion(self.window, self, "Evolutionary Stage Insertion")

    def insertNewGalaxyType(self):
        self.mainFrame.grid_forget()
        newGalaxyTypeInsertionManager = NewGalaxyTypeInsertionManager(self.localMySqlInstancePassword)
        newGalaxyTypeInsertionManager.manageInsertion(self.window, self, "Galaxy Type Insertion")

    def insertNewPlanet(self):
        self.mainFrame.grid_forget()
        newPlanetInsertionManager = NewPlanetInsertionManager(self.localMySqlInstancePassword)
        newPlanetInsertionManager.manageInsertion(self.window, self, "New Planet Insertion")

    def insertNewPlanetarySystem(self):
        self.mainFrame.grid_forget()
        newPlanetarySystemManager = NewPlanetarySystemInsertionManager(self.localMySqlInstancePassword)
        newPlanetarySystemManager.manageInsertion(self.window, self, "New Planetary System Insertion")

    def insertNewStar(self):
        self.mainFrame.grid_forget()
        newStarInsertionManager = NewStarInsertionManager(self.localMySqlInstancePassword)
        newStarInsertionManager.manageInsertion(self.window, self, "New Star Insertion")

    def insertNewMoon(self):
        self.mainFrame.grid_forget()
        newMoonInsertionManager = NewMoonInsertionManager(self.localMySqlInstancePassword)
        newMoonInsertionManager.manageInsertion(self.window, self, "New Moon insertion")

    def manageOption(self, windowTitle, menuManager):
        OptionBase.manageOption(self, windowTitle, menuManager)

        # place the buttons:
        createNewGalaxyButton = Button(self.mainFrame, text="Create New Galaxy", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.insertNewGalaxy)
        createNewPlanetButton = Button(self.mainFrame, text="Create a New Planet", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.insertNewPlanet)
        createNewGalaxyType = Button(self.mainFrame, text="Create a New Galaxy Type", font=self.buttonFontStyle, padx=65, pady=self.yPadding, command=self.insertNewGalaxyType)
        createNewEvolutionaryStage = Button(self.mainFrame, text="Create a New Evolutionary Stage", font=self.buttonFontStyle, padx=45, pady=self.yPadding, command=self.insertNewEvolutionaryStage)
        createNewPlanetarySystem = Button(self.mainFrame, text="Create a new planetary system", font=self.buttonFontStyle, padx=45, pady=self.yPadding, command=self.insertNewPlanetarySystem)
        createNewStar = Button(self.mainFrame, text="Create a new star", font=self.buttonFontStyle, padx=45, pady=self.yPadding, command=self.insertNewStar)
        createANewMoon = Button(self.mainFrame, text="Create a new moon", font=self.buttonFontStyle, padx=45, pady=self.yPadding, command=self.insertNewMoon)

        createNewGalaxyButton.grid(row=1, column=1)
        createNewPlanetButton.grid(row=2, column=1)
        createNewGalaxyType.grid(row=3, column=1)
        createNewEvolutionaryStage.grid(row=4, column=1)
        createNewPlanetarySystem.grid(row=5, column=1)
        createNewStar.grid(row=6, column=1)
        createANewMoon.grid(row=7, column=1)
