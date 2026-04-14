import os
import json
from google import genai
from google.genai import types

# Load Knowledge Base Data once
try:
    kb_path = os.path.join(os.path.dirname(__file__), 'knowledge_base.json')
    with open(kb_path, 'r', encoding='utf-8') as f:
        AUTHOR_KNOWLEDGE_BASE = json.load(f)
except Exception:
    AUTHOR_KNOWLEDGE_BASE = {}

def get_ai_client():
    # Load from environment variables (secured in backend/.env)
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        return None

def process_new_ticket(ticket_description, author_email=None):
    """
    Returns a dictionary with:
    - category
    - priority
    - draft_response
    """
    client = get_ai_client()
    
    # Cost Optimization: Only extract the specific author's data to save tokens!
    specific_author_context = "No specific author data found in KB."
    if author_email and isinstance(AUTHOR_KNOWLEDGE_BASE, dict):
        authors = AUTHOR_KNOWLEDGE_BASE.get("authors", [])
        for a in authors:
            if a.get('email') == author_email:
                specific_author_context = json.dumps(a, indent=2)
                break
    
    # Fallback response
    result = {
        "category": "General",
        "priority": "Medium",
        "draft_response": "Write manually. (AI Service unavailable)"
    }
    
    if not client:
        return result

    prompt = f"""
    SYSTEM PROMPT:
    You are a BookLeaf Publishing support assistant.
    Be professional, empathetic, and specific.
    Always provide clear next steps.
    Do not give generic answers.
    
    CONTEXT (Author Database):
    Here are the specific details of the author raising this ticket. Use this data to accurately answer any questions regarding their royalties, copies sold, ISBNs, book status, etc.
    {specific_author_context}
    
    TASK: Analyze the following ticket description and provide:
    1. Category (Choose from: Royalty & Payments, ISBN & Metadata Issues, Printing & Quality, Distribution & Availability, Book Status & Production Updates, General Inquiry)
    2. Priority (Choose from: Critical, High, Medium, Low)
    3. Draft Response (A professional reply to the user)
    
    Format the output EXACTLY as follows (3 lines):
    CATEGORY: [category]
    PRIORITY: [priority]
    RESPONSE: [response]
    
    USER INPUT (Ticket Description - Truncated to save tokens):
    {ticket_description[:1000]}
    """
    
    import re
    # Try models in order — most capable to most available
    for model_name in ['gemini-2.0-flash', 'gemini-2.0-flash-lite', 'gemini-1.5-flash']:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            text = response.text.strip()

            # Robustly parse Category
            cat_match = re.search(r'\*?\*?CATEGORY:\*?\*?\s*(.*)', text, re.IGNORECASE)
            if cat_match:
                result['category'] = cat_match.group(1).strip()

            # Robustly parse Priority
            pri_match = re.search(r'\*?\*?PRIORITY:\*?\*?\s*(.*)', text, re.IGNORECASE)
            if pri_match:
                result['priority'] = pri_match.group(1).strip()

            # Robustly parse Response (capture everything after RESPONSE:)
            res_match = re.search(r'\*?\*?RESPONSE:\*?\*?\s*(.*)', text, re.IGNORECASE | re.DOTALL)
            if res_match:
                result['draft_response'] = res_match.group(1).strip()

            print(f"AI processed ticket successfully using model: {model_name}")
            break  # Success — stop trying other models

        except Exception as e:
            print(f"Error with model {model_name}: {e}")
            continue  # Try next model
        
    return result
