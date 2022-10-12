#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# p1meter.py - Python3 script to reada P1W meter over tcpip.

# Copyright (c) 2022, Harry van der Wolf. all rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public Licence as published
# by the Free Software Foundation, either version 2 of the Licence, or
# version 3 of the Licence, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public Licence for more details.


import os, os.path, sqlite3, urllib.request, json, csv
#import panda as pd
from datetime import date
from datetime import timedelta

"""
https://homewizard-energy-api.readthedocs.io/

json string from p1 meter:
{"smr_version":50,"meter_model":"Sagemcom XS210 ESMR 5.0","wifi_ssid":"Wolfslair","wifi_strength":86,
 "total_power_import_t1_kwh":5473.942,"total_power_import_t2_kwh":6114.19,"total_power_export_t1_kwh":39.036,"total_power_export_t2_kwh":134.491,
 "active_power_w":-892,"active_power_l1_w":-892,"active_power_l2_w":null,"active_power_l3_w":null,"total_gas_m3":6937.601,"gas_timestamp":220930133000}

Where:
total_power_import_t1_kwh       =>      Stroomimport dal
total_power_import_t2_kwh       =>      Stroomimport normaal
total_power_export_t1_kwh       =>      Stroomexport dal
total_power_export_t2_kwh       =>      Stroomexport normaal
active_power_w                  =>      Huidig stroomverbruik Watts (negatief is leveren door zonnepanelen)
active_power_l1_w               =>      Huidig stroomverbruik Watts (negatief is leveren door zonnepanelen)
total_gas_m3                    =>      Totaal verbruik gas m3
gas_timestamp                   =>      Gas timestamp jjmmddhhmmss

The update frequency for SMR 5.0 is every second for power and every 5 minutes for gas.
"""
# Some constants
#DB_file = "/home/hvdwolf/try.db"
DB_file = "/home/harryvanderwolf/p1meter_data.db"
# I used to write csv as well but stopped it. Set to True to re-enable
csv_file = False
p1_data_file = '/home/harryvanderwolf/p1meter_data.csv'
IP_p1w = '192.168.2.137'
Version = 0.2
# End of constants

# Get the data from P1meter WiFi dongle
with urllib.request.urlopen("http://192.168.2.137/api/v1/data") as url:
    data = json.load(url)
    #pdata = pd.read_json(data)

# Check for the database
if not os.path.isfile(DB_file):
    # create db and tables
    connection = sqlite3.connect(DB_file)
    connection.text_factory = str  # allows utf-8 data to be stored
    cursor = connection.cursor()
    #cursor.execute('create table p1meter_data(id integer primary key, smr_version integer, meter_model text, wifi_ssid text, wifi_strength integer, total_power_import_t1_kwh real, total_power_import_t2_kwh real, total_power_export_t1_kwh real, total_power_export_t2_kwh real, active_power_w real, active_power_l1_w real, active_power_l2_w real, active_power_l3_w real, total_gas_m3 real, gas_timestamp integer)')
    cursor.execute('create table p1meterdata(id integer primary key, importdalkwh real, importnormaalkwh real, exportdalkwh real, exportnormaalkwh real, verbruiknuw real, verbruiknul1w real, gastotaalm3 real, timestamp text)') 
    cursor.execute('CREATE VIEW v_p1data as select id,(importdalkwh+importnormaalkwh) as importkwh, (exportdalkwh+exportnormaalkwh) as exportkwh, verbruiknuw, verbruiknul1w, gastotaalm3, timestamp from p1meterdata group by id order by timestamp')
    cursor.execute('CREATE VIEW v_p1daily as select id,(importdalkwh+importnormaalkwh) as importkwh, (exportdalkwh+exportnormaalkwh) as exportkwh, verbruiknuw, verbruiknul1w, gastotaalm3, timestamp, max(timestamp) from p1meterdata group by date(timestamp)')
    cursor.execute('CREATE VIEW v_p1weekly as select id,(importdalkwh+importnormaalkwh) as importkwh, (exportdalkwh+exportnormaalkwh) as exportkwh, verbruiknuw, verbruiknul1w, gastotaalm3, timestamp, strftime("%W", timestamp) weekno, max(timestamp) from p1meterdata where strftime("%w",timestamp)=="0" group by date(timestamp)')
    cursor.execute('CREATE UNIQUE INDEX idx_timestamp on p1meterdata(timestamp)')
    connection.commit()
    connection.close()

#print(json.dumps(data))
importdalkwh = data["total_power_import_t1_kwh"]
importnormaalkwh = data["total_power_import_t2_kwh"]
exportdalkwh = data["total_power_export_t1_kwh"]
exportnormaalkwh = data["total_power_export_t2_kwh"]
verbruiknuw = data["active_power_w"]
verbruiknul1w = data["active_power_l1_w"]
gastotaalm3 = data["total_gas_m3"]
tmstmp = str(data["gas_timestamp"])
# gas_timestamp => 220930133000
timestamp = "20"+tmstmp[0:2]+"-"+tmstmp[2:4]+"-"+tmstmp[4:6]+" "+tmstmp[6:8]+":"+tmstmp[8:10]+":"+tmstmp[10:12]
print(timestamp)

connection = sqlite3.connect(DB_file)
cursor = connection.cursor()
cursor.execute("insert into p1meterdata(importdalkwh,importnormaalkwh,exportdalkwh,exportnormaalkwh,verbruiknuw,verbruiknul1w,gastotaalm3,timestamp) values(?,?,?,?,?,?,?,?);", (importdalkwh,importnormaalkwh,exportdalkwh,exportnormaalkwh,verbruiknuw,verbruiknul1w,gastotaalm3,timestamp))
#cursor.execute("insert into p1meter_data(smr_version,meter_model,wifi_ssid,wifi_strength,total_power_import_t1_kwh,total_power_import_t2_kwh,total_power_export_t1_kwh, total_power_export_t2_kwh, active_power_w, active_power_l1_w, active_power_l2_w, active_power_l3_w, total_gas_m3, gas_timestamp) values (?)", (json.dumps(data),))
connection.commit()
connection.close()
#pdata.to_sql('p1meter_data', con=cursor, if_exists='append', index=FALSE)

if (csv_file):
    # Write to csv file
    if (os.path.isfile(p1_data_file)):
        data_file = open(p1_data_file, 'a')
        csv_writer = csv.writer(data_file)
        csv_writer.writerow(data.values())
        data_file.close()
    else:
        data_file = open(p1_data_file, 'a')
        csv_writer = csv.writer(data_file)
        header = data.keys()
        csv_writer.writerow(header)
        csv_writer.writerow(data.values())
        data_file.close()
