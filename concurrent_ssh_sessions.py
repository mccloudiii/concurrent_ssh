import paramiko
import concurrent.futures
import time

def execute_commands_on_device(hostname, username, password, commands, output_file):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)

        channel = ssh.invoke_shell()
        time.sleep(1)  # Allow time for the shell to be ready

        with open(output_file, 'w') as f:
            for command in commands:
                channel.send(command + "\n")
                time.sleep(2)  # Wait for the command to be executed and output to be generated
                
                output = ""
                while channel.recv_ready():
                    output += channel.recv(1024).decode()

                # Write output to the file
                f.write(f"Command: {command}\n")
                f.write(f"Output:\n{output}\n")
                f.write("\n" + "-"*50 + "\n\n")

        channel.close()
        ssh.close()
    except Exception as e:
        print(f"Failed to execute commands on {hostname}: {str(e)}")

def main():
    # Enable Paramiko logging
    paramiko.util.log_to_file('paramiko.log')
    devices = [
        {"hostname": "sandbox-iosxe-recomm-1.cisco.com", 
         "username": "admin", 
         "password": "C1sco12345"},
        {"hostname": "sandbox-iosxr-1.cisco.com", 
         "username": "admin", 
         "password": "C1sco12345"}
    ]

    commands = [
        'term len 0',
        'show version',
        'show ip interface brief',
        'show running-config'
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for device in devices:
            output_file = f"{device['hostname']}_output.txt"
            futures.append(executor.submit(execute_commands_on_device, device['hostname'], device['username'], device['password'], commands, output_file))

        for future in concurrent.futures.as_completed(futures):
            if future.exception() is not None:
                print(f"Execution generated an exception: {future.exception()}")

if __name__ == '__main__':
    main()