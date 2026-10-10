"""Verified official API candidates; availability is distinct from an implemented connector."""
PUBLIC_APIS={
    'Guild Wars 2':{'aliases':('gw2',),'source':'https://wiki.guildwars2.com/wiki/API:Main',
        'requirements':'Available in Waypoint. API key permissions: account + progression.'},
    'World of Warcraft':{'aliases':('wow','wow retail','world of warcraft retail'),
        'source':'https://community.developer.battle.net/documentation/world-of-warcraft',
        'requirements':'Official Battle.net game-data/profile APIs exist. Battle.net authorization and a Waypoint adapter are required before connecting. Not enabled yet.'},
    'World of Warcraft Classic':{'aliases':('wow classic',),
        'source':'https://community.developer.battle.net/documentation/world-of-warcraft-classic',
        'requirements':'Official Classic game-data APIs exist. This does not confirm private account-progress coverage. Battle.net setup and a Waypoint adapter are required. Not enabled yet.'},
    'Old School RuneScape':{'aliases':('osrs','old school runescape'),
        'source':'https://secure.runescape.com/m=hiscore_oldschool/',
        'requirements':'Official public Hiscores can be looked up by player name; no API token is needed. Hiscores do not provide a complete quest/achievement checklist. A Waypoint adapter is not enabled yet.'},
    'Path of Exile':{'aliases':('poe','poe 1','path of exile 1'),
        'source':'https://www.pathofexile.com/developer/docs',
        'requirements':'Official read-only APIs use registered-app OAuth. New application registrations are currently closed. A registered Waypoint application and adapter are required. Not enabled yet.'},
    'Path of Exile 2':{'aliases':('poe2','poe 2'),
        'source':'https://www.pathofexile.com/developer/docs/reference',
        'requirements':'Official APIs include PoE2 resources, with different coverage from PoE1. Registered-app OAuth is required and new registrations are currently closed. Not enabled yet.'}
}
