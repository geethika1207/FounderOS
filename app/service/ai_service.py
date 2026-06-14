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


def get_analysis(idea:str, core_features:list, db_design:dict):
    whole_analysis = f"""
You are FounderOS, an expert startup technical architect.

idea : {idea}
core_features : {core_features}
db_design : {db_design}

Based on the  idea, core_features, db_design tat are  provided , generate the technical planning details.

**STRICT RULE** - Make sure the the endpoints naming must have to match with the tables and fields which are in db_design that i already provided to u .. Make sure the endpoints must have to be based on the db_design that i already provided.
 Return ONLY valid JSON. No extra text. No markdown.

{{
    "endpoints" : <based on the core features list endpoints with the respective HTTP methods for example POST/signup , GET/info list all the endpoints that the project idea requires and respective to  the endpoints also give what two tables and fields in that tables have to join if the endpoint needs to join two tables >
    "roadmap" : <based on the project complexity , design a roadmap day to day realestically to complete the project by the developer >
    "risk_areas": <Identify risk areas SPECIFIC to this exact idea only. Do NOT include generic risks like 'security', 'authentication', 'testing' that apply to every app. Only include risks unique to THIS idea's domain, 
    features, and technical challenges. For example, for an AI platform: prompt injection, AI hallucination in outputs, LLM rate limits. 
    For a marketplace: payment disputes, seller fraud, inventory sync.>
}} 

"""
    raw = ask_groq(whole_analysis)
    return json.loads(raw)