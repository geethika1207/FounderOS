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

def chat_prompt(question:str, idea:str, analysis:dict):
    prompt = f"""
You are FounderOS, an expert startup technical architect.

analysis : 
{analysis}

idea:
{idea}

Based on the provided analysis answer the given question 

**STRICT RULE** - 
You are an expert startup advisor. You have been given a full backend 
architecture analysis for a specific startup idea.

Only answer questions related to this analysis.

- If the user sends a greeting or thank you, respond warmly and briefly.
- If the question is completley unrelated to the analysis, idea  , then only return : 
   {{"error" : "Can you be more specific? I can only answer questions related to your analysis."}}   

- If the question has **clear intent** to build/create/launch any product, app, service, platform, tool, or business idea, then only return:
    {{"error" : "It looks like you have a new idea! Please start a new analysis to get a complete architecture breakdown."}} 

**IMPORTANT** - Base your answers on the provided analysis for the questions that are related to analysis and also answer to the questions that somehow related to the provided idea above for eg: TechStack something that related to the project idea 
Reference specific tables, endpoints, and features from the analysis for the questions that are related to analysis in your response. 
When user asks you to recommend something , understand about the idea and analysis that are provided and reccommend a simpler way that user can follow to build the idea .. dont give generic recommendations that almost applicable to any project .
for eg : user asks to recommend techstack then tell them the simpler way ...

OTHERWISE return in the exact json format . NO EXTRA TEXT. NO MARKDOWN

{{
    "answer" : <Give your answer here>
}}

question : {question}

"""
    raw= ask_groq(prompt)
    return json.loads(raw)