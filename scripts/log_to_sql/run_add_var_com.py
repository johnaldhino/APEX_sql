import apex_add_variables
import apex_add_com_vars

# runnum = '4003'

Entries = [] # list of dictionaries containing variable names and values to be exracted from elog end of run file, SQL column name to be inserted into

Entries = apex_add_variables.Read_Vars('Variables_com.csv')



print(f"Entries are {Entries}")


# Open up file into which run numbers lacking a text file will be listed

run_file = open('no_file_runs.txt','a')

#for x in range(3500,5201): # 3009 is last run
for x in range(3009,5023): # 5023 is last run
# for x in range(300,4302):
    print(x)

    if x is not None:


        Run_Entries = apex_add_com_vars.APEX_get_end(str(x),Entries)


        
        text_file_found = True

        for entry in Run_Entries:
            if not 'Value' in entry:
                text_file_found = False
        

            #apex_add_variables.APEX_mysql(str(x),Entries)

        

        if text_file_found:
            # print(f"For run {x} Entries = {Run_Entries}")
            apex_add_com_vars.APEX_mysql(str(x),Run_Entries)
        else:
            print(f"For run {x} log file not found")
            run_file.write(f"{x}\n")

        # query_vars,query_vals,HV_insert,HV_result,success = apex_test_add_all.APEX_get_end(str(x))

        # if success:# if comment file was found
        #     apex_test_add_all.APEX_mysql(query_vars,query_vals,HV_insert,HV_result,str(x))

        #     print(str(query_vars) + ' ' + str(query_vals) + ' ' + str(HV_insert) + ' ' + str(HV_result) + ' --- supposed for run ' + str(x) )
            
    else:
        print("{} is none".format(x))
