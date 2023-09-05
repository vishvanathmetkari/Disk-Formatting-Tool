
import subprocess
import os,sys
import pexpect
import time
from delete_partitions import *
from grant_access_to_user import *
from select_disk import *
from get_disk_info import *
import re

pattern_nvme = r'^nvme'
pattern_s = r'^s'

def create_partition(size,partition,device_path,user,mount_point):
    print("----First Deleting all partitions ----")
    delete_all_partitions(device_path)
    print("--- Deleted all partitions and re-creating -----")
    print()
    print()
    disk_path = '/dev/{}'.format(device_path)
    partitions_created_count=partition
    for number in range(partition):
        total_disk_size,remaining_gigabytes=get_disk_status(device_path,"disk_size")
        if float(remaining_gigabytes) > size:
            if re.match(pattern_nvme, device_path):
                disk_name = device_path+'p{}'.format(number+1)
                mounting_path = '{}_{}'.format(mount_point,disk_name[4:])
            elif re.match(pattern_s,device_path):
                disk_name = device_path+'{}'.format(number+1)
                mounting_path = '{}_{}'.format(mount_point,disk_name[2:])
            partition_path = f"/dev/{disk_name}"
            print("--------------------------------------------------------------------")
            try:
                fdisk_command = f"sudo gdisk {disk_path}"
                child = pexpect.spawn(fdisk_command)
                child.logfile = sys.stdout.buffer 
                time.sleep(.2)
                child.expect("GPT fdisk.*")
                child.sendline("n")  # Send 'p' to create a primary partition
                time.sleep(.2)
                child.expect("Partition number.*:")
                child.sendline("")   # Press Enter to accept the default partition number
                time.sleep(.2)

                child.expect(".*(?i)First sector.*:")
                child.sendline("")   # Press Enter to accept the default first sector
                time.sleep(.2)

                child.expect("Last sector.*:")
                child.sendline("+{}G".format(size))   # Press Enter to accept the default last sector (100%)
                time.sleep(.2)

                child.expect("Hex code or GUID.*:")
                child.sendline("")  # Send 'w' to write changes and exit
                time.sleep(.2)

                child.expect("Command.*:")
                child.sendline("w")  # Send 'w' to write changes and exit
                time.sleep(.2)

                child.expect("Do you want to proceed.*:")
                child.sendline("Y")  # Send 'w' to write changes and exit
                time.sleep(.2)

                child.expect(pexpect.EOF)
                make_changes = 'sudo partprobe {}'.format(disk_path)
                subprocess.run(make_changes, shell=True, check=True)
                time.sleep(1)

                fs_type = f"sudo mkfs -t ext4 {partition_path}"
                subprocess.run(f'echo "y" | {fs_type}', shell=True, check=True)
                print("Primary partition created successfully.")
                time.sleep(1)

                print("start mounting ...")
                print("--- creating a mounting point at /mnt/")
                try:
                    mount_point_command = 'sudo mkdir {}'.format(mounting_path)
                    subprocess.run(mount_point_command, shell=True, check=True)
                    print("--- mount point {} created successfully !!!!".format(mounting_path))
                    time.sleep(1)
                except:
                    delete_data = 'sudo rm -rf {}/*'.format(mounting_path)
                    subprocess.run(delete_data, shell=True, check=True)
                
                    delete_m_point = 'sudo rm -rf {}'.format(mounting_path)
                    subprocess.run(delete_m_point, shell=True, check=True)

                    mount_point_command = 'sudo mkdir {}'.format(mounting_path)
                    subprocess.run(mount_point_command, shell=True, check=True)
                    print("--- mount point {} created successfully !!!!".format(mounting_path))
                    time.sleep(1)

                mount_command = 'sudo mount {} {}'.format(partition_path,mounting_path)
                subprocess.run(mount_command, shell=True, check=True)

                grant_access_of_folder(mounting_path,user)

                print("Disk {} mount succesfully at {}".format(disk_name,mounting_path))
                time.sleep(1)
                partitions_created_count -=1
                print("remaining partitions : ",partitions_created_count)

                # print(" Your disk has been successfully created. It is now ready for use.")
            except pexpect.ExceptionPexpect as e:
                print("An error occurred:", e)
        else:
            break
    return partitions_created_count  

