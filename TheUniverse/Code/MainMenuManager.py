'''

------SUMMARY-------
Presents all of the higher level main options
the user can pick from in the app; it is from
here that the user can proceed to more devoted
option menus, such as

The user can also quit out of the app from here

When the user exits a more devoted option menu, they will always
be left with this screen.

--------IMPORTS----------
tkinter, used for all of the UI
font from tkinter, used to create button font
RecordInsertionManager, used for the Insertion option
RecordDeletionManager, used for the deletion option
RecordSearchManager, used for the search option
RecordUpdateManager, used fot the update option

'''
from tkinter import *
from tkinter import font
from Code.InsertionManagers.RecordInsertionManager import RecordInsertionManager
from Code.DeletionManagers.RecordDeletionManager import RecordDeletionManager
from Code.SearchManagers.RecordSearchManager import RecordSearchManager
from Code.UpdateManagers.RecordUpdateManager import RecordUpdateManager

class MainMenuManager:

    global sqlInstancePassword

    global performSearchButton
    global updateRecordButton
    global insertRecordButton
    global deleteARecordButton

    global helpLabelForWhenAnOptionIsActive

    def __init__(self, sqlInstancePassword):
        self.sqlInstancePassword = sqlInstancePassword

    def disableOrEnableAllMainMenuButtons(self, turnOn):
        self.performSearchButton['state'] = turnOn
        self.updateRecordButton['state'] = turnOn
        self.insertRecordButton['state'] = turnOn
        self.deleteARecordButton['state'] = turnOn
        if (turnOn == DISABLED):
            self.helpLabelForWhenAnOptionIsActive['text'] = "Other options disabled until current option is done"
        else:
            self.helpLabelForWhenAnOptionIsActive['text'] = ""

    def bringUpInsertRecordWindow(self):
        self.disableOrEnableAllMainMenuButtons(DISABLED)
        insertionManager = RecordInsertionManager(self.sqlInstancePassword)
        insertionManager.manageOption("Record Insertion", self)

    def bringUpUpdateRecordWindow(self):
        self.disableOrEnableAllMainMenuButtons(DISABLED)
        recordUpdateManager = RecordUpdateManager(self.sqlInstancePassword)
        recordUpdateManager.manageOption("Record Update", self)

    def bringUpDeleteARecordWindow(self):
        self.disableOrEnableAllMainMenuButtons(DISABLED)
        recordDeleteManager = RecordDeletionManager(self.sqlInstancePassword)
        recordDeleteManager.manageOption("Record Deletion", self)

    def bringUpSearchWindow(self):
        self.disableOrEnableAllMainMenuButtons(DISABLED)
        recordSearchManager = RecordSearchManager(self.sqlInstancePassword)
        recordSearchManager.manageOption("Record Search Manager", self)

    def manageApp(self):
        root = Tk()
        root.title("The Universe Database")

        fontStyle = font.Font(size=50)
        buttonFontStyle = font.Font(size=15)
        title = Label(root, text="The Universe Database", font=fontStyle)
        title.grid(row=0, column=1)

        # the main option buttons:
        xPadding = 80
        yPadding = 20
        self.performSearchButton = Button(root, padx=xPadding, pady=yPadding, text="Perform a search?", font=buttonFontStyle, command=self.bringUpSearchWindow)
        self.updateRecordButton = Button(root, padx=xPadding, pady=yPadding, text="Update a record?", font=buttonFontStyle, command=self.bringUpUpdateRecordWindow)
        self.insertRecordButton = Button(root, padx=xPadding, pady=yPadding, text="Insert a record?", font=buttonFontStyle, command=self.bringUpInsertRecordWindow)
        self.deleteARecordButton = Button(root, padx=xPadding, pady=yPadding, text="Delete a record?", font=buttonFontStyle, command=self.bringUpDeleteARecordWindow)
        quitButton = Button(root, padx=xPadding, pady=yPadding, text="Quit?", font=buttonFontStyle, command=root.quit)

        # place these buttons on the view:
        self.performSearchButton.grid(row=1, column=1)
        self.updateRecordButton.grid(row=2, column=1)
        self.insertRecordButton.grid(row=3, column=1)
        self.deleteARecordButton.grid(row=4, column=1)
        quitButton.grid(row=5, column=1)

        # the help label:
        self.helpLabelForWhenAnOptionIsActive = Label(root, text="", font=buttonFontStyle)
        self.helpLabelForWhenAnOptionIsActive.grid(row=6, column=1)

        root.mainloop()