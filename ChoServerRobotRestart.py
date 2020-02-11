from pypsexec.client import Client
import time
import sys # to raise specific exception using sys.exc_info()
start = time.time()
ip ='10.17.162.2'
try:
    c = Client('10.17.162.2', 'administrator', 'interOP@123', encrypt='False')
    c.connect()
    c.create_service()
    print('service created for following "{}".......\n\n'.format(ip))
    robotlist = ['myChinarobot77','myChinarobot76','myChinarobot50','myChinarobot47','myChinarobot57','myChinarobot17','myChinarobot14',
'myChinarobot12','myChinarobot27','myChinarobot2','myChinarobot37','myChinarobot24','myChinarobot23','myChinarobot54','myChinarobot45',
'myChinarobot43','myChinarobot63','myChinarobot89','myChinarobot74','myChinarobot99','myChinarobot100','myChinarobot96','myChinarobot97',
'myChinarobot94','myChinarobot90','myChinarobot91','myChinarobot25']
    #robotCount = 1
    for robot  in robotlist:

        callback = r"""C:\Progra~1\Nimsoft\bin\pu -u administrator -p interOP@123 /CHOSERVER1_domain/chosechub1/{}/controller restart_all_probes""".format(robot)
        print(callback)
        stdout, stderr, rc= c.run_executable("cmd.exe",arguments='''/c "{}"'''.format(callback))
        stdout = str(stdout, 'utf-8')
        stderr = str(stderr, 'utf-8')
        # print (rc)
        if rc == 0:
            print('Call back executed successfully :\nCallBackName :\n{}\nOutPut :\n{}\n\n'.format(callback, stdout))
        if rc != 0:
            print('Call back failed with error :\nCallBackName :\n{}\nOutPut :\n{}\n\n{}\n\n'.format(callback, stderr,stdout))

        time.sleep(1)

except Exception as e:
    print('Below exception occured .....\n')
    print(e)
    print()

finally:
    c.remove_service()
    c.disconnect()
print('service removed for following "{}"'.format(ip))
print ('Script has taken',(time.time()-start)/60, 'Minuts..')