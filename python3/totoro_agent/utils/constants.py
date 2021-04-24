ACTIONS = {
    "up": "up",
    "down": "down",
    "left": "left",
    "right": "right",
    "bomb": "bomb",
    "detonate": "detonate",
    "none": ""
}

ACTION_LIST = list(ACTIONS.values())

BOMB_DURATION = 40  # 40 ticks
INVULNERABILITY_DURATION = 5
FIRE_START_TICK = 1800  # when fire starts

ENTITIES = {
    'ammo': 'a',
    'bomb': 'b',
    'blast': 'x',
    'powerup': 'bp',
    'metal': 'm',
    'ore': 'o',
    'wood': 'w'
}