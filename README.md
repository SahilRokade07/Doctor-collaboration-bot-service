# Doctor Collaboration Bot Service

An intelligent medical assistant service that leverages local Large Language Models (LLMs) via Ollama to provide medical information, analyze documents, and assist healthcare professionals in their decision-making process. The service implements Retrieval-Augmented Generation (RAG) capabilities to enhance response accuracy and provide contextual medical insights.

## 🏥 Overview

The Doctor Collaboration Bot Service is a FastAPI-based microservice designed specifically for healthcare professionals. It provides:

- **Medical Query Processing**: Intelligent responses to medical questions using specialized medical LLMs
- **PDF Document Analysis**: Automated extraction, summarization, and topic identification from medical documents
- **RAG Implementation**: Context-aware responses using document knowledge base
- **Conversation History**: Persistent storage of interactions for reference and analysis
- **RESTful API**: Easy integration with existing healthcare systems

## 🚀 Features

### Core Capabilities
- **Local LLM Integration**: Uses Ollama to run medical LLMs locally (MedLLaMA2, Meditron)
- **Medical Document Processing**: Extracts text from PDFs and generates intelligent summaries
- **Topic Extraction**: Automatically identifies key medical topics from documents
- **Query Context**: Supports contextual queries with additional medical information
- **Data Persistence**: JSON-based storage for queries, responses, and document summaries
- **Medical Text Processing**: Specialized text cleaning and medical term extraction

### Technical Features
- **Async Processing**: Non-blocking operations for better performance
- **Error Handling**: Robust error handling with timeout management
- **CORS Support**: Cross-origin resource sharing for web applications
- **Docker Support**: Containerized deployment ready
- **Type Safety**: Comprehensive Pydantic schemas for data validation
- **Modular Architecture**: Clean separation of concerns with service-based design

## 🏗️ Architecture

```
src/
├── api/                    # API routes and endpoints
│   ├── routes.py          # Main API routes
│   └── __init__.py
├── core/                   # Core configuration
│   ├── config.py          # Application settings
│   └── __init__.py
├── db/                     # Database handlers
│   ├── handlers.py        # JSON database operations
│   └── __init__.py
├── documents/              # Document processing
│   ├── exporter.py        # Export utilities
│   └── __init__.py
├── models/                 # Model configurations
│   └── llm/               # LLM-specific configs
├── schemas/                # Data validation schemas
│   ├── bot.py             # Bot request/response schemas
│   ├── pdf.py             # PDF processing schemas
│   └── __init__.py
├── services/               # Business logic services
│   ├── bot_service.py     # LLM interaction service
│   ├── pdf_service.py     # PDF processing service
│   ├── json_db_service.py # Database service
│   └── __init__.py
├── utils/                  # Utility functions
│   ├── text_cleaner.py    # Medical text processing
│   └── __init__.py
└── main.py                # FastAPI application entry point
```

## 📋 Prerequisites

- **Python 3.11+**
- **Ollama** installed and running
- **Medical LLM Model** (MedLLaMA2 or Meditron)
- **Docker** (optional, for containerized deployment)

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd doctor_collab_bot_service
```

### 2. Install Dependencies
Using UV (recommended):
```bash
pip install uv
uv pip install -e .
```

Using pip:
```bash
pip install -e .
```

### 3. Install and Configure Ollama

#### Install Ollama:
```bash
# On Linux/macOS
curl -fsSL https://ollama.ai/install.sh | sh

# On Windows
# Download from https://ollama.ai/download
```

#### Pull Medical Models:
```bash
# Pull MedLLaMA2 model
ollama pull medllama2

# Or pull Meditron model
ollama pull meditron
```

#### Start Ollama Service:
```bash
ollama serve
```

### 4. Configure Environment

Create a `.env` file or modify `src/core/config.py`:

```python
# LLM Configuration
OLLAMA_API_URL = "http://localhost:11434"
LLM_MODEL_NAME = "medllama2"  # or "meditron"

# Database Configuration
JSON_DB_PATH = "db/data.json"

# Security Configuration
SECRET_KEY = "your-secure-secret-key-here"
```

## 🚀 Usage

### Starting the Service

#### Development Mode:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

#### Production Mode:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

#### Using Docker:
```bash
# Build the image
docker build -t doctor-collab-bot .

# Run the container
docker run -p 8000:8000 doctor-collab-bot
```

### API Documentation

Once running, access the interactive API documentation at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📝 API Endpoints

### 1. Medical Query Processing

**POST** `/query`

Process medical queries with contextual information.

```json
{
  "query": "What are the symptoms of hypertension?",
  "context": "Patient is 45-year-old male with family history of cardiovascular disease"
}
```

**Response:**
```json
{
  "response": "Hypertension symptoms include headaches, shortness of breath, nosebleeds...",
  "confidence": 0.95,
  "sources": []
}
```

### 2. PDF Document Upload

**POST** `/upload-pdf`

Upload and analyze medical PDF documents.

```bash
curl -X POST "http://localhost:8000/upload-pdf" \
     -F "file=@medical_document.pdf"
```

**Response:**
```json
{
  "filename": "medical_document.pdf",
  "page_count": 5,
  "summary": "This document discusses cardiovascular disease management...",
  "topics": ["hypertension", "cardiovascular disease", "treatment protocols"]
}
```

## 🔧 Configuration

### LLM Models

The service supports multiple medical LLMs:

- **MedLLaMA2**: Specialized for medical question answering
- **Meditron**: Focused on clinical decision support

Configure in `src/core/config.py`:
```python
LLM_MODEL_NAME = "medllama2"  # or "meditron"
```

### Database Configuration

The service uses a JSON-based database for development. For production, consider integrating with:
- PostgreSQL
- MongoDB
- Vector databases (for enhanced RAG)

## 🔒 Security Considerations

- **Data Privacy**: Ensure HIPAA compliance for medical data
- **Access Control**: Implement authentication for production use
- **Audit Logging**: Track all medical queries and responses
- **Data Encryption**: Encrypt sensitive medical information

## 🧪 Testing

Run tests using pytest:
```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=src tests/
```

## 📊 Monitoring and Logging

The service includes basic logging. For production:

1. **Add structured logging**
2. **Implement health checks**
3. **Monitor LLM response times**
4. **Track query patterns**

## 🔄 RAG Implementation

The service implements RAG through:

1. **Document Ingestion**: PDF processing and text extraction
2. **Context Retrieval**: Relevant document sections for queries
3. **Enhanced Responses**: LLM responses augmented with document context
4. **Knowledge Base**: Persistent storage of processed documents

### Enhancing RAG Capabilities

For advanced RAG implementation:

```python
# Add vector embeddings
pip install sentence-transformers chromadb

# Implement semantic search
# Add document chunking
# Create embedding store
```

## 🚧 Development Roadmap

### Planned Features
- [ ] Vector database integration for improved RAG
- [ ] Multi-modal support (images, DICOM files)
- [ ] Authentication and authorization
- [ ] Advanced medical entity recognition
- [ ] Integration with medical terminology APIs
- [ ] Real-time collaboration features
- [ ] Clinical decision support tools

### Performance Improvements
- [ ] Response caching
- [ ] Model optimization
- [ ] Batch processing
- [ ] Load balancing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is designed to assist healthcare professionals and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical decisions.

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team
- Review the API documentation

---

## 🔗 Related Technologies

- **FastAPI**: Modern web framework for building APIs
- **Ollama**: Local LLM runtime
- **Pydantic**: Data validation and settings management
- **PyPDF2**: PDF processing library
- **Uvicorn**: ASGI server implementation

Built with ❤️ for healthcare professionals
