from core.base_plugin import BasePlugin

class Plugin(BasePlugin):
    name = "Network Testing"

    def commands(self):
        return {
            "Ping Gateway": self.ping_gateway,
            "Remote Ping": self.ping_remote,
            "Ping DNS": self.ping_dns,
            "Test DNS": self.test_dns
        }
    
    def ping_gateway(self):
        print("TODO: Ping Gateway")

    def ping_remote(self):
        print("TODO: Ping Remote")

    def ping_dns(self):
        print("TODO: Ping DNS")

    def test_dns(self):
        print("TODO: Test DNS")