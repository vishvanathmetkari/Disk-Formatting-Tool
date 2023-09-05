import re
import subprocess
import json
from prettytable import PrettyTable
from colorama import Fore
from colorama import  Back, Style

# Text color codes
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
RESET = "\033[0m"  # Reset to default color


pattern_nvme = r'^nvme'
pattern_s = r'^s'

# Function to convert storage units to gigabytes
def convert_to_gigabytes(value):
    if value[-1] == "T":
        return float(value[:-1]) * 1024  # Convert terabytes to gigabytes
    elif value[-1] == "G":
        return float(value[:-1])  # No conversion needed, already in gigabytes
    elif value[-1] == "K":
        return float(value[:-1]) / (1024 * 1024)  # No conversion needed, already in gigabytes
    else:
        raise ValueError("Invalid unit detected")
    
def get_remaining_size(re_value):
    size = 0
    for i in re_value:
        if i[-1] == "T":
            converted_size = float(i[:-1]) * 1024  # Convert terabytes to gigabytes
            size+=converted_size
        elif i[-1] == "G":
            converted_size= float(i[:-1])  # No conversion needed, already in gigabytes
            size+=converted_size
        elif i[-1] == "K":
            converted_size =float(i[:-1]) / (1024 * 1024)  # No conversion needed, already in gigabytes
            size+=converted_size
        else:
            raise ValueError("Invalid unit detected")
    return size

def get_disk_status(disk_name, flag):

    cmnd='lsblk --json'
    json_data = subprocess.run(cmnd,shell=True, text=True, capture_output=True)
    get_data=json_data.stdout
    parsed_data = json.loads(get_data)
    total_disk_size=0
    for data in parsed_data['blockdevices']:
        if data['name']==str(disk_name):
            total_disk_size = data['size']
            remaining_size_list =[]
            table = PrettyTable()
            table.field_names = [
                RED + "Name" + RESET,
                RED + "Type" + RESET,
                RED + "Size" + RESET,
                RED + "Mount Points" + RESET,
                RED + "Read-only" + RESET,
                RED + "Removable" + RESET,
            ]

            if re.match(pattern_nvme, disk_name):
                row = [
                    YELLOW + data['name'] + RESET,
                    YELLOW + data['type'] + RESET,
                    YELLOW + data['size'] + RESET,
                    YELLOW + str(data['mountpoints'])+ RESET,
                    YELLOW + str(data['ro']) + RESET,
                    YELLOW + str(data['rm']) + RESET,
                ]

            elif re.match(pattern_s, disk_name):

                row = [
                    YELLOW + data['name'] + RESET,
                    YELLOW + data['type'] + RESET,
                    YELLOW + data['size'] + RESET,
                    YELLOW + str(data['mountpoint'])+ RESET,
                    YELLOW + str(data['ro']) + RESET,
                    YELLOW + str(data['rm']) + RESET,
                    ]

            table.add_row(row)
            if re.match(pattern_nvme, disk_name):
                if 'children' in data:
                    for child in data['children']:
                        # Add child data to the table with yellow color
                            child_row = [
                                YELLOW + child['name'] + RESET,
                                YELLOW + child['type'] + RESET,
                                YELLOW + child['size'] + RESET,
                                YELLOW + str(child['mountpoints']) + RESET,
                                YELLOW + str(child['ro']) + RESET,
                                YELLOW + str(child['rm']) + RESET,
                            ]
                            table.add_row(child_row)
                            remaining_size_list.append(child['size'])
           
            elif re.match(pattern_s, disk_name):
                if 'children' in data:
                    for child in data['children']:
                        child_row = [
                                YELLOW + child['name'] + RESET,
                                YELLOW + child['type'] + RESET,
                                YELLOW + child['size'] + RESET,
                                YELLOW + str(child['mountpoint']) + RESET,
                                YELLOW + str(child['ro']) + RESET,
                                YELLOW + str(child['rm']) + RESET,
                                ]
                        table.add_row(child_row)
                        remaining_size_list.append(child['size'])


            remaining_size=get_remaining_size(remaining_size_list)
            remaining_gigabytes = convert_to_gigabytes(total_disk_size) - remaining_size
            if flag == "all":
                print()
                print(table)
                print()
                print("Total Disk Size: ",RED+total_disk_size+RESET)
                print("Remaining storage:"+RED+" {:.1f}G".format(remaining_gigabytes)+RESET)
                print("-----------------------------------------------------------------------")

            elif flag=="disk_size":
                pass
               # print("Total Disk Size: ",RED+total_disk_size+RESET)
               # print("Remaining storage:"+RED+" {:.1f}G".format(remaining_gigabytes)+RESET)
               # print("-----------------------------------------------------------------------")

    return total_disk_size ,remaining_gigabytes
