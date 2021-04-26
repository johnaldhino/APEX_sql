#!/usr/bin/python


#######################################################
# A python script to delete run entries 
# from sql database falsely added
# from runs that do not have a log entry
#               Variable_name : Value
# Author: John Williamson
# Created: 10 February 2020
#######################################################

import sys
import os
import string

import Directories

sys.path.append(Directories.python_dir)

import MySQLdb
from pymysql import cursors as curs

EXP = "APEX"

import csv

with open("no_file_runs.txt") as csv_file:
    csv_Dict = csv.DictReader(csv_file, delimiter=',')
            
    csv_reader = list(csv_Dict)
            

            
    try:
        db = MySQLdb.connect(host=Directories.host_name, user=Directories.user_name, db=Directories.db_name)
    except MySQLdb.Error:
        print("Could not connect to database. Please ensure that the paper runlist is kept up-to-date. Please email  ( jwilli@jlab.org) and include what run number this message appeared on.")
        sys.exit(1)


    
    for runs in csv_reader:

        sql_command = f"DELETE from {EXP}runlist where run_number={runs['Run_number']};"
        #print(sql_command)


        cursor = db.cursor()


        cursor.execute(sql_command)
