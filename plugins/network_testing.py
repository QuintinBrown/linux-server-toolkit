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
            "Find Gateway": self.find_gateway,
            "Find DNS": self.find_dns,
            "Find IP": self.find_ip
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
        
    def find_dns(self, want_printed=True):
        result = self.run("resolvectl status")
        DNS_server = re.search(r'\bCurrent DNS Server:\s([0-9]+.[0-9]+.[0-9]+.[0-9]+)', result)

        if want_printed:
            print(DNS_server.group(1))
        else:
            return DNS_server.group(1)
    
    def ping_gateway(self):
        gw = self.find_gateway(False)
        print("Pinging gateway...")
        command_result = self.run(f"ping {gw} -c 5")
        sent_search = re.search(r'([0-9])\b\spackets', command_result)
        succeeded_search = re.search(r'([0-9])\b\sreceived', command_result)
        sent = sent_search.group(1)
        succeeded = succeeded_search.group(1)

        print(f"{sent} pings sent, {succeeded} pings succeeded")

    def ping_remote(self):
        print("Pinging 8.8.8.8...")

        command_result = self.run(f"ping 8.8.8.8 -c 5")
        sent_search = re.search(r'([0-9])\b\spackets', command_result)
        succeeded_search = re.search(r'([0-9])\b\sreceived', command_result)
        sent = sent_search.group(1)
        succeeded = succeeded_search.group(1)

        print(f"{sent} pings sent, {succeeded} pings succeeded")

    def ping_dns(self):
        dns = self.find_dns(False)
        print("Pinging DNS server...")
        command_result = self.run(f"ping {dns} -c 5")
        sent_search = re.search(r'([0-9])\b\spackets', command_result)
        succeeded_search = re.search(r'([0-9])\b\sreceived', command_result)
        sent = sent_search.group(1)
        succeeded = succeeded_search.group(1)

        print(f"{sent} pings sent, {succeeded} pings succeeded")

    def test_dns(self):
        print("Pinging www.google.com...")

        command_result = self.run(f"ping www.google.com -c 5")
        sent_search = re.search(r'([0-9])\b\spackets', command_result)
        succeeded_search = re.search(r'([0-9])\b\sreceived', command_result)
        sent = sent_search.group(1)
        succeeded = succeeded_search.group(1)

        print(f"{sent} pings sent, {succeeded} pings succeeded")

    def find_ip(self):
        result = self.run("ip route")
        pretty_result = re.search(r'\bsrc\s([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', result)
        print(pretty_result.group(1))