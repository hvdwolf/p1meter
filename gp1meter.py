#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# gp1.py - Python3 PySimpleGUI script to read from the sqlite3 DB
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
#import matplotlib.pyplot as plt, numpy as np
from datetime import date
from datetime import timedelta

# My python functions
import mpgraphs
import config
import ui_layout

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

# ----------------------------- Define some queries
q_data = "select * from v_p1data";
#q_daily= "select * from v_p1daily"
q_daily = "select importkwh, exportkwh, verbruiknuw, verbruiknul1w, gastotaalm3, strftime('%d-%m-%Y',timestamp) as datum from v_p1daily"

q_netto_per_dag = "select timestamp tmstmp, verbruiknuw, importkwh, exportkwh from v_p1data where substr(timestamp,1,10) == date()"

q_netto_gas_per_dag = "select t_next.timestamp tmstmp, round((t_next.gastotaalm3 - t.gastotaalm3),2) as totaalm3 from p1meterdata  as t inner join p1meterdata as t_next on t_next.rowid=t.rowid+1  where substr(t_next.timestamp,1,10) == date() order by t_next.timestamp"

q_gescheiden_per_dag = "select  substr(t_next.timestamp,12,5) tmstmp, round((t_next.importkwh - t.importkwh)*1000,2) as importwh, round((t_next.exportkwh-t.exportkwh)*1000,2) as exportwh from v_p1data as t inner join v_p1data as t_next on t_next.rowid=t.rowid+1 group by date(t_next.timestamp),t_next.id"

q_verbruik = "select case when strftime('%w',t_next.timestamp)=='0' then 'zondag' when strftime('%w',t_next.timestamp)=='1' then 'maandag' when strftime('%w',t_next.timestamp)=='2' then 'dinsdag' when strftime('%w',t_next.timestamp)=='3' then 'woensdag' when strftime('%w',t_next.timestamp)=='4' then 'donderdag' when strftime('%w',t_next.timestamp)=='5' then 'vrijdag' when strftime('%w',t_next.timestamp)=='6' then 'zaterdag' end 'weekdag', strftime('%d-%m-%Y',t_next.timestamp) datum, (case when strftime('%w',t_next.timestamp)=='0' then 'zo' when strftime('%w',t_next.timestamp)=='1' then 'ma' when strftime('%w',t_next.timestamp)=='2' then 'di' when strftime('%w',t_next.timestamp)=='3' then 'wo' when strftime('%w',t_next.timestamp)=='4' then 'do' when strftime('%w',t_next.timestamp)=='5' then 'vr' when strftime('%w',t_next.timestamp)=='6' then 'za' end ||' '|| strftime('%d-%m',t_next.timestamp)) as dagdatum, round((t_next.importkwh - t.importkwh),1) as importkwh, round((t_next.exportkwh-t.exportkwh),1) as exportkwh, round((t_next.gastotaalm3 - t.gastotaalm3),1) as gastotaalm3 from v_p1daily as t inner join v_p1daily as t_next on t_next.rowid=t.rowid+1"

q_verbruik_per_week = "select t_next.weekno,strftime('%d-%m-%Y',t_next.timestamp), (t_next.weekno ||' (' || strftime('%d-%m',t_next.timestamp)||')') as wknrdatum, round((t_next.importkwh - t.importkwh),1) as importkwh, round((t_next.exportkwh-t.exportkwh),1) as exportkwh, round((t_next.gastotaalm3 - t.gastotaalm3),1) as gastotaalm3 from v_p1weekly as t inner join v_p1weekly as t_next on t_next.rowid=t.rowid+1"

# Select last 14 records
last_fourteen = "select * from  (select * from v_p1data order by id desc limit 14) Var1 order by id asc;"
# select last 7 days (week overview)
last_seven = "select * from (select * from v_p1daily order by id desc limit 7) Var1 order by id asc;"


# New unused query for last date of the month of the current year
q_ldmcy = 'select substr(max(timestamp), 1,10) from v_p1data where strftime("%m", timestamp) != strftime("%m", timestamp, "+1 day") and strftime("%Y", timestamp) = strftime("%Y", "now")'
q_ldmcy = 'select substr(max(timestamp), 1,10) from v_p1data where strftime("%m", timestamp) != strftime("%m", timestamp, "+1 day")'
# select sundays
q_evsun = 'select substr(max(timestamp),1,10) from v_p1data where strftime("%w", timestamp) = "0";'
# Select minimal possible date for selection
q_minimal_date = 'select substr(min(timestamp),1,10) from v_p1data;'

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
        do_query(window, q_verbruik)
        data = pandas.read_sql(q_verbruik, connection)
        mpgraphs.verbruik_per_dag(window, data, values)
        #window.refresh()
    elif event == 'Vandaag':
        #print(date())
        do_query(window, q_netto_per_dag)
        data = pandas.read_sql(q_netto_per_dag, connection)
        mpgraphs.netto_per_dag(window, data, values,"el")
    elif event == '_gasvandaag_':
        #print(date())
        do_query(window, q_netto_gas_per_dag)
        data = pandas.read_sql(q_netto_gas_per_dag, connection)
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
        do_query(window, q_verbruik_per_week)
        data = pandas.read_sql(q_verbruik_per_week, connection)
        mpgraphs.verbruik_per_week(window, data, values)
    elif event == 'Gescheiden vandaag':
        do_query(window, q_gescheiden_per_dag)
        data = pandas.read_sql(q_gescheiden_per_dag, connection)
        mpgraphs.gescheiden_per_dag(window, data, values)
    elif event == 'Dagelijkse totalen':
        do_query(window, q_daily)
        data = pandas.read_sql(q_daily, connection)
        mpgraphs.daily_totals(window, data)
    # For all selected buttons
    #print('You entered ', values[0])
    
window.close()






