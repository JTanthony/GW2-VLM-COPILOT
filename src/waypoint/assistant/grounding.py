"""Conservative numeric-screen grounding; cannot prove OCR itself is correct."""
import re
from waypoint.integrations.game_rules import invalid_character_level

def gold_reading(observation,question,age):
    if not re.search(r'(?i)\bgold\b',question) or not re.search(r'(?i)my gold|gold balance|confirm.*gold|how much.*gold|check.*gold',question): return None
    readings=[]
    for text in observation.get('visible_text',[]):
        for pattern in (r'(?i)\b([\d,]+)\s+gold\b',r'(?i)\bgold\s*:\s*([\d,]+)\b'):
            readings.extend(re.findall(pattern,text))
    readings=set(readings)
    if len(readings)!=1:
        return "I can't reliably read your gold balance in this frame. Open the inventory or wallet so the currency is clearly visible, then ask me to check again."
    value=readings.pop()
    return f'The analyzed frame reads {value} gold (captured {age:.0f} seconds ago). This is a visual reading, not an account API confirmation.'

def guard_screen_stats(answer,observation,window_title):
    # Numeric personal stats must have matching numeric evidence in visible_text.
    evidence=' '.join(observation.get('visible_text',[]))
    stats=re.findall(r'(?i)\b(?:level|lvl)\s*:?\s*(\d+)|\b(\d+(?:\.\d+)?)\s*%\s*(?:hp|health|mana)|\b(\d+(?:\.\d+)?)\s+gold\b',answer)
    for groups in stats:
        value=next(x for x in groups if x)
        if not re.search(r'(?<![\d.])'+re.escape(value)+r'(?![\d.])',evidence):
            return "I can't verify those numeric screen readings from the visible text, so I won't present them as confirmed."
    return invalid_character_level(answer,window_title) or answer
