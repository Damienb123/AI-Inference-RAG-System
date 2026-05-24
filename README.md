# Distributed LLM Inference + RAG System

A distributed AI inference platform built with FastAPI, Redis, RQ workers, and OpenAI APIs.  
The system processes asynchronous AI requests, distributes workloads across worker nodes, and supports scalable Retrieval-Augmented Generation (RAG) pipelines.

## Project Status

Current Development Phase:
- [x] FastAPI API layer
- [x] Redis queue integration
- [x] Distributed RQ worker system
- [x] OpenAI LLM integration
- [ ] Pinecone vector database integration
- [ ] RAG retrieval pipeline
- [ ] Response caching layer
- [ ] Docker multi-service deployment
- [ ] AWS deployment
- [ ] Load balancing + horizontal worker scaling

## System Overview

The platform accepts AI inference requests through a FastAPI API layer and asynchronously distributes workloads to background worker processes through Redis queues.

The architecture is designed to simulate production-grade AI infrastructure patterns including:
- distributed task processing
- asynchronous inference pipelines
- fault-tolerant worker systems
- Retrieval-Augmented Generation (RAG)
- scalable vector retrieval
- response caching

## Project Goals

This project was designed to explore distributed systems engineering patterns commonly used in modern AI infrastructure platforms.

The primary goal is to simulate scalable LLM inference pipelines that separate:
- API orchestration
- asynchronous task execution
- vector retrieval
- model inference
- caching and fault tolerance

The architecture draws inspiration from real-world AI platform systems used in large-scale SaaS and AI companies.

## Tech Stack

### Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-4B8BBE?style=for-the-badge)

### Distributed Systems
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![RQ](https://img.shields.io/badge/RQ-Queue_Workers-red?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

### AI / LLM
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Pinecone](https://img.shields.io/badge/Pinecone-14B8A6?style=for-the-badge)
![RAG](https://img.shields.io/badge/RAG-Retrieval_Augmented_Generation-orange?style=for-the-badge)

### Infrastructure
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)

### Future Enhancements
![Load Balancing](https://img.shields.io/badge/Load_Balancing-Scaling-blue?style=for-the-badge)
![Caching](https://img.shields.io/badge/Caching-Redis-green?style=for-the-badge)
![Fault Tolerance](https://img.shields.io/badge/Fault_Tolerance-Retries-red?style=for-the-badge)
![Observability](https://img.shields.io/badge/Observability-Monitoring-purple?style=for-the-badge)


## Current Features

- Asynchronous AI request processing
- Distributed worker architecture
- Redis-backed job queues
- OpenAI-powered inference generation
- Fault-tolerant task execution
- Background job processing
- Modular service-oriented architecture

## Planned Features

- Vector similarity search with Pinecone
- Retrieval-Augmented Generation (RAG)
- Distributed caching layer
- Load balancing
- Worker autoscaling
- Request tracing + observability
- Rate limiting
- Retry + dead-letter queue support
