from pydantic import BaseModel
from typing import List, Optional

class Finding(BaseModel):
    severity: str
    title: str
    details: str
    suggestion: Optional[str] = None

class FileReview(BaseModel):
    file: str
    findings: List[Finding] = []

class ReviewResult(BaseModel):
    summary: str
    files: List[FileReview] = []
