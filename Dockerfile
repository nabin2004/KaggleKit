# ---- Base image ----
FROM python:3.11-slim

# ---- System deps (keep it minimal) ----
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---- uv binary (no pip bootstrap) ----
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# ---- Set workdir ----
WORKDIR /app

# ---- Copy dependency files first (for caching) ----
COPY pyproject.toml uv.lock ./

# ---- Install dependencies ----
ENV UV_LINK_MODE=copy
RUN uv sync --frozen --no-dev

# ---- Copy rest of the code ----
COPY . .

# ---- Expose API port ----
EXPOSE 8000

# ---- Default command ----
CMD ["uv", "run", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
