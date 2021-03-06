#!/usr/bin/python

#######################################################
# A python script to obtain production runlist
# APEX MySQL run list.
# Author: John Williamson
# Created: 11 April 2019
#######################################################

import sys
import os
import string
import MySQLdb
import csv


# dbserver='halladb.jlab.org'
# dbpass='4p3xu$3r'
# dbSchema='apexdb'
# dbUser='apex-user'  # chose user as script need not change anything in db

#  mysql -h npls3 -u apexuser

dbserver='npls3'
dbSchema='apexdb'
dbUser='apexuser'  # chose user as script need not change anything in db


try:
#    db = MySQLdb.connect(host=dbserver, user=dbUser, passwd=dbpass, db=dbSchema)
    db = MySQLdb.connect(host=dbserver, user=dbUser, db=dbSchema)
except MySQLdb.Error:
    print("Could not connect to database. Please ensure that the paper runlist is kept up-to-date. Please email  ( jwilli@jlab.org) and include what run number this message appeared on.")
    sys.exit(1)

dbQuery = 'select run_number from APEXrunlist where (beam_current > 2.0 OR beam_current_alt > 2.0)  AND run_type = \'Production\' AND dead_time < 50 order by run_number'

    
cur = db.cursor()
    

cur.execute(dbQuery)
# columns = cur.description
# results = [{columns[index][0]:column for index, column in enumerate(value)} for value in cur.fetchall()]
results=cur.fetchall()

col_names = [i[0] for i in cur.description]

# write results as csv file
fp = open('production_runlist/production_runlist.csv','w')
myfile = csv.writer(fp)
myfile.writerow(col_names)
myfile.writerows(results)
fp.close()


# write results as text file (seperated by spaces)
with open('production_runlist/production_runlist.txt', 'w') as fw:
    for row in results:
        print(row[0]) # gets only first element (run number)
        fw.write(f"{row[0]}\n")
