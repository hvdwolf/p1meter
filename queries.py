#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# queries.py - Python3 helper script that defines te queries to be read from the sqlite3 DB

# Copyright (c) 2022, Harry van der Wolf. all rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public Licence as published
# by the Free Software Foundation, either version 2 of the Licence, or
# version 3 of the Licence, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public Licence for more details.

# ----------------------------- Define some queries
q_data = "select * from v_p1data";
#q_daily= "select * from v_p1daily"
q_daily = "select importkwh, exportkwh, verbruiknuw, verbruiknul1w, gastotaalm3, strftime('%d-%m-%Y',timestamp) as datum from v_p1daily"

# This one shows the magenta/green diagram that displays usage or production of electricity for one day
q_netto_per_dag = "select timestamp tmstmp, verbruiknuw, importkwh, exportkwh from v_p1data where substr(timestamp,1,10) == date()"

# This one shows the gas production for one day
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
