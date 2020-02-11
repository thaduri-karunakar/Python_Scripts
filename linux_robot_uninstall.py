import time
import paramiko
import linux_uninstall_global_variable as gfile
import traceback


def robot_uninstall():
    for ip in gfile.ip:
        try:
            ssh = paramiko.SSHClient()  # Creating Connection
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, gfile.port, gfile.username, gfile.password)
            print('service created for following "{}".......\n\n'.format(ip))

            # Uninstalling
            robot_path_stdin, robot_path_stdout, robot_path_stderr = ssh.exec_command("find / -maxdepth 2 -type d -name 'nimsoft'")
            time.sleep(3)
            robot_path = ''.join(robot_path_stdout); robot_path = robot_path.strip()
            print(robot_path)

            if len(robot_path) != 0:
                nimint_stdin, nimint_stdout, nimint_stderr = ssh.exec_command('{}/bin/niminit stop'.format(robot_path))
                time.sleep(5)
                if nimint_stdout.channel.recv_exit_status() == 0:
                    inst_init_stdin, inst_init_stdout, inst_init_stderr = ssh.exec_command('{}/bin/inst_init.sh remove'.format(robot_path))
                    time.sleep(5)
                    if inst_init_stdout.channel.recv_exit_status() == 0:
                        print('{} robot is Uninstalled successfully......\n\n'.format(ip))
                        stdin, inst_init_stdout, stderr = ssh.exec_command('rm -rf {}'.format(robot_path))
                        #     Restarting machine
                        restart_stdin, restart_stdout, restart_stderr = ssh.exec_command('init 6')
                        print('stdout status : ',restart_stdout.channel.recv_exit_status(), 'stderr status : ',restart_stderr.channel.recv_exit_status(),)
                        print('{} Machine restart  successfully......\n\n'.format(ip))
                    else:
                        print('{} robot is failed to remove inst_init.sh with below error :......\n\n{}'.format(ip, inst_init_stderr))

                else:
                    print('{} robot is failed to stop niminit with below error  :......\n\n{}'.format(ip, nimint_stderr))
            else:
                print('robot not installed on {} ...'.format(ip))

        except Exception as ex:
            # print('Below exception occured while connecting with "{}"........\n'.format(ip))
            traceback.print_exc()
        finally:
            ssh.close()
            print('Connection closed for following host "{}"'.format(ip))


robot_uninstall()
