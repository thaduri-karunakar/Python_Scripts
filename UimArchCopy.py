import sys
from pypsexec.client import Client
import time

start = time.time()

class UimArch:
    def __init__(self):
        self.ip = '10.17.188.108'
        self.uimDomain = 'W12R2SERVER4_domain'
        self.hubsrobos = {}
        self.hubs = {}
        self.uimarchhubsrobots = {}
        self.default_probes = {'robot_update_secure', 'hub_secure', 'distsrv', 'nas', 'automated_deployment_engine', 'data_engine', 'ace', 'mpse', 'maintenance_mode', 'baseline_engine', 'prediction_engine', 'sla_engine',
                               'qos_processor', 'nis_server', 'discovery_server', 'discovery_agent', 'cm_data_import', 'udm_manager', 'ppm', 'ems', 'relationship_services', 'topology_agent',
                               'fault_correlation_engine', 'wasp', 'trellis', 'mon_config_service', 'usage_metering', 'telemetry', 'webgtw', 'hub_adapter', 'HA'}

    def remote_connection(self):
        try:
            conn = Client(self.ip, 'administrator', 'interOP@123sys', encrypt='False')
            conn.connect()
            return conn
        except Exception as e:
            print('Below exception occured .....\n')
            print(e)
            print()

    def hublists(self):
        try:
            self.remote_connection().create_service()
            print('service created for following "{}".......\n\n'.format(self.ip))
            callback = r"""C:\Progra~1\Nimsoft\bin\pu -u administrator -p interOP@123 /W12R2SERVER4_domain/W12R2SERVER4_hub/W12R2SERVER4/hub gethubs"""
            hub_stdout, stderr, rc = self.remote_connection().run_executable('cmd.exe', arguments='''/c {}'''.format(callback))
            self.hub_stdout = str(hub_stdout, 'utf-8'); stderr = str(stderr, 'utf-8')
            #print(stdout)

            self.string_partition('hub')    # Calling string_partition function for taking hubs from calllback
        except Exception as e:
            print('Below exception occured .....\n')
            type, value, traceback = sys.exc_info()
            print('Error opening %s: %s' % (value.filename, value.strerror))
            print()

    def robotlists(self):
        try:
            robotlist = []
            ''' ################################# Collecting robots using hub dictionory ############################## '''
            for hub, robot in self.hubs.items():
                self.hubsrobos[hub] = {}  # Creating nested dictionary for hub entry
                callback = r"""C:\Progra~1\Nimsoft\bin\pu -u administrator -p interOP@123 /W12R2SERVER4_domain/{}/{}/hub getrobots "" """"".format(hub, robot)
                robot_stdout, stderr, rc = self.remote_connection().run_executable('cmd.exe', arguments='''/c {}'''.format(callback))
                robot_stdout = str(robot_stdout, 'utf-8'); stderr = str(stderr, 'utf-8')


                self.string_partition('robot')  # Calling string_partition function for taking robots from callback

                ''' ############################## Collecting probes using above robotlist ################################## '''
                for robot in robotlist:
                    self.hubsrobos[hub][robot] = {}  # creating nested disctionary for robot to store probes
                    callback = r"""C:\Progra~1\Nimsoft\bin\pu -u administrator -p interOP@123 /W12R2SERVER4_domain/{}/{}/controller probe_list "" """"".format(hub, robot)
                    stdout, stderr, rc = self.remote_connection().run_executable('cmd.exe',arguments='''/c {}'''.format(callback))
                    stdout = str(stdout, 'utf-8'); stderr = str(stderr, 'utf-8')
                    # print(stdout)
                    for word in stdout.split('\n'):
                        if word.startswith(' pkg_name'):
                            pkg_name = [x for x in word.split()]
                            # robot=probe.replace('\r','')
                            # probelist.append(probe[-1])
                            self.hubsrobos[hub][robot][pkg_name[-1]] = 0  # adding probes in dictionary at robot level
                        if word.startswith(' pkg_version'):
                            pkg_version = [x for x in word.split()]
                            # robot=probe.replace('\r','')
                            # probelist.append(probe[-1])
                            self.hubsrobos[hub][robot][pkg_name[-1]] = pkg_version[-1]
                    # print('probes for {} : {} '.format(robot, probelist))
                    # probelist.clear()
                # print('robots for {}  :  {}'.format(hub,robotlist))
                robotlist.clear()
                # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            # print(self.hubsrobos)
        except Exception as e:
            print('Below exception occured .....\n')
            type, value, traceback = sys.exc_info()
            print('Error opening %s: %s' % (value.filename, value.strerror))
            # print(e)
            print()

    def pkg_name_removing(self):
        for hub in self.hubsrobos:
            self.uimarchhubsrobots[hub] = {}
            for robot in self.hubsrobos[hub]:
                self.uimarchhubsrobots[hub][robot] = {}
                for probe, version in self.hubsrobos[hub][robot].items():
                    if probe not in self.default_probes:
                        self.uimarchhubsrobots[hub][robot][probe] = version
        print(self.uimarchhubsrobots)
        del self.hubsrobos
        with open('uimarchhubsrobots.py', 'w+') as file:
            file.write('uimarchhubsrobots = ')
            file.write(str(self.uimarchhubsrobots))

    def remote_connection_close(self):
        self.remote_connection().remove_service()
        self.remote_connection().disconnect()
        print('service removed for following "{}"'.format(self.ip))
        print('Script has taken', (time.time() - start) / 60, 'Minuets..')

    def hubs_robots_probes_list(self):
        hubcount = 1
        robotcount = 1
        print('Below are the hubs present on the server :\n','='*42,sep='')
        for hub in self.uimarchhubsrobots:
            print('{}. {}  '.format(hubcount, hub))
            hubcount += 1
            for robot in self.uimarchhubsrobots[hub]:
                robotcount += 0.1
                print('   %.1f: %s ' % (robotcount, robot))
                probescout1 = 1
                for probes,version in self.uimarchhubsrobots[hub][robot].items():
                    print('\t    %.1f.%.f %s_%s' % (robotcount, probescout1, probes,version))
                    probescout1 += 1
            robotcount = hubcount
            print()

    def string_partition(self, input_type):
        ''' provide input type is hub/robot'''
        print(input_type)
        if input_type == 'hub':
            print('!!!!!!!!!!!!!!')
            #print(self.stdout)
            for word in self.hub_stdout.split('\n'):

                if word.startswith('  addr ') and self.uimDomain in word:
                    dummy, domain, hub, robot, probe = word.split('/')
                    self.hubs[hub] = robot
            print(self.hubs)
        elif input_type == 'robot':
            for word in self.robot_stdout.split('\n'):
                if word.startswith('  addr ') and self.uimDomain in word:
                    dummy, domain, hub, robot = word.split('/')
                    robot = robot.replace('\r', '')
                    self.robotlists().robotlist.append(robot)
        return

obj = UimArch()
obj.remote_connection()
obj.hublists()
obj.robotlists()
obj.pkg_name_removing()
obj.hubs_robots_probes_list()
obj.remote_connection_close()
