import pypyodbc
import time

start = time.time()
cnxn = pypyodbc.connect("Driver={SQL Server};"
                        "Server=10.17.162.1;"
                        "Database=CA_UIM_CHOSERVER1;"
                        "uid=sa;pwd=interOP@123sys")
print ('connected')
cursor = cnxn.cursor()
flag = 0
while True:
    cursor.execute(''' select status, count(1) from ssrv2profile where profileNaME = 'mcs_dirscan'  group by status;''')
    row = cursor.fetchall()
    for i in row:
        i = i[0]
        print('OK state Count is ....',i,end='               ')
        cursor.execute(''' select count(*) from CM_COMPUTER_SYSTEM cs inner join SSRV2Profile  sp on cs.cs_id = sp.cs_id where convert(date,sp.created) = convert(date,GETDATE()) and profileName = 'mcs-logmon' and status = 'new';''')
        row1 = cursor.fetchall()
        cursor.execute(''' select count(*) from CM_COMPUTER_SYSTEM cs inner join SSRV2Profile  sp on cs.cs_id = sp.cs_id where convert(date,sp.created) = convert(date,GETDATE()) and profileName = 'mcs-logmon' and status = 'pending';''')
        row2 = cursor.fetchall()
        for pending in row2:
            print ('Pending State Count is .....',pending[0],end='               ')
        for new in row1:
            print('New State Count is ....',new[0])
        if i == 2100:

            flag =1
            print('done')
            break

    if flag ==1:
        break
    time.sleep(2)
print ('Scrip[t has taken : ', (time.time()-start)/60, 'Minutes............')

