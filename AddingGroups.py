import pypyodbc
import time

start = time.time()
cnxn = pypyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=10.17.162.1;"
                        "Database=CA_UIM_CHOSERVER1;"
                        "uid=sa;pwd=interOP@123sys")
print ('connected')
cursor = cnxn.cursor()
hubName = 2
pgrp_id = 188
for hub in range(hubName,31):
    sechubName = 'chosechub{}'.format(hubName)
    critetia = """{"isCsFilter":true,"criteriaOperator":"AND","subCriteria":[{"isCsFilter":true,"negated":false,"attribute":"ANY_ORIGIN","filterOperator":"EQUALS","value":["chosechub"]}]}"""
    critetia = critetia.replace('chosechub', sechubName)
    print (critetia)
    cursor.execute('''INSERT INTO CM_GROUP(grp_type, pgrp_id, name, name_token, description, description_token, priority, last_update, active, master_element_group, criteria)
                    VALUES ('1', {}, 'AllRobots', NULL, '', NULL, '0', '', '1', '0', '{}');'''.format(pgrp_id,critetia))

    print ('hubName is : CHOSECHUB{}'.format(hubName))
    hubName += 1
    pgrp_id +=1
    time.sleep(2)
    print('sleeping for 2 sec.....')
    cnxn.commit()
cursor.close()
cnxn.close()

print ('Scrip[t has taken : ', (time.time()-start)/60, 'Minutes............')