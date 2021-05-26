'''

----SUMMARY---
Allows the user to update
a galaxy discoverer

---IMPORTS---
BaseUpdateManager:

Used to obtain base functionality
for a more specific update, since this
class is for the specific update on
galaxy discovers

tkinter - for all of the UI

mysql:

for performing the update queries and
search query needed to display the initial
record to the user

'''

from Code.UpdateManagers.BaseUpdateManager import BaseUpdateManager
from tkinter import *
import mysql

class GalaxyDiscovererUpdateManager(BaseUpdateManager):

    global discoversToUpdateDropDown
    global discovererNameEditInputBox
    global selectedDiscoverer
    global discoverersToChooseFrom
    global galaxyHasADiscoverer

    def confirm(self):
        thereWasAnError = False
        enteringANewDiscoverer = False
        selectedDiscovererWasMissing = False

        if ((self.insertionValidator.validateWord(False, self.selectedDiscoverer.get(), "Selected discoverer to update") == False) and self.galaxyHasADiscoverer):
            thereWasAnError = True
            #user might being trying to enter a new discoverer name
            selectedDiscovererWasMissing = True

        if (self.insertionValidator.validateWord(False, self.discovererNameEditInputBox.get(), "New discoverer name") == False):
            thereWasAnError = True
        elif self.galaxyHasADiscoverer:
            for discoverer in self.discoverersToChooseFrom:
                if discoverer.lower() == self.discovererNameEditInputBox.get().lower():
                    self.insertionValidator.errorMessage += "The new discoverer already exists in the discoverer list!"
                    thereWasAnError = True
                    break
            if selectedDiscovererWasMissing:
                # the new discoverer name is valid, and no discoverer is selected to update, so treat as an insertion
                enteringANewDiscoverer = True
                thereWasAnError = False
                self.insertionValidator.errorMessage = ''

        if (self.insertionValidator.validateWord(False, self.selectedThingToUpdate.get(), "Selected galaxy to update discover info for") == False):
            thereWasAnError = True

        if (thereWasAnError == False):

            newDiscovererName = self.discovererNameEditInputBox.get()
            if (len(newDiscovererName) > 0):
                messageToDisplay = ""

                if (self.galaxyHasADiscoverer and (enteringANewDiscoverer == False)):

                    query = '''

                        UPDATE GalaxyDiscovers
                        SET DiscovererName = %s
                        WHERE GalaxyName = %s AND DiscovererName = %s;

                    '''
                    messageToDisplay += "-Update discoverer with name " + self.selectedDiscoverer.get() + " for galaxy " + self.selectedThingToUpdate.get() + " to " + newDiscovererName
                    newChanges = [newDiscovererName, self.selectedThingToUpdate.get(), self.selectedDiscoverer.get()]
                else:
                    query = '''
                    
                        INSERT INTO GalaxyDiscovers
                        VALUES(%s, %s);
                    
                    '''
                    messageToDisplay += "-Add in a new discoverer with name " + newDiscovererName + " for galaxy " + self.selectedThingToUpdate.get()
                    newChanges = [self.selectedThingToUpdate.get(), newDiscovererName]

                database = self.makeConnectionToDatabase()

                try:
                    cursor = database.cursor()
                    cursor.execute(query, newChanges)

                    if (self.showConfirmationPopUp(messageToDisplay)):
                        database.commit()
                        self.showSuccessMessage(2, 0, 2)
                        self.resetAllUI(True)
                        self.resetThingToSelectDropdownMenu()

                    else:
                        database.rollback()
                except mysql.connector.Error as error:
                    self.insertionValidator.errorMessage = self.errorMessageForWhenCommitFailsDueToSqlError + ": " + str(error)
                    self.showErrorMessage(2, 0, 2)
                    database.rollback()

                database.close()

            else:
                self.insertionValidator.errorMessage = "NOTHING TO UPDATE..."
                self.showErrorMessage(2, 0, 2)
        else:
            self.showErrorMessage(2, 0, 2)

        self.insertionValidator.errorMessage = ''

    def resetAllUI(self, includingUpdateUI):
        self.resetThingToSelectDropdownMenu()
        self.selectedDiscoverer.set('')
        self.discoversToUpdateDropDown.grid_forget()
        self.discoversToUpdateDropDown.destroy()
        self.discoversToUpdateDropDown = OptionMenu(self.leftFrame, self.selectedDiscoverer, '')
        self.discoversToUpdateDropDown.grid(row=1, column=1, sticky=W + E)

        if (includingUpdateUI):
            self.discovererNameEditInputBox.delete(0, END)

    def selectThingToUpdate(self, nameOfThingSelected):
        if (nameOfThingSelected != 'N/A'):
            database = self.makeConnectionToDatabase()
            cursor = database.cursor()
            query = '''


                        SELECT DiscovererName
                        FROM GalaxyDiscovers
                        WHERE GalaxyName = %s;

                    '''
            cursor.execute(query, [nameOfThingSelected])
            records = cursor.fetchall()
            self.discoverersToChooseFrom = []
            self.discoverersToChooseFrom.append('')
            if ((records != None) and (len(records) > 0)):
                self.galaxyHasADiscoverer = True
                for discoverer in records:
                    print(discoverer)
                    self.discoverersToChooseFrom.append(discoverer[0])
            else:
                self.galaxyHasADiscoverer = False

            self.discoversToUpdateDropDown.grid_forget()
            self.discoversToUpdateDropDown.destroy()
            self.discoversToUpdateDropDown = OptionMenu(self.leftFrame, self.selectedDiscoverer, *self.discoverersToChooseFrom)
            self.discoversToUpdateDropDown.grid(row=1, column=1, sticky=W + E)
        else:
            self.resetAllUI(False)

    def manageUpdate(self, windowToPutFrameOnto, updateManager, updateTitle):
        BaseUpdateManager.manageUpdate(self, windowToPutFrameOnto, updateManager, updateTitle)
        self.galaxyHasADiscoverer = False

        query = '''
        
            SELECT Name 
            FROM Galaxies;
        
        '''
        self.selectedDiscoverer = StringVar()
        self.selectedDiscoverer.set('')
        self.setUpThingToUpdateSelector(0, 1, query, "Selected Galaxy to update discovers for: ")

        Label(self.leftFrame, text="Discoverer to edit: ").grid(row=1, column=0)
        self.discoversToUpdateDropDown = OptionMenu(self.leftFrame, self.selectedDiscoverer, '')
        self.discoversToUpdateDropDown.grid(row=1, column=1, sticky=W + E)

        Label(self.rightFrame, text="New discoverer name: ").grid(row=0, column=0)
        self.discovererNameEditInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.discovererNameEditInputBox.grid(row=0, column=1)

        self.confirmButton.grid(row=1, column=0, sticky=W+E)
        self.cancelButton.grid(row=1, column=1, sticky=W+E)