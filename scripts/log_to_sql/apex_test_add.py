#!/usr/bin/python

#######################################################
# A python script to test insertig info into the 
# APEX MySQL run list.
# Author: John Williamson
# Created: 1 April 2019
#######################################################

import sys
import os
import string
import MySQLdb

#Uncomment the current experiment so that the correct table is filled.

EXP = "APEX"

DEBUG = False
EXIST_CHECK = False

######################################## ###############
# Try connecting to the database. Exit if fail.
#######################################################
if not DEBUG:
    try:
        db = MySQLdb.connect(host='halladb.jlab.org', user='apexrw', passwd='Rw4p3xdb', db="apexdb")
    except MySQLdb.Error:
        print("Could not connect to database. Please ensure that the paper runlist is kept up-to-date. Please email  ( jwilli@jlab.org) and include what run number this message appeared on.")
        sys.exit(1)



    cursor = db.cursor()
    #JW: cursor can be thought of 'pointer' to row in set of rows

    runnum = '4001'
    unique_test = "SELECT run_number FROM " + EXP + "runlist where run_number=" + runnum
    
    #Get number of entries with the current run number as a uniqueness test
    #Exit if not unique
    
    cursor.execute(unique_test)
    # JW: Just tests to see if runnumber is already in DB
    Evts = cursor.fetchall()
    evtAll = [Evt[0] for Evt in Evts]
    nEvtAll = len(evtAll)

if  EXIST_CHECK:
    if nEvtAll==0:
        print("This run number does not exist in the run_list. Please email  ( jwilli@jlab.org) and include what run number this message appeared on.")
        sys.exit(1)



#Extracting end of run comments
# Open relevant file and extract comment

#print("/adaqfs/home/adaq/epics/runfiles_apex/halog_end_" + str(runnum) +".epics" )


#set columns to NULL if something goes wrong
# prescale values variables
prescaleT1 = "NULL"
prescaleT2 = "NULL"
prescaleT3 = "NULL"
prescaleT4 = "NULL"
prescaleT5 = "NULL"
prescaleT6 = "NULL"
prescaleT7 = "NULL" 
prescaleT8 = "NULL"

prescale = []

def prefunc(i,pre_i,line):
    prescale.append("NULL")
    while line[i].isdigit():
        if prescale[pre_i] == "NULL":  #overwrite NULL if we get this far
            prescale[pre_i] = line[i]
        else:
            prescale[pre_i] += line[i]
        i += 1
    while i<length and line[i]!='=': #Scan until the next equal sign. Doing this as opposed to i+=5 to make this safe for minor formatting changes in the prescale file
        i += 1
    i += 1
    return i



        
    

try:
    comment_file = open("/adaqfs/home/adaq/epics/runfiles_apex/halog_end_" + str(runnum) +".epics","r")
 #   found_com = False
    Run_type = ''
    target_type = ''
    start_comment = ''
    
    j = 0 # iterator for lines
    for line in comment_file:    
        print("no of lines {}".format(j+1))

        j += 1 
        #following lines get end of run comment
        if line.startswith("Run_type="):
            for i in range(len(line)):
            
                print("Condition passed!!")
            
                if line[i:i+13]=="comment_text=":            
                    start_comment = line[i+13:].rstrip() + ' '
                    com_k = i
                    print("Condition passed, comment text")

                if line[i:i+9]=="Run_type=":            
                    run_k = i

                if line[i:i+12]=="target_type=":            
                    targ_k = i
                    
            Run_type = line[run_k+9:(targ_k-1)]
            target_type = line[targ_k+12:(com_k-1)]

            #Run_type=Cosmics,target_type=HOME,comment_text=Cosmics test of SciFi config

        if line.startswith("PRESCALE FACTORS:"):
            print("Prescale condition passed")
            i = 21
            length = len(line)
            l = 0
            print(prescale)
            while i < length:
                i = prefunc(i,l,line)
                print(prescale)
                l += 1

        if line.startswith("TIME"):
            print("Time condition passed")
                
#PRESCALE FACTORS:ps1=30000   ps2=30000   ps3=15000   ps4=15000   ps5=1500   ps6=1   ps7=0   ps8=0   
#PRESCALE FACTORS: 


#        if
#            start_comment += line.rstrip() + ' '
   #     start_comment = start_comment.rstrip()

    start_comment = start_comment.rstrip()
    target_type = target_type.rstrip()
    Run_type = Run_type.rstrip()
    comment_file.close()
except IOError:
    print("The end of run comment file seems to be missing. Please email  ( jwilli@jlab.org) and include what run number this message appeared on.")

print(start_comment)
print(target_type)
print(Run_type)

print(len(prescale))
for i in range(len(prescale)):
    print(prescale[i])


#######################################################
# Create and execute update statement
#######################################################


insert_query = "INSERT INTO " + EXP + "runlist (run_number,"
insert_query +=  "end_comment,"
insert_query +=  "target,"
insert_query +=  "run_type,"
insert_query += "prescale_T1, "
insert_query += "prescale_T2, "
insert_query += "prescale_T3, "
insert_query += "prescale_T4, "
insert_query += "prescale_T5, "
insert_query += "prescale_T6, "
insert_query += "prescale_T7, "
insert_query += "prescale_T8) "


insert_query += "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
record_to_insert = [runnum, str(start_comment),str(target_type),str(Run_type)]

for i in range(len(prescale)):
    record_to_insert.append(prescale[i])

print(record_to_insert)
print(insert_query)

#insert_query += " %s)", str(end_comment)

if not DEBUG:
#    cursor.execute(insert_query,record_to_insert)
    print(insert_query)
else:
    print(insert_query)

#print(insert_query)
print("Type of insert_query is : {}".format(type(insert_query)))
print("Type of record_to_insert is : {}".format(type(record_to_insert)))
