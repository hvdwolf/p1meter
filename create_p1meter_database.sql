#CREATE DATABASE p1meter_data.db;

CREATE TABLE p1meterdata(id integer primary key, importdalkwh real, importnormaalkwh real, exportdalkwh real, exportnormaalkwh real, verbruiknuw real, verbruiknul1w real, gastotaalm3 real, timestamp text);

CREATE UNIQUE INDEX idx_timestamp on p1meterdata(timestamp);

CREATE VIEW v_p1data as select id,(importdalkwh+importnormaalkwh) as importkwh, (exportdalkwh+exportnormaalkwh) as exportkwh, verbruiknuw, verbruiknul1w, gastotaalm3, timestamp from p1meterdata group by id order by timestamp;

CREATE VIEW v_p1daily as select id,(importdalkwh+importnormaalkwh) as importkwh, (exportdalkwh+exportnormaalkwh) as exportkwh, verbruiknuw, verbruiknul1w, gastotaalm3, timestamp, max(timestamp) from p1meterdata group by date(timestamp);

CREATE VIEW v_p1weekly as select id,(importdalkwh+importnormaalkwh) as importkwh, (exportdalkwh+exportnormaalkwh) as exportkwh, verbruiknuw, verbruiknul1w, gastotaalm3, timestamp, strftime('%W', timestamp) weekno, max(timestamp) from p1meterdata where strftime('%w',timestamp)=='0' group by date(timestamp);

CREATE VIEW v_p1monthly as select id,(importdalkwh+importnormaalkwh) as importkwh, (exportdalkwh+exportnormaalkwh) as exportkwh, verbruiknuw, verbruiknul1w, gastotaalm3, timestamp, strftime('%m', timestamp) month, case when strftime('%m', timestamp)=='01' then 'jan' when strftime('%m', timestamp)=='02' then 'feb' when strftime('%m', timestamp)=='03' then 'mrt' when strftime('%m', timestamp)=='04' then 'apr' when strftime('%m', timestamp)=='05' then 'mei' when strftime('%m', timestamp)==06 then 'jun' when strftime('%m', timestamp)=='07' then 'jul' when strftime('%m', timestamp)=='08' then 'aug' when strftime('%m', timestamp)=='09' then 'sep' when strftime('%m', timestamp)=='10' then 'okt' when strftime('%m', timestamp)=='11' then 'nov' when strftime('%m', timestamp)=='12' then 'dec' end monthname, max(timestamp) from p1meterdata where strftime("%m", timestamp) != strftime("%m", timestamp, "+1 day") group by date(timestamp);