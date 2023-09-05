import subprocess
import psutil
def delete_all_partitions(device_path):
    print("------------------------------------------------------------------------------------------")
    print("Deleting partitions...")
    print("Disk - :",device_path)
    d_path = '/dev/{}'.format(device_path)
  
    for partition in psutil.disk_partitions():
        if partition.device.startswith(d_path):
            device = partition.device
            mountpoint = partition.mountpoint
            print("---------------------------------")
            print(f"Device: {device}")
            print(f"Mount point: {mountpoint}")
            print()
            print("------ start unmounting ----- {}".format(device))
            try:
                umount_cmd = "sudo umount {}".format(device)
                subprocess.run(umount_cmd, shell=True, check=True)
            except:
                print("Error --- while unmounting device")

            print("------ start deleteling data from mounting point -----{}".format(mountpoint))
            try:
                deleting_data_cmd = "sudo rm -rf {}/*".format(mountpoint)
                subprocess.run(deleting_data_cmd, shell=True, check=True)
            except:
                print("Error --- while deleting data")

            print("------ start deleteling mounting point -----{}".format(mountpoint))
            try:
                mount_point_cmd = "sudo rm -rf {}".format(mountpoint)
                subprocess.run(mount_point_cmd, shell=True, check=True)
            except:
                print("Error --- while deleting mounting point")

    try:
        print("deleting all partitions ----")
        delete_partitions = "sudo sgdisk --zap-all {}".format(d_path)
        subprocess.run(delete_partitions, shell=True, check=True)
        print('deleted all partitions ...')
    except:
        print('Error -- while deleting all partitions ----')
