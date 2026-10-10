"""Optional game-specific checks; shared screen reasoning has no default game."""
import re

def invalid_character_level(answer,window_title):
    if re.search(r'(?i)\bgw2\b|guild wars 2',window_title):
        for level in re.findall(r'(?i)\b(?:you are(?: currently)?|your (?:current )?level is)\s+(?:level\s*)?(\d+)',answer):
            if int(level)>80:
                return "The model returned an invalid GW2 character level. I can't trust this screen reading; please ask me to check again."
    return None
