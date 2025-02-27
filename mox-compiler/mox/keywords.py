import re

# fmt: off
keywords = [
    # A
    "Absorb", "Affinity", "Afflict", "Afterlife",
    "Aftermath", "Amplify", "Annihilator", "Ascend",
    "Assist", "Aura swap", "Awaken",

    # B
    "Backup", "Banding", "Bargain", "Battle cry",
    "Bestow", "Blitz", "Bloodthirst", "Boast",
    "Bushido", "Buyback",

    # C
    "Cascade", "Casualty", "Champion", "Changeling",
    "Cipher", "Cleave", "Companion", "Compleated",
    "Conspire", "Convoke", "Craft", "Crew",
    "Cumulative upkeep", "Cycling",

    # D
    "Dash", "Daybound", "Deathtouch", "Decayed",
    "Defender", "Delve", "Demonstrate", "Dethrone",
    "Devoid", "Devour", "Disguise", "Disturb",
    "Double strike", "Dredge",

    # E
    "Echo", "Embalm", "Emerge", "Enchant",
    "Encore", "Enlist", "Entwine", "Epic",
    "Equip", "Escalate", "Escape", "Eternalize",
    "Evoke", "Evolve", "Exalted", "Exploit", "Extort",

    # F
    "Fabricate", "Fading", "Fear", "First strike",
    "Flanking", "Flash", "Flashback", "Flying",
    "For Mirrodin!", "Forecast", "Foretell", "Fortify",
    "Freerunning", "Frenzy", "Fuse",

    # G
    "Gift", "Graft", "Gravestorm",

    # H
    "Haste", "Haunt", "Hexproof", "Hidden agenda",
    "Hideaway", "Horsemanship",

    # I
    "Improvise", "Indestructible", "Infect", "Ingest", "Intimidate",

    # J
    "Jump-start",

    # K
    "Kicker",

    # L
    "Landwalk", "Level up", "Lifelink", "Living metal", "Living weapon",

    # M
    "Madness", "Melee", "Menace", "Mentor",
    "Miracle", "Modular", "More Than Meets the Eye",
    "Morph", "Mutate", "Myriad",

    # N
    "Nightbound", "Ninjutsu",

    # O
    "Offering", "Offspring", "Outlast", "Overload",

    # P
    "Partner", "Persist", "Phasing", "Plot",
    "Poisonous", "Protection", "Prototype", "Provoke",
    "Prowess", "Prowl",

    # R
    "Rampage", "Ravenous", "Reach", "Read ahead",
    "Rebound", "Reconfigure", "Recover", "Reinforce",
    "Renown", "Replicate", "Retrace", "Riot", "Ripple",

    # S
    "Saddle", "Scavenge", "Shadow", "Shroud",
    "Skulk", "Solved", "Soulbond", "Soulshift",
    "Space sculptor", "Spectacle", "Splice", "Split second",
    "Spree", "Squad", "Storm", "Sunburst",
    "Surge", "Suspend",

    # T
    "Toxic", "Training", "Trample", "Transfigure",
    "Transmute", "Tribute",

    # U
    "Umbra armor", "Undaunted", "Undying", "Unearth",
    "Unleash", "Vanishing",

    # V
    "Vigilance", "Visit",

    # W
    "Ward", "Wither"
]
# fmt: on

KEYWORDS = re.compile(r"\b|".join((r"\b" + k) for k in keywords), re.IGNORECASE)
