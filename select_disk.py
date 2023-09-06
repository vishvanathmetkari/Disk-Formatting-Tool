import subprocess
import psutil


def remove_boot_disk(lst, parent_disk):
    if parent_disk in lst:
        lst.remove(parent_disk)
    else:
        print(f"parent_disk ( Bootable disk not found ) '{parent_disk}' not found in the list.")


def get_parent_disk_names():
    try:
        # Run the command to list parent disks and ignore loop devices
        command = "lsblk -o name -n -d -e 7,11"
        output = subprocess.check_output(command, shell=True, text=True)
        disk_names = output.strip().split('\n')
        return disk_names
    
    except subprocess.CalledProcessError:
        print("Error while running the command.")
        return []


def find_bootable_disk():
    boot_partition = psutil.disk_partitions()
    
    for partition in boot_partition:
        if partition.mountpoint == "/":
            boot_disk = partition.device
            return boot_disk

def find_parent_disk(boot_disk):
    try:
        output = subprocess.check_output(["lsblk", "-no", "pkname", boot_disk], text=True)
        parent_disk = output.strip()
        return parent_disk
    except subprocess.CalledProcessError:
        return None

def get_disk_names():
    bootable_disk = find_bootable_disk()
    if bootable_disk:
        parent_disk = find_parent_disk(bootable_disk)
        all_disk = get_parent_disk_names()
        remove_boot_disk(all_disk, str(parent_disk))
        if parent_disk:
            pass
        else:
            print("Bootable disk not found")
            exit()
    else:
        print("Bootable disk not found.")
        exit()
    return all_disk