import time
import traceback

import uninstallGlobalVariable as gfile
from pypsexec.client import Client


def robot_uninstall():
    for robot_uninstall.ip in gfile.ip:
        try:

            c = Client(robot_uninstall.ip, gfile.username, gfile.password, encrypt='False')
            c.connect()
            c.create_service()
            global conn
            conn = c
            print('service created for following "{}".......\n\n'.format(robot_uninstall.ip))

            # Uninstalling

            cmd = r'''IF EXIST C:\Progra~1\Nimsoft\unins000.exe (echo 1) ELSE IF EXIST C:\Progra~2\Nimsoft\unins000.exe (echo 2) ELSE (echo 3)'''
            stdout, stderr, rc = c.run_executable("cmd.exe", arguments='''/c  {}'''.format(cmd))
            robot_path = str(stdout, 'utf-8')
            print(robot_path)

            if robot_path.strip() == '1':
                stdout, stderr, rc = c.run_executable("cmd.exe",arguments='''/c  "C:\\Progra~1\\Nimsoft\\unins000 /silent"''')
                if rc == 0:
                    print('{} robot is Uninstalled successfully......\n\n'.format(robot_uninstall.ip))
                    time.sleep(2)
                    restart()

                else:
                    print('{} Uninstallation  failed with error :\n\n {} \n\n'.format(robot_uninstall.ip, stderr))

            elif robot_path.strip() == '2':
                stdout, stderr, rc = c.run_executable("cmd.exe", arguments='''/c  "C:\\Progra~2\\Nimsoft\\unins000 /silent"''')
                if rc == 0:
                    print('{} robot is Uninstalled successfully......\n\n'.format(robot_uninstall.ip))
                    time.sleep(2)
                    restart()

                else:
                    print('{} Uninstallation  failed with error :\n\n {} \n\n'.format(robot_uninstall.ip, stderr))

            else:
                print('robot not installed on {} ...'.format(robot_uninstall.ip))

        except Exception as ex:
            # print('Below exception occured while connecting with "{}"........\n'.format(ip))
            traceback.print_exc()
        finally:
            c.remove_service()
            c.disconnect()
            print('Connection closed for following host {}'.format(robot_uninstall.ip))


def restart():
    stdout, stderr, rc = conn.run_executable("cmd.exe", arguments='''/c  "shutdown /r"''')
    # count+=1
    if rc == 0:
        print('{} Machine restart  successfully......\n\n'.format(robot_uninstall.ip))
    else:
        print('{} Machine restart  failed......\n\n'.format(robot_uninstall.ip))


robot_uninstall()
