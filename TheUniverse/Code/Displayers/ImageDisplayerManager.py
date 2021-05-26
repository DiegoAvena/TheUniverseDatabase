'''

----SUMMARY----
This class contains the functionality needed to display
images or ask the user to load in an image

----IMPORTS----
tkinter - for all the UI

filedialog from tkinter:
used to prompt the user to load an image
in

font from tkinter:
used to set up the font needed for the load
image button

ImageTk and Image from PIL - needed in order to display images

'''

from tkinter import *
from tkinter import filedialog
from tkinter import font
from PIL import ImageTk, Image

class ImageDisplayerManager:

    global buttonFontStyle

    global imageDirLabel
    global imageDirLabelPos
    global columnSpan
    global loadImageDirectoryButton
    global imageDir
    global imageCanvas
    global imageCanvasRow
    global itemImage
    global frameImageIsOn

    global imageLoaded

    def openImage(self, askUserToSelectImage, imageDir):

        if (askUserToSelectImage):
            self.imageDir = filedialog.askopenfilename(title='Select image', filetypes=(('png files', '*.png'), ('jpg files', '*.jpg')))
        else:
            self.imageDir = imageDir

        try:

            if (self.imageDir == None):
                self.itemImage = ImageTk.PhotoImage(Image.open('noImage.jpg').resize((65, 65), Image.ANTIALIAS))
                self.imageDir = 'No Image loaded'
                self.imageLoaded = False
            else:

                self.itemImage = ImageTk.PhotoImage(Image.open(self.imageDir).resize((65, 65), Image.ANTIALIAS))
                self.imageLoaded = True

            self.updateImageCanvas()

            self.imageDirLabel.grid_forget()
            self.imageDirLabel.destroy()
            self.imageDirLabel = Label(self.frameImageIsOn, text=self.imageDir)
            self.imageDirLabel.grid(row=self.imageDirLabelPos[0], column=self.imageDirLabelPos[1], columnspan=self.columnSpan)

        except:
            self.imageLoaded = False
            failedDir = self.imageDir
            self.imageDir = 'imageLoadFail.png'
            self.itemImage = ImageTk.PhotoImage(Image.open(self.imageDir).resize((65, 65), Image.ANTIALIAS))
            self.updateImageCanvas()

            self.imageDirLabel.grid_forget()
            self.imageDirLabel.destroy()
            self.imageDirLabel = Label(self.frameImageIsOn, text="Failed to load image at: " + failedDir)
            self.imageDirLabel.grid(row=self.imageDirLabelPos[0], column=self.imageDirLabelPos[1],
                                    columnspan=self.columnSpan)

    def hideAllImageUI(self):
        self.imageDirLabel.grid_forget()
        self.imageCanvas.grid_forget()

    def showAllImageUI(self):
        self.imageDirLabel.grid(row=self.imageDirLabelPos[0], column=self.imageDirLabelPos[1],
                                columnspan=self.columnSpan)
        self.imageCanvas.grid(row=self.imageCanvasRow, column=self.imageDirLabelPos[1], columnspan=self.columnSpan)

    def resetImageUI(self):
        self.imageDirLabel.grid_forget()
        self.imageDirLabel.destroy()
        self.imageDirLabel = Label(self.frameImageIsOn, text="No Image")
        self.imageDirLabel.grid(row=self.imageDirLabelPos[0], column=self.imageDirLabelPos[1], columnspan=self.columnSpan)
        self.itemImage = ImageTk.PhotoImage(Image.open("noImage.jpg").resize((250, 250), Image.ANTIALIAS))
        self.updateImageCanvas()
        self.imageLoaded = False

    def updateImageCanvas(self):

        self.imageCanvas.grid_forget()
        self.imageCanvas.destroy()

        self.imageCanvas = Canvas(self.frameImageIsOn, width=65, height=65)
        self.imageCanvas.grid(row=self.imageCanvasRow, column=self.imageDirLabelPos[1], columnspan=self.columnSpan)
        self.imageCanvas.create_image(5, 5, anchor=NW, image=self.itemImage)

    def initializeImageDisplayer(self, row, column, columnspan, frameImageIsOn, imageDir, allowUserToLoadImagesIn):

        self.buttonFontStyle = font.Font(size=15)

        self.imageDir = ""
        self.frameImageIsOn = frameImageIsOn
        self.loadImageDirectoryButton = Button(self.frameImageIsOn, text="Load image",
                                               font=self.buttonFontStyle, padx=80, pady=10,
                                               command=self.openImage)

        self.imageDirLabel = Label(self.frameImageIsOn, text="No image loaded")
        self.imageDirLabelPos = [row, column]
        self.columnSpan = columnspan
        self.imageDirLabel.grid(row=row, column=column, columnspan=columnspan)

        if (allowUserToLoadImagesIn):
            # place load image button in:
            self.loadImageDirectoryButton = Button(self.frameImageIsOn, text="Load image",
                                                   font=self.buttonFontStyle, padx=80, pady=10,
                                                   command=lambda: self.openImage(True, None))
            self.loadImageDirectoryButton.grid(row=row+1, column=column, columnspan = columnspan)
            self.imageCanvasRow = row + 2
        else:
            self.imageCanvasRow = row + 1

        self.itemImage = ImageTk.PhotoImage(Image.open("noImage.jpg").resize((65, 65), Image.ANTIALIAS))
        self.imageCanvas = Canvas(self.frameImageIsOn, width=65, height=65)
        self.imageCanvas.grid(row=self.imageCanvasRow, column=column, columnspan=columnspan)
        self.imageCanvas.create_image(5, 5, anchor=NW, image=self.itemImage)

        self.imageDir = imageDir
        self.openImage(False, self.imageDir)
