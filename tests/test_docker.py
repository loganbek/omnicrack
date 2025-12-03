import pytest
from unittest.mock import patch, MagicMock
import subprocess
from omnicrack.docker import DockerManager

@pytest.fixture
def docker_manager():
    return DockerManager()

@patch("shutil.which")
@patch("subprocess.run")
def test_check_docker_available_success(mock_run, mock_which, docker_manager):
    mock_which.return_value = "/usr/bin/docker"
    mock_run.return_value = MagicMock(returncode=0)
    
    assert docker_manager.check_docker_available() is True

@patch("shutil.which")
def test_check_docker_not_installed(mock_which, docker_manager):
    mock_which.return_value = None
    assert docker_manager.check_docker_available() is False

@patch("shutil.which")
@patch("subprocess.run")
def test_check_docker_daemon_down(mock_run, mock_which, docker_manager):
    mock_which.return_value = "/usr/bin/docker"
    mock_run.return_value = MagicMock(returncode=1)
    
    assert docker_manager.check_docker_available() is False

@patch("subprocess.run")
def test_pull_image(mock_run, docker_manager):
    mock_run.return_value = MagicMock(returncode=0)
    assert docker_manager.pull_image() is True
    mock_run.assert_called_with(["docker", "pull", "dizcza/docker-hashcat:latest"], check=False)

@patch("subprocess.run")
def test_run_hashcat(mock_run, docker_manager):
    mock_run.return_value = MagicMock(returncode=0, stdout="Success")
    
    args = ["-m", "0", "hash.txt", "wordlist.txt"]
    docker_manager.run_hashcat(args)
    
    # Verify call args
    # We can't easily check the exact dynamic path in -v, so we'll check parts
    call_args = mock_run.call_args[0][0]
    assert call_args[0] == "docker"
    assert call_args[1] == "run"
    assert "dizcza/docker-hashcat:latest" in call_args
    assert "-m" in call_args
    assert "0" in call_args
