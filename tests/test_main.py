import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from omnicrack.main import app

runner = CliRunner()

@pytest.fixture
def mock_components():
    with patch("omnicrack.main.HardwareDetector") as mock_hw, \
         patch("omnicrack.main.HashIdentifier") as mock_id, \
         patch("omnicrack.main.PcapAnalyzer") as mock_pcap, \
         patch("omnicrack.main.DockerManager") as mock_docker, \
         patch("omnicrack.main.SessionManager") as mock_session, \
         patch("builtins.open", new_callable=MagicMock) as mock_open:
        
        # Setup Hardware
        mock_hw_instance = mock_hw.return_value
        mock_hw_instance.has_gpu = True
        mock_hw_instance.gpu_type = "NVIDIA"
        
        # Setup Identifier
        mock_id_instance = mock_id.return_value
        mock_id_instance.identify.return_value = ["MD5"]
        
        # Setup Docker
        mock_docker_instance = mock_docker.return_value
        mock_docker_instance.check_docker_available.return_value = True
        mock_docker_instance.run_hashcat_stream.return_value = iter(["Starting...", "Recovered..."])
        
        # Setup Session
        mock_session_instance = mock_session.return_value
        mock_job = MagicMock()
        mock_job.id = 1
        mock_session_instance.create_job.return_value = mock_job
        
        # Setup File Open
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = "5d41402abc4b2a76b9719d911017c592"
        mock_open.return_value = mock_file
        
        yield {
            "hw": mock_hw,
            "id": mock_id,
            "pcap": mock_pcap,
            "docker": mock_docker,
            "session": mock_session,
            "open": mock_open
        }

def test_crack_command_success(mock_components):
    result = runner.invoke(app, ["crack", "hash.txt"])
    assert result.exit_code == 0
    assert "Detecting Hardware" in result.stdout
    assert "Identifying Target" in result.stdout
    assert "Creating Job" in result.stdout
    assert "Starting Cracking Engine" in result.stdout
    assert "Job Finished" in result.stdout

def test_crack_command_pcap(mock_components):
    # Setup PCAP specific mocks
    mock_components["pcap"].return_value.analyze.return_value = {
        "handshake_found": True,
        "ssid": "TestWiFi"
    }
    
    result = runner.invoke(app, ["crack", "capture.pcap"])
    assert result.exit_code == 0
    assert "Analyzing PCAP" in result.stdout
    assert "Handshake found" in result.stdout

def test_crack_command_no_docker(mock_components):
    mock_components["docker"].return_value.check_docker_available.return_value = False
    
    result = runner.invoke(app, ["crack", "hash.txt"])
    assert result.exit_code == 1
    assert "Docker is not available" in result.stdout
