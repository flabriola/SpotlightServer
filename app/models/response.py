from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class BaseResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    timestamp: datetime = datetime.now()
    llm_provider: str
    processing_time_ms: Optional[float] = None


class ChatResponse(BaseResponse):
    response: str
    conversation_id: Optional[str] = None
    usage_stats: Optional[Dict[str, Any]] = None


class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    relevance_score: Optional[float] = None


class SearchResponse(BaseResponse):
    results: List[SearchResult]
    total_results: int
    search_query: str
    summary: Optional[str] = None


class SummariseResponse(BaseResponse):
    summary: str
    original_length: int
    summary_length: int
    compression_ratio: Optional[float] = None
    key_points: Optional[List[str]] = None


class ErrorResponse(BaseResponse):
    error_code: str
    error_details: Optional[Dict[str, Any]] = None 