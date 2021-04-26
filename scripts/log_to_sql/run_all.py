import apex_test_add_all

# runnum = '4003'


#for x in range(3500,5201): # 5023 is last run
for x in range(3500,5202): # 5023 is last run
# for x in range(4300,4302):
    print(x)

    if x is not None:
        query_vars,query_vals,HV_insert,HV_result,success = apex_test_add_all.APEX_get_end(str(x))

        if success:# if comment file was found
            apex_test_add_all.APEX_mysql(query_vars,query_vals,HV_insert,HV_result,str(x))

            print(str(query_vars) + ' ' + str(query_vals) + ' ' + str(HV_insert) + ' ' + str(HV_result) + ' --- supposed for run ' + str(x) )
            
    else:
        print("{} is none".format(x))
