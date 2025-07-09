import time
from typing import Dict, Any, Optional
from app.models.request import LLMProvider, ChatRequest, SearchRequest, SummariseRequest
from app.models.response import ChatResponse, SearchResponse, SummariseResponse, ErrorResponse
from app.llm_clients.openai import OpenAIClient
from app.llm_clients.anthropic import AnthropicClient
from app.llm_clients.gemini import GeminiClient
from app.tools.search import WebSearchTool
from app.tools.summariser import SummariserTool
from app.utils.classifier import QueryClassifier


class LLMController:
    def __init__(self):
        # Initialize LLM clients
        self.llm_clients = {
            LLMProvider.OPENAI: OpenAIClient(),
            LLMProvider.ANTHROPIC: AnthropicClient(),
            LLMProvider.GEMINI: GeminiClient()
        }
        
        # Initialize tools
        self.search_tool = WebSearchTool()
        self.summariser_tool = SummariserTool()
        self.classifier = QueryClassifier()
    
    def get_llm_client(self, provider: LLMProvider):
        """Get the appropriate LLM client based on provider"""
        return self.llm_clients.get(provider, self.llm_clients[LLMProvider.OPENAI])
    
    async def handle_chat(self, request: ChatRequest) -> ChatResponse:
        """Handle chat requests"""
        start_time = time.time()
        
        try:
            client = self.get_llm_client(request.llm_provider)
            result = await client.chat(
                query=request.query,
                context=request.context,
                conversation_history=request.conversation_history,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            return ChatResponse(
                success=True,
                response=result["response"],
                llm_provider=request.llm_provider.value,
                processing_time_ms=processing_time,
                usage_stats=result.get("usage_stats")
            )
            
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            return ChatResponse(
                success=False,
                message=f"Chat processing failed: {str(e)}",
                response="",
                llm_provider=request.llm_provider.value,
                processing_time_ms=processing_time
            )
    
    async def handle_search(self, request: SearchRequest) -> SearchResponse:
        """Handle search requests"""
        start_time = time.time()
        
        try:
            # Perform web search
            search_results = await self.search_tool.search_with_summary(
                query=request.query,
                max_results=request.max_results
            )
            
            # Optionally enhance with LLM if requested
            summary = None
            if request.include_summary:
                client = self.get_llm_client(request.llm_provider)
                llm_result = await client.search(
                    query=request.query,
                    context={"search_results": search_results["results"]}
                )
                summary = llm_result.get("response", search_results["summary"])
            
            processing_time = (time.time() - start_time) * 1000
            
            # Convert search results to response format
            from app.models.response import SearchResult
            formatted_results = [
                SearchResult(**result) for result in search_results["results"]
            ]
            
            return SearchResponse(
                success=True,
                results=formatted_results,
                total_results=len(formatted_results),
                search_query=request.query,
                summary=summary or search_results["summary"],
                llm_provider=request.llm_provider.value,
                processing_time_ms=processing_time
            )
            
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            return SearchResponse(
                success=False,
                message=f"Search processing failed: {str(e)}",
                results=[],
                total_results=0,
                search_query=request.query,
                llm_provider=request.llm_provider.value,
                processing_time_ms=processing_time
            )
    
    async def handle_summarise(self, request: SummariseRequest) -> SummariseResponse:
        """Handle summarisation requests"""
        start_time = time.time()
        
        try:
            # First use local summariser tool
            local_summary = self.summariser_tool.summarise_content(
                content=request.content,
                length=request.summary_length,
                style=request.summary_style
            )
            
            # Enhance with LLM
            client = self.get_llm_client(request.llm_provider)
            llm_result = await client.summarise(
                content=request.content,
                context={
                    "summary_length": request.summary_length,
                    "summary_style": request.summary_style,
                    "local_summary": local_summary
                }
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            return SummariseResponse(
                success=True,
                summary=llm_result.get("summary", local_summary["summary"]),
                original_length=len(request.content),
                summary_length=len(llm_result.get("summary", local_summary["summary"])),
                compression_ratio=local_summary["compression_ratio"],
                key_points=local_summary.get("key_points"),
                llm_provider=request.llm_provider.value,
                processing_time_ms=processing_time
            )
            
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            return SummariseResponse(
                success=False,
                message=f"Summarisation failed: {str(e)}",
                summary="",
                original_length=len(request.content),
                summary_length=0,
                llm_provider=request.llm_provider.value,
                processing_time_ms=processing_time
            ) 