import subprocess
import re
from datetime import datetime as dt

from server_toolkit_app.base_plugin import BasePlugin

class Plugin(BasePlugin):
    name = "System Reports"

    def commands(self):
        return {
            "Storage Report": {"func": self.storage_report, "interactive": False},
            "Process Report": {"func": self.process_report, "interactive": False},
            "User Report": {"func": self.user_report, "interactive": False},
            "Hardware Report": {"func": self.hardware_report, "interactive": False},
            "Networking Report": {"func": self.networking_report, "interactive": False},
        }
    
    def get_error_code(self, cmd):
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode

    def run(self, cmd):
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
        if self.get_error_code(cmd) != 0:
            raise Exception(result.stderr.strip())

        return result.stdout.strip()
    
    def storage_report(self):
        date = self.run("date")
        hostname = self.run("hostname")
        domain_test = self.run("hostname -d")
        domain = domain_test if domain_test else "None"
        
        disks_search = self.run("lsblk -i --output name,type").splitlines()
        disk_names = []
        for i in range(len(disks_search)):
            cur_disk = re.search(r'(.+)\s+\bdisk', disks_search[i]) # find any name of type disk
            if cur_disk: # if match is found, disk name formatted
                cur_disk_name = cur_disk.group(1).strip()
                if "ram" in cur_disk_name: # should avoid swap space being labeled as disk
                    continue
                else:
                    disk_names.append(cur_disk_name)
        
        inode_usage = {} # Mount:{key} Usage:{inode_usage[key][0]} Filesystem:{inode_usage[key][1]}

        inode_search = self.run("df -i").splitlines()
        for i in range(len(inode_search)):
            cur_line = inode_search[i].split()  
            cur_fs = cur_line[0]
            usage = cur_line[4]
            mount_point = cur_line[-1]

            inode_usage[mount_point] = (usage, cur_fs)

        num_disks = len(disk_names)
        root_disk = self.run("df -h / | tail -1").split()
        root_total = root_disk[1]
        root_used = root_disk[2]
        root_free = root_disk[3]

        SMART_health = {}
        for i in range(len(disk_names)):
            status_result = self.run(f"sudo smartctl -H /dev/{disk_names[i]}")
            if "PASSED" in status_result:
                SMART_health[disk_names[i]] = "PASSED"
            else:
                SMART_health[disk_names[i]] = "FAILED"

        with open(f"storage_report_{hostname}_{dt.now().strftime("%G-%m-%d")}.log", "w", encoding="utf-8") as f:
            f.write(f"Date: {date}\n")
            f.write(f"Hostname: {hostname}\n")
            f.write(f"Domain: {domain}\n")
            f.write("\n")
            f.write(f"Number of disks: {num_disks}\n")

            for i in range(len(disk_names)):
                f.write(f"Disk {i} {disk_names[i]}\n")
            f.write("\n")
            f.write(f"Root Drive Total: {root_total}\n")
            f.write(f"Root Drive Used: {root_used}\n")
            f.write(f"Root Drive Free: {root_free}\n")
            f.write("\n")
            f.write("Inode Usage\n")
            f.write(
                f"{'Filesystem':<20} | "
                f"{'Inode Usage':<15} | "
                f"{'Mount Point':<20}\n"
            )

            f.write("-" * 65 + "\n")

            for key in inode_usage:
                if key == "on":  # Skip header of cmd output
                    continue

                usage = inode_usage[key][0]
                filesystem = inode_usage[key][1]

                f.write(
                    f"{filesystem:<20} | "
                    f"{usage:<15} | "
                    f"{key:<20}\n"
                )

            f.write("\n")
            f.write("Smartctl Status\n")
            for key in SMART_health:
                f.write(f"Disk: {key} Status: {SMART_health[key]}\n")
        
        return f"Storage log written to: storage_log_{hostname}_{dt.now().strftime("%G-%m-%d")}.log"
    
    def process_report(self):
        return "TODO: Process Report"
    
    def user_report(self):
        return "TODO: User Report"
    
    def hardware_report(self):
        return "TODO: Hardware Report"
    
    def networking_report(self):
        return "TODO: Networking Report"
