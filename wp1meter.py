#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# wp1meter.py - Python3 web script to read from the sqlite3 DB
# that was filled by the p1meter.py server based script.

# Copyright (c) 2022, Harry van der Wolf. all rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public Licence as published
# by the Free Software Foundation, either version 2 of the Licence, or
# version 3 of the Licence, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public Licence for more details.

import PySimpleGUI as sg
import os.path, sys, sqlite3
import pandas
import glob
from datetime import date
from datetime import timedelta

# My python functions
import mpgraphs
import config
import ui_layout
import queries as q

def do_query(window, myquery):
    MLINE_KEY = '-ML-'+sg.WRITE_ONLY_KEY        # multiline element's key. Indicate it's an output only element
    cursor.execute(myquery)
    rows = cursor.fetchall()
    window[MLINE_KEY].Update('')
    for row in rows:
        window[MLINE_KEY].print(row)
        #print(row)
    #window['_progress_msg'].print('Grafiek voorbereiden')
    window.refresh()


DB_file = config.sqlite3_DB_file


# Create dictionary values
def get_values(periodes, grafiektype):
    # -CAL- or -GCAL- is date like 2022-11-03 or ''
    values = {
        '_CALENDAR_': '',
        '_GCALENDAR_': '',
        '_vier_': False,
        '_zeven_': False,
        '_twaalf_': False,
        '_veertien_': False,
        '_dertig_': False,
        '_onbeperkt_': False,
        't_alles': False,
        't_electrisch': False,
        't_verbruikt': False,
        't_geproduceerd': False,
        't_gasverbruik': False,
        '_staaf_': True,
        '_lijn_': False,
        '-CAL-': '',
        '-GCAL-': '',
        'controls_cv': None,
        'fig_cv': None
    }

    if (periodes == '4'):
        values.update({'_vier_': True})
    elif (periodes == '7'):
        values.update({'_zeven_': True})
    elif (periodes == '12'):
        values.update({'_twaalf_': True})
    elif (periodes == '14'):
        values.update({'_veertien_': True})
    elif (periodes == '30'):
        values.update({'_dertig_': True})
    elif (periodes == '9999'):
        values.update({'_onbeperkt_': True})
    else:  # if everthing fails, go for a default
        values.update({'_zeven_': True})

    if (grafiektype == 'VPG'):
        values.update({'t_alles': True})
    elif (grafiektype == 'VP'):
        values.update({'t_electrisch': True})
    elif (grafiektype == 'V'):
        values.update({'t_verbruikt': True})
    elif (grafiektype == 'P'):
        values.update({'t_geproduceerd': True})
    elif (grafiektype == 'G'):
        values.update({'t_gasverbruik': True})
    else:
        values.update({'t_alles': True})

    return values


# Return number of periods, be it days/weeks/months
def get_periodes(values):

    if (values['_vier_']):
        aantal = 4
    elif (values['_zeven_']):
        aantal = 7
    elif (values['_twaalf_']):
        aantal = 12
    elif (values['_veertien_']):
        aantal = 14
    elif (values['_dertig_']):
        aantal = 30
    else:
        aantal = 9999

    return aantal


# --------------------------- Start our script
# Check for the database
if not os.path.isfile(DB_file):
    print("\nCan't find the database\n")
    sys.exit(1)

# Connect to the database
connection = sqlite3.connect(DB_file)
cursor = connection.cursor()

# Set some values
event = sys.argv[1]
periodes = sys.argv[2]
grafiektype = sys.argv[3]
global PNG
# Window was a pysimplegui array
window = [[]]

# Remove old png files
fileList = glob.glob('/var/www/html/tmp/*.png')
for filePath in fileList:
    try:
        os.remove(filePath)
    except:
        print("Error while deleting file : ", filePath)

values = get_values(periodes, grafiektype)
#print(event, values)
if event == 'Per dag':
    data = pandas.read_sql(q.q_verbruik, connection)
    PNG = mpgraphs.verbruik_per_dag(window, data.tail(get_periodes(values)), values, True)
elif event == 'Vandaag':
    data = pandas.read_sql(q.q_netto_per_dag, connection)
    mpgraphs.netto_per_dag(window, data, values, "el")
elif event == '_gasvandaag_':
    data = pandas.read_sql(q.q_netto_gas_per_dag, connection)
    mpgraphs.netto_per_dag(window, data, values, "gas")
elif event == '-CAL-':
    myquery = "select timestamp tmstmp, verbruiknuw, importkwh, exportkwh from v_p1data where substr(timestamp,1,10) == '" + \
              values['-CAL-'] + "'"
    data = pandas.read_sql(myquery, connection)
    mpgraphs.netto_per_dag(window, data, values, "el")
elif event == '-GCAL-':
    myquery = "select t_next.timestamp tmstmp, round((t_next.gastotaalm3 - t.gastotaalm3),2) as totaalm3 from p1meterdata  as t inner join p1meterdata as t_next on t_next.rowid=t.rowid+1  where substr(t_next.timestamp,1,10) == '" + \
              values['-GCAL-'] + "' order by t_next.timestamp"
    data = pandas.read_sql(myquery, connection)
    mpgraphs.netto_per_dag(window, data, values, "gas")
elif event == 'Per week':
    data = pandas.read_sql(q.q_verbruik_per_week, connection)
    PNG = mpgraphs.verbruik_per_week(window, data.tail(get_periodes(values)), values, True)
elif event == 'Per maand':
    data = pandas.read_sql(q.q_verbruik_per_maand, connection)
    PNG = mpgraphs.verbruik_per_maand(window, data.tail(get_periodes(values)), values, True)
elif event == 'Gescheiden vandaag':
    data = pandas.read_sql(q.q_gescheiden_per_dag, connection)
    mpgraphs.gescheiden_per_dag(window, data, values)
elif event == 'Dagelijkse totalen':
    data = pandas.read_sql(q.q_daily, connection)
    mpgraphs.daily_totals(window, data)

print(PNG) 
