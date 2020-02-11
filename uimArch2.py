import sys
from pypsexec.client import Client
import time
start = time.time()
class UimArch:
    def __init__(self):
        self.ip = '10.17.188.108'
        self.uimDomain = 'W12R2SERVER4_domain'
        # lineCount = 0
        self.robotList = []
        self.probesList = []
        self.hubsrobos = {}
        self.hubs = {}
    def remoteConnection(self) :
        try:
            conn = Client(self.ip, 'administrator', 'interOP@123sys', encrypt='False')
            conn.connect()
            return conn
        except Exception as e:
            print('Below exception occured .....\n')
            print(e)
            print()
    def hubLists(self):
       try:
            lineCount = 0
            self.remoteConnection().create_service()
            print('service created for following "{}".......\n\n'.format(self.ip))
            callback = r"""C:\Progra~1\Nimsoft\bin\pu -u administrator -p interOP@123 /W12R2SERVER4_domain/W12R2SERVER4_hub/W12R2SERVER4/hub gethubs"""
            stdout, stderr, rc = self.remoteConnection().run_executable('cmd.exe',arguments='''/c {}'''.format(callback))
            stdout = str(stdout, 'utf-8');stderr = str(stderr, 'utf-8')
            #print(stdout)
            for word in stdout.split('\n'):
                if lineCount >= 7:
                    if 'addr' in word and  self.uimDomain in word:
                        dummy, domain, hub, robot, probe = word.split('/')
                        self.hubs[hub] = robot
                lineCount +=1
            # print(self.hubs)
       except Exception as e:
            print('Below exception occured .....\n')
            type, value, traceback = sys.exc_info()
            print('Error opening %s: %s' % (value.filename, value.strerror))
            print()
    def robotLists(self):
        try:
            lineCount = 0
            robotlist = []
            probelist = []
            # self.remoteConnection().create_service()
            # print('service created for following "{}".......\n\n'.format(self.ip))
            ''' ################################# Collecting robots using hub dictionory ############################## '''
            for hub,robot in self.hubs.items():
                self.hubsrobos[hub] = {}    #    Creating nested dictionary for hub entry
                callback = r"""C:\Progra~1\Nimsoft\bin\pu -u administrator -p interOP@123 /W12R2SERVER4_domain/{}/{}/hub getrobots "" """"".format(hub,robot)
                stdout, stderr, rc = self.remoteConnection().run_executable('cmd.exe',arguments='''/c {}'''.format(callback))
                stdout = str(stdout, 'utf-8');stderr = str(stderr, 'utf-8')
                for word in stdout.split('\n'):
                    if word.startswith('  addr ')  and  self.uimDomain in word:
                        dummy, domain, hub, robot = word.split('/')
                        robot=robot.replace('\r','')
                        robotlist.append(robot)

                ''' ############################## Collecting probes using above robotlist ################################## '''
                for robot in robotlist:
                    self.hubsrobos[hub][robot] = [] # creating list object for nested dictionary i.e: robot
                    callback = r"""C:\Progra~1\Nimsoft\bin\pu -u administrator -p interOP@123 /W12R2SERVER4_domain/{}/{}/controller probe_list "" """"".format(hub,robot)
                    stdout, stderr, rc = self.remoteConnection().run_executable('cmd.exe',arguments='''/c {}'''.format(callback))
                    stdout = str(stdout, 'utf-8');
                    stderr = str(stderr, 'utf-8')
                    for word in stdout.split('\n'):
                        if word.startswith(' name'):
                            probe = [x for x in word.split()]
                            # robot=probe.replace('\r','')
                            if probe[-1] not in ['controller', 'spooler', 'hdb']:
                                probelist.append(probe[-1])
                                self.hubsrobos[hub][robot].append(probe[-1])   # adding probes to list in dictionary at robot level
                    print('probes for {} : {} '.format(robot, probelist))
                    probelist.clear()
                print('robots for {}  :  {}'.format(hub,robotlist))
                robotlist.clear()
                print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            print(self.hubsrobos)


        except Exception as e:
            print('Below exception occured .....\n')
            type, value, traceback = sys.exc_info()
            print('Error opening %s: %s' % (value.filename, value.strerror))
            #print(e)
            print()
    def remoteConnectionClose(self):
        self.remoteConnection().remove_service()
        self.remoteConnection().disconnect()
        print('service removed for following "{}"'.format(self.ip))
        print ('Script has taken',(time.time()-start)/60, 'Minuets..')

obj = UimArch()
obj.remoteConnection()
obj.hubLists()
obj.robotLists()
# obj.probesLists()
obj.remoteConnectionClose()

