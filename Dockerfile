# Build stage - using Python Alpine
FROM docker.io/python:3.11-alpine AS builder

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml ./
COPY README.md ./
COPY docs ./docs
COPY mkdocs.yml ./
COPY scripts ./scripts
# Create overrides directory (it's empty but mkdocs might need it)
RUN mkdir -p overrides

# Create virtual environment and install dependencies
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Install dependencies using pip
RUN pip install --no-cache-dir \
    mkdocs>=1.5.0 \
    mkdocs-simple-blog \
    mkdocs-material>=9.0.0 \
    mkdocs-material-extensions>=1.3.0 \
    mkdocs-macros-plugin>=1.0.0 \
    pymdown-extensions>=10.0 \
    Pygments>=2.16.0 \
    uvicorn>=0.25.0 \
    starlette>=0.35.0

# Build the MkDocs site
RUN mkdocs build

# Runtime stage - using Python Alpine slim
FROM docker.io/python:3.11-alpine

# Copy virtual environment from builder
COPY --from=builder /app/venv /app/venv

# Copy built site
COPY --from=builder /app/site /app/site

# Copy server script
COPY serve.py /app/serve.py

# Set environment variables
ENV PATH="/app/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV SITE_DIR=/app/site
ENV HOST=0.0.0.0
ENV PORT=8080

# Change to app directory
WORKDIR /app

# Expose port
EXPOSE 8080

# Run the server
CMD ["python", "/app/serve.py"]