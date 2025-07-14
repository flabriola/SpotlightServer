from fastapi import APIRouter, HTTPException, status
from typing import Union
from app.models.request import ChatRequest, SearchRequest, SummariseRequest, BaseRequest
from app.models.response import ChatResponse, SearchResponse, SummariseResponse, ErrorResponse
from app.controller import LLMController
from app.utils.classifier import QueryClassifier

# Initialize the router
router = APIRouter()

# Initialize controller and classifier
controller = LLMController()
classifier = QueryClassifier()


@router.get("/health")
async def health_check():
    """Health check endpoint for Google Cloud Run"""
    return {"status": "healthy", "service": "MCP-style AI Server"}


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint for conversational AI interactions
    """
    try:
        response = await controller.handle_chat(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed: {str(e)}"
        )


@router.post("/search", response_model=SearchResponse)
async def search_endpoint(request: SearchRequest) -> SearchResponse:
    """
    Search endpoint for web search and information retrieval
    """
    try:
        response = await controller.handle_search(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search processing failed: {str(e)}"
        )


@router.post("/summarise", response_model=SummariseResponse)
async def summarise_endpoint(request: SummariseRequest) -> SummariseResponse:
    """
    Summarisation endpoint for content summarization
    """
    try:
        response = await controller.handle_summarise(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Summarisation processing failed: {str(e)}"
        )


@router.post("/auto", response_model=Union[ChatResponse, SearchResponse, SummariseResponse])
async def auto_endpoint(request: BaseRequest) -> Union[ChatResponse, SearchResponse, SummariseResponse]:
    """
    Auto-routing endpoint that classifies the query and routes to appropriate service
    """
    try:
        # Classify the query
        query_type = classifier.classify_query(request.query, request.context)
        
        # Route to appropriate endpoint based on classification
        if query_type.value == "chat":
            chat_request = ChatRequest(
                query=request.query,
                llm_provider=request.llm_provider,
                context=request.context
            )
            return await controller.handle_chat(chat_request)
            
        elif query_type.value == "search":
            search_request = SearchRequest(
                query=request.query,
                llm_provider=request.llm_provider,  # This can be None for search-only
                context=request.context
            )
            return await controller.handle_search(search_request)
            
        elif query_type.value == "summarise":
            # For summarisation, we need content in context
            content = request.context.get("content", "") if request.context else ""
            if not content:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Content required for summarisation in context field"
                )
            
            summarise_request = SummariseRequest(
                query=request.query,
                content=content,
                llm_provider=request.llm_provider,
                context=request.context
            )
            return await controller.handle_summarise(summarise_request)
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown query type: {query_type}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Auto-routing failed: {str(e)}"
        )


@router.get("/classify")
async def classify_endpoint(query: str):
    """
    Utility endpoint to test query classification
    """
    try:
        query_type = classifier.classify_query(query)
        confidence_scores = classifier.get_classification_confidence(query)
        
        return {
            "query": query,
            "classified_type": query_type.value,
            "confidence_scores": confidence_scores
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Classification failed: {str(e)}"
        ) 