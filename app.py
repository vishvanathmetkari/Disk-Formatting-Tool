from get_disk_info import *
from create_partitions import *
from delete_partitions import *
from grant_access_to_user import *
import yaml
from prettytable import PrettyTable
import argparse

class DiskManager:
    def __init__(self, config_file):
        self.config_data = self.read_config(config_file)
        self.working_disk = []

    def read_config(self, file_path):
        with open(file_path, 'r') as config_file:
            config_data = yaml.safe_load(config_file)
        return config_data
    
    def check_size(self,d_size,user_s,calculated_size):
        s = d_size - user_s
        calculated_size+=user_s
        if s > user_s:
            res=self.check_size(s,user_s,calculated_size)
            return res
        return calculated_size
    
    def disk_format(self):
        self.working_disk.clear()
        print()
        if 'mount_point' in self.config_data:
            mount_point = self.config_data['mount_point']
        else:
            print("mount point not found .. !!")
            exit()
        if 'user' in self.config_data:
            user = self.config_data['user']
            print("Current user:", user)
        else:
            result = subprocess.run(['whoami'], stdout=subprocess.PIPE, text=True)
            if result.returncode == 0:
                user = result.stdout.strip()
                print("Current user:", user)
            else:
                print("Error running 'whoami' command")
        resp = grant_sudo_permission(user)
        if resp:
            if 'size' in self.config_data and 'disk_count' in self.config_data:
                all_disk_size = 0
                disk_dic = {}
                user_size = int(self.config_data['size'])
                disk_count = self.config_data['disk_count']
                print(f"size: {user_size}, disk_count: {disk_count}")
                parent_disk_names = get_disk_names()
                for disk in parent_disk_names:
                    total_disk_size, remaining_gigabytes = get_disk_status(disk, "disk_size")
                    disk_dic[disk] = float(total_disk_size)
                    responce =self.check_size(total_disk_size,user_size,0)
                    all_disk_size+=responce
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

                i = 0
                if all_disk_size >= user_size*disk_count:
                    while 0 < int(disk_count):
                        print("remaining disk_count : ", disk_count)
                        try:
                            device_path = sorted_disk_dic[i][0]
                            self.working_disk.append(device_path)
                        except:
                            print("Disk not found ..!!")
                            exit()
                        total_disk_size, remaining_gigabytes = get_disk_status(device_path, "disk_size")
                        print("Disk ", device_path)
                        if float(total_disk_size) > user_size:
                            print("--- start creating new partitions ...")
                            disk_count = create_partition(user_size, disk_count, device_path, user, mount_point)
                            i += 1
                            print()
                            for disk in self.working_disk:
                                print(CYAN + "-------------------------------- {} ---------------------------------".format(disk) + RESET)
                                total_disk_size, remaining_gigabytes = get_disk_status(disk, "all")

                        elif float(total_disk_size) < user_size:
                            print()
                            print("Oppps !! you have exceeded the Disk limit")
                            print("Total Disk size : ", total_disk_size)
                            print("User-entered total size : {}G".format(user_size))
                            print()
                            exit()
                        else:
                            print()
                            print("Invalid size detected")
                            exit()
                else:
                    print("Insufficient disk space")
                    print("Usable disk size:",all_disk_size)
                    exit()                    
            else:
                print("Both size and disk_count values are required in the YAML configuration file.")
                exit()
        else:
            exit()

    def delete_partitions(self):
        print("Work in Progress")
        # for disk in self.working_disk:
        #     print(f"--- Deleting partitions on disk {disk} ---")
        #     delete_all_partitions(disk)
        #     print("--- Deleted partitions on disk {} ---".format(disk))
        #     print()
        #     print()

    def str_to_bool(self, s):
        return s.lower() in ("true", "yes", "1")

    def main(self):
        parser = argparse.ArgumentParser(description='Manage disk partitions')

        parser.add_argument('--disk_format', type=str, help='Specify True or False for disk_format', nargs='+')
        parser.add_argument('--delete_partitions', type=str, help='Specify True or False for deleting partitions', nargs='+')
        args = parser.parse_args()
        print()
        if args.disk_format is not None:
            create_partitions_flag = self.str_to_bool(args.disk_format[-1].replace("=", '').strip())
            if create_partitions_flag:
                self.disk_format()
            else:
                print("disk_format set to False")

        if args.delete_partitions is not None:
            delete_partitions_flag = self.str_to_bool(args.delete_partitions[-1].replace("=", '').strip())
            if delete_partitions_flag:
                self.delete_partitions()
            else:
                print("delete_partitions set to False")

if __name__ == "__main__":
    disk_manager = DiskManager('config.yml')
    disk_manager.main()
