#!/usr/bin/python

#######################################################
# A python script to extract various parameters
# from end of run log files
# Specifically those thar are printed in the log file 
# in the format:
#               Variable_name : Value
# Author: John Williamson
# Created: 10 February 2020
#######################################################



# different beam energy run parameters:
# 'Set Beam energy (MeV)' 
# Tiefenbach 6GeV Beam energy (MeV) : 2138.14
# Tiefenbach 6GeV orbit correction (dpp) : 0
# Injector Measured Energy : 115.298
# Average North Linac Measured Energy : 1004.05066666666667
# Average South Linac Measured Energy : 1019.02
#
# Set Beam and first Tiefenbach measured are most important parameters I think
# first Tiefenbach measured  is sum of last three measurements
#
#
# Beam current parameters:
#  Beam Current, I think this is the correct measurement of the beam current
#
#
#
# VDC H.V.




import sys
import os
import string
#import MySQLd
#import _mysql

import Directories

sys.path.append(Directories.python_dir)

import MySQLdb
from pymysql import cursors as curs


import csv


import copy

EXP = "APEX"

DEBUG = False
EXIST_CHECK = False





def Read_Vars(Varfile):

    Entries = []
  


    try:
        with open(Varfile) as csv_file:
            csv_Dict = csv.DictReader(csv_file, delimiter=',')
            
            csv_reader = list(csv_Dict)
            
            for row in csv_reader:

                # print(f"SQL name = {row['SQL_name']}")
                # print(f"CODA name = {row['CODA_name']}")
                # print(f"var type = {row['var_type']}")
                


                new_dic = {"SQL_name" : row['SQL_name'], "CODA_name" : row['CODA_name'], "var_type" : row['var_type']}

                           
                Entries.append(new_dic)

        return Entries;

    
    except:
        print("Opening Variables text file failed")




def APEX_get_end(runnum, In_Entries):


    #Extracting end of run comments
    # Open relevant file and extract comment

    Entries =  copy.deepcopy(In_Entries)


    try:
        #comment_file = open("/adaqfs/home/adaq/epics/runfiles_apex/halog_end_" + str(runnum) +".epics","r")
        comment_file = open(Directories.log_file_dir + "halog_end_" + str(runnum) +".epics","r")
        
        ## Below lines get list of line offsets (can be used for HV)
        line_offset = []
        
        offset = 0
        line_offset.clear()
        for line in comment_file:    
            line_offset.append(offset)
            offset += len(line)
        comment_file.seek(0)



        found_com = True
    
        j = 0 # iterator for lines


        for line in comment_file:    


            
            
            for Entry in Entries:
                
                

                Var = Entry['CODA_name']
                if line.startswith(Var) and not 'Value' in Entry:
                    #print(f"Line {j} starts with {Var}")
                    #print(f"line = {line}")
                    var_p = line.find(Var) + len(Var) +1
                    Entry['Value'] = float(line[var_p:len(line)-1])



            j = j+1



    except IOError:
        print("The end of run comment file seems to be missing. Please email  ( jwilli@jlab.org) and include what run number this message appeared on.")
        print("For run number {}".format(runnum))
        found_com = False
        
        




        




    return Entries




#         #######################################################
#         # Create and execute update statement
#         #######################################################


def APEX_mysql(runnum, Entries):

    
    ######################################## ###############
    # Try connecting to the database. Exit if fail.
    #######################################################




    if not DEBUG:
        try:
            db = MySQLdb.connect(host=Directories.host_name, user=Directories.user_name, db=Directories.db_name)
        except MySQLdb.Error:
            print("Could not connect to database. Please ensure that the paper runlist is kept up-to-date. Please email  ( jwilli@jlab.org) and include what run number this message appeared on.")
            sys.exit(1)



        cursor = db.cursor()
        #JW: cursor can be thought of 'pointer' to row in set of rows


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




        #insert_query = "INSERT INTO " + EXP + "runlist (run_number,"
        update_query = "UPDATE " + EXP + "runlist SET "
        

        # retrieve sql column names

        for item in Entries:
            #            insert_query += f"{item['SQL_name']},"
            update_query += f"{item['SQL_name']} = {item['Value']}, "

            
        #        insert_query = insert_query[:-1]
        update_query = update_query[:-2]
    

    
        # retreive values


        # insert_query += f") VALUES({runnum},"
    
        # for item in Entries:
        #     insert_query += f"{item['Value']},"

        
        update_query += f" WHERE run_number = {runnum}"

    
        #        insert_query = insert_query[:-1]
        #insert_query += ")"
        

        print(update_query)
        cursor.execute(update_query)


