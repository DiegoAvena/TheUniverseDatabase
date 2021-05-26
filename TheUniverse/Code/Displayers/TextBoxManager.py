'''

----SUMMARY----
This class contains the functionality needed to
display a large chunk of text inside of a scrollable
textbox. It also contains the functionality needed to ask
the user to select a text file they want to load in and view
from within the app

---Imports---
tkinter - used for all of the UI

filedialog:
used to prompt the user for the location of a text file
they wish to view

font:
used to set up the font needed for
the load description button

'''

from tkinter import *
from tkinter import filedialog
from tkinter import font

class TextBoxManager:
    global loadDescriptionDirectoryButton
    global descriptionDirectoryLabel
    global initialDescriptionDirectoryLabelPos
    global descriptionFileContentsText
    global descriptionDirectory
    global description
    global scrollBar
    global frameThisTextBoxHasBeenPlacedOn
    global buttonFontStyle
    global descriptionLoaded
    global initialFramePos
    global text

    def hideDescriptionUI(self):
        self.descriptionDirectoryLabel.grid_forget()
        self.descriptionContentsFrame.grid_forget()

    def showAllDescriptionUI(self):
        self.descriptionContentsFrame.grid(row=self.initialFramePos[0], column=self.initialFramePos[1], columnspan=2)
        self.descriptionDirectoryLabel.grid(row=self.initialDescriptionDirectoryLabelPos[0],
                                            column=self.initialDescriptionDirectoryLabelPos[1], columnspan=2)

    def resetDescriptionUI(self, directoryLabelRow, directoryLabelColumn):
        self.descriptionLoaded = False
        self.descriptionDirectoryLabel.grid_forget()
        self.descriptionDirectoryLabel.destroy()
        self.descriptionDirectoryLabel = Label(self.frameThisTextBoxHasBeenPlacedOn, text="No description loaded!")
        self.descriptionDirectoryLabel.grid(row=directoryLabelRow, column=directoryLabelColumn, columnspan=2)

        self.text = "NO DESCRIPTION"
        self.descriptionFileContentsText.configure(state=NORMAL)
        self.descriptionFileContentsText.delete(1.0, END)
        self.descriptionFileContentsText.insert(END, "[DESCRIPTION CONTENTS WILL DISPLAY HERE ONCE IT IS LOADED]")
        self.descriptionFileContentsText.configure(state=DISABLED)

    def loadDescription(self):
        self.descriptionDirectory = filedialog.askopenfilename(title='Select description file',
                                                               filetypes=(('txt files', '*.txt'),))
        try:
            with open(self.descriptionDirectory) as descriptionFile:
                lines = descriptionFile.readlines()
                self.text = ""
                for line in lines:
                    self.text += line

                self.descriptionFileContentsText.configure(state=NORMAL)
                self.descriptionFileContentsText.delete(1.0, END)
                self.descriptionFileContentsText.insert(END, self.text)
                self.descriptionFileContentsText.configure(state=DISABLED)

                self.descriptionDirectoryLabel.grid_forget()
                self.descriptionDirectoryLabel.destroy()
                self.descriptionDirectoryLabel = Label(self.frameThisTextBoxHasBeenPlacedOn, text=self.descriptionDirectory)
                self.descriptionDirectoryLabel.grid(row=self.initialDescriptionDirectoryLabelPos[0], column=self.initialDescriptionDirectoryLabelPos[1], columnspan=2)
                self.descriptionLoaded = True
        except:
            self.descriptionDirectory = ''
            self.text= "NO DESCRIPTION"
            self.descriptionFileContentsText.configure(state=NORMAL)
            self.descriptionFileContentsText.delete(1.0, END)
            self.descriptionFileContentsText.insert(END, self.text)
            self.descriptionFileContentsText.configure(state=DISABLED)

            self.descriptionDirectoryLabel.grid_forget()
            self.descriptionDirectoryLabel.destroy()
            self.descriptionDirectoryLabel = Label(self.frameThisTextBoxHasBeenPlacedOn, text="NO DESCRIPTION")
            self.descriptionDirectoryLabel.grid(row=self.initialDescriptionDirectoryLabelPos[0],
                                                column=self.initialDescriptionDirectoryLabelPos[1], columnspan=2)
            self.descriptionLoaded = False
            print("Failed to load description")

    def loadDescriptionWithoutPromptingUser(self, descriptionDirectory):
        self.descriptionDirectory = descriptionDirectory

        try:
            with open(self.descriptionDirectory) as descriptionFile:
                lines = descriptionFile.readlines()
                self.text = ""
                for line in lines:
                    self.text += line

                self.descriptionFileContentsText.configure(state=NORMAL)
                self.descriptionFileContentsText.delete(1.0, END)
                self.descriptionFileContentsText.insert(END, self.text)
                self.descriptionFileContentsText.configure(state=DISABLED)

                self.descriptionDirectoryLabel.grid_forget()
                self.descriptionDirectoryLabel.destroy()
                self.descriptionDirectoryLabel = Label(self.frameThisTextBoxHasBeenPlacedOn, text="Current description directory: " + self.descriptionDirectory)
                self.descriptionDirectoryLabel.grid(row=self.initialDescriptionDirectoryLabelPos[0], column=self.initialDescriptionDirectoryLabelPos[1], columnspan=2)
                self.descriptionLoaded = True
        except:
            self.descriptionDirectory = ''
            self.descriptionFileContentsText.configure(state=NORMAL)
            self.descriptionFileContentsText.delete(1.0, END)
            self.text="NO DESCRIPTION"
            self.descriptionFileContentsText.insert(END, self.text)
            self.descriptionFileContentsText.configure(state=DISABLED)

            self.descriptionDirectoryLabel.grid_forget()
            self.descriptionDirectoryLabel.destroy()
            self.descriptionDirectoryLabel = Label(self.frameThisTextBoxHasBeenPlacedOn, text="NO DESCRIPTION")
            self.descriptionDirectoryLabel.grid(row=self.initialDescriptionDirectoryLabelPos[0],
                                                column=self.initialDescriptionDirectoryLabelPos[1], columnspan=2)
            self.descriptionLoaded = False
            print("Failed to load description")

    def initializeDescriptionBoxForReadingOnlyAndNotLoading(self, frameThisTextBoxHasBeenPlacedOn, directoryLabelRow, directoryLabelColumn, frameRow, frameColumn):
        self.descriptionLoaded = False
        self.descriptionDirectory = ""

        self.frameThisTextBoxHasBeenPlacedOn = frameThisTextBoxHasBeenPlacedOn

        self.descriptionDirectoryLabel = Label(self.frameThisTextBoxHasBeenPlacedOn, text="No description loaded!")
        self.descriptionDirectoryLabel.grid(row=directoryLabelRow, column=directoryLabelColumn, columnspan=2)

        self.initialDescriptionDirectoryLabelPos = []
        self.initialDescriptionDirectoryLabelPos.append(directoryLabelRow)
        self.initialDescriptionDirectoryLabelPos.append(directoryLabelColumn)

        self.description = ""

        self.initialFramePos = []
        self.initialFramePos.append(frameRow)
        self.initialFramePos.append(frameColumn)

        self.descriptionContentsFrame = LabelFrame(self.frameThisTextBoxHasBeenPlacedOn)
        self.descriptionContentsFrame.grid(row=frameRow, column=frameColumn, columnspan=2)

        self.descriptionFileContentsText = Text(self.descriptionContentsFrame, width=80, height=4)
        self.descriptionFileContentsText.pack(side="left")

        self.scrollBar = Scrollbar(self.descriptionContentsFrame, orient="vertical",
                                   command=self.descriptionFileContentsText.yview)
        self.scrollBar.pack(side="left", expand=True, fill="y")

        self.descriptionFileContentsText.configure(yscrollcommand=self.scrollBar.set)
        self.text = "NO DESCRIPTION"
        self.descriptionFileContentsText.insert(END, self.text)
        self.descriptionFileContentsText.configure(state=DISABLED)

    def initializeDescriptionFormForUserLoading(self, frameThisTextBoxHasBeenPlacedOn, buttonRow, buttonColumn, directoryLabelRow, directoryLabelColumn, frameRow, frameColumn):
        self.descriptionLoaded = False
        self.descriptionDirectory = ""
        self.text = "NO DESCRIPTION"

        self.frameThisTextBoxHasBeenPlacedOn = frameThisTextBoxHasBeenPlacedOn

        self.buttonFontStyle = font.Font(size=15)
        self.loadDescriptionDirectoryButton = Button(self.frameThisTextBoxHasBeenPlacedOn, text="LOAD DESCRIPTION",
                                                     font=self.buttonFontStyle, padx=80,
                                                     pady=10, command=self.loadDescription)
        self.loadDescriptionDirectoryButton.grid(row=buttonRow, column=buttonColumn, columnspan=2, sticky=W + E)
        self.descriptionDirectoryLabel = Label(self.frameThisTextBoxHasBeenPlacedOn, text="No description loaded!")
        self.descriptionDirectoryLabel.grid(row=directoryLabelRow, column=directoryLabelColumn, columnspan=2)

        self.initialDescriptionDirectoryLabelPos = []
        self.initialDescriptionDirectoryLabelPos.append(directoryLabelRow)
        self.initialDescriptionDirectoryLabelPos.append(directoryLabelColumn)

        self.description = ""

        self.initialFramePos = []
        self.initialFramePos.append(frameRow)
        self.initialFramePos.append(frameColumn)

        self.descriptionContentsFrame = LabelFrame(self.frameThisTextBoxHasBeenPlacedOn)
        self.descriptionContentsFrame.grid(row=frameRow, column=frameColumn, columnspan=2)

        self.descriptionFileContentsText = Text(self.descriptionContentsFrame, width=80, height=4)
        self.descriptionFileContentsText.pack(side="left")

        self.scrollBar = Scrollbar(self.descriptionContentsFrame, orient="vertical",
                                   command=self.descriptionFileContentsText.yview)
        self.scrollBar.pack(side="left", expand=True, fill="y")

        self.descriptionFileContentsText.configure(yscrollcommand=self.scrollBar.set)
        self.descriptionFileContentsText.insert(END, "[DESCRIPTION CONTENTS WILL DISPLAY HERE ONCE IT IS LOADED]")
        self.descriptionFileContentsText.configure(state=DISABLED)
