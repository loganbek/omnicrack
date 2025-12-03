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

@patch("subprocess.Popen")
def test_run_hashcat_stream(mock_popen, docker_manager):
    process_mock = MagicMock()
    process_mock.stdout = iter(["Line 1\n", "Line 2\n"])
    process_mock.wait.return_value = None
    process_mock.returncode = 0
    mock_popen.return_value = process_mock
    
    args = ["-m", "0", "hash.txt"]
    output = list(docker_manager.run_hashcat_stream(args))
    
    assert len(output) == 2
    assert output[0] == "Line 1\n"
    assert output[1] == "Line 2\n"
    
    mock_popen.assert_called_once()
    call_args = mock_popen.call_args[0][0]
    assert "docker" in call_args
    assert "run" in call_args
