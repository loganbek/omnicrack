from datetime import datetime
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    status = Column(String, default="created") # created, running, paused, completed, failed
    hash_type = Column(String)
    target_file = Column(String)
    wordlist = Column(String, nullable=True)
    command_args = Column(Text) # JSON or string representation of args
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SessionManager:
    def __init__(self, db_path: str = "sqlite:///omnicrack.db"):
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_job(self, hash_type: str, target_file: str, command_args: str, wordlist: Optional[str] = None) -> Job:
        session = self.Session()
        new_job = Job(
            hash_type=hash_type,
            target_file=target_file,
            wordlist=wordlist,
            command_args=command_args,
            status="created"
        )
        session.add(new_job)
        session.commit()
        # Refresh to get ID
        session.refresh(new_job)
        session.close()
        return new_job

    def get_job(self, job_id: int) -> Optional[Job]:
        session = self.Session()
        job = session.query(Job).filter(Job.id == job_id).first()
        session.close()
        return job

    def update_job_status(self, job_id: int, status: str):
        session = self.Session()
        job = session.query(Job).filter(Job.id == job_id).first()
        if job:
            job.status = status
            session.commit()
        session.close()

    def list_jobs(self) -> List[Job]:
        session = self.Session()
        jobs = session.query(Job).all()
        session.close()
        return jobs
