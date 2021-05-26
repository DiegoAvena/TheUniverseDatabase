'''

----SUMMARY----
Contains base functionality needed for
a more specific insertion option that inserts a
record into the database, such as the creation of the
image loader, the creation of the description loader,
etc.

Also:

This class was written before I decided to make
individual classes for image displaying and text displaying,
so this is why those 2 things are created directly in here rather than
through the use of those other 2 classes. I left it this way
because I did not want to break anything.

----Imports----
tkinter - for all of the UI

filedialog from tkinter:
to prompt the user for where they wish to load an image
or description from

BaseDataModifierManager:
used for base data base modifying functionality,
since this specific option will be modifying the table
with insertions

ImageTk and Image from PIL:
This is needed in order to display images

'''

from tkinter import *
from tkinter import filedialog
from Code.BaseDataModifierManager import BaseDataModifierManager
from PIL import ImageTk, Image

class BaseInsertionManager(BaseDataModifierManager):

    # displaying the image of the item that will be inserted
    global imageDirLabel
    global imageDirLabelPos
    global loadImageDirectoryButton
    global imageDir
    global imageCanvas
    global itemImage

    global loadDescriptionDirectoryButton
    global descriptionDirectoryLabel
    global initialDescriptionDirectoryLabelPos
    global descriptionFileContentsText
    global descriptionDirectory
    global description
    global scrollBar

    def initializeDescriptionForm(self, buttonRow, buttonColumn, directoryLabelRow, directoryLabelColumn, frameRow, frameColumn):
        self.descriptionDirectory = ""
        self.loadDescriptionDirectoryButton = Button(self.insertionFrame, text="LOAD DESCRIPTION",
                                                     font=self.buttonFontStyle, padx=80,
                                                     pady=10, command=self.loadDescription)
        self.loadDescriptionDirectoryButton.grid(row=buttonRow, column=buttonColumn, columnspan=2, sticky=W + E)
        self.descriptionDirectoryLabel = Label(self.insertionFrame, text="No description loaded!")
        self.descriptionDirectoryLabel.grid(row=directoryLabelRow, column=directoryLabelColumn, columnspan=2)

        self.initialDescriptionDirectoryLabelPos = []
        self.initialDescriptionDirectoryLabelPos.append(directoryLabelRow)
        self.initialDescriptionDirectoryLabelPos.append(directoryLabelColumn)

        self.description = ""

        descriptionContentsFrame = LabelFrame(self.insertionFrame)
        descriptionContentsFrame.grid(row=frameRow, column=frameColumn, columnspan=2)

        self.descriptionFileContentsText = Text(descriptionContentsFrame, width=80, height=4)
        self.descriptionFileContentsText.pack(side="left")

        self.scrollBar = Scrollbar(descriptionContentsFrame, orient="vertical",
                                   command=self.descriptionFileContentsText.yview)
        self.scrollBar.pack(side="left", expand=True, fill="y")

        self.descriptionFileContentsText.configure(yscrollcommand=self.scrollBar.set)
        self.descriptionFileContentsText.insert(END, "[DESCRIPTION CONTENTS WILL DISPLAY HERE ONCE IT IS LOADED]")
        self.descriptionFileContentsText.configure(state=DISABLED)

    def resetDescriptionUI(self, directoryLabelRow, directoryLabelColumn):
        self.descriptionDirectoryLabel.grid_forget()
        self.descriptionDirectoryLabel.destroy()
        self.descriptionDirectoryLabel = Label(self.insertionFrame, text="No description loaded!")
        self.descriptionDirectoryLabel.grid(row=directoryLabelRow, column=directoryLabelColumn, columnspan=2)

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
                text = ""
                for line in lines:
                    text += line

                self.descriptionFileContentsText.configure(state=NORMAL)
                self.descriptionFileContentsText.delete(1.0, END)
                self.descriptionFileContentsText.insert(END, text)
                self.descriptionFileContentsText.configure(state=DISABLED)

                self.descriptionDirectoryLabel.grid_forget()
                self.descriptionDirectoryLabel.destroy()
                self.descriptionDirectoryLabel = Label(self.insertionFrame, text=self.descriptionDirectory)
                self.descriptionDirectoryLabel.grid(row=self.initialDescriptionDirectoryLabelPos[0], column=self.initialDescriptionDirectoryLabelPos[1], columnspan=2)

                print(text)
        except:
            self.descriptionDirectory = ''
            print("Failed to load description")

    def openImage(self):
        self.imageDir = filedialog.askopenfilename(title='Select image', filetypes=(('png files', '*.png'), ('jpg files', '*.jpg')))

        try:
            self.itemImage = ImageTk.PhotoImage(Image.open(self.imageDir).resize((65, 65), Image.ANTIALIAS))
            self.imageCanvas.create_image(5, 5, anchor=NW, image=self.itemImage)

            self.imageDirLabel.grid_forget()
            self.imageDirLabel.destroy()
            self.imageDirLabel = Label(self.insertionFrame, text=self.imageDir)
            self.imageDirLabel.grid(row=self.imageDirLabelPos[0], column=self.imageDirLabelPos[1], columnspan=2)

        except:
            print("Failed to open image")
            self.imageDir = ''

    def initializeImageDirLabelPos(self, row, column, columnspan):
        self.imageDirLabel.grid(row=row, column=column, columnspan=columnspan)
        self.imageDirLabelPos = []
        self.imageDirLabelPos.append(row)
        self.imageDirLabelPos.append(column)

    def resetImageUI(self, columnspan):
        self.imageDirLabel.grid_forget()
        self.imageDirLabel.destroy()
        self.imageDirLabel = Label(self.insertionFrame, text="No Image")
        self.imageDirLabel.grid(row=self.imageDirLabelPos[0], column=self.imageDirLabelPos[1], columnspan=columnspan)
        self.galaxyImage = ImageTk.PhotoImage(Image.open("noImage.jpg").resize((250, 250), Image.ANTIALIAS))
        self.imageCanvas.create_image(5, 5, anchor=NW, image=self.galaxyImage)

    def manageInsertion(self, windowToPutFrameOnto, insertionManager, insertionTitle):

        BaseDataModifierManager.manageBaseModifierManager(self, windowToPutFrameOnto, insertionManager, insertionTitle)
        self.successMessage = "Record added!"
        self.errorMessageForWhenCommitFailsDueToSqlError = 'FAILED TO INSERT NEW RECORDS FOR SOME REASON, ROLLING BACK CHANGES...'

        # images
        self.imageDir = ""
        self.loadImageDirectoryButton = Button(self.insertionFrame, text="Load image",
                                                     font=self.buttonFontStyle, padx=80, pady=10,
                                                     command=self.openImage)

        self.imageDirLabel = Label(self.insertionFrame, text="No image loaded")

        self.itemImage = ImageTk.PhotoImage(Image.open("noImage.jpg").resize((65, 65), Image.ANTIALIAS))
        self.imageCanvas = Canvas(self.insertionFrame, width=65, height=65)
        self.imageCanvas.create_image(5, 5, anchor=NW, image=self.itemImage)
