# TheUniverseDatabase

![TheUniverseDatabase](https://user-images.githubusercontent.com/43594702/120029814-7220d800-bfab-11eb-97a4-f3785b8c14c4.png)

[See it in action!](https://www.youtube.com/watch?v=TwAcFtfOSaw)

## Contact information

- Name: Diego Avena
- Email: avena@chapman.edu
- Slack: Diego Avena

## Overview

This program creates a local mysql database and loads universe data into
it from a table called UniverseRawData. This table combines data from various resources,
referenced below, that document information on things about our universe such as the
various exoplanets, galaxies, stars, and moons we know about. This is all done in an attempt
to provide a much more unified source of information about our universe, since this information
is currently extremely scattered throughout the internet.

Through this program, the user can:

- Perform updates, insertions, and deletions on
   - planets
   - galaxies
   - stars
   - planetary systems
   - moons
   - galaxy discoverers
   - moon discoverers

- Peform searches on
   - Single planets
   - Multiple planets
   - Single galaxies
   - multiple galaxies
   - Single Stars
   - multiple stars

- Generate pdf and csv reports for all the different types of searches they can do on this database
   - PDF reports
       - Stored in a directory called pdfReports, located in the same directory as this README
       - These reports allow the user to see images for the things they query

   - CSV reports
       - Stored in a directory called csvReports, located in the same directory as this README



## WHAT YOU NEED TO HAVE INSTALLED

Python 3.9 or Python 3.8

1. Pycharm:

    If you open the project and it says there is no python interpreter, then do this:

    - Either
      Click on add interpreter, and make sure to add it in for either python 3.9 or python 3.8.
      OR
      Click on use Python (version num) if the version is either 3.9 or 3.8

    - After creating the new interpreter or setting it up, navigate to the Settings tab
    (File->Settings if on Windows, and PyCharm->Preferences if on mac), and go to Project, open the dropdown,
    select Python Interpreter, and add the following packages (if not already present):

        - mysql-connector-python
        - fpdf
        - Pillow

    After installing these, hit ok. Project should now be able to be run.

2. Datagrip (for resetting the database):

3. A local mysql instance running on your computer:

    - The password for this instance can be anything, since the program will
    prompt you to enter that password on startup anyways

## How to use

- To launch:
    - Locate main.py, double click on it to open it in pycharm, and then hit the play button, this
    will display the main menu options to you

- To reset the database:
    - Go into TheUniverse.sql file, highlight the first
    line of the file, and click the play button. This will delete the database
    if it was created, so that the next time you launch this program,
    the database gets reinitialized entirely

- The main menu:
    - Shows these options to the user:

    - Perform a search
        - will bring up all of the search options
    - Update a record
        - will bring up all of the update options
    - Insert a record
        - will bring up all of the insertion options
    - Delete a record
        - will bring up all of the deletion options
    - quit
        - will close the app

- Record Search Manager
    Shows these options to the user:

    - Single Planet Search
        - will bring up the window for searching for 1 planet
    - Multiple Planet Search
        - will bring up the window for searching for more than 1 planet
    - Single Star Search
        - will bring up the window for searching for 1 star
    - multiple star search
        - will bring up the window for searching for more than 1 star
    - Single Galaxy Search
        - will bring up the window for searching for 1 galaxy
    - Multiple Galaxy Search
        - will bring up the window for searching for more than 1 galaxy

    For information on how to navigate through a multiple search window, such
    as multi-planetary search, please see the image called: multipleSearchWindowNavigation.png

    For information on how to navigate through a single search window, such as
    single star search, please see the image called: singleSearchWindowNavigation.png

    How to return to main menu:
        To exit this option and make all options on the main menu active again, hit the
        exit button located at the top right corner of the window

- Record Update Manager
    Shows these options to the user:

    - Update a galaxy record
        - Will bring up the window for updating a galaxy record
    - Update a planet record
        - Will bring up the window for updating a planet record
    - Update a galaxy type record
        - Will bring up the window for updating a galaxy type record
    - Update a evolutionary stage record
        - Will bring up the window for updating an evolutionary stage record
    - Update a star record
        - Will bring up the window for updating a star record
    - Update a galaxy discoverer record
        - Will bring up the window for updating a galaxy discoverer record
    - Update a moon record
        - Will bring up the window for updating a moon record
    - Update a system record
        - Will bring up the window for updating a system record
    - Update a moon discover record
        - Will bring up the window for updating a moon discoverer record

    For information on how to navigate through a more specific update manager
    after clicking on one of these options, such as GalaxyUpdateManager, see the
    image called: updateWindowNavigation.png

    How to return to main menu:
        To exit this option and make all options on the main menu active again, hit the
        exit button located at the top right corner of the window

- Record Insertion:
    Shows these options to the user:

    - Create a New Galaxy
        - Will bring up the window needed to insert a new galaxy
    - Create a new planet
        - Will bring up the window needed to insert a new planet
    - Create a new galaxy type
        - Will bring up the window needed to insert a new galaxy type
    - Create a new evolutionary stage
        - Will bring up the window needed to insert a new evolutionary stage
    - Create a new planetary system
        - Will bring up the window needed to insert a new planetary system
    - Create a new star
        - Will bring up the window needed to insert a new star
    - Create a new moon
        - Will bring up the window needed to insert a new moon

    For information on how to navigate through a more specific insertion
    manager that appears after clicking one of these options, see the image
    called: insertionWindowNavigation.png

    How to return to main menu:
        To exit this option and make all options on the main menu active again, hit the
        exit button located at the top right corner of the window

- Record Deletion
    Shows these options to the user:

    - Delete a planet
        - Will bring up the window needed to delete a planet
    - Delete a star
        - Will bring up the window needed to delete a star
    - Delete a galaxy
        - Will bring up the window needed to delete a galaxy
    - Delete an evolutionary stage
        - Will bring up the window needed to delete an evolutionary stage
    - Delete a galaxy type
        - Will bring up the window needed to delete a galaxy type
    - Delete a moon
        - Will bring up the window needed to delete a moon
    - Delete a planetary system
        - Will bring up the window needed to delete a planetary system
    - Delete a moon discoverer
        - Will bring up the window needed to delete a moon discoverer
    - Delete a galaxy discoverer
        - Will bring up the window needed to delete a galaxy discoverer

    For more information on how to navigate a more specific deletion manager
    that appears after selecting one of these options, see the image called:
    deletionWindowNavigation.png

    How to return to main menu:
        To exit this option and make all options on the main menu active again, hit the
        exit button located at the top right corner of the window

- A quick note on loading in images:
    If you are trying to load an image from a directory you know has images in it, and
    the image loader is not displaying those images for you to choose from, look at the bottom right
    corner of this image loader display box. There will be a dropdown box here allowing you to pick
    the correct image type, changing this to the correct image type of the images stored in this directory
    will then cause them to be displayed for you to load.



## References
1.) https://www.youtube.com/watch?v=YXPyB4XeYLA
Watched all 5 hours of this tutorial which gives a nice overview
of all the basic tkinter functions. I created a repo on github with each
example from this tutorial series for me to reference from in this project; this is
how I was able to get the basic UI up and running

2.) https://blog.teclado.com/tkinter-scrollable-frames/
I used this to learn how to create the scrollable frames used in things like
the text displayers, the single planetary displayers, etc.

3.) https://stackoverflow.com/questions/5104957/how-do-i-create-a-file-at-a-specific-path
Used this to learn how to use the os module in order to create a directories or get a path
to the directories at which the pdf and csv reports were to be saved at

4.) https://www.w3schools.com/python/python_mysql_create_db.asp
Used this to figure out how I can check if a database already exists via python, which
was needed as I did not want to recreate the Universe Data base if it already exists and I
also wanted to be able to create the database from the python application

5.) https://www.geeksforgeeks.org/working-csv-files-python/
For using the csv module for the creation of a .csv report

6.) https://pyfpdf.readthedocs.io/en/latest/Tutorial/index.html
In order to understand how to initialize a pdf report and save it using FPDF

7.) https://pyfpdf.readthedocs.io/en/latest/reference/image/index.html
For figuring out how to use FPDF to store images in a pdf

8.) https://stackoverflow.com/questions/38350816/python-mysql-connector-internalerror-unread-result-found-when-close-cursor
Was running into a weird error at line 243 inside the SingleGalaxySearchManager script
where it was saying there was an unread value, so I found this solution and the error went away



## Known Issues

1. When a textbox loads in, there are some red messages that
get printed to the console saying:

> 2021-05-17 22:47:38.137 Python[14004:293946] CoreText note: Client requested name ".SFNSMono-Regular", it will get Times-Roman rather than the intended font.        All system UI font access should be through proper APIs such as CTFontCreateUIFontForLanguage() or +[NSFont systemFontOfSize:].
> 2021-05-17 22:47:38.137 Python[14004:293946] CoreText note: Set a breakpoint on CTFontLogSystemFontNameRequest to debug.
> 2021-05-17 22:47:38.187 Python[14004:293946] CoreText note: Client requested name ".SF NS Mono", it will get Times-Roman rather than the intended font. All          system UI font access should be through proper APIs such as CTFontCreateUIFontForLanguage() or +[NSFont systemFontOfSize:].

This does not cause the program to crash though, and I have been unable to get information on this
through google, so I left this for now...

2. On mac, for some reason trying to scroll while a frame is loading into view causes the program to crash with
the error message: 

> python quit unexpectedly while using the
> _tkinter.cpython-38-darwin.so plugin. 
      
3. On mac, for some reason the scroll bars do not load in on multiple planetary search, and things are not placed on
the grid right. When this happens, exiting the multi search window and reentering seems to fix the issue.

> Note to self (for the future): I do not think tkinter plays too nicely with mac...

## Code files in this project

PYTHON FILES:

main.py

- In Code:
    ReportGenerator.py
    OptionBase.py
    MainMenuManager.py
    DataLoader.py
    BaseDataModifierManager.py
    BaseDataBaseInteractionManager.py

    - In UpdateManagers:
        BaseUpdateManager.py
        RecordUpdateManager.py

        - InvividualUpdateManagers:
            EvolutionaryStageUpdateManager.py
            GalaxyDiscovererUpdateManager.py
            GalaxyTypeUpdateManager.py
            GalaxyUpdateManager.py
            MoonDiscovererUpdateManager.py
            MoonUpdateManager.py
            PlanetarySystemUpdateManager.py
            PlanetUpdateManager.py
            StarUpdateManager

    - In SearchManagers
        - In BaseSearchManagers:
            BaseMultiSearchManager.py
            BaseSinglerSearchManager.py
        - In MultiSearchManagers:
            MultiGalaxySearchManager.py
            MultiPlanerarySearchManager.py
            MultiStarSearchManager.py
        - In SingleSearchManagers:
            SingleGalaxySearchManager.py
            SinglePlanetarySearchManager.py
            SingleStarSearchManager.py

        RecordSearchManager.py

    - In InsertionManagers
        - In IndividualInsertionManagers
            NewEvolutionaryStageInsertionManager.py
            NewGalaxyInsertionManager.py
            NewGalaxyTypeInsertionManager.py
            NewMoonInsertionManager.py
            NewPlanetarySystemInsertionManager.py
            NewPlanetInsertionManager.py
            NewStarInsertionManager.py

        BaseInsertionManager.py
        InsertionValidator.py
        RecordInsertionManager.py

    - In Displayers
        ImageDisplayerManager.py
        TextBoxManager.py

    - In DeletionManagers
        BaseDeletionManager.py
        CompositeDeletionManager.py
        RecordDeletionManager.py

SQL FILE:

- TheUniverse.sql

   - This file was used to draft out the queries and all of the
   DDL statements needed to create the database from within
   python.
