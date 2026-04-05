"""
Projects API router.
GET /api/projects/         — list all projects
GET /api/projects/{slug}   — single project detail
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import Project, ProjectList
from app.data.portfolio_data import PROJECTS

router = APIRouter()


@router.get("/", response_model=ProjectList)
async def list_projects():
    return ProjectList(projects=PROJECTS)


@router.get("/{slug}", response_model=Project)
async def get_project(slug: str):
    for project in PROJECTS:
        if project.slug == slug:
            return project
    raise HTTPException(status_code=404, detail=f"Project '{slug}' not found")
