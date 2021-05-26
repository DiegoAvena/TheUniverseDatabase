'''

----SUMMARY---
Allows the user to update
a moon discoverer

---IMPORTS---
BaseUpdateManager:

Used to obtain base functionality
for a more specific update, since this
class is for the specific update on
moon discovers

tkinter - for all of the UI

mysql:

for performing the update queries and
search query needed to display the initial
record to the user

'''

from Code.UpdateManagers.BaseUpdateManager import BaseUpdateManager
from tkinter import *
import mysql

class MoonDiscovererUpdateManager(BaseUpdateManager):

    # initial moon discoverer UI
    global discovererNameLabel
    global discoveryYearLabel

    global moonHasADiscoverer

    # updating UI
    global newDiscovererNameInputBox
    global newDiscoveryYearInputBox

    # perform the moon discoverer update
    def confirm(self):
        thereWasAnError = False
        if (self.insertionValidator.validateWord(False, self.selectedThingToUpdate.get(), "Name of moon to update a discoverer for: ") == False):
            thereWasAnError = True

        newMoonDiscoverer = self.newDiscovererNameInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newMoonDiscoverer)):
            # user wants to delete this discoverer record, but deletions of moonDiscoverers should
            # only be performed in the MoonDeletionManager
            thereWasAnError = True
            self.insertionValidator.errorMessage += "The new moon discoverer name has the delete code, but this cannot be left empty" + "\n"
        elif ((self.moonHasADiscoverer == False) and (self.insertionValidator.validateWord(False, newMoonDiscoverer, "New moon discoverer name")) == False):
            # the moon has no moon discoverer and the user is trying to update it to an empty moon discoverer
            # there should never be a record inserted without a moondiscoverer name into this table
            thereWasAnError = True

        newMoonDiscoveryYear = self.newDiscoveryYearInputBox.get()
        if (self.insertionValidator.validateYear(newMoonDiscoveryYear, "Year moon was discovered") == False):
            thereWasAnError = True

        if (thereWasAnError == False):

            # start forming the update query
            newChanges = []
            confirmationMessage = ""

            query = '''
            
                UPDATE MoonDiscovers
                SET
            
            '''
            if (len(newMoonDiscoverer) > 0):
                try:
                    confirmationMessage += "-Update discoverer name from " + self.initialRecord[0] + " to " + newMoonDiscoverer + "\n"
                except:
                    confirmationMessage += "-Update discoverer name from NULL to " + newMoonDiscoverer + "\n"

                newChanges.append(newMoonDiscoverer)
                query += " DiscovererName = %s"

            if ((len(newMoonDiscoveryYear) > 0)):
                try:
                    confirmationMessage += "-Update moon discovery year from" + str(self.initialRecord[2]) + " to " + newMoonDiscoveryYear + "\n"
                except:
                    confirmationMessage += "-Update moon discovery year from NULL to " + newMoonDiscoveryYear + "\n"

                if (len(newChanges) > 0):
                    query += ","
                newChanges.append(self.insertionValidator.obtainFinalValue(newMoonDiscoveryYear))
                query += " DiscoveryYear = %s"

            if (len(newChanges) > 0):

                if (self.moonHasADiscoverer == False):
                    # there will be a new insertion into moonDiscovers table
                    query = '''

                        INSERT INTO MoonDiscovers 
                        VALUES (%s, %s, %s);

                    '''
                    newChanges.clear()
                    newChanges.append(newMoonDiscoverer)
                    newChanges.append(self.selectedThingToUpdate.get())
                    newChanges.append(self.insertionValidator.obtainFinalValue(newMoonDiscoveryYear))

                else:
                    # there will be an update on this moonDiscoverer record as it already exists
                    newChanges.append(self.selectedThingToUpdate.get())
                    newChanges.append(self.initialRecord[0])
                    query += " WHERE MoonName = %s AND DiscovererName = %s;"

                database = self.makeConnectionToDatabase()
                cursor = database.cursor()
                try :
                    cursor.execute(query, newChanges)
                    if (self.showConfirmationPopUp(confirmationMessage)):
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


    def selectThingToUpdate(self, nameOfThingSelected):

        if (nameOfThingSelected != 'N/A'):
            database = self.makeConnectionToDatabase()
            cursor = database.cursor()

            query = '''
            
                SELECT *
                FROM MoonDiscovers
                WHERE MoonName = %s;
            
            '''
            cursor.execute(query, [nameOfThingSelected])
            record = cursor.fetchone()
            self.initialRecord = []

            if (record != None):
                for attribute in record:
                    self.initialRecord.append(attribute)

                self.moonHasADiscoverer = True
                self.discovererNameLabel.configure(text=self.initialRecord[0])
                self.discoveryYearLabel.configure(text=str(self.initialRecord[2]))
            else:
                self.moonHasADiscoverer = False
                self.discovererNameLabel.configure(text='N/A')
                self.discoveryYearLabel.configure(text='N/A')

        else:
            self.resetAllUI(False)

    def resetAllUI(self, includingUpdatingUI):
        self.moonHasADiscoverer = False
        self.discovererNameLabel.configure(text='N/A')
        self.discoveryYearLabel.configure(text='N/A')
        self.resetThingToSelectDropdownMenu()
        if (includingUpdatingUI):
            self.newDiscovererNameInputBox.delete(0, END)
            self.newDiscoveryYearInputBox.delete(0, END)

    def manageUpdate(self, windowToPutFrameOnto, updateManager, updateTitle):
        BaseUpdateManager.manageUpdate(self, windowToPutFrameOnto, updateManager, updateTitle)
        query = '''
        
            SELECT Name
            FROM Moons;
        
        '''
        self.setUpThingToUpdateSelector(0, 1, query, "Moon to update discoverers for: ")

        self.moonHasADiscoverer = False

        Label(self.leftFrame, text="Discoverer to update: ").grid(row=1, column=0)
        self.discovererNameLabel = Label(self.leftFrame, text="N/A")
        self.discovererNameLabel.grid(row=1, column=1)

        Label(self.leftFrame, text="Discovery year: ").grid(row=2, column=0)
        self.discoveryYearLabel = Label(self.leftFrame, text="N/A")
        self.discoveryYearLabel.grid(row=2, column=1)

        # updating UI
        Label(self.rightFrame, text="New discoverer name: ").grid(row=0, column=0)
        self.newDiscovererNameInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newDiscovererNameInputBox.grid(row=0, column=1)

        Label(self.rightFrame, text="New discovery year").grid(row=1, column=0)
        self.newDiscoveryYearInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newDiscoveryYearInputBox.grid(row=1, column=1)

        self.cancelButton.grid(row=1, column=0, sticky=W+E)
        self.confirmButton.grid(row=1, column=1, sticky=W+E)
