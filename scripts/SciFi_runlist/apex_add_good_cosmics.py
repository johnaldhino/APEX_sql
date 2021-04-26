
#!/usr/bin/python

#######################################################
# A python script to insert list to csv file
# Author: John Williamson
# Created: 13th May 2019
#######################################################

import sys
import os
import string
import MySQLdb
import csv


#-----------------------------------------------------
def csv_writer(data, path):
    """
    Write data to a CSV file 
    """
    with open(path, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        
        for line in data:
            writer.writerow(line)


#---------------------------------------------------
# Add numbers to runlist 

def add_numbers(first, last, data):
    for i in range(last+1-first):
        data.append([first+i])


#---------------------------------------------------


data = [[3505],[3506]]


#add_numbers(3528,3592,data)

number_list = [[3528,3592],[3667,3668],[3753,3753],[3831,3831],[3999,4011],[4036,4037],[4060,4060],[4103,4104],[4117,4118],[4112,4124],[4367,4367],[4370,4372],[4415,4417],[4490,4494],[4538,4546],[4621,4624],[4661,4661],[4972,4975],[5008,5020]]

for entry in number_list:
   add_numbers(entry[0],entry[1],data)
        





path = "/adaqfs/home/adaq/scripts/APEX-sql/SciFi_runlist/good_cosmics.csv"


for line in data:
    print(line)

csv_writer(data,path)




