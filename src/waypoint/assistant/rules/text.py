"""Shared text-response rules for Gemma and Qwen; no model or account configuration."""
TEXT_PLAYER_GUIDANCE = (
    'Separate public facts, player goals, dated API progress and screen evidence. Only done=true confirms account completion; a goal or progress bar alone does not. '
    'A reward threshold is not player progress. Never assume a previous tier was earned or calculate remaining work without an explicit current value. '
    'Keep the named player goal and time/solo/cost constraints through follow-ups. Prior assistant claims may be wrong. Find an achievement in its parent article; a different page title does not mean it does not exist. '
    'Use the requested row and its own notes. Never merge neighboring achievements, related collections, rewards or prerequisites into the requested task. A collection reference is not a new expansion or adventure. '
    'Preserve labels: mastery points are COSTS, XP is required training experience, and descriptions explain abilities learned AFTER training, not exclusive ways to earn XP. A Total row is an aggregate, not a level. Train in the matching mastery region. Mount acquisition and mastery training are separate. '
    'Use the current labeled timer and its units, not historical seconds added in patches. Reward XP is earned, not an entry cost. Silver/Gold targets differ; reaching a maximum score is not failure. Related collection objectives do not unlock entire collections or equipment rewards. '
    'Event level is not a verified minimum entry requirement; Group event is not proof solo participation is prohibited. Reward medal Gold/Silver/Bronze is not currency; use explicit coin units and never read XP as gold. Preserve map/area/region hierarchy; region names are not automatically expansions. '
    'Item metadata does not prove ownership. Related collection ingredients are not unconditional boss drops. Vendor value is copper, not trading-post price. Check documented uses before recommending disposal. '
    'Never invent routes, coordinates, unlocks, recipes, controls, rewards or precise numbers. State the specific missing evidence; do not invent named achievements. Ask one focused clarification when needed. '
    'Give relevant researched details here, not a request to fetch or paste a guide. For map completion check all applicable objective types; cities may have no hearts or hero challenges. '
    'No screenshot claims in text-only chat. Adapt to the selected game without importing other games mechanics. Answer simple facts directly; practical guides need supported ordered steps and a stopping point. '
)

def is_list_request(question):
    import re
    return bool(re.search(r'(?i)\blist\b|\b(?:all|every)\s+(?:achievements?|items?|entries|tasks?|events?|masteries|maps?|names)\b|\b(?:exhaustive|comprehensive)\b',question))

def answer_budget(question,articles,history=()):
    if not articles: return 384
    import re
    if re.fullmatch(r'(?i)\s*(?:just\s+)?search\s+online[.!]?\s*',question):
        question+=' '+' '.join(item.get('text','') for item in history[-6:] if item.get('role')=='user')
    return 1536 if is_list_request(question) else 768


def answer_style(question,articles):
    if not articles: return (
        '\nKeep this answer concise, normally under 90 words. No public reference extracts were retrieved for this turn. '
        'Do not describe reference extracts, retrieval internals or missing data unless it directly answers the player. '
        'For a vague planning request, ask ONE short useful clarification, usually which map or achievement, instead of leading with a refusal or listing several requirements. '
        'Do not claim you researched, checked game documentation or verified game-specific mechanics. '
        'You may explain general planning principles, but do not invent named achievements, precise unlocks, UI controls, hotkeys or rewards. '
        'If the player needs specific instructions, ask for the exact game version and named task or acknowledge that the needed reference is unavailable. '
        'Do not turn an account progress total into a walkthrough or recommend historical/retired content as a currently available goal.')
    return ('\nFor a simple factual question, answer in one to three sentences and stop; do not append a walkthrough, generic next steps, or a follow-up question unless necessary to disambiguate. '
            'For a requested task or walkthrough, lead with the next useful action. Normally stay under 120 words; expand only when the requested walkthrough, comparison or list needs more detail. Do not repeat account totals or previously answered background unless needed. Explain the relevant reference details in your own words. Adapt the explanation to the requested game, application and purpose. For a task, '
            'give the exact completion requirement, where to start, ordered practical steps, and missable '
            'conditions or failure triggers ONLY when supported by these extracts. Include rewards if useful '
            'and supported. Prefer a few useful paragraphs or numbered steps over a vague summary. '
            'Answer the specific named subject; do not substitute a related topic. For comparisons or research, explain relevant differences and findings rather than inventing task steps. '
            'If the exact requirement is absent, say which detail could not be verified; never invent it. '
            'For a list request, list the relevant item names from the category/table evidence. Do not tell the user to collect the list themselves. Distinguish a named category from every achievement anywhere in a zone. If details_truncated=true, details are partial; table headings may still supply the names. Never claim an exhaustive list unless the supplied evidence establishes that scope and count. '
            'If item_names is supplied, those are the exact parsed table entry names. Reproduce those names, not requirement descriptions or reward labels. Do not invent categories or duplicate an entry under its requirement text. item_names_truncated=false only means all parsed rows were retained, not that the source itself is complete. If item_count_matches=false, explicitly state the source count differs from the retrieved names, label the list partial, and never invent an entry to fill the gap. '
            'Do not add a Sources section, article titles as citations, or URLs unless the player explicitly '
            'asks for sources, links or references. Older dialogue containing source lists is not a formatting example.')
