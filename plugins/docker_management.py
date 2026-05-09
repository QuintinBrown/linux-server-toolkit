import subprocess
import pty

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
        return self.run("sudo docker ps")
    
    def restart_unhealthy(self):
        return self.run("sudo docker ps --filter \"health=unhealthy\" | xargs -r docker restart")
    
    def start_shell(self):
        print("The currently running containers are:\n")
        print(self.list_containers())
        container = input("\nWhich would you like to start a shell inside? ")
        exec_cmd = ["sudo", "docker", "exec", "-it", container, "/bin/bash"]
        pty.spawn(exec_cmd)
        return
    
    def container_stats(self):
        return "TODO: Container Stats"
    
    def clean_images(self):
        print("The dangling images are\n")
        print(self.run("sudo docker images -f \"dangling=true\""))
        print()
        prune_image_command = ["sudo", "docker", "image", "prune", "-f"]
        pty.spawn(prune_image_command)
        return
    
    def clean_volumes(self):
        print("The dangling volumes are\n")
        print(self.run("sudo docker volume ls --filter \"dangling=true\""))
        print()
        prune_volume_command = ["sudo", "docker", "volume", "prune"]
        pty.spawn(prune_volume_command)
        return
    
    def compose_stack(self):
        return "TODO: Compose Stack Status"
    
    def view_logs(self):
        return "TODO: View Logs"