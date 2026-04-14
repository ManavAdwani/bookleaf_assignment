import os
import json
import re

# Load Knowledge Base Data once
try:
    kb_path = os.path.join(os.path.dirname(__file__), 'knowledge_base.json')
    with open(kb_path, 'r', encoding='utf-8') as f:
        AUTHOR_KNOWLEDGE_BASE = json.load(f)
except Exception:
    AUTHOR_KNOWLEDGE_BASE = {}


def get_ai_client():
    """Returns a Groq client if API key is available, else None."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("GROQ_API_KEY not set.")
        return None
    try:
        from groq import Groq
        return Groq(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Groq client: {e}")
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

    # Fallback response if AI unavailable
    result = {
        "category": "General",
        "priority": "Medium",
        "draft_response": "Write manually. (AI Service unavailable)"
    }

    if not client:
        return result

    prompt = f"""You are a BookLeaf Publishing support assistant.
Be professional, empathetic, and specific. Always provide clear next steps.

AUTHOR DATA (use this to answer questions about royalties, books, ISBNs, status):
{specific_author_context}

Analyze the following support ticket and respond EXACTLY in this format (3 lines, no extra text):
CATEGORY: [choose one: Royalty & Payments, ISBN & Metadata Issues, Printing & Quality, Distribution & Availability, Book Status & Production Updates, General Inquiry]
PRIORITY: [choose one: Critical, High, Medium, Low]
RESPONSE: [professional reply to the author using their actual data]

TICKET:
{ticket_description[:1000]}"""

    # Try models in order
    models = ['llama3-70b-8192', 'llama3-8b-8192', 'mixtral-8x7b-32768', 'gemma2-9b-it']

    for model_name in models:
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model_name,
                temperature=0.4,
                max_tokens=1024,
            )
            text = chat_completion.choices[0].message.content.strip()

            # Parse Category
            cat_match = re.search(r'\*?\*?CATEGORY:\*?\*?\s*(.*)', text, re.IGNORECASE)
            if cat_match:
                result['category'] = cat_match.group(1).strip()

            # Parse Priority
            pri_match = re.search(r'\*?\*?PRIORITY:\*?\*?\s*(.*)', text, re.IGNORECASE)
            if pri_match:
                result['priority'] = pri_match.group(1).strip()

            # Parse Response (everything after RESPONSE:)
            res_match = re.search(r'\*?\*?RESPONSE:\*?\*?\s*(.*)', text, re.IGNORECASE | re.DOTALL)
            if res_match:
                result['draft_response'] = res_match.group(1).strip()

            print(f"AI processed ticket successfully using model: {model_name}")
            break  # Success — stop trying other models

        except Exception as e:
            print(f"Error with model {model_name}: {e}")
            continue

    return result
