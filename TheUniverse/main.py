'''

----------SUMMARY-----------
Initializes the database and runs
the entire app

---------IMPORTS-----------
DataLoader - used for loading data and initializing the DB
MainMenuManager - used to present the user with the main menu options

'''

from Code.DataLoader import DataLoader
from Code.MainMenuManager import MainMenuManager

# initialize the DB:
dataLoader = DataLoader("UniverseRawData.csv")
dataLoader.initializeDatabase()

# now manage the app:
mainMenuManager = MainMenuManager(dataLoader.password)
mainMenuManager.manageApp()