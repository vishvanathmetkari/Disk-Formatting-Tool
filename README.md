
# Disk Formatting Tool
### Overview
This tool is designed to simplify the process of formatting and partitioning both SD and NVMe disks. It automates the selection of the disk with the highest available size and partitions it according to the parameters specified in a YAML configuration file. The tool can format multiple disks, as specified in the configuration, and mount them at the designated mount point.

### Prerequisites
Before using this tool, ensure you have the following prerequisites:

- Python 3.x installed on your system.
- The required Python packages listed in requirements.txt.

### Configuration
To use this tool, you need to create a YAML configuration file (config.yaml) with the following parameters:

```yaml
    size: 10              # Size of each partition in GB
    disk_count: 3         # Number of disk partitions
    user: whileone        # User for mounting the disks
    mount_point: "/mnt/data" # Mount point for the disks

```

You can customize the values of size, disk_count, user, and mount_point according to your requirements.

### Usage
- Clone this repository to your local machine:
```python
    git clone https://github.com/vishvanathmetkari/Disk-Formatting-Tool.git
```
- Navigate to the project directory:
```python
    cd Disk-Formatting-Tool
```
- Install the required Python packages:
```python
    pip install -r requirements.txt

```
Ensure that your config.yaml file is correctly configured.

- Run the app.py script:
```python
    python3 app.py
```
The tool will automatically select the disk with the highest available size and partition it according to your specified parameters. It will then delete all existing partitions and their mount points, create new partitions as per the configuration in the YAML file, and mount the disk at the specified mount point.

If there are remaining disks to be formatted (as specified in disk_count), the tool will select the next available disk and repeat the partitioning process until the desired number of disks are formatted.

### Note
Make sure to back up any important data on the disks before running this tool, as it will erase all existing data during the formatting process.

---
