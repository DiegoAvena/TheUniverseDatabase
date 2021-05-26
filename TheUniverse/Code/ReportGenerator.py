'''

-----SUMMARY----
Responsible for producing both a pdf and csv report out of the
record supplied by the option calling on it. These reports are saved
in a directory called pdfReports or a directory called csvReports depending
on the report type

-----IMPORTS-----
FPDF - used for the generation of pdf reports
csv - used fot the generation of csv reports
os - used to obtain the path to the report directories or create them if they do not exist

'''

from fpdf import FPDF
import csv
import os

class ReportGenerator:

    global pdf
    global csvFileToWriteTo
    global records # stores the data that will be written to the reports
    global pdfSaveDirectory
    global csvSaveDirectory

    def __init__(self):
        self.records = []
        self.refreshReportGenerator()
        self.pdfSaveDirectory = "pdfReports/"
        self.csvSaveDirectory = "csvReports/"

    # clears any report data that was created
    def refreshReportGenerator(self):
        self.pdf = FPDF()
        self.records.clear()

    '''
    
    Use this method to save all of the initialized reports 
    to a .csv file and a .pdf file inside of a set pdf and set 
    csv directory. 
      
    '''
    def saveGeneratedReports(self, pdfName):

        completePDFName = os.path.join(self.pdfSaveDirectory, pdfName + ".pdf")
        if not os.path.exists(self.pdfSaveDirectory):
            os.makedirs(self.pdfSaveDirectory)

        self.pdf.output(completePDFName)

        completeCSVName = os.path.join(self.csvSaveDirectory, pdfName+".csv")
        if not os.path.exists(self.csvSaveDirectory):
            os.makedirs(self.csvSaveDirectory)

        csvFileToWriteTo = open(completeCSVName, "w")
        csvWriter = csv.writer(csvFileToWriteTo)
        csvWriter.writerows(self.records)
        csvFileToWriteTo.close()

    '''
    
    this method is used to initialize all report data that will potentially 
    be saved; this means that it does not actually yet store any reports, 
    it only preps things needed to save them 
    
    '''
    def generateReports(self, records, imageDirectory, attributeNames):

        if (len(self.records) == 0):
            self.records.append(attributeNames)

        self.records.append(records)

        self.pdf.add_page()
        self.pdf.set_font("Arial", size=15)
        for i in range(0, len(records)):
            if ((imageDirectory == None) or (str(records[i]) != imageDirectory)):
                self.pdf.cell(200, 10, txt=attributeNames[i] + str(records[i]), ln=1, align='L')
            else:
                # this is an image:
                try:
                    self.pdf.image(imageDirectory, w=80, h=80)
                except:
                    continue

