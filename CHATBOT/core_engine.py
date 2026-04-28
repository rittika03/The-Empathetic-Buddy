import os
import json
import re
import chromadb
from groq import Groq

# OVERRIDING EVERYTHING: Hardcoding the Groq key
GROQ_API_KEY = ""
client = Groq(api_key=GROQ_API_KEY)

# Using Llama 3 8B: Explicitly approved by OpenAImer Track B Rules, ultra-fast, massive daily quota.
LLM_MODEL = 'llama-3.1-8b-instant'

# Local DB Setup (Using Chroma's built-in ONNX model)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

try:
    collection = chroma_client.get_collection(name="clinical_frameworks")
except:
    collection = chroma_client.create_collection(name="clinical_frameworks")
    # Pre-seed with basic frameworks for the demo
    frameworks = [
        "CBT: For all-or-nothing thinking, challenge absolutes. Ask for exceptions.",
        "DBT: For numbness, use grounding techniques like 5-4-3-2-1 sensory awareness.",
        "Validation: For help-rejecting complaining, avoid giving advice. Focus entirely on validating the frustration."
    ]
    collection.add(ids=["1", "2", "3"], documents=frameworks)

# Safety Guardrails
CRISIS_KEYWORDS = r"\b(suicide|kill myself|end it all|want to die|don't want to live anymore)\b"

def run_safety_check(message):
    if re.search(CRISIS_KEYWORDS, message.lower()):
        return True, "I'm so sorry you're feeling this way. Please know you aren't alone. Please reach out to a crisis hotline immediately."
    return False, ""

def extract_state(message, history, profile):
    prompt = f"""
    Analyze the user's latest message. Return ONLY valid JSON matching this exact schema. Do not include any preamble or markdown formatting.
    History: {history}
    Profile: {profile}
    Message: {message}
    Schema: {{"primary_state":"", "cognitive_pattern":"", "defense_mechanism":"", "risk_level":"", "intent":"", "extracted_entities":[]}}
    """
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            response_format={"type": "json_object"} # THIS FORCES STRICT JSON
        )
        raw_text = response.choices[0].message.content
        return json.loads(raw_text)
       
    except Exception as e:
        # If it fails, print the actual error to your terminal so you can see it!
        print(f"\n JSON EXTRACTION ERROR: {e}")
        return {"primary_state": "distressed", "cognitive_pattern": "unknown", "risk_level": "low", "extracted_entities": []}

def retrieve_framework(query):
    results = collection.query(query_texts=[query], n_results=1)
    return results['documents'][0][0] if results['documents'] else ""

def update_profile(profile, extracted_entities):
    for entity in extracted_entities:
        if entity not in profile['stressors']:
            profile['stressors'].append(entity)
    return profile

def generate_response(state, profile, framework, history, message):
    prompt = f"""
    You are an expert, highly perceptive clinical psychologist AI. Your goal is to uncover implicit distress and guide the user, mirroring the tone of a professional therapist.

    CRITICAL INSTRUCTIONS TO BEAT THE "SYMPATHY PARROT" TRAP:
    1. DO NOT simply repeat or summarize what the user just said.
    2. DO NOT use overly dramatic sympathy adjectives (e.g., "That sounds incredibly tough", "That is profoundly difficult"). It sounds robotic and fake.
    3. BE CONCISE. Keep your response to 2-4 sentences maximum.
    4. MAKE CONNECTIONS: If the user mentions multiple stressors, connect them to find the underlying psychological weight.
    5. THE CLINICAL PIVOT: End your response with exactly ONE sharp, probing question that forces the user to think about the root cause of their feeling, NOT just the symptom.
    6. ACTIONABILITY: If the user explicitly asks "What can I do?", do not give platitudes. Use the provided Clinical Framework to give one immediate, micro-actionable coping strategy.
   
    SYSTEM TELEMETRY (DO NOT OUTPUT THIS IN THE CHAT):
    State: {json.dumps(state)}
    Profile: {json.dumps(profile)}
    Framework: {framework}
    History: {history}
    """
   
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": message}
        ],
        temperature=0.6
    )
    return response.choices[0].message.content