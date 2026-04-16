# Personal AI Summarization Tool

*THIS IS AI GENERATED WILL REPLACE* 

A self-hosted document summarization app that runs small LLMs on constrained hardware. Upload a document or paste text, add a prompt, and get a summary back — all processed locally on a mini-PC with CPU-only inference.

## Motivation

I spend a lot of time reading articles and documentation, and I wanted a tool that could help me digest them faster — without sending my data to a third-party API. This project is also an excuse to own the full stack end-to-end: frontend, backend, auth, storage, inference, and deployment.

## Features

- Upload files or paste text for summarization
- Custom prompts per request
- Saved document history with per-user storage quotas
- Real-time progress updates during processing
- Runs entirely on local hardware

## Tech Stack

**Frontend**
- Next.js
- Mantine (UI components)

**Backend**
- FastAPI
- SQLite (metadata) + local filesystem (file storage)
- Redis (sessions + job progress)
- PyMuPDF / pytesseract (text extraction)

**Inference**
- Single small LLM running on CPU (model TBD)
- llama.cpp with GGUF quantization

**Infrastructure**
- K3s (single-node cluster)
- Caddy (reverse proxy + TLS)

## Architecture

```
[Next.js] ──> [FastAPI] ──> [Worker] ──> [LLM Pod]
                 │              │
                 ├──> [SQLite + Filesystem]
                 └──> [Redis] <──┘
```

1. User uploads a file or submits text with a prompt
2. FastAPI validates the request, stores the file, and queues a job
3. A worker extracts text and forwards it to the LLM pod
4. Progress updates stream through Redis back to the frontend
5. Final summary is returned and saved to the user's history

## Auth

Session-based auth with HttpOnly cookies, backed by Redis. Passwords hashed with Argon2. See `docs/auth.md` for details *(TODO)*.

## Getting Started

*TODO: setup instructions, env vars, and local dev workflow*

## Roadmap

- [ ] Core upload → extract → summarize loop
- [ ] Session auth + user accounts
- [ ] Document history UI
- [ ] Storage quota enforcement
- [ ] K3s deployment manifests
- [ ] TLS via Caddy + Let's Encrypt
- [ ] Model fine-tuning experiments

## License

*TODO*