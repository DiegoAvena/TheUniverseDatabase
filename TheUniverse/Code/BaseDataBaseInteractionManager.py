'''

----SUMMARY-----
contains base functionality for any option that
will require interaction with the localMySQL database,
such as modifying data in it (which
implies searches, deletions, updates), and
searching for data in it

----CLASSES THAT INHERIT FROM THIS CLASS-----
BaseDataBaseModifierManager
BaseSingleSearchManager
BaseMultiSearchManager

----IMPORTS----
mysql - used to make the connection to the database
tkinter - used for all UI
font from tkinter, used for making the button font

'''

import mysql
from tkinter import *
from tkinter import font

class BaseDataBaseInteractionManager:

    global localMySqlInstancePassword

    # a message to show to the user on successful completion of
    # a command
    global successMessage

    # linked to the confirm method
    global confirmButton

    global buttonFontStyle
    global yPadding

    # insertion frame is the frame on which
    # all of the UI needed is placed upon
    global insertionFrame

    # meant to store a reference to the Option submenu
    # that created this instance in the first place, so that
    # when the instance of this class ends later, it can
    # load that submenu back in
    global insertionManager

    # linked to the cancel method
    global cancelButton

    def __init__(self, localMySqlInstancePassword):
        self.localMySqlInstancePassword = localMySqlInstancePassword

    def showSuccessMessage(self, row, column, columnspan):
        pass

    # called when the cancelButton is hit
    # will close the current specific option and return
    # the user back to the option menu (not the main menu, but
    # the sub menu created for the option the user wants to focus on, so
    # either the Update option menu, or the Search option menu, etc.)
    def cancel(self):
        self.insertionFrame.grid_forget()
        self.insertionFrame.destroy()
        self.insertionManager.showMainFrameAgain()


    # linked to the confirm button, used to
    # go forth with a command or attempt
    # to perform a command
    def confirm(self):
        pass

    def initializeInteractionBase(self, windowToPutFrameOnto, insertionManager, insertionTitle):

        self.insertionFrame = LabelFrame(windowToPutFrameOnto)
        self.insertionFrame.grid(row=1, column=1)

        self.buttonFontStyle = font.Font(size=15)
        self.yPadding = 20

        self.confirmButton = Button(self.insertionFrame, text="CONFIRM", font=self.buttonFontStyle, padx=80,
                                    pady=5, command=self.confirm)
        self.cancelButton = Button(self.insertionFrame, text="CANCEL", font=self.buttonFontStyle, padx=80, pady=5,
                                   command=self.cancel)

        self.insertionManager = insertionManager
        insertionManager.setMainTitle(insertionTitle)

    def makeConnectionToDatabase(self):
        dataBase = mysql.connector.connect(host="localhost",
                                           user="root",
                                           password=self.localMySqlInstancePassword,
                                           auth_plugin='mysql_native_password',
                                           database='TheUniverse'
                                           )
        return dataBase