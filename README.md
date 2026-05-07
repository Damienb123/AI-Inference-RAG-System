# AI-Inference-RAG-System

### ***Project in progress***

## Distributed LLM Inference Service

### Overview
A system that accepts AI requests such as chats and RAG queries via APIs, queues incoming requests, distributes work across all workers, and handles retries and failures

### Tech Stack
- FastAPI (API layer)
- Redis / RabbitMQ (queue)
- Worker nodes (python)
- Working integration of Docker

### Features of the system
- Request queueing
- Rate limiting
- Caching responses
- Retry on failure
- Load balancing
