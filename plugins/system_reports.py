import subprocess
import re

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
        return "TODO: Storage Report"
    
    def process_report(self):
        return "TODO: Process Report"
    
    def user_report(self):
        return "TODO: User Report"
    
    def hardware_report(self):
        return "TODO: Hardware Report"
    
    def networking_report(self):
        return "TODO: Networking Report"
