import pygame

TITLE = "Vampire Siege"
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
FPS = 60

ARENA_WIDTH  = 1920
ARENA_HEIGHT = 1080

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

# --- Player ---
PLAYER_SPEED      = 4
PLAYER_MAX_HP     = 100
PLAYER_START_WEAPON = "shotgun"

DODGE_DURATION_MS  = 280
DODGE_COOLDOWN_MS  = 1400
DODGE_SPEED_MULT   = 3.2

# --- Map ---
TOMBSTONE_COUNT    = 12
WAVE_BANNER_MS     = 2200   # how long the "WAVE X" banner shows

# --- Weapons ---
SHOTGUN_PELLETS       = 5       # pellets per shot
SHOTGUN_SPREAD_DEG    = 20      # total spread angle in degrees
SHOTGUN_PELLET_SPEED  = 12
SHOTGUN_PELLET_DAMAGE = 20
SHOTGUN_COOLDOWN_MS   = 400
SHOTGUN_MAGAZINE      = 6       # bursts before reload
SHOTGUN_RELOAD_MS     = 2200

HOLY_WATER_MAX        = 3
HOLY_WATER_SPEED      = 8
HOLY_WATER_DAMAGE     = 60
HOLY_WATER_RADIUS     = 64      # splash AoE radius in px
HOLY_WATER_COOLDOWN_MS= 800
FOUNTAIN_REFILL_MS    = 8000    # time for fountain to refill after drain

HOLY_WATER_PUDDLE_MS  = 3200    # puddle lifetime after splash
HOLY_WATER_PUDDLE_TICK= 600     # ms between puddle damage ticks
HOLY_WATER_PUDDLE_DMG = 18      # damage per tick

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
DRACULA_P2_HP_BONUS      = 400    # added to max HP on phase transition
DRACULA_P2_SCALE         = 1.5
DRACULA_P2_SPEED         = 1.8
DRACULA_P2_TRANSFORM_MS  = 2800   # transformation animation duration
DRACULA_P2_BAT_COUNT     = 5      # bats per summon in phase 2
DRACULA_P2_BAT_INTERVAL  = 4500   # ms between bat summons

# Mirror enemy
MIRROR_HP             = 120
MIRROR_DAMAGE         = 12
MIRROR_PATROL_MS      = 4500   # time in patrol before conjuring
MIRROR_CONJURE_MS     = 1800   # charge-up duration (stop + purple glow)
MIRROR_DASH_SPEED     = 9      # px per tick during dash
MIRROR_DASH_DURATION_MS = 1800 # max dash duration before returning to patrol
MIRROR_BAT_COUNT      = 7
BAT_SPEED             = 3.5
BAT_DAMAGE            = 10
ARENA_CENTER_X        = ARENA_WIDTH // 2

# Heal pickup
HEAL_PICKUP_AMOUNT    = 35
HEAL_PICKUP_RESPAWN_MS = 25_000

# --- Wave definitions ---
# each entry: normal vamps, fast vamps, has_boss, has_mirror
WAVE_DEFINITIONS = [
    {"vampires": 10, "fast_vampires": 0,  "has_boss": False, "has_mirror": False, "hp_mult": 1.0},
    {"vampires": 15, "fast_vampires": 5,  "has_boss": False, "has_mirror": True,  "hp_mult": 1.35},
    {"vampires": 8,  "fast_vampires": 4,  "has_boss": True,  "has_mirror": True,  "hp_mult": 1.7},
]
SPAWN_MARGIN = 40   # px from arena edge where enemies can spawn

# --- Enemy contact damage cooldown ---
CONTACT_DAMAGE_COOLDOWN_MS = 800
