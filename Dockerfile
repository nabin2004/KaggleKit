# ---- Base image ----
FROM python:3.11-slim

# ---- System deps (keep it minimal) ----
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Install uv ----
RUN pip install --no-cache-dir uv

# ---- Set workdir ----
WORKDIR /app

# ---- Copy dependency files first (for caching) ----
COPY pyproject.toml uv.lock ./

# ---- Install dependencies ----
RUN uv sync --frozen

# ---- Copy rest of the code ----
COPY . .

# ---- Expose API port ----
EXPOSE 8000

# ---- Default command ----
CMD ["uv", "run", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
