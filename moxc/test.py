from mox import parse
from mox.utils import pretty_print

TEST_CARDS = [
    {
        "name": "ED-E, Lonesome Eyebot",
        "type": "Artifact Creature",
        "oracle": "Flying\nED-E My Love — Whenever you attack, if the number of attacking creatures is greater than the number of quest counters on ED-E, Lonesome Eyebot, put a quest counter on it.\n{2}, Sacrifice ED-E: Draw a card, then draw an additional card for each quest counter on ED-E.",
    },
    {
        "name": "Illuminated Wings",
        "type": "Enchantment",
        "oracle": "Enchant creature\nEnchanted creature has flying.\n{2}, Sacrifice this Aura: Draw a card.",
    },
    {
        "name": "Sunspire Gatekeepers",
        "type": "Creature",
        "oracle": "When Sunspire Gatekeepers enters, if you control two or more Gates, create a 2/2 white Knight creature token with vigilance.",
    },
    {
        "name": "Cabal Torturer",
        "type": "Creature",
        "oracle": "{B}, {T}: Target creature gets -1/-1 until end of turn.\nThreshold — {3}{B}{B}, {T}: Target creature gets -2/-2 until end of turn. Activate only if seven or more cards are in your graveyard.",
    },
    {
        "name": "Sauron, Lord of the Rings",
        "type": "Creature",
        "oracle": "When you cast this spell, amass Orcs 5, mill five cards, then return a creature card from your graveyard to the battlefield.\nTrample\nWhenever a commander an opponent controls dies, the Ring tempts you.",
    },
    {
        "name": "Supreme Verdict",
        "type": "Sorcery",
        "oracle": "This spell can't be countered.\nDestroy all creatures.",
    },
    {
        "name": "Final Act",
        "type": "Sorcery",
        "oracle": "Choose one or more —\n• Destroy all creatures.\n• Destroy all planeswalkers.\n• Destroy all battles.\n• Exile all graveyards.\n• Each opponent loses all counters.",
    },
    {
        "name": "Kaya, Intangible Slayer",
        "type": "Planeswalker",
        "oracle": "Hexproof\n+2: Each opponent loses 3 life and you gain 3 life.\n0: You draw two cards. Then each opponent may scry 1.\n−3: Exile target creature or enchantment. If it wasn't an Aura, create a token that's a copy of it, except it's a 1/1 white Spirit creature with flying in addition to its other types.",
    },
    {
        "name": "Serra Angel",
        "type": "Creature",
        "oracle": "Flying\nVigilance",
    },
    {
        "name": "Tephraderm",
        "type": "Creature",
        "oracle": "Whenever a creature deals damage to Tephraderm, Tephraderm deals that much damage to that creature.\nWhenever a spell deals damage to Tephraderm, Tephraderm deals that much damage to that spell's controller.",
    },
    {
        "name": "Prowl, Stoic Strategist",
        "type": "Creature",
        "oracle": "More Than Meets the Eye {2}{W} (You may cast this card converted for {2}{W}.)\nWhenever Prowl attacks, exile up to one other target tapped creature or Vehicle. For as long as that card remains exiled, its owner may play it.\nWhenever a player plays a card exiled with Prowl, you draw a card and convert Prowl.",
    },
    {
        "name": "Bloodchief's Thirst",
        "type": "Sorcery",
        "oracle": "Kicker {2}{B} (You may pay an additional {2}{B} as you cast this spell.)\nDestroy target creature or planeswalker with mana value 2 or less. If this spell was kicked, instead destroy target creature or planeswalker.",
    },
    {
        "name": "Authority of the Consuls",
        "type": "Enchantment",
        "oracle": "Creatures your opponents control enter tapped.\nWhenever a creature an opponent controls enters, you gain 1 life.",
    },
    {
        "name": "Butterbur, Bree Innkeeper",
        "type": "Creature",
        "oracle": "At the beginning of your end step, if you don't control a Food, create a Food token.",
    },
    {
        "name": "Lightning Bolt",
        "type": "Instant",
        "oracle": "Lightning Bolt deals 3 damage to any target.",
    },
    {
        "name": "Fog",
        "type": "Instant",
        "oracle": "Prevent all combat damage that would be dealt this turn.",
    },
    {
        "name": "An Offer You Can't Refuse",
        "type": "Instant",
        "oracle": "Counter target noncreature spell. Its controller creates two Treasure tokens. ",
    },
    {
        "name": "Blood Artist",
        "type": "Creature",
        "oracle": "Whenever this creature or another creature dies, target player loses 1 life and you gain 1 life.",
    },
    {
        "name": "Zimone, Mystery Unraveler",
        "type": "Creature",
        "oracle": "Landfall — Whenever a land you control enters, manifest dread if this is the first time this ability has resolved this turn. Otherwise, you may turn a permanent you control face up. (To manifest dread, look at the top two cards of your library. Put one onto the battlefield face down as a 2/2 creature and the other into your graveyard. Turn it face up any time for its mana cost if it’s a creature card.)",
    },
    {
        "name": "Molten Disaster",
        "type": "Sorcery",
        "oracle": "Kicker {R} (You may pay an additional {R} as you cast this spell.)\nIf this spell was kicked, it has split second. (As long as this spell is on the stack, players can’t cast spells or activate abilities that aren’t mana abilities.)\nMolten Disaster deals X damage to each creature without flying and each player.",
    },
    # {"name": "", "type": "", "oracle": ""},
]


for card in TEST_CARDS:
    print(card["name"])
    print("--")
    print(card["oracle"])
    print("--")

    card = parse(card["oracle"], name=card["name"], type=card["type"])
    pretty_print(card, print_name=False)
