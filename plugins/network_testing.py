import subprocess
import re

from server_toolkit_app.base_plugin import BasePlugin

class Plugin(BasePlugin):
    name = "Network Testing"

    def commands(self):
        return {
            "Ping Gateway": self.ping_gateway,
            "Remote Ping": self.ping_remote,
            "Ping DNS": self.ping_dns,
            "Test DNS": self.test_dns,
            "Find Gateway": self.find_gateway,
            "Find DNS": self.find_dns,
            "Find IP": self.find_ip
        }
    
    def run(self, cmd):
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    
    def ping(self, dest, count=5):
        command_result = self.run(f"ping {dest} -c {count}")
        sent_search = re.search(r'([0-9])\b\spackets', command_result)
        succeeded_search = re.search(r'([0-9])\b\sreceived', command_result)
        sent = sent_search.group(1)
        succeeded = succeeded_search.group(1)

        return(f"{sent} pings sent, {succeeded} pings succeeded")

    def find_gateway(self):
        result = self.run("ip route")
        pretty_result = re.search(r'\bvia\s([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', result)
        return pretty_result.group(1)
        
    def find_dns(self):
        result = self.run("resolvectl status")
        DNS_server = re.search(r'\bCurrent DNS Server:\s([0-9]+.[0-9]+.[0-9]+.[0-9]+)', result)
        return DNS_server.group(1)
    
    def ping_gateway(self):
        gw = self.find_gateway(False)
        print("Pinging gateway...")
        return self.ping(gw)

    def ping_remote(self):
        print("Pinging 8.8.8.8...")
        return self.ping("8.8.8.8")

    def ping_dns(self):
        dns = self.find_dns(False)
        print("Pinging DNS server...")
        return self.ping(dns)

    def test_dns(self):
        print("Pinging www.google.com...")
        return self.ping("www.google.com")

    def find_ip(self):
        result = self.run("ip route")
        pretty_result = re.search(r'\bsrc\s([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', result)
        return(pretty_result.group(1))