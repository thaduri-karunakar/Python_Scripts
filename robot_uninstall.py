import time
import paramiko
import traceback
import robot_uninstall_variable as gfile
from pypsexec.client import Client

start = time.time()


def windows_robot_uninstall():
    """ windows robots uninstallation """
    print('Windows robot uninstall is processesing....\n','*'*43,sep='')
    for windows_robot_uninstall.ip in gfile.ip:
        try:

            c = Client(windows_robot_uninstall.ip, gfile.username, gfile.password, encrypt='False')
            c.connect()
            c.create_service()
            global conn
            conn = c
            print('service created for following "{}".......'.format(windows_robot_uninstall.ip))

            # Uninstalling

            cmd = r'''IF EXIST C:\Progra~1\Nimsoft\unins000.exe (echo 1) ELSE IF EXIST C:\Progra~2\Nimsoft\unins000.exe (echo 2) ELSE (echo 3)'''
            stdout, stderr, rc = c.run_executable("cmd.exe", arguments='''/c  {}'''.format(cmd))
            robot_path = str(stdout, 'utf-8')
            # print(robot_path)

            if robot_path.strip() == '1':
                stdout, stderr, rc = c.run_executable("cmd.exe",
                                                      arguments='''/c  "C:\\Progra~1\\Nimsoft\\unins000 /silent"''')
                if rc == 0:
                    print('{} robot is Uninstalled successfully......'.format(windows_robot_uninstall.ip))
                    time.sleep(2)
                    restart()

                else:
                    print('{} Uninstallation  failed with error : {} \n\n'.format(windows_robot_uninstall.ip, stderr))

            elif robot_path.strip() == '2':
                stdout, stderr, rc = c.run_executable("cmd.exe",
                                                      arguments='''/c  "C:\\Progra~2\\Nimsoft\\unins000 /silent"''')
                if rc == 0:
                    print('{} robot is Uninstalled successfully......'.format(windows_robot_uninstall.ip))
                    time.sleep(2)
                    restart()

                else:
                    print('{} Uninstallation  failed with error : {} \n\n'.format(windows_robot_uninstall.ip, stderr))

            else:
                print('robot not installed on "{}" ...'.format(windows_robot_uninstall.ip))

        except Exception as ex:
            # print('Below exception occured while connecting with "{}"........\n'.format(ip))
            traceback.print_exc()
        finally:
            c.remove_service()
            c.disconnect()
            print('Connection closed for following host {}'.format(windows_robot_uninstall.ip))
            print('*'*48,'\n')


def linux_robot_uninstall():
    """ Linux robots uninstallation """
    print('Linux robot uninstall is processesing....\n','*'*43,sep='')
    for ip in gfile.ip:
        try:
            ssh = paramiko.SSHClient()  # Creating Connection
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, gfile.port, gfile.username, gfile.password)
            print('service created for following "{}".......'.format(ip))

            # Uninstalling
            robot_path_stdin, robot_path_stdout, robot_path_stderr = ssh.exec_command("find / -maxdepth 2 -type d -name 'nimsoft'")
            time.sleep(3)
            robot_path = ''.join(robot_path_stdout); robot_path = robot_path.strip()
            # print(robot_path)

            if len(robot_path) != 0:
                nimint_stdin, nimint_stdout, nimint_stderr = ssh.exec_command('{}/bin/niminit stop'.format(robot_path))
                time.sleep(3)
                if nimint_stdout.channel.recv_exit_status() == 0:
                    inst_init_stdin, inst_init_stdout, inst_init_stderr = ssh.exec_command('{}/bin/inst_init.sh remove'.format(robot_path))
                    time.sleep(5)
                    if inst_init_stdout.channel.recv_exit_status() == 0:
                        print('{} robot is Uninstalled successfully......'.format(ip))
                        stdin, inst_init_stdout, stderr = ssh.exec_command('rm -rf {}'.format(robot_path))
                        time.sleep(2)
                        #     Restarting machine
                        restart_stdin, restart_stdout, restart_stderr = ssh.exec_command('init 6')
                        #print('stdout status : ',restart_stdout.channel.recv_exit_status(), 'stderr status : ',restart_stderr.channel.recv_exit_status(),)
                        print('{} Machine restart  successfully......'.format(ip))
                    else:
                        print('{} robot is failed to remove inst_init.sh with below error :......\n{}'.format(ip, inst_init_stderr))

                else:
                    print('{} robot is failed to stop niminit with below error  :......\n{}'.format(ip, nimint_stderr))
            else:
                print('robot not installed on "{}" ...'.format(ip))

        except Exception as ex:
            # print('Below exception occured while connecting with "{}"........\n'.format(ip))
            traceback.print_exc()
        finally:
            ssh.close()
            print('Connection closed for following host "{}"'.format(ip))
            print('*' * 52, '\n')

def restart():
    stdout, stderr, rc = conn.run_executable("cmd.exe", arguments='''/c  "shutdown /r"''')
    # count+=1
    if rc == 0:
        print('{} Machine restart  successfully......\n\n'.format(windows_robot_uninstall.ip))
    else:
        print('{} Machine restart  failed......\n\n'.format(windows_robot_uninstall.ip))

class RobotUninstall:
    """ Unistalling UIM robots on Windows and Linux platforms """

    windows_robot_uninstall() if gfile.os == 'w' else linux_robot_uninstall() if gfile.os == 'l' else print(
        'Provided platform "{}" is not supportable'.format(gfile.os))
    print ('Script has taken',(time.time()-start)/60, 'Minuts..')