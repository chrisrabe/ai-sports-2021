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
MAX_STARE_CONTEST_DURATION = 50  # 50 ticks to eyeball opponent

ENTITIES = {
    'ammo': 'a',
    'bomb': 'b',
    'blast': 'x',
    'powerup': 'bp',
    'metal': 'm',
    'ore': 'o',
    'wood': 'w',
    'player': 'p',
    'enemy': 'e',
    'enemy_on_bomb': 'eb',
    'player_on_bomb': 'pb'
}

BLOCKAGES = [
    ENTITIES['bomb'],
    ENTITIES['metal'],
    ENTITIES['ore'],
    ENTITIES['wood'],
    ENTITIES['player'],
    ENTITIES['player_on_bomb'],
    ENTITIES['enemy'],
    ENTITIES['enemy_on_bomb']
]

DEFAULT_REWARDS = {
    ENTITIES['bomb']: -6,
    ENTITIES['blast']: -8,
    ENTITIES['ammo']: 20,
    ENTITIES['powerup']: 15,
    # avoid walls
    ENTITIES['metal']: -10,
    ENTITIES['ore']: -10,
    ENTITIES['wood']: -10,
    ENTITIES['player']: 0,
    ENTITIES['enemy']: 0,
    ENTITIES['player_on_bomb']: -20,  # avoid
    ENTITIES['enemy_on_bomb']: 30,  # yes
    # special rewards
    'enemy': -2,
    'pinch': -2,  # articulation point
    'wall': -10,
    'destructibles_plant': 1,
    'hazard_zone': -10,
}
