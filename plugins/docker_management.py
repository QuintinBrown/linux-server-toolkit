import subprocess
import pty

from server_toolkit_app.base_plugin import BasePlugin

class Plugin(BasePlugin):
    name = "Docker Management"

    def commands(self):
        return {
            "List All Containers": {"func": self.list_containers, "interactive": False},
            "Restart Unhealthy Containers": {"func": self.restart_unhealthy, "interactive": False},
            "Start Container Exec Shell": {"func": self.start_shell, "interactive": True},
            "Container Stats": {"func": self.container_stats, "interactive": False},
            "Clean Dangling Images": {"func": self.clean_images, "interactive": True},
            "Clean Dangling Volumes": {"func": self.clean_volumes, "interactive": True},
            "Compose Stack Status": {"func": self.compose_stack, "interactive": False},
            "View Logs": {"func": self.view_logs, "interactive": False}
        }
    
    def run(self, cmd):
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            raise Exception(result.stderr.strip())

        return result.stdout.strip()
    
    def list_containers(self):
        return self.run("sudo docker ps")
    
    def restart_unhealthy(self):
        return self.run("sudo docker ps -q --filter \"health=unhealthy\" | xargs -r docker restart")
    
    def start_shell(self):
        print("The currently running containers are:\n")
        print(self.list_containers())

        container = input("\nWhich container would you like to start a shell in? ").strip()

        if not container:
            print("No container selected")
            return
        
        exec_cmd = ["sudo", "docker", "exec", "-it", container, "/bin/bash"]
        pty.spawn(exec_cmd)

    def container_stats(self):
        return "TODO: Container Stats"
    
    def clean_images(self):
        print("The dangling images are\n")
        print(self.run("sudo docker images -f \"dangling=true\""))
        prune_image_command = ["sudo", "docker", "image", "prune", "-f"]
        pty.spawn(prune_image_command)
    
    def clean_volumes(self):
        print("The dangling volumes are\n")
        list = self.run("sudo docker volume ls --filter \"dangling=true\"")
        print(list)
        prune_volume_command = ["sudo", "docker", "volume", "prune"]
        pty.spawn(prune_volume_command)
    
    def compose_stack(self):
        return "TODO: Compose Stack Status"
    
    def view_logs(self):
        return "TODO: View Logs"