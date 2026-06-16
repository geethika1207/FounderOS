import os
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
client = Groq(api_key=os.getenv("API_KEY"))

def ask_groq(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    raw = response.choices[0].message.content
    raw = raw.strip()
    if raw.startswith("```json"):
        raw = raw[7:]
    if raw.startswith("```"):
        raw = raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
    return raw.strip()

def get_prompt1(idea: str):
    prompt_1 = f"""
You are FounderOS, a senior startup technical architect with 20+ years of experience.

Your task is to analyze the user's input and respond **strictly** in valid JSON only. Never add explanations, markdown, or extra text.
**CRITICAL INSTRUCTIONS** - Follow exactly:

You will receive a user input inside <IDEA> tags.

If the input is a greeting, casual message, or contains no project intent (e.g. "hello", "hi", "how are you"), then only return:
{{
    "error": "Hey there!  I'm FounderOS. Share your startup idea and I'll generate a complete backend architecture for you!"
}}

1. If the input  has **no clear intent** to build/create/launch any product, app, service, platform, tool, or business idea, respond with:
{{
  "error": ""Please provide more details about your project so I can generate a complete backend architecture for you."
}}

2. **Otherwise**, ALWAYS return the full analysis in this exact JSON format:   
{{
    "app_type": <based on the idea list all categories this app fits into>,
    "core_features": <based on the idea list the main MVP features this app needs>,
    "target_users": <based on the idea and core features list for whom this app is helpful>,
    "db_design": <design tables based on core features, along with the tables also give the related fields and datatype for each table>
}}

idea :
{idea}

"""
    raw = ask_groq(prompt_1)
    return json.loads(raw)


def get_analysis(idea: str, core_features: list, db_design: dict):
    whole_analysis = f"""
You are FounderOS, an expert startup technical architect.

idea: {idea}
core_features: {core_features}
db_design: {db_design}

Based on the idea, core_features, and db_design provided, generate the technical planning details.

STRICT RULES:
- Endpoint names and fields MUST match the tables and fields in db_design exactly.
- Return ONLY valid JSON. No extra text. No markdown. No code blocks.
- Every field below MUST follow the exact structure shown. No deviations.

{{
    "end_points": [
        {{
            "method": "POST",
            "path": "/example",
            "description": "What this endpoint does",
            "tables_joined": ["table1", "table2"]
        }}
    ],
    "roadmap": [
        {{
            "phase": "Phase 1",
            "days": "Day 1-3",
            "tasks": ["task 1", "task 2"]
        }}
    ],
    "risk_areas": [
        {{
            "area": "Name of risk",
            "description": "Why it is risky for THIS specific idea"
        }}
    ]
}}

Generate real values following this exact structure for the given idea.
Only include risks unique to this idea's domain. Do NOT include generic risks like security or authentication.
"""
    raw = ask_groq(whole_analysis)
    return json.loads(raw)