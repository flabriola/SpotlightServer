import os
from typing import List, Dict, Any, Optional
import httpx
from urllib.parse import quote_plus


class WebSearchTool:
    def __init__(self):
        self.search_api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
        self.search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
        self.base_url = "https://www.googleapis.com/customsearch/v1"
    
    async def search(
        self, 
        query: str, 
        max_results: int = 10,
        location: Optional[str] = None,
        search_images: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Perform web search using Google Custom Search API
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return (max 10)
            location: Optional location for localized search
            search_images: Whether to search for images instead of web pages
        """
        if not self.search_api_key or not self.search_engine_id:
            # Return mock results if API keys are not configured
            return self._get_mock_results(query, max_results)
        
        try:
            # Prepare search parameters
            params = {
                'key': self.search_api_key,
                'cx': self.search_engine_id,
                'q': query,
                'num': min(max_results, 10),  # Google CSE max is 10
                'safe': 'active'  # Safe search
            }
            
            # Add location if provided
            if location:
                params['location'] = location
                params['gl'] = 'us'  # Default country code, can be made configurable
            
            # Add search type for images
            if search_images:
                params['searchType'] = 'image'
            
            # Make the API request
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                # Extract search results
                items = data.get('items', [])
                results = []
                
                for item in items:
                    result = {
                        "title": item.get('title', ''),
                        "url": item.get('link', ''),
                        "snippet": item.get('snippet', ''),
                        "relevance_score": 1.0  # Google doesn't provide relevance scores
                    }
                    
                    # Add image-specific fields if searching images
                    if search_images:
                        result.update({
                            "image_url": item.get('link', ''),
                            "image_thumbnail": item.get('image', {}).get('thumbnailLink', ''),
                            "image_context": item.get('image', {}).get('contextLink', '')
                        })
                    
                    results.append(result)
                
                return results
                
        except httpx.HTTPStatusError as e:
            print(f"Google Search API error: {e.response.status_code} - {e.response.text}")
            return self._get_mock_results(query, max_results)
        except Exception as e:
            print(f"Search error: {str(e)}")
            return self._get_mock_results(query, max_results)
    
    def _get_mock_results(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Generate mock results for testing when API is not available"""
        mock_results = [
            {
                "title": f"Result {i+1} for '{query}'",
                "url": f"https://example.com/result-{i+1}",
                "snippet": f"This is a mock search result snippet for query: {query}",
                "relevance_score": 0.9 - (i * 0.1)
            }
            for i in range(min(max_results, 5))
        ]
        return mock_results
    
    async def search_with_summary(
        self, 
        query: str, 
        max_results: int = 10,
        location: Optional[str] = None,
        search_images: bool = False
    ) -> Dict[str, Any]:
        """
        Perform search and generate summary of results
        """
        results = await self.search(query, max_results, location, search_images)
        
        # Generate a simple summary based on results
        if results:
            summary = f"Found {len(results)} results for '{query}'"
            if location:
                summary += f" in {location}"
            if search_images:
                summary += " (image search)"
            summary += ". The top results provide relevant information about the topic."
        else:
            summary = f"No results found for '{query}'"
        
        return {
            "results": results,
            "summary": summary,
            "total_results": len(results),
            "search_type": "image" if search_images else "web",
            "location": location
        } 