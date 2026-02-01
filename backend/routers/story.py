"""
Routers for story-related API endpoints.

This module exposes endpoints to create stories, retrieve completed
stories, and contains the background task used to generate stories.
It defines helper utilities for session management and builds the
complete story response structure used by the frontend.
"""

import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.story import Story, StoryNode
from models.job import StoryJob
from schemas.story import (
    CompleteStoryResponse, CompleteStoryNodeResponse, CreateStoryRequest
)
from schemas.job import StoryJobResponse
from core.story_generator import StoryGenerator 

router = APIRouter(
    prefix="/stories",
    tags=["stories"]
)

def get_session_id(session_id: Optional[str] = Cookie(None)):
    """
    Retrieve or create a session identifier stored in a cookie.

    This dependency returns the existing `session_id` from the incoming
    request cookie if present; otherwise it generates a new UUID string.

    Args:
        session_id: Optional cookie value injected by FastAPI.

    Returns:
        A session identifier string.
    """
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id


@router.post("/create", response_model=StoryJobResponse)
def create_story(
        request: CreateStoryRequest,
        background_tasks: BackgroundTasks,
        response: Response,
        session_id: str = Depends(get_session_id),
        db: Session = Depends(get_db)
):
    """
    Create a new story generation job and schedule background processing.

    Stores a new `StoryJob` record with status `pending`, sets a
    `session_id` cookie, and enqueues `generate_story_task` to run in the
    background. Returns the created job metadata to the caller.

    Args:
        request: `CreateStoryRequest` payload containing the story theme.
        background_tasks: FastAPI background task manager.
        response: FastAPI response object used to set cookies.
        session_id: Dependency providing a session identifier.
        db: Database session dependency.

    Returns:
        The persisted `StoryJob` instance (serialized via response model).
    """
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    job_id = str(uuid.uuid4())

    job = StoryJob(
        job_id=job_id,
        session_id=session_id,
        theme=request.theme,
        status="pending"
    )
    db.add(job)
    db.commit()

    background_tasks.add_task(
        generate_story_task,
        job_id=job_id,
        theme=request.theme,
        session_id=session_id
    )

    return job

def generate_story_task(job_id: str, theme: str, session_id: str):
    """
    Background task that generates a story and updates the job record.

    This function obtains a fresh database session, updates the `StoryJob`
    status as it progresses, invokes the `StoryGenerator` to create the
    story, and writes completion or failure information back to the job
    record.

    Args:
        job_id: The UUID string of the job to update.
        theme: The story theme to pass to the generator.
        session_id: The session identifier associated with the request.
    """
    db = SessionLocal()

    try:
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()

        if not job:
            return

        try:
            job.status = "processing"
            db.commit()

            story = StoryGenerator.generate_story(db, session_id, theme)

            job.story_id = story.id  # todo: update story id
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()
        except Exception as e:
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()
    finally:
        db.close()


@router.get("/{story_id}/complete", response_model=CompleteStoryResponse)
def get_complete_story(story_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a fully-resolved story tree by story ID.

    Fetches the `Story` and all associated `StoryNode` records, then
    constructs and returns a `CompleteStoryResponse` containing the root
    node and a mapping of all nodes for client consumption.

    Args:
        story_id: Integer primary key of the story to retrieve.
        db: Database session dependency.

    Returns:
        A `CompleteStoryResponse` describing the entire story graph.

    Raises:
        HTTPException: If the story or its root node cannot be found.
    """
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    complete_story = build_complete_story_tree(db, story)
    return complete_story


def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    """
    Assemble a `CompleteStoryResponse` from stored story nodes.

    Queries all `StoryNode` rows for the given story, converts them to
    `CompleteStoryNodeResponse` objects, finds the root node, and returns
    the final `CompleteStoryResponse` payload used by the API.

    Args:
        db: Active SQLAlchemy session.
        story: The `Story` ORM instance to build the tree for.

    Returns:
        A `CompleteStoryResponse` containing the root node and a mapping of
        all nodes keyed by node id.

    Raises:
        HTTPException: If no root node is found for the story.
    """
    nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all()

    node_dict = {}
    for node in nodes:
        node_response = CompleteStoryNodeResponse(
            id=node.id,
            content=node.content,
            is_ending=node.is_ending,
            is_winning_ending=node.is_winning_ending,
            options=node.options
        )
        node_dict[node.id] = node_response

    root_node = next((node for node in nodes if node.is_root), None)
    if not root_node:
        raise HTTPException(status_code=500, detail="Story root node not found")

    return CompleteStoryResponse(
        id=story.id,
        title= story.title,
        session_id=story.session_id,
        created_at=story.created_at,
        root_node=node_dict[root_node.id],
        all_nodes=node_dict
    )