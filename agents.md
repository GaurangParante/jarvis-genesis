# JARVIS Genesis Agents

## Purpose

This file defines the agent map for the project.
Each agent should have a narrow job so the system can combine them intelligently.

## Agent Design Rules

- One agent should own one clear domain
- Agents should not overlap too much
- Each agent should have a capability list
- Each agent should have example tasks
- Each agent should have safety boundaries

## Agent List

### 1. FORGE

Role:
- coding and software engineering agent

Best for:
- writing code
- fixing bugs
- generating scripts
- creating project files
- API work
- database work

Capabilities:
- python
- fastapi
- flask
- laravel
- javascript
- sql
- debugging
- project creation
- automation scripts

Example tasks:
- create a Python script
- fix a bug in my app
- build a FastAPI endpoint
- generate a database schema

### 2. ORBIT

Role:
- desktop automation and system control agent

Best for:
- opening apps
- file browsing
- screenshots
- webcam capture
- screen recording
- OS-level actions

Capabilities:
- application control
- browser opening
- file management
- folder management
- screenshot
- webcam
- screen recording
- desktop control

Example tasks:
- open VS Code
- take a screenshot
- record the screen
- open downloads folder

### 3. PHANTOM

Role:
- research and analysis agent

Best for:
- internet research
- trend analysis
- competitor analysis
- topic discovery
- general investigation

Capabilities:
- research
- analysis
- summarization
- trend detection
- comparison

Example tasks:
- find trending YouTube topics
- compare two products
- research a technology stack

### 4. APOLLO

Role:
- YouTube content and growth agent

Best for:
- YouTube scripts
- SEO
- titles
- descriptions
- content ideas
- channel strategy

Capabilities:
- YouTube
- SEO
- script writing
- content planning
- analytics

Example tasks:
- create a YouTube script
- generate a title
- write a description
- suggest thumbnail text

### 5. NOVA

Role:
- social media content and posting agent

Best for:
- social posts
- captions
- post ideas
- engagement content
- platform-specific copy

Capabilities:
- Instagram
- LinkedIn
- Twitter/X
- Facebook
- short-form content

Example tasks:
- write a LinkedIn post
- create an Instagram caption
- draft a Twitter thread

### 6. MERCURY

Role:
- email and communication agent

Best for:
- drafting emails
- replying to messages
- organizing communication tasks
- outreach workflows

Capabilities:
- email drafting
- reply generation
- inbox workflows
- communication planning

Example tasks:
- write a reply to this email
- draft an outreach email
- prepare a follow-up message

### 7. ARCHIVE

Role:
- knowledge base and document agent

Best for:
- storing notes
- retrieving documents
- managing knowledge
- working with PDFs or saved references

Capabilities:
- document handling
- note organization
- retrieval
- knowledge storage

Example tasks:
- save this reference
- find my notes on project planning
- summarize this document

### 8. TITAN

Role:
- finance and budgeting agent

Best for:
- expenses
- budgets
- financial summaries
- personal money tracking

Capabilities:
- finance
- budgeting
- expense tracking
- reporting

Example tasks:
- analyze my expenses
- make a budget summary
- track my spending

### 9. ATHENA

Role:
- fitness and wellness agent

Best for:
- workout plans
- diet guidance
- calorie tracking
- healthy routines

Capabilities:
- fitness
- diet
- workout planning
- habit support

Example tasks:
- make me a workout plan
- suggest a diet routine
- help me track calories

### 10. SENTINEL

Role:
- security and protection agent

Best for:
- passwords
- login alerts
- security checks
- sensitive account monitoring

Capabilities:
- security
- password alerts
- account safety
- login monitoring

Example tasks:
- check security on this account
- alert me about suspicious login
- help me manage account safety

## How Agents Should Work Together

Single-agent examples:
- FORGE for coding
- ORBIT for desktop actions
- APOLLO for YouTube writing

Multi-agent examples:
- research topic with PHANTOM
- write script with APOLLO
- upload or navigate with ORBIT

- build code with FORGE
- research library with PHANTOM
- run system setup with ORBIT

- prepare social content with NOVA
- verify account safety with SENTINEL
- send email with MERCURY

## Agent Selection Rules

- If the task is coding, choose FORGE
- If the task is desktop control, choose ORBIT
- If the task is research, choose PHANTOM
- If the task is YouTube, choose APOLLO
- If the task is social media, choose NOVA
- If the task is email, choose MERCURY
- If the task is knowledge storage, choose ARCHIVE
- If the task is finance, choose TITAN
- If the task is fitness, choose ATHENA
- If the task is security, choose SENTINEL

## Expansion Rule

When a request is bigger than one agent:
- split it into subtasks
- assign each subtask to the right agent
- run them in sequence or parallel
- merge the results

## Safety Rule for Agents

Agents must not bypass human approval when the task involves:
- passwords
- logins
- account creation
- public posting
- deletions
- payment actions
- security-sensitive changes

