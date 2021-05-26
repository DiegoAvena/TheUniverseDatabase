'''

----SUMMARY----
This option displays a submenu to the user for all of
the more specific updates they can do.

----IMPORTS----
OptionBase:

Used to obtain base option functionality
since this is an option for record updates

Various update Managers (...UpdateManager):

Each is used to load and manage
a more specific update option (as
indicated by the name of the class), so
for example, GalaxyUpdateManager manages
the behavior for updating a galaxy, etc.
These are presented to the user upon their
clicking of the corresponding button.

'''

from Code.OptionBase import OptionBase
from Code.UpdateManagers.IndividualUpdateManagers.GalaxyTypeUpdateManager import GalaxyTypeUpdateManager
from Code.UpdateManagers.IndividualUpdateManagers.EvolutionaryStageUpdateManager import EvolutionaryStageUpdateManager
from Code.UpdateManagers.IndividualUpdateManagers.GalaxyUpdateManager import GalaxyUpdateManager
from Code.UpdateManagers.IndividualUpdateManagers.PlanetUpdateManager import PlanetUpdateManager
from Code.UpdateManagers.IndividualUpdateManagers.StarUpdateManager import StarUpdateManager
from Code.UpdateManagers.IndividualUpdateManagers.GalaxyDiscovererUpdateManager import GalaxyDiscovererUpdateManager
from Code.UpdateManagers.IndividualUpdateManagers.PlanetarySystemUpdateManager import PlanetarySystemUpdateManager
from Code.UpdateManagers.IndividualUpdateManagers.MoonUpdateManager import MoonUpdateManager
from Code.UpdateManagers.IndividualUpdateManagers.MoonDiscovererUpdateManager import MoonDiscovererUpdateManager

from tkinter import *

class RecordUpdateManager(OptionBase):

    def showGalaxyUpdateFrame(self):
        self.mainFrame.grid_forget()
        galaxyUpdateManager = GalaxyUpdateManager(self.localMySqlInstancePassword)
        galaxyUpdateManager.manageUpdate(self.window, self, "Galaxy update manager")

    def showUpdateGalaxyTypeFrame(self):
        self.mainFrame.grid_forget()
        galaxyTypeUpdateManager = GalaxyTypeUpdateManager(self.localMySqlInstancePassword)
        galaxyTypeUpdateManager.manageUpdate(self.window, self, "Galaxy Type Update")

    def showUpdateEvolutionaryStageTypeFrame(self):
        self.mainFrame.grid_forget()
        evolutionaryStageType = EvolutionaryStageUpdateManager(self.localMySqlInstancePassword)
        evolutionaryStageType.manageUpdate(self.window, self, "Evolutionary stage Update")

    def showUpdatePlanetFrame(self):
        self.mainFrame.grid_forget()
        planetUpdateManager = PlanetUpdateManager(self.localMySqlInstancePassword)
        planetUpdateManager.manageUpdate(self.window, self, "Planet Update")

    def showStarUpdateFrame(self):
        self.mainFrame.grid_forget()
        starUpdateManager = StarUpdateManager(self.localMySqlInstancePassword)
        starUpdateManager.manageUpdate(self.window, self, "Star Update")

    def showGalaxyDiscovererUpdateFrame(self):
        self.mainFrame.grid_forget()
        galaxyDiscovererUpdateManager = GalaxyDiscovererUpdateManager(self.localMySqlInstancePassword)
        galaxyDiscovererUpdateManager.manageUpdate(self.window, self, "Galaxy Discoverer update")

    def showPlanetarySystemUpdateFrame(self):
        self.mainFrame.grid_forget()
        planetarySystemUpdateManager = PlanetarySystemUpdateManager(self.localMySqlInstancePassword)
        planetarySystemUpdateManager.manageUpdate(self.window, self, "System update")

    def showMoonUpdateFrame(self):
        self.mainFrame.grid_forget()
        moonUpdateManager = MoonUpdateManager(self.localMySqlInstancePassword)
        moonUpdateManager.manageUpdate(self.window, self, "Moon update")

    def showMoonDiscovererUpdateFrame(self):
        self.mainFrame.grid_forget()
        moonDiscovererUpdateManager = MoonDiscovererUpdateManager(self.localMySqlInstancePassword)
        moonDiscovererUpdateManager.manageUpdate(self.window, self, "Moon discoverer update")

    # present all of the options the user has for updating a record
    def manageOption(self, windowTitle, menuManager):
        OptionBase.manageOption(self, windowTitle, menuManager)

        updateGalaxyButton = Button(self.mainFrame, text="Update a galaxy record", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showGalaxyUpdateFrame)
        updateGalaxyButton.grid(row=0, column=1)

        updatePlanetButton = Button(self.mainFrame, text="Update a planet record", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showUpdatePlanetFrame)
        updatePlanetButton.grid(row=1, column=1)

        updateGalaxyTypeButton = Button(self.mainFrame, text="Update a galaxy type record", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showUpdateGalaxyTypeFrame)
        updateGalaxyTypeButton.grid(row=2, column=1)

        updateEvolutionaryStageButton = Button(self.mainFrame, text="Update a evolutionary stage record", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showUpdateEvolutionaryStageTypeFrame)
        updateEvolutionaryStageButton.grid(row=3, column=1)

        updateStarButton = Button(self.mainFrame, text="Update a star record", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command = self.showStarUpdateFrame)
        updateStarButton.grid(row=4, column=1)

        updateGalaxyDiscovererButton = Button(self.mainFrame, text="Update a galaxy discoverer record", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showGalaxyDiscovererUpdateFrame)
        updateGalaxyDiscovererButton.grid(row=5, column=1)

        updateMoonButton = Button(self.mainFrame, text="Update a moon record", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showMoonUpdateFrame)
        updateMoonButton.grid(row=6, column=1)

        updatePlanetarySystemButton = Button(self.mainFrame, text="Update a system record", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showPlanetarySystemUpdateFrame)
        updatePlanetarySystemButton.grid(row=7, column=1)

        updateMoonDiscovererButton = Button(self.mainFrame, text="Update a moon discoverer record", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showMoonDiscovererUpdateFrame)
        updateMoonDiscovererButton.grid(row=8, column=1)
        