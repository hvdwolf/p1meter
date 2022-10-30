#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# gp1meter.py - Python3 PySimpleGUI script to read from the sqlite3 DB
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



# --------------------------- Start our script
# Check for the database
if not os.path.isfile(DB_file):
    print("\nCan't find the database\n")
    sys.exit(1)

# Connect to the database
connection = sqlite3.connect(DB_file)
cursor = connection.cursor()

#window = sg.Window('Overzicht p1 meter data', mainLayout)
# Display the GUI to the user
window =  ui_layout.create_and_show_gui()

while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Sluiten': # if user closes window or clicks Sluiten
        connection.close()
        break
    elif event == 'Verbruik per dag':
        do_query(window, q.q_verbruik)
        data = pandas.read_sql(q.q_verbruik, connection)
        if (values['_zeven_']):
            # last 7 days
            mpgraphs.verbruik_per_dag(window, data.tail(7), values)
        elif (values['_veertien_']):
            # last 14 days
            mpgraphs.verbruik_per_dag(window, data.tail(14), values)
        else:
            # all days so far
            mpgraphs.verbruik_per_dag(window, data, values)
        #window.refresh()
    elif event == 'Vandaag':
        #print(date())
        do_query(window, q.q_netto_per_dag)
        data = pandas.read_sql(q.q_netto_per_dag, connection)
        mpgraphs.netto_per_dag(window, data, values,"el")
    elif event == '_gasvandaag_':
        #print(date())
        do_query(window, q.q_netto_gas_per_dag)
        data = pandas.read_sql(q.q_netto_gas_per_dag, connection)
        mpgraphs.netto_per_dag(window, data, values, "gas")
    elif event == '-CAL-':
        #print(values['-CAL-'])
        myquery = "select timestamp tmstmp, verbruiknuw, importkwh, exportkwh from v_p1data where substr(timestamp,1,10) == '" + values['-CAL-'] + "'"
        do_query(window, myquery)
        data = pandas.read_sql(myquery, connection)
        mpgraphs.netto_per_dag(window, data, values, "el")
    elif event == '-GCAL-':
        myquery = "select t_next.timestamp tmstmp, round((t_next.gastotaalm3 - t.gastotaalm3),2) as totaalm3 from p1meterdata  as t inner join p1meterdata as t_next on t_next.rowid=t.rowid+1  where substr(t_next.timestamp,1,10) == '" + values['-GCAL-'] + "' order by t_next.timestamp"
        do_query(window, myquery)
        data = pandas.read_sql(myquery, connection)
        mpgraphs.netto_per_dag(window, data, values, "gas")
    elif event == 'Verbruik per week':
        do_query(window, q.q_verbruik_per_week)
        data = pandas.read_sql(q.q_verbruik_per_week, connection)
        mpgraphs.verbruik_per_week(window, data, values)
    elif event == 'Verbruik per maand':
        do_query(window, q.q_verbruik_per_maand)
        data = pandas.read_sql(q.q_verbruik_per_maand, connection)
        mpgraphs.verbruik_per_maand(window, data, values)
    elif event == 'Gescheiden vandaag':
        do_query(window, q_gescheiden_per_dag)
        data = pandas.read_sql(q.q_gescheiden_per_dag, connection)
        mpgraphs.gescheiden_per_dag(window, data, values)
    elif event == 'Dagelijkse totalen':
        do_query(window, q_daily)
        data = pandas.read_sql(q.q_daily, connection)
        mpgraphs.daily_totals(window, data)
    # For all selected buttons
    #print('You entered ', values[0])
    
window.close()
