from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from enum import Enum


class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"


class QueryType(str, Enum):
    CHAT = "chat"
    SEARCH = "search"
    SUMMARISE = "summarise"


class BaseRequest(BaseModel):
    query: str
    llm_provider: LLMProvider = LLMProvider.OPENAI
    context: Optional[Dict[str, Any]] = None


class ChatRequest(BaseRequest):
    conversation_history: Optional[List[Dict[str, str]]] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000


class SearchRequest(BaseRequest):
    search_type: Optional[str] = "web"
    max_results: Optional[int] = 10
    include_summary: Optional[bool] = True


class SummariseRequest(BaseRequest):
    content: str
    summary_length: Optional[str] = "medium"  # short, medium, long
    summary_style: Optional[str] = "bullet_points"  # paragraph, bullet_points, key_points 