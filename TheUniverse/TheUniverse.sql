DROP DATABASE IF EXISTS TheUniverse;
CREATE DATABASE TheUniverse;
USE TheUniverse;

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

SELECT GalaxyName
FROM Galaxies INNER JOIN (

    SELECT GalaxyName
    FROM PlanetarySystems
    INNER JOIN Stars
    ON PlanetarySystems.Name = Stars.PlanetarySystem

     ) AS SystemStarIsIn
    ON Galaxies.Name = SystemStarIsIn.GalaxyName;

CREATE INDEX planetNameIndex
    ON Planets(Name);

CREATE TABLE DwarfPlanets (

    Name VARCHAR(80) PRIMARY KEY

);

CREATE INDEX dwarfPlanetIndex
    ON DwarfPlanets(Name);

CREATE TABLE PlanetsInHabitZone (

    Name VARCHAR(80) PRIMARY KEY

);

CREATE INDEX planetsInHabitZoneIndex ON
    PlanetsInHabitZone(Name);

CREATE TABLE StarsPlanetsOrbit (

    StarName VARCHAR(80),
    PlanetName VARCHAR(80),

    CONSTRAINT PK_StarsPlanetsOrbit PRIMARY KEY (StarName, PlanetName)

);

# according to mysql docs, this index can be used in where clauses that
# use both these values or in where clauses where it is only StarName
# being checked
CREATE INDEX starNameAndPlanetThatOrbitsItIndex
    ON StarsPlanetsOrbit(StarName, PlanetName);

# since the above index cannot be used in queries where the where only contains
# PlanetName, I create a index for just this column right here
CREATE INDEX nameOfPlanetInStarsPlanetsOrbitIndex
    ON StarsPlanetsOrbit(PlanetName);

CREATE TABLE PlanetAtmospheres (

    Name VARCHAR(80),
    Gas VARCHAR(25),
    CONSTRAINT PK_PlanetAtmospheres PRIMARY KEY (Name, Gas)

);

# idea for these indexes is the same as mentioned above
CREATE INDEX planetNameAndTheGasInItsAtmosphereIndex
    ON PlanetAtmospheres(Name, Gas);

CREATE INDEX nameOfGasInPlanetAtmospheresIndex
    ON PlanetAtmospheres(Gas);

CREATE TABLE PlanetarySystems (

    Name VARCHAR(80) PRIMARY KEY,
    DistanceFromEarth DOUBLE NOT NULL ,
    GalaxyName VARCHAR(80)

);

CREATE INDEX nameOfSystemIndex
    ON PlanetarySystems(Name);

CREATE INDEX nameOfGalaxyPlanetarySystemIsInIndex
    ON PlanetarySystems(GalaxyName);

CREATE TABLE Galaxies (

    Name VARCHAR(80) PRIMARY KEY,
    NumberOfStars BIGINT UNSIGNED,
    Age FLOAT,
    DistanceFromEarth DOUBLE NOT NULL,
    Mass FLOAT,
    YearDiscovered FLOAT,
    ImageDirectory Text,
    GalaxyType VARCHAR(80)

);

CREATE INDEX nameOfGalaxyIndex
    ON Galaxies(Name);

CREATE INDEX typeOfGalaxyAGalaxyIsIndex
    ON Galaxies(GalaxyType);

CREATE TABLE EvolutionaryStages (

    EvolutionaryStage VARCHAR(80) PRIMARY KEY,
    Description TEXT

);

CREATE INDEX evolutionaryStageNameIndex
    ON EvolutionaryStages(EvolutionaryStage);

CREATE TABLE Stars (

    Name VARCHAR(80) PRIMARY KEY,
    Mass FLOAT,
    Radius FLOAT,
    EvolutionaryStage VARCHAR(80),
    DistanceFromEarth DOUBLE NOT NULL,
    PlanetarySystem VARCHAR(80),
    ImageDirectory Text

);

CREATE INDEX starNameIndex
    ON Stars(Name);

CREATE INDEX planetarySystemStarIsInIndex
    ON Stars(PlanetarySystem);

CREATE INDEX stagesOfStarsIndex
    ON Stars(EvolutionaryStage);

CREATE TABLE GalaxyTypes (

    GalaxyType VARCHAR(20) PRIMARY KEY,
    Description TEXT NOT NULL

);

CREATE INDEX galaxyTypeNameIndex
    ON GalaxyTypes(GalaxyType);

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
    ImageDirectory Text,
    Description TEXT,
    DistanceFromPlanetItOrbits FLOAT

);

CREATE INDEX moonNameIndex
    ON Moons(Name);

CREATE INDEX planetMoonOrbitsIndex
    On Moons(PlanetItOrbits);

CREATE TABLE GalaxyDiscovers(

    GalaxyName VARCHAR(80),
    DiscovererName VARCHAR(80),

    CONSTRAINT PK_GalaxyDiscovers PRIMARY KEY (GalaxyName, DiscovererName)

);

CREATE INDEX galaxyNameAndDiscovererIndex
    ON GalaxyDiscovers(GalaxyName, DiscovererName);

CREATE INDEX discovererNameInGalaxyDiscoverersIndex
    ON GalaxyDiscovers(DiscovererName);

CREATE TABLE MoonDiscovers (

    DiscovererName VARCHAR(80),
    MoonName VARCHAR(80),
    DiscoveryYear INT,
    CONSTRAINT PK_GalaxyDiscovers PRIMARY KEY (MoonName, DiscovererName)

);

CREATE INDEX moonNameAndDiscovererIndex
    ON MoonDiscovers(MoonName, DiscovererName);

CREATE INDEX moonDiscovererIndex
    ON MoonDiscovers(DiscovererName);

# a view for all the exo planets in the habit zone:
CREATE VIEW ExoPlanetsInHabitZone AS
    SELECT ExoPlanetNames.Name
    FROM (

        SELECT PlanetName AS Name
        FROM StarsPlanetsOrbit
        INNER JOIN Stars
        ON (Stars.Name = StarsPlanetsOrbit.StarName)
            AND (Stars.PlanetarySystem != 'Solar System')

    ) AS ExoPlanetNames
    INNER JOIN PlanetsInHabitZone
        ON ExoPlanetNames.Name = PlanetsInHabitZone.Name;

# a view for all the exo planets:
CREATE VIEW ExoPlanets AS
    SELECT PlanetName AS Name
    FROM StarsPlanetsOrbit
    INNER JOIN Stars
        ON (Stars.Name = StarsPlanetsOrbit.StarName)
                AND (Stars.PlanetarySystem != 'Solar System');

# FOREIGN KEYS
ALTER TABLE DwarfPlanets ADD CONSTRAINT FK_DwarfPlanets
    FOREIGN KEY (Name) REFERENCES Planets (Name)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE PlanetsInHabitZone ADD CONSTRAINT FK_PlanetsInHabitZone
    FOREIGN KEY (Name) REFERENCES Planets (Name)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE StarsPlanetsOrbit ADD CONSTRAINT FK_StarNamesPlanetsOrbit
    FOREIGN KEY (StarName) REFERENCES Stars (Name)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE StarsPlanetsOrbit ADD CONSTRAINT FK_PlanetNamesInStarsPlanetsOrbit
    FOREIGN KEY (PlanetName) REFERENCES Planets (Name)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE GalaxyDiscovers ADD CONSTRAINT FK_GalaxyDiscovers
    FOREIGN KEY (GalaxyName) REFERENCES Galaxies (Name)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE MoonDiscovers ADD CONSTRAINT FK_MoonDiscovers
    FOREIGN KEY (MoonName) REFERENCES Moons (Name)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE PlanetAtmospheres ADD CONSTRAINT FK_PlanetAtmospheres
    FOREIGN KEY (Name) REFERENCES Planets (Name)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE Galaxies ADD CONSTRAINT FK_Galaxies
    FOREIGN KEY (GalaxyType) REFERENCES GalaxyTypes (GalaxyType)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

ALTER TABLE Stars ADD CONSTRAINT FK_EvolutionaryStages
    FOREIGN KEY (EvolutionaryStage) REFERENCES EvolutionaryStages (EvolutionaryStage)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

ALTER TABLE Stars ADD CONSTRAINT FK_StarPlanetSystem
    FOREIGN KEY (PlanetarySystem) REFERENCES PlanetarySystems (Name)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

ALTER TABLE Moons ADD CONSTRAINT FK_PlanetMoonOrbits
    FOREIGN KEY (PlanetItOrbits) REFERENCES Planets (Name)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

ALTER TABLE PlanetarySystems ADD CONSTRAINT FK_GalaxySystemBelongsTo
    FOREIGN KEY (GalaxyName) REFERENCES Galaxies (Name)
    ON DELETE SET NULL
    ON UPDATE CASCADE;
