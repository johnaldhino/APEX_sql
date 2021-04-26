#!/usr/bin/python

#######################################################
# A python script to test getting SciFi runlist from Database
# APEX MySQL run list.
# Author: John Williamson
# Created: 11 April 2019
#######################################################

import sys
import os
import string
import MySQLdb
import csv


###############################################
# command to get various related parameters ####################
#
# select run_number from APEXrunlist where run_type = 'SciFi';
# -- gets runs where SciFi was in comments
#
#  select Run_number from HV_Values where (Detector = 'SciFi' and HV_or_I = 'read_HV' and No_of_value = 0 and value < -200) or (Detector = 'SciFi' and HV_or_I = 'read_HV' and No_of_value = 3 and value < -200) group by Run_number;
# --- gets runs where either left or right (0th or 3rd read HV) is above a certain value
#
#
#
#select run_number from APEXrunlist where run_type = 'SciFi' and run_number not in (  select Run_number from HV_Values where (Detector = 'SciFi' and HV_or_I = 'read_HV' and No_of_value = 0 and value < -200) or (Detector = 'SciFi' and HV_or_I = 'read_HV' and No_of_value = 3 and value < -200) ) group by run_number;
#----- command gets all runs where run-type is SciFi but HV aren't changed


dbserver='halladb.jlab.org'
dbpass='4p3xu$3r'
dbSchema='apexdb'
dbUser='apex-user'  # chose user as script need not change anything in db


try:
    db = MySQLdb.connect(host=dbserver, user=dbUser, passwd=dbpass, db=dbSchema)
except MySQLdb.Error:
    print("Could not connect to database. Please ensure that the paper runlist is kept up-to-date. Please email  ( jwilli@jlab.org) and include what run number this message appeared on.")
    sys.exit(1)


### form query here to execute later

## both these are described above
dbQuery_comment = 'select run_number from APEXrunlist where run_type = \'SciFi\'' 

dbQuery_HV = 'select Run_number from HV_Values where (Detector = \'SciFi\' and HV_or_I = \'read_HV\' and No_of_value = 0 and value < -200) or (Detector = \'SciFi\' and HV_or_I = \'read_HV\' and No_of_value = 3 and value < -200) '


cur = db.cursor()


#select run_number from APEXrunlist where run_type = 'SciFi' and run_number not in (  select Run_number from HV_Values where (Detector = 'SciFi' and HV_or_I = 'read_HV' and No_of_value = 0 and value < -200) or (Detector = 'SciFi' and HV_or_I = 'read_HV' and No_of_value = 3 and value < -200) ) group by run_number;


# query to get the union of runs with SciFi comment and switched on HV

dbQuery = dbQuery_comment + " or run_number in (" + dbQuery_HV + ") group by run_number;"
cur.execute(dbQuery)
results=cur.fetchall()

fp = open('SciFi_runlist/all_runs.csv','w')
myfile = csv.writer(fp)
myfile.writerows(results)
fp.close()


# query to get runs the SciFi comment but not HV
dbQuery = dbQuery_comment + " and run_number not in (" + dbQuery_HV + ") group by run_number;"
print(dbQuery)
cur.execute(dbQuery)
results=cur.fetchall()

fp = open('SciFi_runlist/comment_nohV_runs.csv','w')
myfile = csv.writer(fp)
myfile.writerows(results)
fp.close()


# query to get runs with HV but not SciFi comment
dbQuery = dbQuery_HV + " and run_number not in (" + dbQuery_comment + ") group by run_number;"
print(dbQuery)
cur.execute(dbQuery)
results=cur.fetchall()

fp = open('SciFi_runlist/nocomment_HV_runs.csv','w')
myfile = csv.writer(fp)
myfile.writerows(results)
fp.close()









