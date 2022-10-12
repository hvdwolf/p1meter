# graphp1meter

graphp1meter is a Python3 PySimpleGui program to display collected values from the [Homewizard WiFi P1-meter](https://www.homewizard.com/nl/p1-meter/).
The values are collected by a Python3 script running from some server. In my case every 6 minutes on my RPi4 on Debian Buster.

I made this quickly for my own purpose after I received my solar panels on my roof. If you can use it, feel free to download.
Note: The texts/labels inside these scripts are in Dutch.

## Requirements
- Server (This is supposed to be a linux like server. In my case a RaspberryPi 4 running Debian Buster.)
    * Python3
    * Sqlite3
- Client
    * Python3
    * This collection of scripts
    * install other requirements with "python3 -m pip install pysimplegui numpy matplotlib"

## Usage
- Server script:
    * Specify the ip-address of your P1W meter inside the script.
    * Specify the location of your sqlite3 database inside the script.
    * Create a crontab where you let your script run every x minutes, where I advise 6 minutes or longer. You get a gas update every 5 minutes and to prevent double entries I read every 6 minutes.
    * Make sure you can access the database from your client. Or create another crontab line to copy it every 10 minutes (or so) to a location where you can access it.

- Client:
    * In the config.py first specify the location of your (regularly copied) database.
    * from the command line type "./gp1meter.py" or on Windows "python3 gp1meter.py".


