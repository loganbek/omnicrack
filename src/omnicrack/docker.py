import subprocess
import shutil
from typing import List, Optional

class DockerManager:
    def __init__(self, image: str = "dizcza/docker-hashcat:latest"):
        self.image = image

    def check_docker_available(self) -> bool:
        """
        Checks if docker CLI is available and running.
        """
        if shutil.which("docker") is None:
            return False
        
        try:
            result = subprocess.run(
                ["docker", "info"], 
                capture_output=True, 
                check=False
            )
            return result.returncode == 0
        except Exception:
            return False

    def pull_image(self) -> bool:
        """
        Pulls the hashcat docker image.
        """
        try:
            result = subprocess.run(
                ["docker", "pull", self.image],
                check=False
            )
            return result.returncode == 0
        except Exception:
            return False

    def run_hashcat(self, args: List[str]) -> subprocess.CompletedProcess:
        """
        Runs hashcat in a docker container with provided arguments.
        Mounts the current directory to /data in the container.
        """
        # Basic command structure
        # docker run --rm -it -v $(pwd):/data --gpus all dizcza/docker-hashcat:latest [args]
        
        # Note: --gpus all requires nvidia-container-toolkit. 
        # We might need to make this configurable or detect it.
        # For now, we'll assume it's desired if available, but maybe we should let the caller decide?
        # The AGENT_CONTEXT says "The tool must auto-detect this."
        # HardwareDetector handles detection, but here we just run the container.
        # We'll add --gpus all by default for now, but catch errors if runtime not found?
        # Or maybe just pass it through.
        
        cmd = [
            "docker", "run", "--rm", "-i", 
            "-v", f"{subprocess.os.getcwd()}:/data",
            self.image
        ]
        
        # Append hashcat args
        cmd.extend(args)
        
        try:
            return subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
        except Exception as e:
            # Return a dummy completed process with error
            return subprocess.CompletedProcess(args=cmd, returncode=1, stderr=str(e))

    def run_hashcat_stream(self, args: List[str]):
        """
        Runs hashcat in a docker container and yields output line by line.
        """
        cmd = [
            "docker", "run", "--rm", "-i", 
            "-v", f"{subprocess.os.getcwd()}:/data",
            self.image
        ]
        cmd.extend(args)
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            for line in process.stdout:
                yield line
                
            process.wait()
            if process.returncode != 0:
                yield f"Error: Process exited with code {process.returncode}"
                
        except Exception as e:
            yield f"Error: {str(e)}"
