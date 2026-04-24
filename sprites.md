# Vampire Siege — Sprite Design Document

## Art Style
- **Reference:** Castlevania: Symphony of the Night aesthetic at Stardew Valley pixel density
- **Character resolution:** 32×48 px (player, vampires); 48×64 px (Dracula); 72×96 px (Dracula phase 2 — Pygame scales the 48×64 base at runtime)
- **Item resolution:** 24×24 px (cross); 16×20 px (water pot); 8×8 px (pellet); 48×32 px (splash); 64×64 px (fountain)
- **UI resolution:** per element, listed below
- **Background:** transparent PNG on all sprites
- **Shading:** 3–4 shades per color region, hard pixel edges, zero anti-aliasing
- **Lighting:** subtle top-left rim light, heavy downward cast shadows

### Master Palette
| Role | Hex |
|---|---|
| Void black | #0D0010 |
| Dark purple | #1A0530 |
| Blood red shadow | #5C0000 |
| Blood red mid | #8B0000 |
| Blood red highlight | #C41E3A |
| Bone white | #E8DCC8 |
| Tarnished gold | #C8A84B |
| Silver | #C0C0C0 |
| Holy blue | #4169E1 |
| Holy blue highlight | #B0C8FF |
| Leather brown shadow | #3B1F0F |
| Leather brown mid | #5C3317 |
| Leather brown highlight | #7A4A25 |
| Stone grey shadow | #4A4A4A |
| Stone grey mid | #7A7A7A |
| Stone grey highlight | #B0B0B0 |

---

## Base GPT Prompt Suffix
> Append this to **every** individual frame prompt below:
>
> `pixel art, [WxH] pixels, Castlevania Symphony of the Night meets Stardew Valley style, gothic dark palette, transparent background, no anti-aliasing, hard pixel edges, 3-4 shades per color region, slight top-left rim lighting`

---

## Characters

---

### 1. Player — Vampire Hunter

**Concept:** Young determined hunter. Worn dark leather long coat, copper-red hair, carries a sawn-off shotgun. Agile and combat-ready.

**Silhouette:** Medium height, fills ~85% of sprite height. Slight forward combat lean.

**Physical details (top to bottom):**
- Hair: short, copper-red, slightly messy — #8B3A1A / #C4622D / #E8894A
- Face: angular, small determined eyes, no hat, pale warm skin — #C8956A / #DBA882 / #ECC9A8
- Coat: dark brown leather, knee-length, brass buttons down center, collar up — #3B1F0F / #5C3317 / #7A4A25
- Shirt: cream linen visible at collar and cuffs — #E8DCC8
- Gloves: dark leather, same palette as coat
- Trousers: dark grey — #1E1E2E / #2D2D42
- Boots: brown leather with brass buckle, knee-high — #2A1505 / #4A2810

**Weapon (idle/walk):** Sawn-off double-barrel shotgun, held at right hip. Barrel points right. Wood stock (#5C3317), metal barrels (#9A9A9A).

---

#### idle — 2 frames

**Frame 1:** Standing upright, slight forward lean, weight on both feet, right foot 1px forward. Shotgun rested at right hip pointing right. Arms relaxed. Eyes forward.

**Frame 2:** Identical to frame 1 but chest shifted 1px downward and coat hem 1px upward (breathing cycle).

> **Prompt:** `vampire hunter idle frame [1/2], young determined hunter standing, slight forward combat lean, copper-red short messy hair, dark brown leather long coat with brass buttons and upturned collar, cream shirt visible at neck, dark grey trousers, brown boots with brass buckle, sawn-off shotgun rested at right hip pointing right, arms relaxed, 32x48 pixels` + suffix

---

#### walk_right — 4 frames

**Frame 1:** Right foot ~4px forward, left arm swings back ~3px, right arm forward holding shotgun, coat bottom edge flares right by 2px, head level.

**Frame 2:** Feet together, neutral stance, coat settled, arms centered.

**Frame 3:** Left foot ~4px forward, right arm swings back slightly (shotgun shifts back), left arm forward, coat bottom flares left by 2px.

**Frame 4:** Feet together, neutral, same as frame 2.

> **Prompt:** `vampire hunter walking right frame [1/2/3/4], [describe specific foot/arm position from above], coat flapping, determined stride, 32x48 pixels` + suffix

#### walk_left
Horizontal mirror of walk_right — handled at runtime via `pygame.transform.flip(sprite, True, False)`. **Do not generate separately.**

---

#### shotgun_fire — 2 frames

**Frame 1:** Both hands grip shotgun. Arms extended forward-right at chest height, slight forward body lean, muzzle points right at arm's-length. Left hand supports barrel from below, right hand on grip. Eyes narrowed, focused.

**Frame 2 (recoil):** Arms pulled 3px back toward body, body leans back 2px, head tilts slightly back. Muzzle flash at barrel tip: 6–8 bright yellow/white pixels radiating from barrel end in a small starburst.

> **Prompt:** `vampire hunter shotgun fire frame [1/2], [aim pose / recoil pose], two-handed grip on sawn-off shotgun, [muzzle flash pixel burst at barrel tip — frame 2 only], 32x48 pixels` + suffix

---

#### water_throw — 2 frames

**Frame 1 (wind-up):** Right arm raised overhead, elbow bent, small round blue glass pot visibly gripped in right hand. Body weight shifted to back foot (left foot), left arm counterbalances forward and down. Eyes looking forward at throw target.

**Frame 2 (release):** Right arm extended forward at 45° downward angle, hand open (pot no longer in hand — it is in flight), follow-through motion. Body weight shifted fully to front foot. Left arm swings back.

> **Prompt:** `vampire hunter holy water throw frame [1/2], [wind-up: arm raised overhead gripping small round blue glass pot / release: arm extended forward-down open hand follow-through], 32x48 pixels` + suffix

---

#### damaged — 1 frame

Body knocked 2px rightward. Head tilted back 2px. Left arm raised in front of face as a guard. Right arm (shotgun) drops to side. Coat flares leftward. Grimace expression (mouth open, eyebrows angled in pain). Sprite will be tinted red at runtime — generate without tint.

> **Prompt:** `vampire hunter damaged hit pose, body recoiling right, head tilted back, left arm raised as guard, grimace expression, coat flaring, 32x48 pixels` + suffix

---

#### death — 4 frames

**Frame 1:** Body staggering. Torso tilted ~20° backward, legs still upright, arms falling outward, shotgun dropping from hand (angled away).

**Frame 2:** Knees buckling. Body dropped 6px from frame 1, knees bent forward, torso still visible but lowering, arms now completely at sides.

**Frame 3:** Kneeling position. Sitting on knees, torso slumped forward 15°, head drooping, arms hanging.

**Frame 4:** Fully collapsed. Body horizontal on ground, coat spread flat, arms at sides, head to the right. Takes up lower 16px of sprite height.

> **Prompt:** `vampire hunter death animation frame [1/2/3/4], [staggering backward / knees buckling dropping / kneeling slumped / collapsed horizontal on ground], 32x48 pixels` + suffix

---

### 2. Normal Vampire

**Concept:** Victorian aristocrat vampire. Tall, pale, unhurried. Moves with unnatural stillness between lurching deliberate steps.

**Silhouette:** Fills full 32×48 sprite height. Thin and elongated.

**Physical details:**
- Hair: slicked back jet black with sharp widow's peak — #0A0A0A
- Face: gaunt, hollow cheeks, pale grey skin, blood-red glowing eyes (2×2 px glow), visible elongated fangs below lower lip — skin #A09898 / #C8C0B8 / #DDD8D0
- Cape exterior: floor-length, high collar framing the head — #0A0A1E / #12122E / #1A1A40
- Cape lining: deep crimson, only visible when cape opens — #5C0000 / #8B0000
- Shirt: white frilled front, visible at chest opening — #E8DCC8
- Waistcoat: black, beneath cape — #0A0A0A / #181818
- Legs: black trousers, pointed black shoes
- Hands: clawed fingertips visible at cape edges

---

#### idle — 2 frames

**Frame 1:** Cape fully wrapped around body. Head raised slightly, looking slightly downward with contempt. Red eyes glowing. Hands at sides, claws just visible at cape hem.

**Frame 2:** Cape edges shift 2px outward at hem (slight flutter). Head position unchanged.

> **Prompt:** `Victorian vampire standing idle frame [1/2], tall gaunt aristocrat, slicked black widow's peak hair, pale grey skin, blood-red glowing eyes, elongated fangs, high-collared floor-length dark cape [closed / cape hem fluttering 2px outward], white frilled shirt at chest, clawed hands at sides, 32x48 pixels` + suffix

---

#### walk — 4 frames

**Frame 1:** Left foot 4px forward, visible below cape hem. Cape opens slightly at left to reveal leg, arms shift slightly outward from body.

**Frame 2:** Feet together, cape fully closed again.

**Frame 3:** Right foot 4px forward, cape opens at right.

**Frame 4:** Feet together, cape closed.

> **Prompt:** `Victorian vampire walking frame [1/2/3/4], [left foot forward cape opening left / neutral cape closed / right foot forward cape opening right / neutral cape closed], lurching aristocratic stride, 32x48 pixels` + suffix

---

#### damaged — 1 frame

Head snapped back 3px. Cape blown fully open revealing body beneath (frilled shirt, waistcoat visible). Left arm raised in shock/rage, right arm at side. Body recoils back 2px.

> **Prompt:** `Victorian vampire hit/damaged, head recoiling sharply back, cape blown fully open revealing frilled shirt and waistcoat, left arm raised in shock, body recoiling, 32x48 pixels` + suffix

---

#### death — 3 frames

**Frame 1:** Stumbling backward 3px, cape swirling open wide, arms flailing outward, head thrown back.

**Frame 2:** Body crumbling from feet up. Lower half dissolving into grey pixel dust particles (10–12 scattered 1px dots below knee line). Upper half still intact but tilting. Cape settling.

**Frame 3:** Only a small mound of grey ash pixels remains (6px tall, 12px wide) at floor with the collapsed cape draped over it. A single clawed hand visible at cape edge.

> **Prompt:** `Victorian vampire death frame [1/2/3], [stumbling cape swirling / body crumbling into ash from feet up upper half still standing / collapsed ash pile with cape and one clawed hand], 32x48 pixels` + suffix

---

### 3. Fast Vampire

**Concept:** Feral, smaller, animalistic. Bat-like. Crouched low. Moves in quick erratic bursts.

**Silhouette:** 32×48 sprite but character fills only ~70% of height. Crouched stance puts head near vertical center of sprite.

**Physical details:**
- Hair: wild, unkempt, dark brown/black, jagged — #0A0A0A / #1A0E05
- Face: sunken yellow glowing eyes, large protruding fangs, torn ear tips, gaunt — skin #7A6E6A / #9A9090
- Clothing: tattered dark rags, barely covering, shredded at all edges — #1A0E00 / #2E1A05 / #3D2510
- Arms: elongated, reaching nearly to the ground, visible bone at elbows
- Legs: crouched permanently, feet splayed

---

#### idle — 2 frames

**Frame 1:** Deep crouch, head low between shoulders, yellow eyes staring forward, fingers splayed and touching the ground, weight on toes.

**Frame 2:** Weight shifted left, body 1px lower, head tilts 1px right (tension before burst).

> **Prompt:** `feral smaller vampire crouching idle frame [1/2], hunched animalistic pose, wild jagged dark hair, yellow glowing sunken eyes, large protruding fangs, torn ear tips, tattered dark rags, elongated arms nearly touching ground, splayed feet, gaunt bony silhouette, 32x48 pixels` + suffix

---

#### walk — 4 frames (animate at 2× normal vampire speed)

**Frame 1:** Mid-bound, right leg extended back, left leg forward, body lunging low, both arms swinging wide outward for balance.

**Frame 2:** Landing, both feet on ground, body at lowest point, arms swinging inward.

**Frame 3:** Mid-bound other direction, left leg back, right leg forward.

**Frame 4:** Landing, same as frame 2.

> **Prompt:** `feral vampire fast walk frame [1/2/3/4], erratic bounding low gait, [mid-bound lunging / landing crouch / mid-bound other side / landing crouch], arms swinging wide, 32x48 pixels` + suffix

---

#### damaged — 1 frame

Launched upward and back — body 3px up, 3px back from center, limbs flailing outward, head thrown back, eyes wide, fangs bared.

> **Prompt:** `feral vampire damaged, launched upward-backward by impact, limbs flailing, head thrown back, eyes wide, fangs bared, 32x48 pixels` + suffix

---

#### death — 3 frames

**Frame 1:** Launched backward 4px, midair, limbs splayed, body beginning to fragment (2–3 loose pixel fragments detaching from edge of silhouette).

**Frame 2:** Body mid-disintegration — silhouette broken into 4–5 irregular pixel chunks in an outward burst pattern.

**Frame 3:** Scattered ash pixel burst — 15–20 individual 1–2px grey/brown dots spread across the sprite area, no coherent silhouette remaining.

> **Prompt:** `feral vampire violent death frame [1/2/3], [launched backward fragmenting / mid-disintegration into pixel chunks / ash burst scattered pixels], 32x48 pixels` + suffix

---

### 4. Mirror Enemy — The Shadow

**Concept:** A spectral dark reflection of the player. Identical silhouette. Color-inverted palette. Something is visually wrong — it feels like a cursed mirror image.

**Silhouette:** Identical to player (32×48 px). Faces LEFT (since it mirrors the player who faces right).

**Color inversion logic:**
- Where player has dark leather (#3B1F0F) → Shadow has silver-white (#D0D0E0)
- Where player has mid leather (#5C3317) → Shadow has light grey (#B0B0C0)
- Where player has copper-red hair → Shadow has silver-white hair (#E8E8F0) with faint purple sheen (#9B30FF tint)
- Where player has warm skin → Shadow has deep shadow-purple skin (#2D1040 / #4A2060)
- Eyes: hollow glowing purple #9B30FF, 2×2 px glow
- Coat details (buttons, collar): dark void #0D0010 where player has bright brass

**Distortion detail:** 1–2 pixels somewhere on the outline are "off" — e.g., an extra pixel on the shoulder that shouldn't be there, a gap in the coat hem. Subtle.

**Frames:** Same animation set as player (idle ×2, walk ×4, damaged, death). All frames face LEFT. Pygame additionally applies `pygame.transform.flip` dynamically at runtime based on mirror position.

> **Prompt:** `dark mirror ghost reflection of a vampire hunter, identical silhouette facing LEFT, inverted color scheme: silver-white coat where original is dark leather, deep purple skin where original is warm, silver-white hair with faint purple sheen, hollow glowing purple eyes, spectral slightly distorted look with 1-2 misplaced pixels on outline, [frame description matching player frame], 32x48 pixels` + suffix

---

### 5. Dracula — Phase 1

**Concept:** The boss. Ancient vampire lord. Imposing, aristocratic, unhurried. Every movement deliberate and threatening.

**Sprite size:** 48×64 px

**Physical details:**
- Hair: slicked back sharply, jet black, dramatic widow's peak — #0A0A0A
- Face: angular, high cheekbones, thin sharp nose, thin dark mustache, pale grey-purple skin, blood-red glowing eyes (3×3 px glow), visible long curved fangs — skin #8C8080 / #B0A8A0
- Cape: floor-length, very high collar (frames the head like a halo), exterior black (#050010 / #0D0022 / #150033), interior deep crimson lining (#5C0000 / #8B0000 / #B00000) only visible when cape opens
- Tuxedo: black jacket, visible at chest, sharp lapels
- Ascot tie: white, at collar, prominent — #F0EAD6
- Gloves: black, formal
- Shoes: pointed, formal, black

---

#### idle — 2 frames

**Frame 1:** Cape fully closed. Arms clasped behind back (arms not visible at sides). Head raised, looking slightly downward with ancient contempt. Cape collar up, framing the face. Feet together.

**Frame 2:** Cape edges at hem shift 3px outward (slow flutter). Head unchanged. Ascot tie shifts 1px.

> **Prompt:** `Dracula vampire lord boss idle frame [1/2], imposing tall aristocrat, jet black slicked hair sharp widow's peak, thin mustache, pale grey-purple skin, blood-red glowing eyes, long curved fangs, extremely high-collared floor-length black cape [closed arms behind back / hem fluttering], white ascot tie, black tuxedo lapels visible, feet together, 48x64 pixels` + suffix

---

#### walk — 4 frames

Slow and deliberate. Long dramatic stride. Arms outstretched slightly at sides when moving — not behind back.

**Frame 1:** Right foot 5px forward, cape sweeps wide right (hem fans out right side), left arm raises slightly outward.

**Frame 2:** Feet together, cape settling, arms return to sides.

**Frame 3:** Left foot 5px forward, cape sweeps wide left, right arm raises slightly.

**Frame 4:** Feet together, cape settling.

> **Prompt:** `Dracula walking frame [1/2/3/4], slow menacing aristocratic stride, [right foot forward cape sweeping right arm out / neutral cape settling / left foot forward cape sweeping left arm out / neutral], 48x64 pixels` + suffix

---

#### damaged — 1 frame

Head snapped back 4px in fury (not pain — rage). Cape blown fully open, crimson lining entirely visible. One arm raised with pointed finger toward the player in fury. Body recoils back 3px. Expression: furious snarl, fangs bared.

> **Prompt:** `Dracula damaged, furious rather than pained, head snapping back, cape blown fully open revealing crimson lining, one arm raised with pointing finger, fangs bared in snarl, 48x64 pixels` + suffix

---

#### death — 5 frames

**Frame 1:** Staggering — torso tilted 15° backward, cape swirling open, arms reaching out to sides for balance, expression disbelief.

**Frame 2:** Body bowing — torso hunched 30° forward now, head dropping, one arm clutching at chest, cape still open and swirling.

**Frame 3:** Crumbling begins at feet — lower 20px dissolving into dark pixel dust, torso still recognizable but lowering, cape beginning to collapse.

**Frame 4:** Only upper torso and cape remain — floating 10px above growing ash pile, face visible with fading eye glow.

**Frame 5:** Empty collapsed cape on floor (8px tall mound) with a faint blood-red mist — 8–12 individual red pixels scattered outward in a burst pattern around the cape.

> **Prompt:** `Dracula death animation frame [1/2/3/4/5], [staggering disbelief arms out / bowing clutching chest / crumbling from feet up dust forming / only upper torso floating above ash / empty cape collapsed with red mist scatter], 48x64 pixels` + suffix

---

### 6. Dracula — Phase 2

**Concept:** Same character, but control is slipping. Aristocratic facade cracking. Monstrous nature emerging.

**Base sprite size:** 48×64 px — Pygame scales to 72×96 at runtime using a 1.5× scale matrix. Design the sprite at 48×64 with phase 2 visual changes — do not pre-scale.

**Visual changes from Phase 1:**
- Cape edges now ragged/frayed — torn pixel border (alternating 1–2px notches along hem)
- Hair no longer slicked — several strands projecting outward irregularly
- Hands: claws now extended and visibly curled outward (not gloved — claws pierce through)
- Tuxedo: shoulder seams ripped (2–3px gap/tear at each shoulder)
- Skin: small cracks at jaw and forehead (3–4 dark pixel lines)
- Eyes: 4×4 px glow now instead of 3×3, brighter red (#FF3030)
- Expression: no longer contemptuous — now openly enraged

**Frames:** Identical set to Phase 1 (idle ×2, walk ×4, damaged, death). Each redrawn with phase 2 modifications.

> **Prompt:** `Dracula boss phase 2 transformation, same figure as before but monstrous and cracking, frayed torn ragged cape hem, wild disheveled hair with protruding strands, clawed hands extended through ripped gloves, ripped tuxedo at shoulders, cracked skin at jaw and forehead, larger brighter glowing red eyes, openly enraged expression, [frame description], 48x64 pixels` + suffix

---

## Items & Objects

---

### Silver Cross — Orbiting Weapon

**Size:** 24×24 px. Single sprite — Pygame applies rotation transform at runtime.

**Description:** Ornate gothic crucifix. Vertical arm slightly longer than horizontal. Body: tarnished gold (#C8A84B base, #E8C860 highlight, #8A6A20 shadow). Silver edge highlighting on all arm edges (#D0D0D0, 1px). Small ruby gemstone at center crossing (2×2 px, #8B0000 center, #CC2020 highlight pixel). Glow: 4 outermost pixels at each arm tip are 1 shade brighter than arm (#E8C860), suggesting faint radiance. Arm width: 4px. No background.

> **Prompt:** `ornate gothic crucifix pixel art, 24x24 pixels, tarnished gold body with silver edge highlighting, small ruby gemstone at center crossing, faint golden glow at arm tips, gothic intricate style, transparent background, no anti-aliasing`

---

### Shotgun Pellet — Silver Prayer Bullet

**Size:** 8×8 px. Single sprite — Pygame handles travel direction and optional rotation.

**Description:** Small oval bullet, slightly pointed at left tip (travel direction), flat-ish at right. Silver metallic body (#C0C0C0 mid, #E0E0E0 highlight on upper edge, #808080 shadow on lower edge). 1px near-white aura border around the entire bullet (#F0F0FF at low contrast). Two tiny dark pixel marks on the body side (1×1 px each, #404040) suggesting engraved prayer text.

> **Prompt:** `silver prayer bullet pixel art, 8x8 pixels, small oval shape slightly pointed at one end, silver metallic shading, faint white glow aura, two tiny engraved mark pixels on side, transparent background, no anti-aliasing`

---

### Holy Water Pot — Full

**Size:** 16×20 px.

**Description:** Round-bellied glass vial, slightly wider at mid-height than top or bottom. Cork stopper at top (4px tall, round, brown #5C3317 / #7A4A25). Glass body: pale blue-tinted (#B8C8FF exterior highlight, #4169E1 as interior water color at 60% — suggest transparency via checker pattern of 1 blue : 1 very light grey pixel in the glass area). Water fill line visible at 70% of pot height (solid blue below the line, glass-effect above). Tiny cross etched on glass front (2×4 px, #2040A0 dark blue, 1px wide vertical and horizontal).

> **Prompt:** `small round holy water glass vial with cork stopper, full of blue glowing holy water at 70% fill line, pale blue-tinted glass effect, tiny cross etched on glass front, pixel art 16x20 pixels, gothic inventory item style, transparent background, no anti-aliasing`

---

### Holy Water Pot — Empty

**Size:** 16×20 px. Same shape as full.

**Description:** Same cork. Glass body: pale grey tint (#D8D8E0 exterior, interior is the same checker but with light grey instead of blue). No water fill line. Cross etching still visible. Conveys emptiness.

> **Prompt:** `same small round glass vial with cork stopper, empty with no water inside, pale grey-tinted glass effect, cross etching on front still visible, pixel art 16x20 pixels, transparent background, no anti-aliasing`

---

### Holy Water Splash — Impact Animation

**Size:** 48×32 px per frame (wider than tall — horizontal ground spread).

**3 frames:**

**Frame 1 (impact):** Tiny burst at center-bottom of sprite. 8×8 area of bright blue pixels (#B0C8FF center, #4169E1 around it) radiating from a central point. 4–6 small droplet pixels (1–2px each) scattered upward and outward in a starburst from center.

**Frame 2 (spread):** Main puddle forming — oval blue pool at center-bottom (20×8 px, #4169E1 fill, #B0C8FF highlight pixels along top edge). 8–10 droplet pixels in semicircle arc rising upward above pool, at varied heights. Pool edges are 1px lighter than center.

**Frame 3 (dissipate):** Pool shrinking to 12×4 px, more transparent (lighter blue #8CA8D0). Outer droplets gone. 4–6 faint mist pixels (#D0E0FF, 1px each) at edges above pool. Center 4px of pool still bright.

> **Prompt:** `holy water splash impact animation frame [1/2/3], [tiny blue burst starburst droplets / expanding oval puddle with arc of droplets / shrinking dissipating puddle with faint mist pixels], blue glowing water, pixel art 48x32 pixels, transparent background, gothic magic effect style, no anti-aliasing`

---

## Map Objects

---

### Italian Fountain — State 1: Flowing (3-frame loop)

**Size:** 64×64 px.

**Description:** Baroque stone fountain. Viewed at slight top-down angle (isometric-adjacent but mostly front-facing).

- Base basin: round, 50px wide at widest, 12px tall. Stone texture (#4A4A4A shadow, #7A7A7A mid, #B0B0B0 highlight on rim lip). Interior basin darker (#2C2C2C).
- Central pedestal: 8px wide column rising from basin center, 20px tall, same stone palette.
- Mid bowl: at top of pedestal, 20px wide, 6px tall bowl, same stone. Basin interior dark.
- Column finial: small gothic cross at very top, 8×8 px, tarnished gold (#C8A84B).
- Water: cascades from mid bowl over rim into base basin. Represented as a 4px wide column of blue-white pixels (#B0C8FF highlights, #4169E1 base) falling from mid bowl rim to base basin. Where water hits base, 2–3 splash pixels (#B0C8FF) scatter sideways.

**3 animation frames:** Water pixel column shifts downward by 3px each frame (cycling back). Splash pixels at base alternate positions.

> **Prompt:** `baroque stone water fountain, round base basin, central stone pedestal with smaller mid bowl and gothic cross finial in tarnished gold, water cascading from mid bowl to base basin as blue-white pixel stream, slight gothic architectural detail on basin rim, pixel art 64x64 pixels, slight top-down angle view, gothic stone palette, transparent background, no anti-aliasing` + suffix

---

### Italian Fountain — State 2: Empty/Dry

**Size:** 64×64 px. Same structure as State 1.

**Changes:** No water pixels anywhere. Stone slightly darker overall (all mid tones shifted 1 shade darker — conveys dry stone). 3–4 darker grey pixels (#3A3A3A) along interior edges of both basin and mid bowl (dry residue marks).

> **Prompt:** `same baroque stone fountain, completely dry and empty, no water, darker dry stone texture, faint dry residue marks as darker pixels along basin interior edges, pixel art 64x64 pixels, transparent background, no anti-aliasing` + suffix

---

### Italian Fountain — State 3: Refilling (3 frames → transitions to State 1)

**Size:** 64×64 px.

**Frame 1 (trickle):** 1–2 blue pixels at the very rim of the mid bowl, dripping. Base basin interior has 4px wide × 2px tall shallow puddle at bottom center.

**Frame 2 (flow):** 3px wide stream from mid bowl rim. Base basin puddle now 12px wide × 4px tall.

**Frame 3 (nearly full):** 4px wide stream, continuous. Base basin puddle 24px wide × 6px tall. Mid bowl has visible water level (4px of blue inside bowl). One more frame and it reaches State 1.

> **Prompt:** `baroque stone fountain slowly refilling, [frame 1: tiny 1-2 pixel water trickle at bowl rim, shallow puddle at base / frame 2: small stream 3px wide, medium puddle / frame 3: 4px stream, large puddle nearly at basin level], pixel art 64x64 pixels, transparent background, no anti-aliasing` + suffix

---

## UI Elements

---

### HP Bar

**Size:** 128×16 px.

**Description:** Gothic stone frame border, 3px thick on all sides. Border: #2C2C2C with 1px #606060 highlight on top and left inner edges. Interior fill area: 122×10 px. Fill: blood red (#8B0000) for current HP, very dark red (#200000) for missing HP portion. Small white skull icon (8×8 px, simple pixelated skull shape, #E8DCC8) anchored to left end, inside the border.

> **Prompt:** `gothic stone frame HP health bar UI element, 128x16 pixels, dark stone border with slight inner highlight, blood red fill for health, very dark red for missing health, small white pixel skull icon on left end, pixel art, transparent background, no anti-aliasing`

---

### Wave Banner

**Size:** 200×32 px.

**Description:** Parchment scroll. Yellowed parchment (#D4C89A mid, #E8DCA8 highlight, #A89060 shadow at rolled ends). Both left and right ends show a rolled scroll cap (12px wide, oval, same parchment color with shadow suggesting the roll). Dark red border line (#5C0000) runs along top and bottom edge of the flat scroll area. Center text area (140×20 px) is flat parchment — Pygame renders wave number text here at runtime. No text in the generated sprite.

> **Prompt:** `gothic parchment scroll banner, 200x32 pixels, yellowed parchment with rolled ends left and right, dark red border lines on top and bottom edges, flat empty center area for text, pixel art, transparent background, no anti-aliasing`

---

### Upgrade Card

**Size:** 96×128 px.

**Description:**
- Border: 6px gothic ornate frame. Dark stone (#1A0A00) with 4 gold filigree corner decorations (small 8×8 swirl/flourish pattern in #C8A84B at each corner).
- Interior background: dark purple (#150028).
- Icon area: 32×32 px centered horizontally, positioned at top third of interior (starting ~16px from interior top). Bordered by a thin 1px gold line (#C8A84B).
- Text area: remaining interior space below icon (roughly 32×48 px). Empty — Pygame renders upgrade name and description at runtime.
- Overall feel: a collectible card from a gothic trading card game.

> **Prompt:** `gothic upgrade card frame, 96x128 pixels, dark stone border with small gold filigree swirl decorations at each corner, dark purple interior, thin gold-bordered 32x32 icon display area in upper third, empty text area below, pixel art, Castlevania style UI card, transparent background, no anti-aliasing`

---

### Holy Water Counter (HUD)

Reuses the **Holy Water Pot — Full** sprite (16×20 px) × 3 displayed in a row. When a charge is spent, that slot switches to the **Holy Water Pot — Empty** sprite. No additional sprite needed.

---

## Sprite Summary Table

Multi-frame sprites use the suffix `_1`, `_2`, … before `.svg`. Convert each SVG to PNG at the same name before loading in Pygame.

| Sprite | Size | Frames | Filenames | Notes |
|---|---|---|---|---|
| Player idle | 32×48 | 2 | `player_idle_1.svg` `player_idle_2.svg` | |
| Player walk_right | 32×48 | 4 | `player_walk_1.svg` … `player_walk_4.svg` | walk_left = runtime flip |
| Player shotgun_fire | 32×48 | 2 | `player_fire_1.svg` `player_fire_2.svg` | |
| Player water_throw | 32×48 | 2 | `player_throw_1.svg` `player_throw_2.svg` | |
| Player damaged | 32×48 | 1 | `player_damaged.svg` | |
| Player death | 32×48 | 4 | `player_death_1.svg` … `player_death_4.svg` | |
| Normal vampire idle | 32×48 | 2 | `vampire_idle_1.svg` `vampire_idle_2.svg` | |
| Normal vampire walk | 32×48 | 4 | `vampire_walk_1.svg` … `vampire_walk_4.svg` | |
| Normal vampire damaged | 32×48 | 1 | `vampire_damaged.svg` | |
| Normal vampire death | 32×48 | 3 | `vampire_death_1.svg` … `vampire_death_3.svg` | |
| Fast vampire idle | 32×48 | 2 | `fast_idle_1.svg` `fast_idle_2.svg` | |
| Fast vampire walk | 32×48 | 4 | `fast_walk_1.svg` … `fast_walk_4.svg` | animate 2× speed |
| Fast vampire damaged | 32×48 | 1 | `fast_damaged.svg` | |
| Fast vampire death | 32×48 | 3 | `fast_death_1.svg` … `fast_death_3.svg` | |
| Mirror enemy idle | 32×48 | 2 | `mirror_idle_1.svg` `mirror_idle_2.svg` | faces left |
| Mirror enemy walk | 32×48 | 4 | `mirror_walk_1.svg` … `mirror_walk_4.svg` | runtime flip added |
| Mirror enemy damaged | 32×48 | 1 | `mirror_damaged.svg` | |
| Mirror enemy death | 32×48 | 4 | `mirror_death_1.svg` … `mirror_death_4.svg` | |
| Dracula P1 idle | 48×64 | 2 | `dracula_p1_idle_1.svg` `dracula_p1_idle_2.svg` | |
| Dracula P1 walk | 48×64 | 4 | `dracula_p1_walk_1.svg` … `dracula_p1_walk_4.svg` | |
| Dracula P1 damaged | 48×64 | 1 | `dracula_p1_damaged.svg` | |
| Dracula P1 death | 48×64 | 5 | `dracula_p1_death_1.svg` … `dracula_p1_death_5.svg` | |
| Dracula P2 idle | 48×64 | 2 | `dracula_p2_idle_1.svg` `dracula_p2_idle_2.svg` | scaled 1.5× at runtime |
| Dracula P2 walk | 48×64 | 4 | `dracula_p2_walk_1.svg` … `dracula_p2_walk_4.svg` | scaled 1.5× at runtime |
| Dracula P2 damaged | 48×64 | 1 | `dracula_p2_damaged.svg` | scaled 1.5× at runtime |
| Dracula P2 death | 48×64 | 5 | `dracula_p2_death_1.svg` … `dracula_p2_death_5.svg` | scaled 1.5× at runtime |
| Silver cross | 24×24 | 1 | `cross.svg` | runtime rotation |
| Shotgun pellet | 8×8 | 1 | `pellet.svg` | runtime rotation |
| Holy water pot full | 16×20 | 1 | `water_full.svg` | |
| Holy water pot empty | 16×20 | 1 | `water_empty.svg` | |
| Holy water splash | 48×32 | 3 | `splash_1.svg` `splash_2.svg` `splash_3.svg` | |
| Holy water puddle (DoT) | 32×32 | 1 | `puddle.svg` | runtime scale for pulse |
| Bat | 16×16 | 2 | `bat_1.svg` `bat_2.svg` | runtime rotation for direction |
| Blood decal | 24×16 | 1 | `blood_decal.svg` | ground splatter on kill |
| Tombstone | 36×52 | 1 | `tombstone.svg` | map obstacle |
| Heal pickup | 20×20 | 2 | `heal_1.svg` `heal_2.svg` | pulsing animation |
| Cross pickup | 20×20 | 1 | `cross_pickup.svg` | ground drop |
| Fountain flowing | 64×64 | 3 | `fountain_flow_1.svg` … `fountain_flow_3.svg` | loop |
| Fountain empty | 64×64 | 1 | `fountain_empty.svg` | |
| Fountain refilling | 64×64 | 3 | `fountain_refill_1.svg` … `fountain_refill_3.svg` | → transitions to flowing |
| Face portrait — healthy | 72×72 | 1 | `portrait_healthy.svg` | HP ≥ 75% |
| Face portrait — damaged | 72×72 | 1 | `portrait_damaged.svg` | HP 30–74% |
| Face portrait — critical | 72×72 | 1 | `portrait_critical.svg` | HP < 30% |
| HUD shotgun sprite | 50×46 | 1 | `hud_gun.svg` | bottom panel decoration |
| HP bar frame | 128×16 | 1 | `hp_bar.svg` | fill drawn at runtime |
| Wave banner | 200×32 | 1 | `wave_banner.svg` | text drawn at runtime |
| Upgrade card frame | 96×128 | 1 | `upgrade_card.svg` | icon + text drawn at runtime |
