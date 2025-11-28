import subprocess
import shutil

class HardwareDetector:
    def __init__(self):
        self.gpu_type = None
        self.has_gpu = False

    def detect(self):
        """
        Detects if NVIDIA or AMD GPU is present.
        Sets self.has_gpu and self.gpu_type.
        """
        # Check for NVIDIA
        if self._check_command("nvidia-smi"):
            self.has_gpu = True
            self.gpu_type = "NVIDIA"
            return

        # Check for AMD (ROCm)
        if self._check_command("rocm-smi"):
            self.has_gpu = True
            self.gpu_type = "AMD"
            return
        
        # Fallback/No GPU
        self.has_gpu = False
        self.gpu_type = None

    def _check_command(self, command: str) -> bool:
        """
        Checks if a command exists and runs successfully.
        """
        if shutil.which(command) is None:
            return False
            
        try:
            result = subprocess.run(
                [command], 
                capture_output=True, 
                text=True, 
                check=False
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
