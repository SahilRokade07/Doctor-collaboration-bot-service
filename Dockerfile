FROM python:3.11-slim

WORKDIR /app

# Copy requirements files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN pip install uv && \
    uv pip install -r uv.lock

# Copy source code
COPY src/ ./src/

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
