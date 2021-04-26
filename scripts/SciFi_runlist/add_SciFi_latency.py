#!/usr/bin/python

#######################################################
# A python script to insert SciFi Latencies to APEXrunlist table
# Author: John Williamson
# Created: 14 May 2019
#######################################################

import sys
import os
import string
import MySQLdb


try:
    db = MySQLdb.connect(host='halladb.jlab.org', user='apexrw', passwd='Rw4p3xdb', db="apexdb")
except MySQLdb.Error:
    print("Could not connect to database. Please ensure that the paper runlist is kept up-to-date. Please email  ( jwilli@jlab.org) and include what run number this message appeared on.")
            sys.exit(1)

            

cursor = db.cursor()


query_vars = "REPLACE INTO APEXrunlist (run_number,left_SF_lat,right_SF_lat) VALUES





#cursor.execute(query_vars,query_values)


