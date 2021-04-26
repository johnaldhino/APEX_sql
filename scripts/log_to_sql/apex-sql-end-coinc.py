#!/usr/bin/python

#######################################################
# A python script to insert run information into the
#   tritium MySQL run list.
# Author: Tyler Hague
# Created: 28 Nov 2017
#######################################################

import sys
import os
import string
import MySQLdb

#Uncomment the current experiment so that the correct table is filled.
#EXP = "TEST"
#EXP = "PRECOMMISSIONING"
#EXP = "COMMISSIONING"
#EXP = "MARATHON"
#EXP = "SRC"
#EXP = "EP"
EXP = "APEX"

DEBUG = True

#Read in the run number from the rcRunNumber file
try:
    runnum_file = open("/adaqfs/home/adaq/datafile/rcRunNumberR","r")
    runnum = runnum_file.readline()
    runnum = runnum.rstrip() #Removes \n end of line character and any trailing whitespace. There shouldn't be any in this case, but just in case
    runnum_file.close()
except IOError:
    print 'Run Number not found by the MySQL script. Please email  ( @jlab.org) and include what run number this message appeared on.'
    sys.exit(1) #Exit. Run number is the primary key, so an insert cannot be made without it

#######################################################
# Try connecting to the database. Exit if fail.
#######################################################
if not DEBUG:
    try:
        db = MySQLdb.connect(host='halladb.jlab.org', user='apexrw', passwd='Rw4p3xdb', db="apexdb")
    except MySQLdb.Error:
        print 'Could not connect to database. Please ensure that the paper runlist is kept up-to-date. Please email  ( jwilli@jlab.org) and include what run number this message appeared on.'
        sys.exit(1)

#######################################################
# Ensure that the run number exists in the table
#   We are updating the entry.
#######################################################
if not DEBUG:
    cursor = db.cursor()

    
    unique_test = "SELECT run_number FROM " + EXP + "runlist where run_number=" + runnum
    
    #Get number of entries with the current run number as a uniqueness test
    #Exit if not unique
    
    cursor.execute(unique_test)
    Evts = cursor.fetchall()
    evtAll = [Evt[0] for Evt in Evts]
    nEvtAll = len(evtAll)

    if nEvtAll==0:
        print 'This run number does not exist in the run_list. Please email  ( jwilli@jlab.org) and include what run number this message appeared on.'
        sys.exit(1)
    
    cursor2.execute(unique_test)
    Evts = cursor2.fetchall()
    evtAll = [Evt[0] for Evt in Evts]
    nEvtAll = len(evtAll)

    if nEvtAll==0:
        print 'This run number does not exist in the run_list. Please email  ( jwilli@jlab.org) and include what run number this message appeared on.'
        sys.exit(1)



update_query = "UPDATE " + EXP + "runlist SET note=\"test ocda\""
update_query += "WHERE run_number=" + runnum

if not DEBUG:
    cursor2.execute(update_query)
#######################################################
# Extract end of run info to update the database
#######################################################

# get run info here instead of when run start since the start of run info takes time to update -shujie
#runtype = "" #If something goes wrong with generating/reading this file default to blank
#comment = ""
#try:
#   title_file = open("/adaqfs/home/adaq/scripts/RUN_INFO_R.TITLE_COL","r")
#    for line in title_file:
#        if line.startswith("Run_type="):
#            run_type = line[9:].rstrip()
#        if line.startswith("comment_text="):
#            comment = line[13:].rstrip()
#    title_file.close()
#except IOError:
#    print 'Title file seems to be missing. Please email  ( jwilli@jlab.org) and include what run number this message appeared on.'

#Extracting end of run comments
try:
    comment_file = open("/adaqfs/home/adaq/scripts/.runendR.comments","r")
    found = False
    end_comment = ''
    for line in comment_file:
        if not found:
            i = 0
            while i<(len(line)-13) and not found:

                if line[i:i+13]=="comment_text=":
                    found = True
                    end_comment = line[i+13:].rstrip() + ' '
                 
                i += 1
        else:
            end_comment += line.rstrip() + ' '
    end_comment = end_comment.rstrip()
    comment_file.close()
except IOError:
    print 'The end of run comment file seems to be missing. Please email  ( jwilli@jlab.org) and include what run number this message appeared on.'

#Extract time, events, trigger totals, and charge
triggers = ['NULL' for _ in range(8)]
charge = '-0.01'
time = 'NULL'
events = 'NULL'
try:
    halog_com = open("/adaqfs/home/adaq/epics/runfiles_apex/halog_com_" + runnum + ".epics","r")
    
    found_triggers = False
    found_charge = False
    temp_cnt=0
    for line in halog_com:
        if line.startswith("EVENTS   : "):
            events = ''
            events = line[11:].rstrip()
        elif line.startswith("TIME     : "):
            i = 11
            time = ''
           
            while line[i].isdigit() or line[i]=='.':
                time += line[i]
                i += 1
        elif line.startswith("RHRS information:"): # skip the LHRS trigger info for now 
            temp_cnt+=1
            
            #  found_triggers = True
            if (temp_cnt==2):
                line=next(halog_com)
               
                i = -1
                fill = False
                
                for c in line:
                    if c==':':
                        i += 1
                        fill = True
                        triggers[i] = ''
                    elif c.isdigit() and fill:
                        triggers[i] += c
                    elif c=='-' and fill:
                        triggers[i] = '0'
                        fill = False
                    elif (c==' ' and not triggers[i]=='') or (not c.isdigit() and not c==' '):
                        fill = False
                        triggers[6]='0'
                break
            # use a separate script to calculate charge
        # elif line.startswith("APPROXIMATE BCM CHARGES"):
        #     found_charge = True
        # elif found_charge:
        #     i = 0
        #     fill = False
        #     while i<len(line):
        #         if line[i:i+6] == 'Unser:':
        #             i=i+6
        #             fill = True
        #             charge = ''
        #         elif (line[i].isdigit() or line[i]=='.') and fill:
        #             charge += line[i]
        #         elif line[i]=='-' and fill:
        #             charge = 'NULL'
        #             fill = False
        #         else:
        #             fill = False
        #         i += 1
        #     found_charge = False
    halog_com.close()
except IOError:
    print 'The halog comment file seems to be missing. Please email  ( jwilli@jlab.org) and include what run number this message appeared on.'

#######################################################
# Create and execute update statement
#######################################################
update_query = "UPDATE " + EXP + "runlist SET end_time=NOW(), end_comment=\"" + end_comment + "\", "
update_query += "event_count=" + events + ", "
update_query += "time_mins=" + time + ", "
#update_query += "charge=" + charge + ", "
update_query += "T1_count=" + triggers[0] + ", "
update_query += "T2_count=" + triggers[1] + ", "
update_query += "T3_count=" + triggers[2] + ", "
update_query += "T4_count=" + triggers[3] + ", "
update_query += "T5_count=" + triggers[4] + ", "
update_query += "T6_count=" + triggers[5] + ", "
update_query += "T7_count=" + triggers[6] + ", "
update_query += "T8_count=" + triggers[7] + " "
update_query += "WHERE run_number=" + runnum

if not DEBUG:
    cursor.execute(update_query)
    cursor2.execute(update_query)
else:
    print update_query

#print insert_query
print 'Successfully updated the MySQL run list! Have an awesome shift!'


