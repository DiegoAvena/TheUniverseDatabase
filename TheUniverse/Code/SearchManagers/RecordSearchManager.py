'''

----SUMMARY----
This option displays a submenu to the user for all of
the more specific searches they can do.

----IMPORTS----
OptionBase:

Used to obtain base option functionality
since this is an option for record searches

Various update Managers (...SearchManager):

Each is used to load and manage
a more specific search option (as
indicated by the name of the class), so
for example,SinglePlanetarySearchManager manages
the behavior for searching for a single planet, etc.
These are presented to the user upon their
clicking of the corresponding button.

'''

from Code.OptionBase import OptionBase
from tkinter import *
from Code.SearchManagers.SingleSearchManagers.SinglePlanetarySearchManager import SinglePlanetarySearchManager
from Code.SearchManagers.MultiSearchManagers.MultiPlanetarySearchManager import MultiPlantarySearchManager
from Code.SearchManagers.SingleSearchManagers.SingleStarSearchManager import SingleStarSearchManager
from Code.SearchManagers.MultiSearchManagers.MultiStarSearchManager import MultiStarSearchManager
from Code.SearchManagers.SingleSearchManagers.SingleGalaxySearchManager import SingleGalaxySearchManager
from Code.SearchManagers.MultiSearchManagers.MultiGalaxySearchManager import MultiGalaxySearchManager

class RecordSearchManager(OptionBase):

    def showSinglePlanetarySearchFrame(self):
        self.mainFrame.grid_forget()
        singlePlanetarySearchManager = SinglePlanetarySearchManager(self.localMySqlInstancePassword)
        singlePlanetarySearchManager.manageSinglePlanetarySearch(self.window, self)

    def showMultiPlanetarySearchFrame(self):
        self.mainFrame.grid_forget()
        multiplanetaryManager = MultiPlantarySearchManager(self.localMySqlInstancePassword)
        multiplanetaryManager.manageMultiSearch(self.window, self, "Multi-planetary Search")

    def showSingleStarSearchFrame(self):
        self.mainFrame.grid_forget()
        singleStarSearchManager = SingleStarSearchManager(self.localMySqlInstancePassword)
        singleStarSearchManager.manageSingleStarSearch(self.window, self)

    def showMultiStarSearchFrame(self):
        self.mainFrame.grid_forget()
        multiStarSearchManager = MultiStarSearchManager(self.localMySqlInstancePassword)
        multiStarSearchManager.manageMultiSearch(self.window, self, "Multi-star search")

    def showMultiGalaxySearchFrame(self):
        self.mainFrame.grid_forget()
        multGalaxySearchManager = MultiGalaxySearchManager(self.localMySqlInstancePassword)
        multGalaxySearchManager.manageMultiSearch(self.window, self, "Multi-galaxy search")

    def showSingleGalaxySearchFrame(self):
        self.mainFrame.grid_forget()
        singleGalaxySearchManager = SingleGalaxySearchManager(self.localMySqlInstancePassword)
        singleGalaxySearchManager.manageSingleGalaxySearch(self.window, self)

    def manageOption(self, windowTitle, menuManager):

        OptionBase.manageOption(self, windowTitle, menuManager)

        singlePlanetSearchButton = Button(self.mainFrame, text="Single Planet Search", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showSinglePlanetarySearchFrame)
        singlePlanetSearchButton.grid(row=0, column=1)

        multiPlanetSearchButton = Button(self.mainFrame, text="Multiple Planet Search", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showMultiPlanetarySearchFrame)
        multiPlanetSearchButton.grid(row=1, column=1)

        singleStarSearchButton = Button(self.mainFrame, text="Single Star Search", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showSingleStarSearchFrame)
        singleStarSearchButton.grid(row=2, column=1)

        multiStarSearchButton = Button(self.mainFrame, text="Multiple Star Search", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showMultiStarSearchFrame)
        multiStarSearchButton.grid(row=3, column=1)

        singleGalaxySearchButton = Button(self.mainFrame, text="Single Galaxy Search", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showSingleGalaxySearchFrame)
        singleGalaxySearchButton.grid(row=4, column=1)

        multiGalaxySearchButton = Button(self.mainFrame, text="Multiple Galaxy Search", font=self.buttonFontStyle, padx=80, pady=self.yPadding, command=self.showMultiGalaxySearchFrame)
        multiGalaxySearchButton.grid(row=5, column=1)

