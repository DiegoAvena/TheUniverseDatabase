'''
---------Summary---------:

Connects to the local MySQL database
or creates it if it does not exits. Due
to this, this class also contains
all of the DDL mySQL code, such
as CREATE TABLE, CREATE VIEW, etc.

---------Imports-------:
connector - used to make the connection to the database or initialize it
copy - used for deepcopy

'''

import mysql.connector
import copy
from tkinter import *
from tkinter import font

class DataLoader:

    global root
    global errorLabel
    global passwordInputBox
    global password

    global csvName

    def __init__(self, csvName):
        self.csvName = csvName

    def initializeDatabase(self):
        self.root = Tk()
        self.root.title("Database initializer")

        self.errorLabel = None

        fontStyle = font.Font(size=50)
        buttonFontStyle = font.Font(size=15)
        title = Label(self.root, text="Database login", font=fontStyle)
        title.grid(row=0, column=0, columnspan=2)

        Label(self.root, text="Enter the password for your localMySQL instance:").grid(row=1, column=0)
        self.passwordInputBox = Entry(self.root, width=50, borderwidth=1)
        self.passwordInputBox.grid(row=1, column=1)

        # the confirm bitton
        Button(self.root, padx=80, pady=20, text="Confirm password and initialize database?", font=buttonFontStyle,
               command=self.connectToLocalMySQLInstance).grid(row=2, column=0, columnspan=2, sticky=W + E)

        self.root.mainloop()

    def connectToLocalMySQLInstance(self):

        try:
            self.password = self.passwordInputBox.get()
            database = mysql.connector.connect(host="localhost",
                                               user="root",
                                               password=self.password,
                                               auth_plugin='mysql_native_password',
                                               )

            cursor = database.cursor()

            # check if the database exists already before
            # trying to create it
            cursor.execute("SHOW DATABASES")
            for DB in cursor:
                if (DB[0].lower() == "theuniverse"):
                    dataBase = mysql.connector.connect(host="localhost",
                                                       user="root",
                                                       password=self.password,
                                                       auth_plugin='mysql_native_password',
                                                       database='TheUniverse'
                                                       )
                    print("Database existed!")
                    # shut down the password window to make way for the main program window:
                    self.root.destroy()
                    return dataBase

            print("The universe database did not exist, creating it...")
            database = mysql.connector.connect(host="localhost",
                                               user="root",
                                               password=self.password,
                                               auth_plugin='mysql_native_password',
                                               )

            # use the connection to the local instance to create database:
            cursor = database.cursor()
            cursor.execute("CREATE DATABASE TheUniverse;")

            # connect to the universe database now:
            database = mysql.connector.connect(host="localhost",
                                               user="root",
                                               password=self.password,
                                               auth_plugin='mysql_native_password',
                                               database='TheUniverse'
                                               )
            cursor = database.cursor()

            # create the tables in this database now:
            # NOTE: for years, I went with the FLOAT
            # datatype because for some reason the YEAR
            # datatype was causing years to become 0 if they
            # were from say 1900s and below...
            planetsTableCommand = '''

                                    CREATE TABLE Planets (

                                        Name VARCHAR(80) PRIMARY KEY,
                                        Mass FLOAT,
                                        Gravity FLOAT,
                                        Radius FLOAT,
                                        DistanceFromEarth DOUBLE NOT NULL,
                                        EquilibriumTemperature FLOAT,
                                        ESI FLOAT,
                                        RotationPeriod FLOAT,
                                        OrbitalPeriod FLOAT,
                                        EscapeVelocity FLOAT,
                                        ImageDirectory TEXT,
                                        DescriptionDirectory TEXT

                                    );

                                '''

            cursor.execute(planetsTableCommand)

            dwarfPlanetsTableCommand = '''

                                    CREATE TABLE DwarfPlanets (

                                        Name VARCHAR(80) PRIMARY KEY

                                    );

                                '''

            cursor.execute(dwarfPlanetsTableCommand)

            planetsInHabitZoneCommand = '''

                                    CREATE TABLE PlanetsInHabitZone (

                                        Name VARCHAR(80) PRIMARY KEY

                                    );

                                '''

            cursor.execute(planetsInHabitZoneCommand)

            starsPlanetsOrbitCommand = '''

                                    CREATE TABLE StarsPlanetsOrbit (

                                        StarName VARCHAR(80),
                                        PlanetName VARCHAR(80),

                                        CONSTRAINT PK_StarsPlanetsOrbit PRIMARY KEY (StarName, PlanetName)

                                    );

                                '''

            cursor.execute(starsPlanetsOrbitCommand)

            planetAtmospheresCommand = '''

                                    CREATE TABLE PlanetAtmospheres (

                                        Name VARCHAR(80),
                                        Gas VARCHAR(25),
                                        CONSTRAINT PK_PlanetAtmospheres PRIMARY KEY (Name, Gas)

                                    );

                                '''

            cursor.execute(planetAtmospheresCommand)

            planetarySystemsCommand = '''

                                    CREATE TABLE PlanetarySystems (

                                        Name VARCHAR(80) PRIMARY KEY,
                                        DistanceFromEarth DOUBLE NOT NULL ,
                                        GalaxyName VARCHAR(80)

                                    );

                                '''

            cursor.execute(planetarySystemsCommand)

            galaxiesCommand = '''

                                    CREATE TABLE Galaxies (

                                    Name VARCHAR(80) PRIMARY KEY,
                                    NumberOfStars BIGINT UNSIGNED,
                                    Age FLOAT,
                                    DistanceFromEarth DOUBLE NOT NULL,
                                    Mass FLOAT,
                                    YearDiscovered FLOAT,
                                    ImageDirectory TEXT,
                                    GalaxyType VARCHAR(80)

                                );

                                '''

            cursor.execute(galaxiesCommand)

            evolutionaryStagesCommand = '''

                                    CREATE TABLE EvolutionaryStages (

                                        EvolutionaryStage VARCHAR(80) PRIMARY KEY,
                                        Description TEXT

                                    );

                                '''

            cursor.execute(evolutionaryStagesCommand)

            starsCommand = '''

                                    CREATE TABLE Stars (

                                        Name VARCHAR(80) PRIMARY KEY,
                                        Mass FLOAT,
                                        Radius FLOAT,
                                        EvolutionaryStage VARCHAR(80),
                                        DistanceFromEarth DOUBLE NOT NULL,
                                        PlanetarySystem VARCHAR(80),
                                        ImageDirectory TEXT

                                    );

                                '''

            cursor.execute(starsCommand)

            galaxyTypeCommand = '''

                                    CREATE TABLE GalaxyTypes (

                                        GalaxyType VARCHAR(80) PRIMARY KEY,
                                        Description TEXT NOT NULL

                                    );

                                '''

            cursor.execute(galaxyTypeCommand)

            moonsCommand = '''

                                    CREATE TABLE Moons (

                                        Name VARCHAR(80) PRIMARY KEY,
                                        Mass FLOAT,
                                        PlanetItOrbits VARCHAR(80),
                                        Gravity FLOAT,
                                        Radius FLOAT,
                                        DistanceFromEarth DOUBLE,
                                        MeanSurfaceTemperature FLOAT,
                                        EscapeVelocity FLOAT,
                                        RotationPeriod FLOAT,
                                        OrbitalPeriod FLOAT,
                                        ImageDirectory TEXT,
                                        Description TEXT,
                                        DistanceFromPlanetItOrbits FLOAT

                                    );

                                '''

            cursor.execute(moonsCommand)

            galaxyDiscovers = '''

                                    CREATE TABLE GalaxyDiscovers(

                                        GalaxyName VARCHAR(80),
                                        DiscovererName VARCHAR(80),

                                        CONSTRAINT PK_GalaxyDiscovers PRIMARY KEY (GalaxyName, DiscovererName)

                                );

                                '''

            cursor.execute(galaxyDiscovers)

            moonDiscoverers = '''

                                    CREATE TABLE MoonDiscovers (

                                        DiscovererName VARCHAR(80),
                                        MoonName VARCHAR(80),
                                        DiscoveryYear INT,
                                        CONSTRAINT PK_GalaxyDiscovers PRIMARY KEY (MoonName, DiscovererName)

                                    );

                                '''

            cursor.execute(moonDiscoverers)

            # add in indexes:
            index = '''

                        CREATE INDEX planetNameIndex 
                            ON Planets(Name);

                    '''
            cursor.execute(index)

            index = '''

                        CREATE INDEX dwarfPlanetIndex
                            ON DwarfPlanets(Name);

                    '''
            cursor.execute(index)

            index = '''

                        CREATE INDEX planetsInHabitZoneIndex 
                            ON PlanetsInHabitZone(Name);

                    '''
            cursor.execute(index)

            # according to mysql docs, this index can be used in where clauses that
            # use both these values or in where clauses where it is only StarName
            # being checked
            index = '''

                        CREATE INDEX starNameAndPlanetThatOrbitsItIndex
                            ON StarsPlanetsOrbit(StarName, PlanetName);

                    '''
            cursor.execute(index)

            # since the above index cannot be used in queries where the where only contains
            # PlanetName, I create a index for just this column right here
            index = '''

                        CREATE INDEX nameOfPlanetInStarsPlanetsOrbitIndex
                            ON StarsPlanetsOrbit(PlanetName);

                    '''
            cursor.execute(index)

            # idea for these indexes is the same as mentioned above
            index = '''

                        CREATE INDEX planetNameAndTheGasInItsAtmosphereIndex
                            ON PlanetAtmospheres(Name, Gas);

                    '''
            cursor.execute(index)

            index = '''

                        CREATE INDEX nameOfGasInPlanetAtmospheresIndex
                            ON PlanetAtmospheres(Gas);

                    '''
            cursor.execute(index)

            index = '''

                        CREATE INDEX nameOfSystemIndex
                            ON PlanetarySystems(Name);

                    '''
            cursor.execute(index)

            index = '''

                        CREATE INDEX nameOfGalaxyPlanetarySystemIsInIndex
                            ON PlanetarySystems(GalaxyName);

                    '''
            cursor.execute(index)

            index = '''

                        CREATE INDEX nameOfGalaxyIndex
                            ON Galaxies(Name);

                    '''
            cursor.execute(index)

            index = '''

                        CREATE INDEX typeOfGalaxyAGalaxyIsIndex
                            ON Galaxies(GalaxyType);

                    '''
            cursor.execute(index)

            index = '''

                        CREATE INDEX evolutionaryStageNameIndex
                            ON EvolutionaryStages(EvolutionaryStage);

                    '''
            cursor.execute(index)

            index = '''

                        CREATE INDEX starNameIndex
                            ON Stars(Name);

                    '''
            cursor.execute(index)

            index = '''

                        CREATE INDEX planetarySystemStarIsInIndex
                            ON Stars(PlanetarySystem);

                    '''
            cursor.execute(index)

            index = '''

                        CREATE INDEX stagesOfStarsIndex
                            ON Stars(EvolutionaryStage);

                    '''
            cursor.execute(index)

            index = '''

                        CREATE INDEX galaxyTypeNameIndex
                            ON GalaxyTypes(GalaxyType);

                    '''
            cursor.execute(index)

            index = '''

                        CREATE INDEX moonNameIndex
                            ON Moons(Name);

                    '''
            cursor.execute(index)

            index = '''

                        CREATE INDEX planetMoonOrbitsIndex
                            ON Moons(PlanetItOrbits);

                    '''
            cursor.execute(index)

            index = '''

                        CREATE INDEX galaxyNameAndDiscovererIndex
                            ON GalaxyDiscovers(GalaxyName, DiscovererName);

                    '''
            cursor.execute(index)

            index = '''

                        CREATE INDEX discovererNameInGalaxyDiscoverersIndex
                            ON GalaxyDiscovers(DiscovererName);

                    '''
            cursor.execute(index)

            index = '''

                        CREATE INDEX moonNameAndDiscovererIndex
                            ON MoonDiscovers(MoonName, DiscovererName);

                    '''
            cursor.execute(index)

            index = '''

                        CREATE INDEX moonDiscovererIndex
                            ON MoonDiscovers(DiscovererName);

                    '''
            cursor.execute(index)

            # add in the foreign keys as well now:
            dwarfPlanetFK = '''

                                    ALTER TABLE DwarfPlanets ADD CONSTRAINT FK_DwarfPlanets
                                        FOREIGN KEY (Name) REFERENCES Planets (Name)
                                        ON DELETE CASCADE
                                        ON UPDATE CASCADE;

                                '''

            cursor.execute(dwarfPlanetFK)

            planetsInOrbitZoneFK = '''

                                    ALTER TABLE PlanetsInHabitZone ADD CONSTRAINT FK_PlanetsInHabitZone
                                        FOREIGN KEY (Name) REFERENCES Planets (Name)
                                        ON DELETE CASCADE
                                        ON UPDATE CASCADE;

                                '''

            cursor.execute(planetsInOrbitZoneFK)

            starsPlanetsOrbitFK = '''

                                    ALTER TABLE StarsPlanetsOrbit ADD CONSTRAINT FK_StarNamesPlanetsOrbit
                                        FOREIGN KEY (StarName) REFERENCES Stars (Name)
                                            ON DELETE CASCADE
                                            ON UPDATE CASCADE;

                                '''

            cursor.execute(starsPlanetsOrbitFK)

            starsPlanetsOrbitFKTwo = '''

                                    ALTER TABLE StarsPlanetsOrbit ADD CONSTRAINT FK_PlanetNamesInStarsPlanetsOrbit
                                        FOREIGN KEY (PlanetName) REFERENCES Planets (Name)
                                        ON DELETE CASCADE
                                        ON UPDATE CASCADE;

                                '''

            cursor.execute(starsPlanetsOrbitFKTwo)

            galaxyDiscoversFK = '''

                                    ALTER TABLE GalaxyDiscovers ADD CONSTRAINT FK_GalaxyDiscovers
                                        FOREIGN KEY (GalaxyName) REFERENCES Galaxies (Name)
                                        ON DELETE CASCADE
                                        ON UPDATE CASCADE;

                                '''

            cursor.execute(galaxyDiscoversFK)

            moonDiscoverersFK = '''


                                    ALTER TABLE MoonDiscovers ADD CONSTRAINT FK_MoonDiscovers
                                    FOREIGN KEY (MoonName) REFERENCES Moons (Name)
                                    ON DELETE CASCADE
                                    ON UPDATE CASCADE;

                                '''

            cursor.execute(moonDiscoverersFK)

            planetAtmospheresFK = '''

                                    ALTER TABLE PlanetAtmospheres ADD CONSTRAINT FK_PlanetAtmospheres
                                    FOREIGN KEY (Name) REFERENCES Planets (Name)
                                    ON DELETE CASCADE
                                    ON UPDATE CASCADE;

                                '''

            cursor.execute(planetAtmospheresFK)

            galaxiesFK = '''

                                    ALTER TABLE Galaxies ADD CONSTRAINT FK_Galaxies
                                        FOREIGN KEY (GalaxyType) REFERENCES GalaxyTypes (GalaxyType)
                                        ON DELETE SET NULL
                                        ON UPDATE CASCADE;

                                '''

            cursor.execute(galaxiesFK)

            starsFK = '''

                                    ALTER TABLE Stars ADD CONSTRAINT FK_EvolutionaryStages
                                        FOREIGN KEY (EvolutionaryStage) REFERENCES EvolutionaryStages (EvolutionaryStage)
                                        ON DELETE SET NULL
                                        ON UPDATE CASCADE;

                                '''

            cursor.execute(starsFK)

            starsFKTwo = '''

                                    ALTER TABLE Stars ADD CONSTRAINT FK_StarPlanetSystem
                                        FOREIGN KEY (PlanetarySystem) REFERENCES PlanetarySystems (Name)
                                        ON DELETE SET NULL
                                        ON UPDATE CASCADE;

                                '''

            cursor.execute(starsFKTwo)

            moonsFK = '''

                                    ALTER TABLE Moons ADD CONSTRAINT FK_PlanetMoonOrbits
                                        FOREIGN KEY (PlanetItOrbits) REFERENCES Planets (Name)
                                        ON DELETE SET NULL
                                        ON UPDATE CASCADE;

                                '''

            cursor.execute(moonsFK)

            planetarySystemsFK = '''

                                    ALTER TABLE PlanetarySystems ADD CONSTRAINT FK_GalaxySystemBelongsTo
                                        FOREIGN KEY (GalaxyName) REFERENCES Galaxies (Name)
                                        ON DELETE SET NULL
                                        ON UPDATE CASCADE;

                                '''

            cursor.execute(planetarySystemsFK)

            # views:
            exoPlanetsInHabitZoneView = '''

                        CREATE VIEW ExoPlanetsInHabitZone AS
                            SELECT ExoPlanetNames.PlanetName
                            FROM (

                                SELECT PlanetName
                                FROM StarsPlanetsOrbit
                                INNER JOIN Stars
                                    ON (Stars.Name = StarsPlanetsOrbit.StarName)
                                        AND (Stars.PlanetarySystem != 'Solar System')

                            ) AS ExoPlanetNames
                            INNER JOIN PlanetsInHabitZone
                                ON ExoPlanetNames.PlanetName = PlanetsInHabitZone.Name;

                    '''
            cursor.execute(exoPlanetsInHabitZoneView)

            # a view for all the exo planets:
            exoPlanetsView = '''

                        CREATE VIEW ExoPlanets AS
                            SELECT PlanetName
                            FROM StarsPlanetsOrbit
                            INNER JOIN Stars
                                ON (Stars.Name = StarsPlanetsOrbit.StarName)
                                AND (Stars.PlanetarySystem != 'Solar System');

                    '''
            cursor.execute(exoPlanetsView)

            # now load the base data into the DB:
            self.loadDataIntoDatabase(database)

            # shut down the password window to make way for the main program window:
            self.root.destroy()
        except:
            if (self.errorLabel == None):
                self.errorLabel = Label(self.root, text="FAILED TO CONNECT TO DATABASE WITH THAT PASSWORD, TRY AGAIN").grid(row=3, column=0, columnspan=2)

    # Load data from the raw table into the database:
    def loadDataIntoDatabase(self, databaseConnector):

        with open(self.csvName) as file:
            # skip the first line, since the first line is just the name of the columns
            file.readline()

            # get the actual data now, which follows after line 1:
            data = file.readlines()

        # databaseConnector = self.connectToLocalMySQLInstance()
        cursor = databaseConnector.cursor()

        records = []
        finalRecord = []
        formingCollection = False
        finalWordToAdd = ""
        collectionDelimiter = []
        for i in data[:]:
            i = i.strip().split(",")
            for word in i:

                finalWordToAdd += word
                # check if a collection needs to be formed:
                for char in word:
                    if (char == '['):
                        formingCollection = True
                        collectionDelimiter.append('[')

                    elif (char == ']'):
                        try:
                            collectionDelimiter.pop()
                        except:
                            print("FAILED TO POP ITEM AT WORD:" + word)
                            break

                if (len(collectionDelimiter) == 0):
                    formingCollection = False


                if (formingCollection == False):
                    # safe to add this word in:
                    finalRecord.append(finalWordToAdd.strip())
                    finalWordToAdd = ""
                else:
                    finalWordToAdd += ","

            finalWordToAdd = ""
            records.append(copy.deepcopy(finalRecord))
            finalRecord.clear()

        for record in records[:]:

            # populate the galaxy type data table:
            galaxyTypeRecord = [record[len(record) - 2].strip(), record[len(record) - 1].strip()]

            # I place IGNORE here because multiple galaxies can have
            # the same galaxy type, which would cause a primary key error
            query = "INSERT IGNORE INTO GalaxyTypes VALUES (%s, %s);"
            cursor.execute(query, galaxyTypeRecord)

            # Form planet and dwarf planet records:
            planetRecord = []
            planetAtmosphereRecords = []

            for i in range(0, 7):

                if (record[0] == 'N/A'):
                    break

                # append name, mass, gravity, radius, distance, and Equilibrium temperature, but skip atmosphere (goes in its own table for atomization purposes)
                if (i != 3):
                    # not an atmosphere
                    planetRecord.append(self.determineFinalValueToStore(record[i]))
                else:
                    # form atmosphere record and add it to atmosphereRecords
                    atmosphereGases = self.obtainCollection(record[i])
                    for gas in atmosphereGases:
                        if (gas != 'N/A'):
                            # the atmosphere of this planet is known:
                            planetAtmosphereRecords.append([planetRecord[0], gas.strip()])

            planetRecord.append(self.determineFinalValueToStore(record[12]))  # THE ESI
            planetRecord.append(self.determineFinalValueToStore(record[8]))  # rotation period
            planetRecord.append(self.determineFinalValueToStore(record[9]))  # orbital period
            planetRecord.append(self.determineFinalValueToStore(record[7]))  # escape velocity

            # append image directory and planet description
            for i in range(10, 12):
                planetRecord.append(self.determineFinalValueToStore(record[i]))

            # form a galaxy record for the system the star of this planet is in:
            galaxyRecord = []
            discovererRecords = []
            indexAtWhichGalaxyDataStarts = (len(record) - 10)
            for i in range(0, 9):
                if (i == 6):
                    # a discoverer name:
                    discoverNames = self.obtainCollection(record[indexAtWhichGalaxyDataStarts + i])
                    for name in discoverNames:
                        discovererRecords.append([galaxyRecord[0].strip(), name])
                else:
                    galaxyRecord.append(record[indexAtWhichGalaxyDataStarts + i])

            # place galaxy into database:
            # I place ignore here because multiple systems
            # will belong to the same galaxy; this would cause an error otherwise
            query = "INSERT IGNORE INTO Galaxies VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(query, galaxyRecord)

            # place galaxy discoverer records into database:
            # I use ignore here because a galaxy might have multiple discoverers; this would cause en error otherwise
            for discovererRecord in discovererRecords:
                query = "INSERT IGNORE INTO GalaxyDiscovers VALUES (%s, %s);"
                cursor.execute(query, discovererRecord)

            # form system record:
            systemRecord = []
            indexAtWhichSystemDataStarts = (len(record) - 12)
            for i in range(0, 3):
                if (record[indexAtWhichSystemDataStarts] != 'N/A'):
                    systemRecord.append(record[indexAtWhichSystemDataStarts + i].strip())

            if len(systemRecord) > 0:
                # place the system record into the database:
                # I use ignore here because multiple planets might belong to
                # the same system; this would cause an error otherwise
                query = "INSERT IGNORE INTO PlanetarySystems VALUES (%s, %s, %s);"
                cursor.execute(query, systemRecord)

            # form star record:
            starRecords = []
            starNames = self.obtainCollection(record[30])
            starMasses = self.obtainCollection(record[31])
            starRadiuses = self.obtainCollection(record[32])
            starEvolutionaryStages = self.obtainCollection(record[33])
            starEvolurtionaryStageDirectories = self.obtainCollection(record[34])
            starDistancesFromEarth = self.obtainCollection(record[35])
            starImageDirectories = self.obtainCollection(record[36])
            evolutionaryStageRecords = []

            for i in range(0, len(starNames)):
                if (starNames[i] == 'N/A'):
                    continue

                starRecord = []

                # store the star name:
                starRecord.append(starNames[i].strip())

                # store the star mass:
                starRecord.append(self.determineFinalValueToStore(starMasses[i]))

                # store the star radius:
                starRecord.append(self.determineFinalValueToStore(starRadiuses[i]))

                # store the star evolutionary stage:
                starRecord.append(self.determineFinalValueToStore(starEvolutionaryStages[i].strip()))

                if (starEvolutionaryStages[i] != 'N/A'):
                    # the evolutionary stage of this star is known, for a record for it:
                    evolutionaryStageRecords.append([starEvolutionaryStages[i].strip(), starEvolurtionaryStageDirectories[i].strip()])

                # store the distance from Earth
                starRecord.append(self.determineFinalValueToStore(starDistancesFromEarth[i]))

                # store the system the star is in:
                starRecord.append(self.determineFinalValueToStore(record[indexAtWhichSystemDataStarts].strip()))

                # store the image directory for the star:
                starRecord.append(self.determineFinalValueToStore(starImageDirectories[i]))

                # add this star record to the star records list:
                starRecords.append(starRecord)

            # having created the star records, add them into the database now, along with the evolutionary stage records:
            for evolutionaryStage in evolutionaryStageRecords:
                # I use ignore here because multiple stars might be of the same
                # evolutionary stage; this would cause an error otherwise
                query = "INSERT IGNORE INTO EvolutionaryStages VALUES (%s, %s);"
                cursor.execute(query, evolutionaryStage)

            # store the star records into the database now:
            for starRecord in starRecords:
                # I use ignore here because multiple planets may orbit a star;
                # this would cause an error otherwise
                query = "INSERT IGNORE INTO Stars VALUES (%s, %s, %s, %s, %s, %s, %s);"
                cursor.execute(query, starRecord)

            # can now store the planet record:
            if (len(planetRecord) == 12):
                query = "INSERT INTO Planets VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                cursor.execute(query, planetRecord)
                for atmosphericRecord in planetAtmosphereRecords:
                    query = "INSERT INTO PlanetAtmospheres VALUES(%s, %s);"
                    cursor.execute(query, atmosphericRecord)

                # store the name of the star this planet orbits as well:
                starPlanetOrbits = [starNames[0], planetRecord[0]]
                query = "INSERT INTO StarsPlanetsOrbit VALUES(%s, %s);"
                cursor.execute(query, starPlanetOrbits)

                if (record[14].strip() == 'yes'):
                    # this planet is a dwarf planet:
                    query = "INSERT INTO DwarfPlanets VALUES(%s);"
                    cursor.execute(query, [planetRecord[0]])

                if (record[13].strip() == 'yes'):
                    # this planet is in the habit zone:
                    query = "INSERT INTO PlanetsInHabitZone VALUES(%s);"
                    cursor.execute(query, [planetRecord[0]])

            # can now form the moon records for this planet:
            moonRecords = []
            moonDiscovererRecords = []
            if (record[15] != 'N/A'):
                moonNames = self.obtainCollection(record[15])
                moonMasses = self.obtainCollection(record[16])
                moonGravities = self.obtainCollection(record[17])
                moonRadiuses = self.obtainCollection(record[18])
                moonDistances = self.obtainCollection(record[19])
                moonMeanSurfaceTemps = self.obtainCollection(record[20])
                moonEscapeVelocities = self.obtainCollection(record[21])
                moonRotationPeriods = self.obtainCollection(record[22])
                moonOrbitalPeriods = self.obtainCollection(record[23])
                moonImageDirectories = self.obtainCollection(record[24])
                moonDescriptionDirectories = self.obtainCollection(record[25])
                moonDistancesFromPlanetTheyOrbit = self.obtainCollection(record[26])
                moonDiscovers = self.obtainCollection(record[27])
                moonYearsDiscovered = self.obtainCollection(record[28])

                for i in range(0, len(moonNames)):
                    moonRecord = []

                    # store the name of the moon:
                    moonRecord.append(moonNames[i].strip())

                    # store the moon mass:
                    moonRecord.append(self.determineFinalValueToStore(moonMasses[i]))

                    # store the name of the planet this moon orbits:
                    moonRecord.append(planetRecord[0])

                    # store the moon gravity:
                    moonRecord.append(self.determineFinalValueToStore(moonGravities[i]))

                    # store the moon radius:
                    moonRecord.append(self.determineFinalValueToStore(moonRadiuses[i]))

                    # store the moon distance from earth:
                    moonRecord.append(self.determineFinalValueToStore(moonDistances[i]))

                    # store the moon mean surface temperature:
                    moonRecord.append(self.determineFinalValueToStore(moonMeanSurfaceTemps[i]))

                    # store the moon escape velocities:
                    moonRecord.append(self.determineFinalValueToStore(moonEscapeVelocities[i]))

                    # store the moon rotational periods:
                    moonRecord.append(self.determineFinalValueToStore(moonRotationPeriods[i]))

                    # store the moon orbital period
                    moonRecord.append(self.determineFinalValueToStore(moonOrbitalPeriods[i]))

                    # store the image directory for the moon:
                    moonRecord.append(self.determineFinalValueToStore(moonImageDirectories[i]))

                    # store the description directory for the moon:
                    moonRecord.append(self.determineFinalValueToStore(moonDescriptionDirectories[i]))

                    # store the moon distance from the planet it orbits:
                    moonRecord.append(self.determineFinalValueToStore(moonDistancesFromPlanetTheyOrbit[i]))

                    # form a moon discoverer record:
                    if (moonDiscovers[i].strip() != 'N/A'):
                        moonDiscovererRecord = []

                        # store the moon discoverer name:
                        moonDiscovererRecord.append(moonDiscovers[i].strip())

                        # store the moon name:
                        moonDiscovererRecord.append(moonRecord[0])

                        # finally, store the year the discovery was made:
                        moonDiscovererRecord.append(self.determineFinalValueToStore(moonYearsDiscovered[i]))

                        # add it into the moon discoverers collection:
                        moonDiscovererRecords.append(moonDiscovererRecord)

                    # store moon record into the moon records collection:
                    moonRecords.append(moonRecord)

            # place the moons this planet has into the database:
            for moonRecord in moonRecords:
                query = "INSERT INTO Moons VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                cursor.execute(query, moonRecord)

            # place the moon discoverer record into the database:
            for moonDiscovererRecord in moonDiscovererRecords:
                query = "INSERT INTO MoonDiscovers VALUES(%s, %s, %s);"
                cursor.execute(query, moonDiscovererRecord)

        databaseConnector.commit()
        databaseConnector.close()

    # converts an N/A into a None type
    # so that it gets stored as NULL in
    # the database
    def determineFinalValueToStore(self, rawValue):
        if (rawValue.strip() == 'N/A'):
            return None
        else:
            return rawValue

    # used to form an array of items, used for
    # things like generating an atmospheric gas collection for
    # a planet record, etc.
    def obtainCollection(self, recordToGetItFrom):
        return recordToGetItFrom.replace('[', '').replace(']', '').replace('"', '').split(",")
