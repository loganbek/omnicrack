import pytest
from unittest.mock import patch, MagicMock
from omnicrack.hardware import HardwareDetector

@pytest.fixture
def detector():
    return HardwareDetector()

def test_initialization(detector):
    assert detector.gpu_type is None
    assert detector.has_gpu is False

@patch("shutil.which")
@patch("subprocess.run")
def test_detect_nvidia_success(mock_run, mock_which, detector):
    # Simulate nvidia-smi success
    mock_which.return_value = "/usr/bin/nvidia-smi"
    mock_run.return_value = MagicMock(returncode=0, stdout="NVIDIA GeForce RTX 3080")
    
    detector.detect()
    
    assert detector.has_gpu is True
    assert detector.gpu_type == "NVIDIA"
    mock_run.assert_called_with(["nvidia-smi"], capture_output=True, text=True, check=False)

@patch("shutil.which")
@patch("subprocess.run")
def test_detect_amd_success(mock_run, mock_which, detector):
    # Simulate nvidia-smi failure, but rocm-smi success
    def which_side_effect(cmd):
        if cmd == "nvidia-smi": return None
        if cmd == "rocm-smi": return "/opt/rocm/bin/rocm-smi"
        return None
    mock_which.side_effect = which_side_effect

    def run_side_effect(cmd, **kwargs):
        if "nvidia-smi" in cmd:
            return MagicMock(returncode=1)
        if "rocm-smi" in cmd:
            return MagicMock(returncode=0, stdout="AMD Radeon RX 6800")
        return MagicMock(returncode=1)

    mock_run.side_effect = run_side_effect
    
    detector.detect()
    
    assert detector.has_gpu is True
    assert detector.gpu_type == "AMD"

@patch("shutil.which")
@patch("subprocess.run")
def test_detect_no_gpu(mock_run, mock_which, detector):
    # Simulate both failing
    mock_which.return_value = None # Or return path but fail run
    
    # Case 1: Tools don't exist
    detector.detect()
    assert detector.has_gpu is False
    assert detector.gpu_type is None

    # Case 2: Tools exist but fail
    mock_which.return_value = "/usr/bin/nvidia-smi"
    mock_run.return_value = MagicMock(returncode=1)
    detector.detect()
    assert detector.has_gpu is False
    assert detector.gpu_type is None
