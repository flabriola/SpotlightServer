# API Server for Spotlight Mobile Application

A scalable FastAPI server for Spotlight Mobile Application with chat, search, and summarisation capabilities. Designed for deployment on Google Cloud Run with support for multiple LLM providers.

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

# Search API Configuration (Google Custom Search)
SEARCH_API_KEY=your_google_search_api_key_here
SEARCH_ENGINE_ID=your_custom_search_engine_id_here
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

### Search Request
```json
POST /api/v1/search
{
  "query": "latest AI research 2024",
  "llm_provider": "anthropic",
  "max_results": 10,
  "include_summary": true
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

## Development Notes

This is a scaffold implementation. The following components need full implementation:

- **LLM Client Logic**: Actual API calls to OpenAI, Anthropic, and Gemini
- **Web Search Integration**: Real Google Custom Search API implementation
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

## License

MIT License
