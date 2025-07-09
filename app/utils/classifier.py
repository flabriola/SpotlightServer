from typing import Dict, Any, Optional
from app.models.request import QueryType
import re


class QueryClassifier:
    def __init__(self):
        # Define patterns for different query types
        self.search_patterns = [
            r'\b(search|find|look|lookup|what is|who is|where is|when is|how to)\b',
            r'\b(latest|news|current|recent|today)\b',
            r'\b(compare|vs|versus|difference)\b'
        ]
        
        self.chat_patterns = [
            r'\b(help|explain|tell me|discuss|talk about)\b',
            r'\b(opinion|think|feel|believe)\b',
            r'\b(conversation|chat|ask)\b'
        ]
        
        self.summarise_patterns = [
            r'\b(summarize|summarise|summary|brief|overview)\b',
            r'\b(key points|main points|highlights)\b',
            r'\b(tldr|tl;dr|in short|briefly)\b'
        ]
    
    def classify_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> QueryType:
        """
        Classify the query to determine the appropriate endpoint
        """
        query_lower = query.lower()
        
        # Check for explicit content to summarise
        if context and "content" in context:
            return QueryType.SUMMARISE
        
        # Count pattern matches for each type
        search_score = sum(1 for pattern in self.search_patterns if re.search(pattern, query_lower))
        chat_score = sum(1 for pattern in self.chat_patterns if re.search(pattern, query_lower))
        summarise_score = sum(1 for pattern in self.summarise_patterns if re.search(pattern, query_lower))
        
        # Return the type with highest score
        scores = {
            QueryType.SEARCH: search_score,
            QueryType.CHAT: chat_score,
            QueryType.SUMMARISE: summarise_score
        }
        
        # If no clear winner, default to chat
        max_score = max(scores.values())
        if max_score == 0:
            return QueryType.CHAT
        
        # Return the query type with highest score
        for query_type, score in scores.items():
            if score == max_score:
                return query_type
        
        return QueryType.CHAT
    
    def get_classification_confidence(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
        """
        Get confidence scores for each classification type
        """
        query_lower = query.lower()
        
        search_score = sum(1 for pattern in self.search_patterns if re.search(pattern, query_lower))
        chat_score = sum(1 for pattern in self.chat_patterns if re.search(pattern, query_lower))
        summarise_score = sum(1 for pattern in self.summarise_patterns if re.search(pattern, query_lower))
        
        total_score = search_score + chat_score + summarise_score
        
        if total_score == 0:
            return {
                QueryType.SEARCH: 0.33,
                QueryType.CHAT: 0.34,
                QueryType.SUMMARISE: 0.33
            }
        
        return {
            QueryType.SEARCH: search_score / total_score,
            QueryType.CHAT: chat_score / total_score,
            QueryType.SUMMARISE: summarise_score / total_score
        } 