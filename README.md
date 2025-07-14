# AI Server

A scalable FastAPI server for AI search applications with chat, search, and summarisation capabilities. Designed for deployment on Google Cloud Run with support for multiple LLM providers.

## Architecture

```
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI entry point
│   ├── router.py            # API routes (chat/search/summarise)
│   ├── controller.py        # Core orchestration logic
│   ├── llm_clients/         # LLM provider integrations
│   │   ├── __init__.py
│   │   ├── openai.py        # OpenAI GPT integration
│   │   ├── anthropic.py     # Anthropic Claude integration
│   │   └── gemini.py        # Google Gemini integration
│   ├── tools/               # External tools and utilities
│   │   ├── search.py        # Web search functionality
│   │   └── summariser.py    # Content summarisation
│   ├── utils/
│   │   └── classifier.py    # Query type classification
│   └── models/
│       ├── request.py       # Pydantic request schemas
│       └── response.py      # Pydantic response schemas
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
└── README.md
```

## Features

- **Multi-LLM Support**: OpenAI GPT, Anthropic Claude, Google Gemini
- **Three Core Endpoints**: Chat, Search, Summarisation
- **Auto-Routing**: Intelligent query classification and routing
- **Google Custom Search**: Real web and image search integration
- **Scalable**: Designed for Google Cloud Run deployment
- **Type-Safe**: Full Pydantic validation for requests/responses

## API Endpoints

### Base URL: `/api/v1`

1. **POST /chat** - Conversational AI interactions
2. **POST /search** - Web search with AI enhancement
3. **POST /summarise** - Content summarisation
4. **POST /auto** - Auto-routing based on query classification
5. **GET /classify** - Test query classification
6. **GET /health** - Health check for monitoring

## Search Endpoint

The search endpoint provides real-time web and image search functionality using Google Custom Search API. It works independently without requiring LLM providers and returns actual search results from Google.

### Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | ✅ | - | Search query string |
| `max_results` | integer | ❌ | 10 | Maximum results (1-10) |
| `location` | string | ❌ | null | For localized search |
| `search_images` | boolean | ❌ | false | Search images instead of web pages |

### Example Requests

#### Basic Web Search
```bash
curl -X POST http://localhost:8080/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Python programming"}'
```

**Output:**
```json
{
  "success": true,
  "message": null,
  "timestamp": "2025-07-09T11:52:45.462555",
  "llm_provider": "search_only",
  "processing_time_ms": 764.078,
  "results": [
    {
      "title": "Welcome to Python.org",
      "url": "https://www.python.org/",
      "snippet": "The official home of the Python Programming Language.",
      "relevance_score": 1.0,
      "image_url": null,
      "image_thumbnail": null,
      "image_context": null
    },
    {
      "title": "Python (programming language) - Wikipedia",
      "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
      "snippet": "Python is a high-level, general-purpose programming language.",
      "relevance_score": 1.0,
      "image_url": null,
      "image_thumbnail": null,
      "image_context": null
    }
  ],
  "total_results": 2,
  "search_query": "Python programming",
  "summary": "Found 2 results for 'Python programming'. The top results provide relevant information about the topic.",
  "search_type": "web",
  "location": null
}
```

#### Image Search
```bash
curl -X POST http://localhost:8080/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "cute cats",
    "search_images": true,
    "max_results": 2
  }'
```

**Output:**
```json
{
  "success": true,
  "message": null,
  "timestamp": "2025-07-09T11:52:45.462555",
  "llm_provider": "search_only",
  "processing_time_ms": 803.893,
  "results": [
    {
      "title": "Super Cute Cats Compilation - YouTube",
      "url": "https://i.ytimg.com/vi/SQJrYw1QvSQ/hq720.jpg",
      "snippet": "Super Cute Cats Compilation - YouTube",
      "relevance_score": 1.0,
      "image_url": "https://i.ytimg.com/vi/SQJrYw1QvSQ/hq720.jpg",
      "image_thumbnail": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQGPUi4-zhS7XOmXMlo4KoW917RkwBHxRq7Wtd_SbEGSGAQijUAMXc8KQ&s",
      "image_context": "https://www.youtube.com/watch?v=SQJrYw1QvSQ"
    },
    {
      "title": "Adorable Gray and White Kitten on Wooden Floor",
      "url": "https://i.pinimg.com/736x/38/36/32/38363200987839853c58c85ecec15488.jpg",
      "snippet": "Adorable Gray and White Kitten on Wooden Floor",
      "relevance_score": 1.0,
      "image_url": "https://i.pinimg.com/736x/38/36/32/38363200987839853c58c85ecec15488.jpg",
      "image_thumbnail": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgshdTnV02VLe93ti227WoLGSjq3At47uikeD5kwLjFhutDmHpMgwysg&s",
      "image_context": "https://www.pinterest.com/pin/596164069443954135/"
    }
  ],
  "total_results": 2,
  "search_query": "cute cats",
  "summary": "Found 2 results for 'cute cats' (image search). The top results provide relevant information about the topic.",
  "search_type": "image",
  "location": null
}
```

#### Localized Search
```bash
curl -X POST http://localhost:8080/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "restaurants",
    "location": "San Francisco",
    "max_results": 3
  }'
```

**Output:**
```json
{
  "success": true,
  "message": null,
  "timestamp": "2025-07-09T11:52:45.462555",
  "llm_provider": "search_only",
  "processing_time_ms": 721.701,
  "results": [
    {
      "title": "Restaurants Care: Home",
      "url": "https://restaurantscare.org/",
      "snippet": "Restaurants Care is a relief fund for California restaurant workers.",
      "relevance_score": 1.0,
      "image_url": null,
      "image_thumbnail": null,
      "image_context": null
    },
    {
      "title": "Darden Restaurants: A Leader in the Full-Service Restaurant Industry",
      "url": "https://www.darden.com/",
      "snippet": "Darden Restaurants is the premier full-service dining company.",
      "relevance_score": 1.0,
      "image_url": null,
      "image_thumbnail": null,
      "image_context": null
    }
  ],
  "total_results": 2,
  "search_query": "restaurants",
  "summary": "Found 2 results for 'restaurants' in San Francisco. The top results provide relevant information about the topic.",
  "search_type": "web",
  "location": "San Francisco"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the request was successful |
| `llm_provider` | string | Always "search_only" for search endpoint |
| `processing_time_ms` | float | Request processing time in milliseconds |
| `results` | array | Array of search result objects |
| `total_results` | integer | Number of results returned |
| `search_query` | string | The original search query |
| `summary` | string | Human-readable summary of results |
| `search_type` | string | "web" or "image" |
| `location` | string | Location used for search (if provided) |

### Search Result Object

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Result title |
| `url` | string | Result URL |
| `snippet` | string | Result description/snippet |
| `relevance_score` | float | Relevance score (1.0 for Google results) |
| `image_url` | string | Image URL (only for image search) |
| `image_thumbnail` | string | Thumbnail URL (only for image search) |
| `image_context` | string | Context page URL (only for image search) |

## Environment Variables

Create a `.env` file with the following variables:

```bash
# Environment Configuration
ENVIRONMENT=development
PORT=8080

# CORS Configuration
ALLOWED_ORIGINS=*

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Anthropic Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Google Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-pro

# Google Custom Search API Configuration
GOOGLE_SEARCH_API_KEY=your_google_search_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_custom_search_engine_id_here
```

## Quick Start

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the server**:
   ```bash
   python -m app.main
   ```

4. **Access the API**:
   - Server: http://localhost:8080
   - Docs: http://localhost:8080/docs
   - Health: http://localhost:8080/health

### Google Cloud Run Deployment

The repository is configured for automatic deployment to Google Cloud Run via CI/CD.

1. **Build and deploy**:
   ```bash
   docker build -t gcr.io/PROJECT_ID/ai-server .
   docker push gcr.io/PROJECT_ID/ai-server
   gcloud run deploy ai-server --image gcr.io/PROJECT_ID/ai-server
   ```

2. **Set environment variables** in Cloud Run console or via gcloud CLI.

## Usage Examples

### Chat Request
```json
POST /api/v1/chat
{
  "query": "Explain quantum computing",
  "llm_provider": "openai",
  "temperature": 0.7,
  "max_tokens": 1000
}
```

### Search Request (Web)
```json
POST /api/v1/search
{
  "query": "latest AI research 2024",
  "max_results": 10,
  "location": "San Francisco",
  "search_images": false
}
```

### Search Request (Images)
```json
POST /api/v1/search
{
  "query": "cute cats",
  "max_results": 10,
  "search_images": true
}
```

### Summarise Request
```json
POST /api/v1/summarise
{
  "query": "Summarise this article",
  "content": "Long article content...",
  "llm_provider": "gemini",
  "summary_length": "medium",
  "summary_style": "bullet_points"
}
```

### Auto-Route Request
```json
POST /api/v1/auto
{
  "query": "What is machine learning?",
  "llm_provider": "openai"
}
```

## Google Custom Search Setup

To use the search functionality, you need to set up Google Custom Search:

1. **Create a Google Cloud Project** and enable the Custom Search API
2. **Get an API Key** from Google Cloud Console
3. **Create a Custom Search Engine** at https://cse.google.com/
4. **Set environment variables**:
   - `GOOGLE_SEARCH_API_KEY`: Your Google API key
   - `GOOGLE_SEARCH_ENGINE_ID`: Your Custom Search Engine ID

## Development Notes

This is a scaffold implementation. The following components need full implementation:

- **LLM Client Logic**: Actual API calls to OpenAI, Anthropic, and Gemini
- **Advanced Summarisation**: Enhanced content processing algorithms
- **Error Handling**: Production-ready error handling and logging
- **Authentication**: API key management and user authentication
- **Rate Limiting**: Request throttling and quota management
- **Monitoring**: Logging, metrics, and observability

## Technology Stack

- **FastAPI**: Modern, fast web framework
- **Pydantic**: Data validation and serialization
- **Uvicorn/Gunicorn**: ASGI server for production
- **Docker**: Containerization for cloud deployment
- **Google Cloud Run**: Serverless container platform
- **Google Custom Search API**: Web and image search

## License

MIT License
