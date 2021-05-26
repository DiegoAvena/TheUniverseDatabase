'''

---Summary---
This class contains all of the methods needed for
validating data the user inputs through the input fields
that are made available through specific options like NewGalaxyInsertionManager,
etc.

It also forms an error message if it finds errors that those specific options can
then use to display to the user, telling the user what they need to fix
in order to proceed with their commands

'''

class InsertionValidator:

    global errorMessage

    def __init__(self):
        self.errorMessage = ""

    def checkIfUserTryingToDeleteValue(self, valueToCheck):
        if (valueToCheck.upper() == 'N/A'):
            return True
        return False

    def makeSureDecimalIsWithinACertainRange(self, decimalToValidate, nameOfValueBeingChecked, canBeEmpty, bottomBound, topBound):
        if (len(decimalToValidate) == 0 or (decimalToValidate == '')):
            if (canBeEmpty == False):
                self.errorMessage += nameOfValueBeingChecked + " cannot be empty" + "\n"
                return False
            else:
                # value is empty, nothing to worry about here:
                return True

        try:
            decimalCheck = float(decimalToValidate)
            if ((decimalCheck < bottomBound) or (decimalCheck > topBound)):
                self.errorMessage += nameOfValueBeingChecked + " must be between " + str(bottomBound) + " and " + str(topBound) + "\n"
                return False
        except:
            self.errorMessage += nameOfValueBeingChecked + " must be a numeric value" + "\n"
            return False

        return True



    def validateWord(self, canBeEmpty, wordToValidate, nameOfValueBeingChecked):
        if ((len(wordToValidate) == 0) or (wordToValidate == 'N/A')):
            if (canBeEmpty == False):
                self.errorMessage += nameOfValueBeingChecked + " cannot be empty" + "\n"
                return False

        return True


    def validateInteger(self, integerToValidate, canBeNegative, nameOfValueBeingChecked, canBeEmpty):

        if (len(integerToValidate) == 0):

            if (canBeEmpty):
                # value was empty, so nothing to worry about
                return True
            else:
                self.errorMessage += (nameOfValueBeingChecked + " cannot be left empty" + "\n")
                return False

        try:
            integerCheck = int(integerToValidate)
            if (canBeNegative == False):
                return self.determineIfValueIsNotNegative(integerCheck, nameOfValueBeingChecked)
        except:
            self.errorMessage += (nameOfValueBeingChecked + " must be an integer" + "\n")
            return False

        return True

    def determineIfValueIsNotNegative(self, valueToCheck, nameOfValueBeingChecked):
        if (valueToCheck < 0):
            self.errorMessage += nameOfValueBeingChecked + " must be >= 0" + "\n"
            return False

        return True

    def validateYear(self, yearToValidate, nameOfValueBeingChecked):
        if len(yearToValidate) > 4:
            self.errorMessage += nameOfValueBeingChecked + "must not exceed 4 digits."
            return False

        return self.validateInteger(yearToValidate, False, nameOfValueBeingChecked, True)


    def validateDecimalValue(self, decimalToValidate, canBeNegative, nameOfValueBeingChecked, canBeEmpty):
        if (len(decimalToValidate) == 0):

            if (canBeEmpty):
                # value was empty, so nothing to worry about
                return True
            else:
                self.errorMessage += nameOfValueBeingChecked + " cannot be left empty" + "\n"
                return False

        try:
            decimalCheck = float(decimalToValidate)
            if (canBeNegative == False):
                return self.determineIfValueIsNotNegative(decimalCheck, nameOfValueBeingChecked)
        except:
            self.errorMessage += nameOfValueBeingChecked + " must be a numeric value " + "\n"
            return False

        return True

    def obtainFinalValue(self, value):
        if ((len(value) == 0) or (value == 'N/A') or (value == '')):
            return None
        return value