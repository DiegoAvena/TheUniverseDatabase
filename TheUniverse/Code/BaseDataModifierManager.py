'''

----SUMMARY----
This contains the base functionality for all
options that will cause changes on the contents
of the database, such as updates, insertions, and
deletions.

----CLASSES THAT INHERIT FROM THIS CLASS----
BaseDeletionManager
CompositeDeletionManager
BaseInsertionManager
BaseUpdateManager

---IMPORTS---
tkinter:
used for all of the UI

messagebox from tkinter:
used to display pop up messages to the user for them
to check over the data and confirm

InsertionValidator:
Used to validate data that the user inputed in input fields

BaseDataBaseInteractionManager:
Used to obtain functionality such as connection to the database,
and other things such as the initialization of the confirm and cancel buttons,
and the frame on which all UI  will be placed

'''

from tkinter import messagebox
from tkinter import *
from Code.InsertionManagers.InsertionValidator import InsertionValidator
from Code.BaseDataBaseInteractionManager import BaseDataBaseInteractionManager

class BaseDataModifierManager(BaseDataBaseInteractionManager):

    global errorMessageForWhenCommitFailsDueToSqlError
    global errorMessageFrame # this is the frame on which the error messages will be displayed on
    global errorMessageScrollBar

    global insertionValidator # used to validate any new data user inserts
    global errorMessagesLabel # stores the contents of the error message

    def showSuccessMessage(self, row, column, columnspan):

        if (self.errorMessageFrame != None):
            self.errorMessageFrame.grid_forget()
            self.errorMessageFrame.destroy()

        self.errorMessageFrame = LabelFrame(self.insertionFrame)
        self.errorMessageFrame.grid(row=row, column=column, columnspan=columnspan)

        self.errorMessagesLabel = Text(self.errorMessageFrame, width=80, height=3)
        self.errorMessagesLabel.pack(side="left")

        self.errorMessageScrollBar = Scrollbar(self.errorMessageFrame, orient="vertical",
                                               command=self.errorMessagesLabel.yview)
        self.errorMessageScrollBar.pack(side="left", expand=True, fill="y")

        self.errorMessagesLabel.configure(yscrollcommand=self.errorMessageScrollBar.set)
        self.errorMessagesLabel.insert(END, self.successMessage)
        self.errorMessagesLabel.configure(state=DISABLED)

    def showErrorMessage(self, row, column, columnspan):

        if (self.errorMessageFrame != None):
            self.errorMessageFrame.grid_forget()
            self.errorMessageFrame.destroy()

        self.errorMessageFrame = LabelFrame(self.insertionFrame)
        self.errorMessageFrame.grid(row=row, column=column, columnspan=columnspan)

        self.errorMessagesLabel = Text(self.errorMessageFrame, width=80, height=3)
        self.errorMessagesLabel.pack(side="left")

        self.errorMessageScrollBar = Scrollbar(self.errorMessageFrame, orient="vertical",
                                   command=self.errorMessagesLabel.yview)
        self.errorMessageScrollBar.pack(side="left", expand=True, fill="y")

        self.errorMessagesLabel.configure(yscrollcommand=self.errorMessageScrollBar.set)
        self.errorMessagesLabel.insert(END, "ERRORS FOUND WHILE TRYING TO SUBMIT: " + "\n" + self.insertionValidator.errorMessage)
        self.errorMessagesLabel.configure(state=DISABLED)

    # use this to confirm the transactions
    # if the user hits no, then the transaction is rolledback
    # if the user hits yes, then the transaction is committed
    def showConfirmationPopUp(self, messageToDisplay):
        return messagebox.askyesno("Does this record look correct then?", messageToDisplay)

    def manageBaseModifierManager(self, windowToPutFrameOnto, insertionManager, insertionTitle):

        self.initializeInteractionBase(windowToPutFrameOnto, insertionManager, insertionTitle)

        self.successMessage = "Record added!"

        self.errorMessageForWhenCommitFailsDueToSqlError = 'FAILED TO INSERT NEW RECORDS FOR SOME REASON, ROLLING BACK CHANGES...'

        self.insertionValidator = InsertionValidator()

        self.errorMessageFrame = LabelFrame(self.insertionFrame)
