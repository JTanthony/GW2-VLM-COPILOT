"""Keep conversational messages independent of screen capture availability."""
import re

def is_greeting(question):
    text=re.sub(r'[^a-z\s]','',question.lower()).strip()
    return text in {'hello','hi','hey','hello waypoint','hi waypoint','good morning','good evening','thanks','thank you','how are you','how are you doing'}

def needs_screen(question):
    text=question.lower()
    return any(term in text for term in ('screen','screenshot','what do you see','what can you see','what am i looking at','what is shown','what is on','what should i do next','where am i','this enemy','this quest','this objective','my health','my hp','check again','my gold','gold balance','confirm i have'))

def force_new_analysis(question):
    return any(term in question.lower() for term in ('check again','look again','recheck','confirm i have','my gold','gold balance'))


def is_research_request(question):
    return bool(re.search(r"\b(research|look\s+up|search|blish\s*hud|bishhud)\b", question, re.I))
