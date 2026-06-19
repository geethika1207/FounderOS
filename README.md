# FounderOS – AI-Powered Backend Architecture Generator

FounderOS is a full-stack AI application that converts a single natural-language startup idea into a complete backend architecture — database schema, REST API design, a phased development roadmap, and domain-specific risk areas — in seconds.

The goal is to compress hours of manual technical planning into an instant, structured blueprint, so founders and developers can move from idea to implementation without first spending a day designing their own backend from scratch.

---

## Live Demo

- 🔗 **Backend:** https://founderos-3ps7.onrender.com
- 🔗 **Frontend:** https://founderos-app.lovable.app
- 📄 **API Docs:** https://founderos-3ps7.onrender.com/docs

---

## Problem Statement

Early-stage technical planning is often a bottleneck for:

- Solo developers who spend hours designing tables, endpoints, and relationships before writing a single line of code.
- Hackathon teams and early-stage builders who need a working architecture fast, not after a full day of planning.
- Engineers who want a sanity-checked starting point — schema, endpoints, and risks — before committing to a design.

Most existing tools either generate a full app with no architectural reasoning, or require the user to already know how to design a backend.

## Solution

FounderOS solves this by allowing users to describe their startup idea in plain English.

The platform analyzes the idea, designs a relational database schema, generates matching REST API endpoints, builds a day-by-day roadmap, and identifies risks specific to that idea's domain — then lets the user ask follow-up questions about the architecture it just generated.

---

## Key Features

### Natural Language Idea Input
Users describe their startup idea in a single sentence, no technical detail required.

### AI-Generated Database Design
Produces relational tables with fields, datatypes, and foreign key relationships based on the idea's core features.

### AI-Generated API Endpoints
Produces REST endpoints with HTTP methods, paths, descriptions, and which tables each endpoint joins — matched exactly to the generated schema.

### Development Roadmap
Breaks the build into phases with day ranges and concrete tasks, giving a realistic implementation timeline.

### Domain-Specific Risk Analysis
Surfaces risks unique to the idea's domain (e.g. payment disputes for marketplaces, HIPAA compliance for healthcare apps) rather than generic boilerplate risks like "add authentication."

### Context-Aware Follow-Up Chat
Users can ask questions about their generated architecture, and the AI responds with full context of the schema, endpoints, roadmap, and risks it already produced — no need to re-explain the idea.

### Analysis History
Every submitted idea and its full architecture is saved and retrievable, with a sidebar of recent analyses and a full history view.

### Secure Authentication
JWT-based authentication with per-user data isolation, ensuring each user only sees their own analyses.

### Response Caching
Identical idea submissions are cached, returning instantly on repeat requests instead of re-calling the LLM.

---

## System Architecture
User Browser (Anywhere in the World)

↓

React Frontend (Lovable — published app)

↓

FastAPI Backend (Render — https://founderos-3ps7.onrender.com)

↓

PostgreSQL Database (Supabase — Managed DB)

↓

Redis Cache (Upstash)

↓

Groq API (Groq Cloud — LLaMA 3.3 70B)

---

## Request Flow
User submits a startup idea

↓

Frontend sends authenticated request to FastAPI

↓

Backend checks Redis cache for an identical idea

↓

If cached → return stored result instantly

↓

If not cached → construct structured prompt

↓

Groq (LLaMA 3.3 70B) generates app type, core features,

target users, and database design

↓

Second structured prompt generates API endpoints,

roadmap, and risk areas — matched to the schema

↓

Combined result is cached in Redis and saved to PostgreSQL

↓

Frontend renders the full architecture view

↓

User can ask follow-up questions via the chat endpoint,

which loads the stored analysis as context for each answer

---

## Tech Stack

### Backend
- FastAPI — API framework
- PostgreSQL — Database (hosted on Supabase)
- SQLAlchemy 1.x — ORM
- Pydantic — Data validation
- JWT (python-jose) — Authentication
- bcrypt (passlib) — Password hashing
- Redis (Upstash) — Response caching
- Groq API (LLaMA 3.3 70B) — AI-powered architecture generation

### Frontend
- React — User interface
- Lovable — Frontend generation and deployment
- Monospace typography for technical content (tables, endpoints, paths)

### AI Layer
- Groq API
- LLaMA 3.3 70B
- Structured JSON prompt engineering with strict schema enforcement

### Deployment
- Frontend: Lovable
- Backend: Render Web Service
- Database: Supabase PostgreSQL
- Cache: Upstash Redis
- Uptime: UptimeRobot (keeps Render's free tier from sleeping)  

---

## Challenges Faced

### 1. Inconsistent LLM Output Structure
The AI sometimes returned endpoints and risk data as a list, sometimes as a dictionary, breaking the frontend. Fixed by enforcing a strict JSON schema in the prompt with explicit example structures.

### 2. Render Free-Tier Cold Starts
Render's free tier sleeps after inactivity, causing fetch and CORS failures on wake-up. Fixed by configuring UptimeRobot to ping the `/docs` endpoint every five minutes.

### 3. Response Schema Drift Between Backend and Frontend
Internal field names (e.g. `risk_factors`) diverged from API response names (`risk_areas`), and some IDs were missing entirely, causing silent rendering failures. Fixed by auditing every Pydantic schema against actual API output.

### 4. Stale Frontend State Across Sessions
Accounts with existing history would sometimes show a previous analysis's data on a new submission. Traced to component state not resetting, fixed by clearing state per request and keying views to the analysis ID.

### 5. Caching Without Breaking Persistence
Redis caching initially caused cache hits to skip the database save. Fixed by separating caching logic from persistence, so every request — cached or not — is still saved with its own ID.

---

## Key Learning Outcomes

- Designing multi-step LLM pipelines with strict structured output validation.
- Building a context-aware AI chat system that reuses prior generation context.
- Designing relational schemas dynamically based on AI-generated specifications.
- Implementing Redis caching alongside persistent storage without data loss.
- JWT authentication with per-user data isolation in a multi-tenant system.
- Production deployment using Render, Supabase, and Upstash.
- Debugging response schema drift between backend and frontend.
- Diagnosing and fixing frontend state bugs that only appear under specific data conditions.
- Coordinating iterative fixes between an AI-generated frontend and a custom FastAPI backend.

## Future Improvements

- Clean REST path naming derived from table names (e.g. `/users` instead of `/users_table`)
- Editable architecture — let users manually adjust generated schema before saving
- Export architecture as a downloadable PDF or Markdown spec
- Multi-idea comparison view
- Architecture versioning and diff view across regenerations
- Team collaboration and shared workspaces

## Author

**Geethika Tammineni**

Aspiring Software Engineer | Backend Development | AI-Powered Applications

Passionate about building scalable software products that leverage data, automation, and artificial intelligence to solve real-world problems.
