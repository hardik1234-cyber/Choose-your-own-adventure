"""Routers for job status tracking endpoints.

This module provides endpoints to query the status and details of
story generation jobs.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from models.job import StoryJob
from schemas.job import StoryJobResponse

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)


@router.get("/{job_id}", response_model=StoryJobResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    """
    Retrieve the status and details of a story generation job.

    Queries the database for a job with the given ID and returns its
    current status, theme, completion timestamp, and associated story ID
    if available.

    Args:
        job_id: The UUID string identifier of the job to retrieve.
        db: Database session dependency.

    Returns:
        A `StoryJobResponse` containing job metadata and status.

    Raises:
        HTTPException: If the job with the given ID is not found (404).
    """
    job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job