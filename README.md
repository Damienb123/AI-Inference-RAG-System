# Distributed LLM Inference Service
### ***Project in progress***
## Overview
A system that accepts AI requests via APIs such as chats and RAG queries, queues them, distributes work across all workers, and handles retries and failures

## Tech Stack
- FastAPI (API layer)
- Redis / RabbitMQ (queue)
- Worker nodes (Python)
- Current integration with Docker


## Features of the system
- Request queueing
- Rate limiting
- caching responses
- retry on failure
- load balancing
