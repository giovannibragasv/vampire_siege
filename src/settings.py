import pygame

TITLE = "Vampire Siege"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# --- Master palette (Castlevania/Stardew gothic) ---
C_VOID       = (13,   0,  16)
C_DARK_PURPLE= (26,   5,  48)
C_BLOOD_DARK = (92,   0,   0)
C_BLOOD_MID  = (139,  0,   0)
C_BLOOD_HIGH = (196,  30,  58)
C_BONE       = (232, 220, 200)
C_GOLD       = (200, 168,  75)
C_SILVER     = (192, 192, 192)
C_HOLY_BLUE  = (65,  105, 225)
C_HOLY_LIGHT = (176, 200, 255)
C_WHITE      = (255, 255, 255)

# --- Arena ---
ARENA_WIDTH  = SCREEN_WIDTH
ARENA_HEIGHT = SCREEN_HEIGHT

# --- Player ---
PLAYER_SPEED      = 4
PLAYER_MAX_HP     = 100
PLAYER_START_WEAPON = "shotgun"  # weapon equipped on start

# --- Weapons ---
SHOTGUN_PELLETS       = 5       # pellets per shot
SHOTGUN_SPREAD_DEG    = 20      # total spread angle in degrees
SHOTGUN_PELLET_SPEED  = 12
SHOTGUN_PELLET_DAMAGE = 20
SHOTGUN_COOLDOWN_MS   = 500

HOLY_WATER_MAX        = 3
HOLY_WATER_SPEED      = 8
HOLY_WATER_DAMAGE     = 60
HOLY_WATER_RADIUS     = 64      # splash AoE radius in px
HOLY_WATER_COOLDOWN_MS= 800
FOUNTAIN_REFILL_MS    = 8000    # time for fountain to refill after drain

CROSS_ORBIT_RADIUS    = 80      # px from player center
CROSS_ORBIT_SPEED_DEG = 120     # degrees per second
CROSS_SPIN_SPEED_DEG  = 240     # self-rotation degrees per second
CROSS_DAMAGE          = 8       # damage per contact (applied at cooldown)
CROSS_HIT_COOLDOWN_MS = 600

# --- Upgrade pool ---
UPGRADES = [
    {
        "id": "orbit_slot",
        "name": "Silver Cross",
        "desc": "Add another orbiting cross",
    },
    {
        "id": "orbit_speed",
        "name": "Holy Momentum",
        "desc": "Crosses orbit 40% faster",
    },
    {
        "id": "orbit_radius",
        "name": "Wider Sanctum",
        "desc": "Crosses orbit 30px farther out",
    },
    {
        "id": "shotgun_damage",
        "name": "Blessed Rounds",
        "desc": "Shotgun pellets deal 50% more damage",
    },
    {
        "id": "max_hp",
        "name": "Iron Faith",
        "desc": "Gain 30 max HP and heal to full",
    },
    {
        "id": "move_speed",
        "name": "Hunter's Step",
        "desc": "Move 30% faster",
    },
]
UPGRADE_CHOICES = 3  # options shown per between-wave screen

# --- Enemies ---
VAMPIRE_SPEED  = 1.8
VAMPIRE_HP     = 60
VAMPIRE_DAMAGE = 10

FAST_VAMPIRE_SPEED  = 3.5
FAST_VAMPIRE_HP     = 30
FAST_VAMPIRE_DAMAGE = 8

DRACULA_SPEED       = 1.2
DRACULA_HP          = 600
DRACULA_DAMAGE      = 25
DRACULA_P2_HP_BONUS = 400    # added to max HP on phase transition
DRACULA_P2_SCALE    = 1.5
DRACULA_P2_SPEED    = 1.8

# Mirror enemy reflects player across vertical arena center
MIRROR_SPEED  = VAMPIRE_SPEED  # matches player indirectly via position
MIRROR_HP     = 80
MIRROR_DAMAGE = 12
ARENA_CENTER_X = ARENA_WIDTH // 2

# --- Wave definitions ---
# each entry: normal vamps, fast vamps, has_boss, has_mirror
WAVE_DEFINITIONS = [
    {"vampires": 10, "fast_vampires": 0,  "has_boss": False, "has_mirror": False},
    {"vampires": 15, "fast_vampires": 5,  "has_boss": False, "has_mirror": True},
    {"vampires": 8,  "fast_vampires": 4,  "has_boss": True,  "has_mirror": True},
]
SPAWN_MARGIN = 40   # px from arena edge where enemies can spawn

# --- Enemy contact damage cooldown ---
CONTACT_DAMAGE_COOLDOWN_MS = 800
