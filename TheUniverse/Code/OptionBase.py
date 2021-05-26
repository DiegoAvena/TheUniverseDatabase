'''

------SUMMARY------
Contains base functionality for all of the higher level
options Deletion, Search, Insertion, and Update. This
functionality includes the creation of the subwindows needed
to get the options information presented to the user, the cancel
button needed to close this subwindow and make the main menu window active again,
etc.

------CLASSES THAT INHERIT FROM THIS CLASS----
RecordUpdateManager
RecordSearchManager
RecordInsertionManager
RecordDeletionManager

------IMPORTS--------
tkinter, used for all of the UI
font from tkinter, used for the creation of the button font
ReportGenerator, used for the generation of a pdf and csv report, used by the search options
'''

from tkinter import *
from tkinter import font
from Code.ReportGenerator import ReportGenerator

class OptionBase:

    global localMySqlInstancePassword

    global menuManager
    global window
    global buttonFontStyle
    global xPadding
    global yPadding
    global windowTitleLabel
    global startingWindowTitle
    global mainFrame

    global reportGenerator

    def __init__(self, localMySqlInstancePassword):
        self.localMySqlInstancePassword = localMySqlInstancePassword

    '''
    
    Called when the user exits out of a 
    more specific option that was presented 
    by this option menu, allowing for this 
    option menu to be presented once more 
    
    '''
    def showMainFrameAgain(self):
        self.mainFrame.grid(row=1, column=1)
        self.setMainTitle(self.startingWindowTitle)
        self.reportGenerator.refreshReportGenerator()

    def setMainTitle(self, titleToChangeTo):
        self.windowTitleLabel['text'] = titleToChangeTo

    '''
    
    Called when this options window closes, 
    allowing for all of the main menu buttons to 
    become active again
    
    '''
    def onWindowClose(self):
        self.menuManager.disableOrEnableAllMainMenuButtons(ACTIVE)
        self.window.destroy()

    # use this method to present the UI for this option to the user
    def manageOption(self, windowTitle, menuManager):
        self.window = Toplevel()

        # used to generate reports, both .pdf and .csv
        self.reportGenerator = ReportGenerator()

        self.xPadding = 80
        self.yPadding = 20

        fontStyle = font.Font(size=25)
        self.buttonFontStyle = font.Font(size=15)

        self.startingWindowTitle = windowTitle
        self.windowTitleLabel = Label(self.window, text=windowTitle, font=fontStyle)
        self.windowTitleLabel.grid(row=0, column=1, columnspan=3)

        self.menuManager = menuManager

        '''
        
        Creates an event for when this 
        window closes, so that onWindowClose 
        method gets called
        
        referenced from: 
        https://stackoverflow.com/questions/111155/how-do-i-handle-the-window-close-event-in-tkinter
        
        '''
        self.window.protocol("WM_DELETE_WINDOW", self.onWindowClose)

        self.window.title(windowTitle)

        # the main frame:
        self.mainFrame = LabelFrame(self.window)
        self.mainFrame.grid(row=1, column=1)
