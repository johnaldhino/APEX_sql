#!/usr/bin/python

#######################################################
# A python script to test inserting info from csv to mysql
# Author: John Williamson
# Created: 13th May 2019
#######################################################

import sys
import os
import string
import MySQLdb
import csv


#---------------------------------------------------
# getting runlist from file

runlist = []

with open('/adaqfs/home/adaq/scripts/APEX-sql/SciFi_runlist/good_cosmics.csv') as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=',')
    for row in csv_reader:
        runlist.append(row)


print(runlist)


#-------------------------------------------------
# testing DB connection


dbserver='halladb.jlab.org'
dbpass='4p3xu$3r'
dbSchema='apexdb'
dbUser='apex-user'  # chose user as script need not change anything in db



try:
    db = MySQLdb.connect(host=dbserver, user=dbUser, passwd=dbpass, db=dbSchema)
except MySQLdb.Error:
    print("Could not connect to database. Please ensure that the paper runlist is kept up-to-date. Please email  ( jwilli@jlab.org) and include what run number this message appeared on.")
    sys.exit(1)




format_strings = ','.join(['%s'] * len(runlist))

dbQuery = 'select V1.run_number, V1.value_1, V2.value_2, V1.prescale_T1, V1.prescale_T2, V1.prescale_T3, V1.prescale_T4, V1.prescale_T5, V1.prescale_T6, V1.prescale_T7, V1.prescale_T8 from (select APEXrunlist.run_number, APEXrunlist.prescale_T1, APEXrunlist.prescale_T2, APEXrunlist.prescale_T3, APEXrunlist.prescale_T4, APEXrunlist.prescale_T5, APEXrunlist.prescale_T6, APEXrunlist.prescale_T7, APEXrunlist.prescale_T8, HV_Values.value as value_1 from APEXrunlist inner join HV_Values on APEXrunlist.run_number=HV_Values.run_number where HV_Values.HV_or_I = \'read_HV\' and HV_Values.No_of_value = 3 and HV_Values.value < -200 group by APEXrunlist.run_number) as V1 inner join (select APEXrunlist.run_number, HV_Values.value as value_2 from APEXrunlist inner join HV_Values on APEXrunlist.run_number=HV_Values.run_number where HV_Values.HV_or_I = \'read_HV\' and HV_Values.No_of_value = 0 and HV_Values.value < -200 group by APEXrunlist.run_number) as V2 on V1.run_number=V2.run_number where V1.run_number in (%s)' 



values =  str(runlist)

# dbQuery += str(runlist)
# dbQuery += ')'



print(dbQuery % format_strings, runlist)

cur = db.cursor()
cur.execute(dbQuery % format_strings, runlist)
results=cur.fetchall()

print(results)
