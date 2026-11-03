"""Keep conversational messages independent of screen capture availability."""
import re

def is_greeting(question):
    text=re.sub(r'[^a-z\s]','',question.lower()).strip()
    text=re.sub(r'\s+',' ',text)
    text=re.sub(r'^(hi|hello|hey) (?:chat|copilot|gw2 vlm copilot)$',r'\1',text)
    return text in {'hello','hi','hey','hello waypoint','hi waypoint','good morning','good evening','thanks','thank you','how are you','how are you doing'}

def is_social_message(question):
    """Skip research only when every clause is a greeting or introduction.

    A greeting followed by a factual question must still reach research.
    Personal names and test introductions are not public search terms.
    """
    if is_greeting(question):return True
    clauses=[part.strip() for part in re.split(r'[.!?\n]+',question) if part.strip()]
    if not clauses:return False
    patterns=(
        r"(?:you can call me|call me|my name is) [\w'-]{1,40}(?: [\w'-]{1,40})?",
        r"i(?:'m| am) testing (?:you|your model|this app|the app|this model)(?: (?:for|as) (?:a |an )?(?:gw2|guild wars 2|game|gaming)(?: game)? copilot)?",
    )
    return all(is_greeting(part) or any(re.fullmatch(pattern,part,re.I) for pattern in patterns) for part in clauses)

def needs_screen(question):
    text=question.lower()
    return any(term in text for term in ('screen','screenshot','what do you see','what can you see','what am i looking at','what is shown','what is on','what should i do next','where am i','this enemy','this quest','this objective','my health','my hp','check again','my gold','gold balance','confirm i have'))

def force_new_analysis(question):
    return any(term in question.lower() for term in ('check again','look again','recheck','confirm i have','my gold','gold balance'))


def is_research_request(question):
    return bool(re.search(r"\b(research|look\s+up|search|blish\s*hud|bishhud)\b", question, re.I))
