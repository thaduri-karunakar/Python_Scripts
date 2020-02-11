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
        self.s = ''
        self.default_probes = {'robot_update_secure', 'hub_secure', 'distsrv', 'nas', 'automated_deployment_engine',
                               'data_engine', 'ace', 'mpse', 'maintenance_mode', 'baseline_engine', 'prediction_engine',
                               'sla_engine',
                               'qos_processor', 'nis_server', 'discovery_server', 'discovery_agent', 'cm_data_import',
                               'udm_manager', 'ppm', 'ems', 'relationship_services', 'topology_agent',
                               'fault_correlation_engine', 'wasp', 'trellis', 'mon_config_service', 'usage_metering',
                               'telemetry', 'webgtw', 'hub_adapter', 'HA'}

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
            stdout, stderr, rc = self.remote_connection().run_executable('cmd.exe',
                                                                         arguments='''/c {}'''.format(callback))
            stdout = str(stdout, 'utf-8');
            stderr = str(stderr, 'utf-8')
            self.s =stdout
            # print(stdout)

            self.string_partition('hub')  # Calling string_partition function for taking hubs from calllback
        except Exception as e:
            print('Below exception occured .....\n')
            print(e)



    def string_partition(self, input_type):
        ''' provide input type is hub/robot'''
        print('!!!!!!!!!!!!!!')
        print(self.hublists().s)
        for word in self.s.split('\n'):
            if word.startswith('  addr ') and self.uimDomain in word:
                dummy, domain, hub, robot, probe = word.split('/')
                self.hubs[hub] = robot

    def remote_connection_close(self):
        self.remote_connection().remove_service()
        self.remote_connection().disconnect()
        print('service removed for following "{}"'.format(self.ip))
        print('Script has taken', (time.time() - start) / 60, 'Minuets..')
obj = UimArch()
obj.remote_connection()
obj.hublists()
obj.remote_connection_close()
