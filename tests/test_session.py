import pytest
import os
from omnicrack.session import SessionManager, Job

@pytest.fixture
def session_manager():
    # Use in-memory DB for testing
    return SessionManager(db_path="sqlite:///:memory:")

def test_create_job(session_manager):
    job = session_manager.create_job(
        hash_type="MD5",
        target_file="hashes.txt",
        command_args="-m 0 hashes.txt"
    )
    
    assert job.id is not None
    assert job.hash_type == "MD5"
    assert job.status == "created"

def test_get_job(session_manager):
    created_job = session_manager.create_job(
        hash_type="SHA1",
        target_file="sha1.txt",
        command_args="-m 100"
    )
    
    fetched_job = session_manager.get_job(created_job.id)
    assert fetched_job is not None
    assert fetched_job.id == created_job.id
    assert fetched_job.hash_type == "SHA1"

def test_update_job_status(session_manager):
    job = session_manager.create_job(
        hash_type="MD5",
        target_file="test.txt",
        command_args=""
    )
    
    session_manager.update_job_status(job.id, "running")
    
    updated_job = session_manager.get_job(job.id)
    assert updated_job.status == "running"

def test_list_jobs(session_manager):
    session_manager.create_job("MD5", "1.txt", "")
    session_manager.create_job("SHA1", "2.txt", "")
    
    jobs = session_manager.list_jobs()
    assert len(jobs) == 2
