from get_disk_info import *
from create_partitions import *
from delete_partitions import *
from grant_access_to_user import *
import yaml
from prettytable import PrettyTable

def read_config(file_path):
    with open(file_path, 'r') as config_file:
        config_data = yaml.safe_load(config_file)
    return config_data

def main(config_data):
    print()
    if 'mount_point' in config_data:
        mount_point = config_data['mount_point']
    else:
        print("mount point not found .. !!")
        exit()
    if 'user' in config_data:
        user = config_data['user']
        print("Current user:", user)
    else:
        result = subprocess.run(['whoami'], stdout=subprocess.PIPE, text=True)
        if result.returncode == 0:
            user = result.stdout.strip()
            print("Current user:", user)
        else:
            print("Error running 'whoami' command")
    resp =grant_sudo_permission(user)
    if resp:    
        if 'size' in config_data and 'disk_count' in config_data:
            disk_dic = {}
            user_size = int(config_data['size'])
            disk_count = config_data['disk_count']
            print(f"size: {user_size}, disk_count: {disk_count}")
            parent_disk_names = get_disk_names()
            for disk in parent_disk_names:
                total_disk_size,remaining_gigabytes=get_disk_status(disk,"disk_size")
                # total_disk_size=convert_to_gigabytes(str(total_disk_size)) 
                disk_dic[disk]=float(total_disk_size)
            sorted_disk_dic = dict(sorted(disk_dic.items(), key=lambda item: item[1], reverse=True))
            sorted_disk_dic = list(sorted_disk_dic.items())
            # Create a PrettyTable object
            table = PrettyTable()
            table.field_names = ["Name", "Size (G)"]

            for key, value in sorted_disk_dic:
                table.add_row([key, value])
            print()
            print("-------------- All Disk --------------")
            print(table)
            print()
            
            i=0
            working_disk  =[]
            while 0<int(disk_count):
                print("remaining disk_count : ",disk_count)
                try:
                    device_path=sorted_disk_dic[i][0]
                    working_disk.append(device_path)
                except:
                    print("Disk not found ..!!")
                total_disk_size,remaining_gigabytes=get_disk_status(device_path,"disk_size")
                # total_disk_size=convert_to_gigabytes(str(total_disk_size))
                print("Disk ",device_path)
                if float(total_disk_size) > user_size:
                    print("--- start creating new partitions ...")
                    time.sleep(3)
                    disk_count=create_partition(user_size,disk_count,device_path,user,mount_point)
                    i+=1
                    print()
                    for disk in working_disk:
                        print(CYAN+"-------------------------------- {} ---------------------------------".format(disk)+RESET)
                        total_disk_size,remaining_gigabytes=get_disk_status(disk,"all")

                elif float(total_disk_size) < user_size:
                    print()
                    print("Oppps !! you have exceeded the Disk limit")
                    print("Total Disk size : ",total_disk_size)
                    print("User-entered total size : {}G".format(user_size))
                    print()
                    exit()
                else:
                    print()
                    print("Invalid size detected")
                    exit()
        else:
            print("Both size and disk_count values are required in the YAML configuration file.")
            exit()
    else:
        exit()
if __name__ == "__main__":
    config_data = read_config('config.yml')
    main(config_data)

   
