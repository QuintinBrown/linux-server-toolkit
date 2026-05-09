import subprocess
import re

from core.base_plugin import BasePlugin

class Plugin(BasePlugin):
    name = "Network Testing"

    def commands(self):
        return {
            "Ping Gateway": self.ping_gateway,
            "Remote Ping": self.ping_remote,
            "Ping DNS": self.ping_dns,
            "Test DNS": self.test_dns,
            "Find Gateway": self.find_gateway
        }
    
    def run(self, cmd):
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()

    def find_gateway(self, want_printed=True):
        result = self.run("ip route")
        pretty_result = re.search(r'\bvia\s([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', result)
        if want_printed:
            print(pretty_result.group(1))
        else:
            return pretty_result.group(1)
    
    def ping_gateway(self):
        print("TODO: Ping Gateway")


    def ping_remote(self):
        print("TODO: Ping Remote")

    def ping_dns(self):
        print("TODO: Ping DNS")

    def test_dns(self):
        print("TODO: Test DNS")