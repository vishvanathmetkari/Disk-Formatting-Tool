
import subprocess
import pwd 

def check_user_permission(user):
    try:
        subprocess.run(['sudo', '-lU', user], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True  
    except subprocess.CalledProcessError:
        return False  

def grant_access_of_folder(folder_path, username):
    try:
        # Change ownership of the folder to the selected user
        subprocess.run(["sudo", "chown", username, folder_path], check=True)
        # Set read, write, and execute permissions for the user
        subprocess.run(["sudo", "chmod", "700", folder_path], check=True)
        print(f"Access granted of {folder_path} to {username}.")
    except subprocess.CalledProcessError as e:
        print("Error:", e)

def check_sudoers_entry(username, command):
    try:
        # Use grep to search for the sudoers entry in the sudoers file
        grep_command = f"grep '{username} ALL=(ALL) NOPASSWD: {command}' /etc/sudoers"
        # Add sudo to the grep command
        grep_command_with_sudo = f"sudo {grep_command}"
     
        result = subprocess.run(['bash', '-c', grep_command_with_sudo], text=True, capture_output=True)
    
        # Check the return code of the grep command
        if result.returncode == 0:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False

def check_whoami_entry(whoami, command):
    try:
        # Use grep to search for the sudoers entry in the sudoers file
        grep_command = f"grep '{whoami} ALL=(ALL) NOPASSWD: {command}' /etc/sudoers"
        grep_command_with_sudo = f"sudo {grep_command}"
        result = subprocess.run([ 'bash', '-c', grep_command_with_sudo], text=True, capture_output=True)

        # Check the return code of the grep command
        if result.returncode == 0:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False

def grant_sudo_permission(username):
    command = 'ALL'
    try:
        user_info = pwd.getpwnam(username)

        if not check_sudoers_entry(username, command):
            cmd = f'echo "{username} ALL=(ALL:ALL) ALL" | sudo tee -a /etc/sudoers'
            try:
                # Run the command
                subprocess.run(cmd, shell=True, check=True)
                print(f'echo "{username} ALL=(ALL:ALL) ALL" | sudo tee -a /etc/sudoers')
            except subprocess.CalledProcessError as e:
                print(f'Error: {e}')

            # Construct the sudoers entry
            sudoers_entry = f"{username} ALL=(ALL) NOPASSWD: {command}"
            try:
                # Use sudo to append the new sudoers entry to the sudoers file
                subprocess.run(['sudo', 'bash', '-c', f'echo "{sudoers_entry}" >> /etc/sudoers'], check=True)
                print("----------------------------------------------------------------------------------------------")
                print(f"Sudo permissions granted to {username} for {command}")

            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
           
            try:
                # Run the 'whoami' command
                result = subprocess.run(['whoami'], stdout=subprocess.PIPE, text=True)
                # Check if the command was successful
                if result.returncode == 0:
                    # Print the output of the 'whoami' command
                    whoami_cmd = result.stdout.strip()
                else:
                    print("Error running 'whoami' command")
                if not check_whoami_entry(whoami_cmd, command):
                    whoami_cmd = f"{whoami_cmd} ALL=(ALL) NOPASSWD: {command}"  
                    # Use sudo to append the new sudoers entry to the sudoers file
                    subprocess.run(['sudo', 'bash', '-c', f'echo "{whoami_cmd}" >> /etc/sudoers'], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
                return False
        else:
            print("----------------------------------------------------------------------------------------------")
            print(f"The sudoers entry for {username} and {command} already exists.")
            return True
    except:
        print("----------------------------------------------------------------------------------------------")
        print(f'User {username} does not exist.')
        return False
    
