#!/usr/bin/python

#######################################################
# A python script to test inserting info into the 
# APEX MySQL run list.
# Author: John Williamson
# Created: 1 April 2019
#######################################################

import sys
import os
import string
#import MySQLdb
#import _mysql

import Directories

#Uncomment the current experiment so that the correct table is filled.

#sys.path.append(" ~/.local/lib/python3.7/site-packages")
#sys.path.append("/home/johnw/.local/lib/python3.7/site-packages")
sys.path.append(Directories.python_dir)

for p in sys.path:
    print(p)
    


#import mysqlclient
#import MySQLdb
import MySQLdb
#import pymysql
from pymysql import cursors as curs
#import _mysql

EXP = "APEX"

DEBUG = False
EXIST_CHECK = False
#sethv = False


def HV_parse(line,m,n,sethv,HV,no_HV):

    line_length = len(line)

    if not sethv:
        n = m +n  # set marker for where "Set HV (V)" is
        
        sethv = True

#        print("notsethv condition with m = {} and n = {}".format(m,n))

        
                    
    if m > n:
            
#        print("m bigger than n condition with m = {} and n = {}".format(m,n))
        while line[m].isdigit():
                if HV[no_HV] == "NULL":  #overwrite NULL if we get this far
                    if line[m-1] == '-':
                        HV[no_HV] = line[m-1]
                        HV[no_HV] +=line[m]
#                        print("- condition with m = {} and n = {}, and line[m] = {}".format(m,n,line[m]))
                    else:
                        HV[no_HV] = line[m]
                    m +=1
                else:
                    HV[no_HV] += line[m]
                    m += 1
        while m<line_length and not line[m].isdigit():
            m += 1

        if HV[no_HV] != "NULL" and m < line_length: 
            no_HV += 1
            HV.append("NULL")
        else:
            pass
#            m += 1
    else:
        m += 1
    return [HV,m,n,sethv,no_HV]

def prefunc(i,pre_i,line,prescale):
    prescale.append("NULL")
    length = len(line)
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

comment_file = ''
line_offset = []

def getHV(line_no,comment_file,no_HV,no_rows=1):
#    for i in range(0,4):
#    first parameter is line in comment file (line_no)
#    2nd parameter is comment file which is beig read
#    3rd parameter is number of HV entries per row
#    4th parameter is number of rows of HV entries


    # print("~~~~~~~~")
    # print(str(line_no))
    #    comment_file.seek(line_offset[line_no]) # this line is detector name
    comment_file.seek(line_offset[line_no+2]) # these line are channel names

    
    line_count = 0
    line_limit = 3
    
    # Hold HV set values
    HV = []
    HV.append("NULL")

    # holds HV read values
    RV = [] 
    RV.append("NULL")

    # holds measured current valuers (micro-Amps)
    i_vals = []
    i_vals.append("NULL")

    for line in comment_file:
 

        space_counter = 0
        if line_count < line_limit:
            # print("======= printing line{}  ============".format(line_no+2+line_count))
            # print(line)

            line_length = len(line)


            sethv =  False
            readhv = False
            i_read = False

            no_HV = 0
            no_RV = 0
            no_I = 0

            m = 0
            n = 10000

            while m < line_length:
                if line[m:m+10]=="Set HV (V)" or sethv:
                    n = 10
                    [HV,m,n,sethv,no_HV] = HV_parse(line,m,n,sethv,HV,no_HV)
#                    print("SciFi set HV    with m = {}".format(m))

                    
                elif line[m:m+11]=="Read HV (V)" or readhv:
                    n = 11
                    [RV,m,n,readhv,no_RV] = HV_parse(line,m,n,readhv,RV,no_RV)
#                    print("SciFi Read HV    with m = {}".format(m))

                elif line[m:m+6]=="I (uA)" or i_read:
                    n = 6
                    # I (uA)        -338     -0     -1   -338      0     -2 
                    [i_vals,m,n,i_read,no_I] = HV_parse(line,m,n,i_read,i_vals,no_I)
#                    print("SciFi currents   with m = {}".format(m))


                else:
#                    print("'miss' condition with m = {}".format(m))
                    m += 1


                #     if not sethv:
                #         n = m +10  # set marker for where "Set HV (V)" is

                #     sethv = True
                    
                #     if m > n:
                        
                #         while line[m].isdigit():
                #             if HV[no_HV] == "NULL":  #overwrite NULL if we get this far
                #                 if line[m-1] == '-':
                #                     HV[no_HV] = line[m-1]
                #                     HV[no_HV] +=line[m]
                #                 else:
                #                     HV[no_HV] = line[m]
                #                 m +=1
                #             else:
                #                 HV[no_HV] += line[m]
                #                 m += 1
                #         while m<line_length and not line[m].isdigit():
                #             m += 1

                #         if HV[no_HV] != "NULL" and m < line_length: 
                #             no_HV += 1
                #             HV.append("NULL")
                #     else:
                #         m += 1

                # else:
                #     m +=1
















            line_count +=1
                    


                    # if m > 15 and not line[m] == ' ':
                    #     if HV[nohv] == "NULL":
                    #         HV[nohv] = line[m]
                    #     else:
                    #         HV[nohv] += line[m]
                        
                    # if m > 15 and line[m] == ' ':
                    #     space_counter += 1
                    #     if space_counter%3 == 0:
                    #         nohv += 1


                    # for nohv in range(no_HV):
# #                        print("SciFi condition passed with m = {} and m + 1 = {}".format(m,m+10))
#                         HV[nohv] = line[m+15:m+19]
        

    
    comment_file.seek(line_offset[line_no+2])

    # print(comment_file.readline())
    # print("~~~~~~~~")
    comment_file.seek(line_offset[line_no+1])

    return [HV,RV,i_vals]

# SciFi
#                CH1      2      3      4      5     6       
# Set HV (V)     -750  -1400  -1400   -750      0  -1200 
# Read HV (V)    -751     -4     -3   -751    -13     -4 
# I (uA)        -338     -0     -1   -338      0     -2 






def APEX_get_end(runnum):

    ######################################## ###############
    # Try connecting to the database. Exit if fail.
    #######################################################
    if not DEBUG:
        try:
#            db = MySQLdb.connect(host='halladb.jlab.org', user='apexrw', passwd='Rw4p3xdb', db="apexdb")
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


    
    try:
#        comment_file = open("/adaqfs/home/adaq/epics/runfiles_apex/halog_end_" + str(runnum) +".epics","r")
        comment_file = open(Directories.log_file_dir + str(runnum) +".epics","r")
        
        ## Below lines get list of line offsets (can be used for HV)
        #        line_offset = []
        
        HV = []
        offset = 0
        line_offset.clear()
        for line in comment_file:    
            line_offset.append(offset)
            offset += len(line)
        comment_file.seek(0)



        found_com = True
        Run_type = ''
        target_type = ''
        start_comment = ''
    
        j = 0 # iterator for lines
        for line in comment_file:    

            #if j % 20 == 0:
            #            print("no of lines {}".format(j))

            #            j += 1 
            #following lines get end of run comment
            if line.startswith("Run_type="):

                # intialise in case they are not found
                targ_k = None
                run_k = None
                com_k = None

                for i in range(len(line)):
            
                    #                    print("Condition passed!!")
            
                    if line[i:i+13]=="comment_text=":            
                        start_comment = line[i+13:].rstrip() + ' '
                        com_k = i
                        print("Condition passed, comment text")

                    if line[i:i+9]=="Run_type=":            
                        run_k = i

                    if line[i:i+12]=="target_type=":            
                        targ_k = i
                    
                if not targ_k == None and not run_k ==  None:
                    Run_type = line[run_k+9:(targ_k-1)]

                if not targ_k == None and not com_k == None:
                    target_type = line[targ_k+12:(com_k-1)]

                print("after targ_k etc")

                #Run_type=Cosmics,target_type=HOME,comment_text=Cosmics test of SciFi config

            if line.startswith("PRESCALE FACTORS:"):
#                print("Prescale condition passed")
                i = 21
                length = len(line)
                l = 0
   #             print(prescale)
                while i < length:
                    i = prefunc(i,l,line,prescale)
#                    print(prescale)
                    l += 1

#            if line.startswith("TIME"):
#                print("Time condition passed")
                
            if line.startswith("SciFi"):
                #                HV = []
#                print("SciFI condition passed")
                
                [HV ,RV,i_vals]= getHV(j,comment_file,6)
                
                if DEBUG:
                    print("Number of HV values is {}".format(len(HV)))
                    print("Found HV for SciFi is {}".format(HV))
                
                    print("Number of HV read (RV) values is {}".format(len(RV)))
                    print("Found RV for SciFi is {}".format(RV))

                    print("Number of current read values is {}".format(len(i_vals)))
                    print("Found i_vals for SciFi is {}".format(i_vals))
                


            #PRESCALE FACTORS:ps1=30000   ps2=30000   ps3=15000   ps4=15000   ps5=1500   ps6=1   ps7=0   ps8=0   
            #PRESCALE FACTORS: 


            #        if
            #            start_comment += line.rstrip() + ' '
            #     start_comment = start_comment.rstrip()

            j += 1 

        start_comment = start_comment.rstrip()
        target_type = target_type.rstrip()
        Run_type = Run_type.rstrip()
        
        if len(prescale) == 0:
            for x in range(0,8):
                prescale.append("NULL")
                
                #        print(prescale)
                
        print("until end of comment_file stuff")

        comment_file.close()
    except IOError:
        print("The end of run comment file seems to be missing. Please email  ( jwilli@jlab.org) and include what run number this message appeared on.")
        print("For run number {}".format(runnum))
        found_com = False

        return('not found','not found','not found','not found',found_com)


    # following checks if comment fiel was found before trying to print
    if found_com and DEBUG:
        
        print(start_comment)
        print(target_type)
        print(Run_type)

        print(len(prescale))
        for i in range(len(prescale)):
            print(prescale[i])

    print("after found and debug print statemnt")
        #######################################################
        # Create and execute update statement
        #######################################################

        #INSERT INTO test (run_number,comment, creation) VALUES (2000, 'First Run!', '2018-01-01') ON DUPLICATE KEY UPDATE creation = '2018-01-01';



    insert_query = "REPLACE INTO " + EXP + "runlist (run_number,"
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

    
    #INSERT INTO test (run_number,comment, creation) VALUES (2000, 'First Run!', '2018-01-01') ON DUPLICATE KEY UPDATE creation = '2018-01-01';

    for i in range(len(prescale)):
        record_to_insert.append(prescale[i])
        
    print("reached before printing record to insert")
        
    print(record_to_insert)
    print(insert_query)

            #insert_query += " %s)", str(end_comment)





        #  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Put together statement to add SciFi (and other HV) table
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


        # Run_number,  Detector, HV_or_I , No_of_value, Value -- columns to put into

        # Arrays being inserted -- HV, RV, i_vals

    HV_insert_query = "REPLACE INTO " + "HV_Values (Run_number,Detector, HV_or_I , No_of_value, Value) VALUES(%s,%s,%s,%s,%s) "

        # # modify inset_query (to put in appropriate no of %s)
        # for j in range(len(HV[0])-1):
        #                HV_insert_query += "%s,"

        # HV_insert_query += "%s)"

    HV_result = []


    for val in range(len(HV)):

        if range(len(HV) == len(RV)):
                        
            

            # line for setHV
            line = [runnum, 'SciFi', 'set_HV', val, HV[val]]
            HV_result.append(line)
                
            # line for Read HV
            line = [runnum, 'SciFi', 'read_HV', val, RV[val]]
            HV_result.append(line)
            # line for current
            line = [runnum, 'SciFi', 'current', val, i_vals[val]]
            HV_result.append(line)
            
            print(HV_insert_query)
            #        print(HV_result)
            
        



    if found_com:
        return(insert_query,record_to_insert,HV_insert_query,HV_result,found_com)

    if not found_com:
        #            return('not found','not found',found_com)
        return('not found','not found','not found','not found',found_com)


            
        
        # if not DEBUG:
        # #    cursor.execute(insert_query,record_to_insert)
        #     print(insert_query)
        # else:
        #     print(insert_query)
        
        # print(insert_query)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~ Function to carry out mysql insertion ~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def APEX_mysql(query_vars,query_values, HV_vars, HV_vals, runnum):

    ## first part of function checks if db exists
    
    if not DEBUG:
        try:
#            db = MySQLdb.connect(host='halladb.jlab.org', user='apexrw', passwd='Rw4p3xdb', db="apexdb")
            db = MySQLdb.connect(host=Directories.host_name, user=Directories.user_name, db=Directories.db_name)
        except MySQLdb.Error:
            print("Could not connect to database. Please ensure that the paper runlist is kept up-to-date. Please email  ( jwilli@jlab.org) and include what run number this message appeared on.")
            sys.exit(1)


        print("reached before cursor")
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


    # ~~~~~ Here is where data is inserted into table

    if not DEBUG:
        
        print("Reached stage before first execution")
        cursor.execute(query_vars,query_values)
        print("Reached stage before after execution")

        if DEBUG:
            print(query_vars,query_values)
           # line added for HVs

        for i in range(len(HV_vals)):
            cursor.execute(HV_vars,HV_vals[i])
            if DEBUG:
                print(HV_vars,HV_vals[i])
                 #           print(query_vars)
    else:
        pass
        #print(query_vars)
        
        #    print(query_vars)

 


        # runnum = '4002'

        # query_vars,query_vals = APEX_get_end(runnum)

        # APEX_mysql(query_vars,query_vals,runnum)


