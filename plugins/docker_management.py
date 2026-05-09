import subprocess

from server_toolkit_app.base_plugin import BasePlugin

class Plugin(BasePlugin):
    name = "Docker Management"

    def commands(self):
        return {
            "List All Containers": self.list_containers,
            "Restart Unhealthy Containers": self.restart_unhealthy,
            "Start Container Exec Shell": self.start_shell,
            "Container Stats": self.container_stats,
            "Clean Dangling Images": self.clean_images,
            "Clean Dangling Volumes": self.clean_volumes,
            "Compose Stack Status": self.compose_stack,
            "View Logs": self.view_logs
        }
    
    def run(self, cmd):
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    
    def list_containers(self):
        return "TODO: List Containers"
    
    def restart_unhealthy(self):
        return "TODO: Restart Unealthy Containers"
    
    def start_shell(self):
        return "TODO: Start Exec Shell"
    
    def container_stats(self):
        return "TODO: Container Stats"
    
    def clean_images(self):
        return "TODO: Clean Dangling Images"
    
    def clean_volumes(self):
        return "TODO: Clean Dangling Volumes"
    
    def compose_stack(self):
        return "TODO: Compose Stack Status"
    
    def view_logs(self):
        return "TODO: View Logs"