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

DEFAULT_REWARDS = {
    ENTITIES['bomb']: -6,
    ENTITIES['blast']: -8,
    ENTITIES['ammo']: 20,
    ENTITIES['powerup']: 15,
    # avoid walls
    ENTITIES['metal']: -10,
    ENTITIES['ore']: -10,
    ENTITIES['wood']: -10,

    # special rewards
    'enemy': -2,
    'pinch': -2,  # articulation point
    'wall': -10
}
