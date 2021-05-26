'''

----SUMMARY----
This option displays a submenu to the user for all of
the more specific deletions they can do.

----IMPORTS----
OptionBase:

Used to obtain base option functionality
since this is an option for record deletions

tkinter - for all the UI

BaseDeletionManager

Used to load and manage the more specific deletion
options on tables that have single column primary keys

CompositeDeletionManager
Used to load and manage the more specific deletion options
on tables that have composite primary keys, such as
the GalaxyDiscovers table

'''

from Code.OptionBase import OptionBase
from tkinter import *
from Code.DeletionManagers.BaseDeletionManager import BaseDeletionManager
from Code.DeletionManagers.CompositeDeletionManager import CompositeDeletionManager

class RecordDeletionManager(OptionBase):

    def showPlanetDeletionFrame(self):
        self.mainFrame.grid_forget()
        searchQuery = '''
        
            SELECT Name
            FROM Planets;
        
        '''

        deletionQuery = '''
        
            DELETE FROM Planets
            WHERE Name = %s;
        
        '''
        planetDeletionManager = BaseDeletionManager(self.localMySqlInstancePassword)
        planetDeletionManager.manageDeletion(self.window, self, "Planet deletion", "Planet to delete: ", "Planets", searchQuery, deletionQuery)


    def showStarDeletionFrame(self):
        self.mainFrame.grid_forget()
        searchQuery = '''
        
            SELECT Name 
            FROM Stars;
        
        '''

        deletionQuery = '''
        
            DELETE FROM Stars 
            WHERE Name = %s;
        
        '''
        starDeletionManager = BaseDeletionManager(self.localMySqlInstancePassword)
        starDeletionManager.manageDeletion(self.window, self, "Star deletion", "Star to delete: ", "Stars", searchQuery, deletionQuery)

    def showDeletePlanetarySystemFrame(self):
        self.mainFrame.grid_forget()
        searchQuery = '''
        
            SELECT Name
            FROM PlanetarySystems;
        
        '''

        deletionQuery = '''
        
            DELETE FROM PlanetarySystems
            WHERE Name = %s;
        
        '''
        planetarySystemDeletionManager = BaseDeletionManager(self.localMySqlInstancePassword)
        planetarySystemDeletionManager.manageDeletion(self.window, self, "Planetary system deletion", "System to delete: ", "PlanetarySystems", searchQuery, deletionQuery)

    def showDeleteMoonFrame(self):
        self.mainFrame.grid_forget()
        searchQuery = '''
        
            SELECT Name
            FROM Moons;
        
        '''

        deletionQuery = '''
        
            DELETE FROM Moons
            WHERE Name = %s;
        
        '''
        moonDeletionManager = BaseDeletionManager(self.localMySqlInstancePassword)
        moonDeletionManager.manageDeletion(self.window, self, "Moon deletion", "Moon to delete: ", "Moons", searchQuery, deletionQuery)

    def showGalaxyTypeDeletionFrame(self):
        self.mainFrame.grid_forget()
        searchQuery = '''
        
            SELECT GalaxyType
            FROM GalaxyTypes;
        
        '''

        deletionQuery = '''
        
            DELETE FROM GalaxyTypes
            WHERE GalaxyType = %s;
        
        '''
        galaxyTypeDeletionManager = BaseDeletionManager(self.localMySqlInstancePassword)
        galaxyTypeDeletionManager.manageDeletion(self.window, self, "Galaxy type deletion", "Galaxy type to delete: ", "Galaxies", searchQuery, deletionQuery)

    def showEvolutionaryStageDeletionFrame(self):
        self.mainFrame.grid_forget()
        searchQuery = '''
        
            SELECT EvolutionaryStage
            FROM EvolutionaryStages;
        
        '''

        deletionQuery = '''
        
            DELETE FROM EvolutionaryStages
            WHERE EvolutionaryStage = %s;
        
        '''
        evolutionaryStageDeletionManager = BaseDeletionManager(self.localMySqlInstancePassword)
        evolutionaryStageDeletionManager.manageDeletion(self.window, self, "Evolutionary stage deletion", "Evolutionary stage to delete: ", "EvolutionaryStages", searchQuery, deletionQuery)

    def showGalaxyDiscovererDeletionFrame(self):
        self.mainFrame.grid_forget()
        searchQuery = '''
        
            SELECT DISTINCT GalaxyName
            FROM GalaxyDiscovers;
        
        '''

        secondSearchQuery = '''
        
            SELECT DiscovererName
            FROM GalaxyDiscovers
            WHERE GalaxyName = %s;
        
        '''

        deletionQuery = '''
        
            DELETE FROM GalaxyDiscovers
            WHERE GalaxyName = %s AND DiscovererName = %s;
        
        '''
        galaxyDiscovererDeletionManager = CompositeDeletionManager(self.localMySqlInstancePassword)
        galaxyDiscovererDeletionManager.manageDeletion(self.window, self, "Galaxy discoverer deletion", "Name of galaxy to delete discoverers for: ", "GalaxyDiscoverers", searchQuery, secondSearchQuery, deletionQuery, "Discoverer to delete: ")

    def showMoonDiscovererDeletionFrame(self):
        self.mainFrame.grid_forget()
        searchQuery = '''
        
            SELECT DISTINCT MoonName
            FROM MoonDiscovers;
        
        '''

        secondSearchQuery = '''
        
            SELECT DiscovererName
            FROM MoonDiscovers 
            WHERE MoonName = %s;
        
        '''

        deletionQuery = '''
        
            DELETE FROM MoonDiscovers
            WHERE MoonName = %s AND DiscovererName = %s;
        
        '''
        moonDiscovererDeletionManager = CompositeDeletionManager(self.localMySqlInstancePassword)
        moonDiscovererDeletionManager.manageDeletion(self.window, self, "Moon discoverer deletion: ", "Name of moon to delete discoverers for: ", "MoonDiscoverers", searchQuery, secondSearchQuery, deletionQuery, "Discoverer to delete: ")

    def showGalaxyDeletionFrame(self):
        self.mainFrame.grid_forget()
        searchQuery = '''
        
            SELECT Name 
            FROM Galaxies;
        
        '''

        deletionQuery = '''
        
            DELETE FROM Galaxies 
            WHERE Name = %s;
        
        '''
        galaxyDeletionManager = BaseDeletionManager(self.localMySqlInstancePassword)
        galaxyDeletionManager.manageDeletion(self.window, self, "Galaxy deletion", "Galaxy to delete: ", "Galaxies", searchQuery, deletionQuery)

    def manageOption(self, windowTitle, menuManager):
        OptionBase.manageOption(self, windowTitle, menuManager)

        Button(self.mainFrame, text="Delete a planet", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showPlanetDeletionFrame).grid(row=0, column=0, columnspan=2, sticky=W+E)
        Button(self.mainFrame, text="Delete a star", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showStarDeletionFrame).grid(row=1, column=0, columnspan=2, sticky=W+E)
        Button(self.mainFrame, text="Delete a galaxy", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showGalaxyDeletionFrame).grid(row=2, column=0, columnspan=2, sticky=W+E)
        Button(self.mainFrame, text="Delete an evolutionary stage", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showEvolutionaryStageDeletionFrame).grid(row=3, column=0, columnspan=2, sticky=W+E)
        Button(self.mainFrame, text="Delete a galaxy type", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showGalaxyTypeDeletionFrame).grid(row=4, column=0, columnspan=2, sticky=W+E)
        Button(self.mainFrame, text="Delete a moon", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showDeleteMoonFrame).grid(row=5, column=0, columnspan=2, sticky=W+E)
        Button(self.mainFrame, text="Delete a planetary system", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showDeletePlanetarySystemFrame).grid(row=6, column=0, columnspan=2, sticky=W+E)
        Button(self.mainFrame, text="Delete a moon discoverer", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showMoonDiscovererDeletionFrame).grid(row=7, column=0, columnspan=2, sticky=W+E)
        Button(self.mainFrame, text="Delete a galaxy discoverer", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showGalaxyDiscovererDeletionFrame).grid(row=8, column=0, columnspan=2, sticky=W+E)
