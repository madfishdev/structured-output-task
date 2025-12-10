# Structured Output Test

Full-stack app that extracts structured data from images using LLM.

## Quick Start

```bash
# Open backend/.env.docker and set OPENROUTER_API_KEY with the one sent via email.

docker compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## What's Implemented

**Core features:**
- Auth (register/login with password confirmation)
- Dynamic field builder (name + type)
- Image upload to MinIO (S3-compatible)
- Duplicate prevention via SHA256 hashing
- LLM structured output (OpenRouter + GPT-4o)

**Optional:**
- Redis caching (1hr TTL)
- Logging (INFO/DEBUG/ERROR levels)

I skipped history feature due to time constraints.

## Key Decisions

**Deduplication:** Hash image bytes, store as '{username}/{hash}.{ext}'. Per-user namespace so same image for different users stays separate.

**Caching:** Redis with cache key = hash(username + prompt + fields + image). Expires after 1 hour.

**Auth:** JWT in localStorage (note: HttpOnly cookies would be better for production).

## What I'd Add Next

- History feature (store analyses in PostgreSQL)
- Refresh tokens
- Rate limiting