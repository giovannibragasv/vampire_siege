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

## Style Lock

**`player_idle_1` is the canonical reference for all sprites.**

Every character prompt must:
- Explicitly say "same pixel scale and art style as player_idle_1"
- Describe **only what changes** from the reference
- Never deviate from: hard pixel edges, no anti-aliasing, 3–4 shades per region, transparent background

**Locked player description** (copy verbatim into every player prompt):
> `young vampire hunter with copper-red messy short hair, pale warm skin, dark brown leather long coat with brass buttons and upturned collar, cream shirt visible at collar, dark grey trousers, brown knee-high boots with brass buckle, sawn-off double-barrel shotgun, 32x48 pixels, gothic pixel-art game sprite, transparent background, hard pixel edges, no anti-aliasing`

---

## Characters

---

### 1. Player — Vampire Hunter

**Concept:** Young determined hunter. Worn dark leather long coat, copper-red hair, carries a sawn-off shotgun. Agile and combat-ready.

**Silhouette:** Medium height, fills ~85% of sprite height. Slight forward combat lean.

**Physical details (top to bottom):**
- Hair: short, copper-red, slightly messy — #8B3A1A / #C4622D / #E8894A
- Face: angular, small determined eyes, pale warm skin — #C8956A / #DBA882 / #ECC9A8
- Coat: dark brown leather, knee-length, brass buttons down center, collar up — #3B1F0F / #5C3317 / #7A4A25
- Shirt: cream linen visible at collar and cuffs — #E8DCC8
- Gloves: dark leather, same palette as coat
- Trousers: dark grey — #1E1E2E / #2D2D42
- Boots: brown leather with brass buckle, knee-high — #2A1505 / #4A2810
- Shotgun: wood stock (#5C3317), double metal barrels (#9A9A9A / #C0C0C0)

---

#### idle — 2 frames

> **`player_idle_1.svg`**
> ```
> Create player_idle_1 — the canonical reference frame for the entire game's art style. Young vampire hunter standing idle facing right: copper-red messy short hair, pale warm skin, angular face with small determined eyes, dark brown leather long coat with brass buttons down center and upturned collar (knee-length), cream linen shirt visible at collar, dark grey trousers, brown knee-high boots with brass buckle. Sawn-off double-barrel shotgun rested at right hip, barrel pointing right, wood stock and silver metal barrels. Both feet shoulder-width apart, weight balanced, arms relaxed at sides. Slight forward combat lean. 32x48 pixels, Castlevania Symphony of the Night meets Stardew Valley pixel art, gothic dark palette, transparent background, hard pixel edges, no anti-aliasing, 3-4 shades per color region.
> ```

> **`player_idle_2.svg`**
> ```
> Same exact character and art style as player_idle_1: young vampire hunter, copper-red messy short hair, pale skin, dark brown leather long coat with brass buttons and upturned collar, cream shirt, dark grey trousers, brown boots, sawn-off shotgun at right hip, 32x48 pixels, transparent background.
>
> Create player_idle_2, the breathing frame: identical to player_idle_1 but chest shifted 1px downward and coat hem shifted 1px upward (subtle breathing cycle). All other details identical — same face, same feet, same weapon position. No other changes.
> ```

---

#### walk_right — 4 frames

> **`player_walk_1.svg`**
> ```
> Same exact character and art style as player_idle_1: young vampire hunter with copper-red messy short hair, pale skin, dark brown leather long coat with brass buttons and upturned collar, cream shirt, dark grey trousers, brown boots, sawn-off shotgun, 32x48 pixels, transparent background.
>
> Create player_walk_1, the first stride frame of a 4-frame walk cycle facing right: right foot extended approximately 4px forward, left foot 3px back. Body slightly lowered compared to idle. Right arm holding shotgun swings slightly forward, left arm swings back ~3px. Coat bottom edge flares right by 2px from forward motion. Head level, eyes forward, determined expression unchanged.
> ```

> **`player_walk_2.svg`**
> ```
> Same exact character and art style as player_idle_1 and player_walk_1: young vampire hunter with copper-red messy short hair, pale skin, wearing a dark brown leather long coat with brass buttons and upturned collar, cream shirt, dark trousers, brown boots, holding a sawn-off shotgun at the right hip pointing right, 32x48 pixels, gothic pixel-art game sprite, transparent background.
>
> Create player_walk_2, the passing/neutral frame of a 4-frame walk cycle facing right: both feet close together under the body, knees slightly bent, no extended stride, torso centered and slightly higher than stride frames, body weight transitioning forward. Arms are closer to neutral: right arm holding shotgun slightly forward, left arm slightly back but not exaggerated. Coat settles closer to the body with only slight backward movement, minimal flare. Head level, eyes forward, expression unchanged.
>
> Maintain identical proportions, same scale, same pixel density, same silhouette, same outfit details, same shading style, no added detail, no style drift.
> ```

> **`player_walk_3.svg`**
> ```
> Same exact character and art style as player_idle_1 and player_walk_1: young vampire hunter with copper-red messy short hair, pale skin, dark brown leather long coat with brass buttons and upturned collar, cream shirt, dark trousers, brown boots, sawn-off shotgun at right side, 32x48 pixels, gothic pixel-art game sprite, transparent background.
>
> Create player_walk_3, the opposite stride frame of a 4-frame walk cycle facing right: left foot extended forward about the same distance as right foot was in player_walk_1, right foot extended back. Body slightly lowered compared to passing frame. Left arm swings forward, right arm (holding shotgun) shifts slightly back with the stride. Coat flares slightly in the opposite direction compared to player_walk_1, with the lower coat edge trailing behind movement. Head level, same determined expression.
>
> Maintain identical proportions, same scale, same pixel density, same silhouette, same weapon shape, same face, same coat length, no distortion, no style drift.
> ```

> **`player_walk_4.svg`**
> ```
> Same exact character and art style as player_idle_1 and player_walk_1: young vampire hunter with copper-red messy short hair, pale skin, dark brown leather long coat with brass buttons, cream shirt, dark trousers, brown boots, holding a sawn-off shotgun, 32x48 pixels, gothic pixel-art game sprite, transparent background.
>
> Create player_walk_4, the second passing frame of a 4-frame walk cycle facing right: both feet again close together under the body, similar to player_walk_2 but slightly offset for animation smoothness. Torso centered, slightly raised. Arms returning toward neutral from the opposite stride: left arm slightly forward, right arm (with shotgun) slightly back but minimal motion. Coat closer to body with subtle motion, less flare than stride frames.
>
> Maintain identical proportions, same scale, same pixel density, same silhouette, same details, ensure it loops smoothly back into player_walk_1, no style drift.
> ```

#### walk_left
Runtime flip of walk_right via `flip_surface()`. **Do not generate separately.**

---

#### shotgun_fire — 2 frames

> **`player_fire_1.svg`**
> ```
> Same exact character and art style as player_idle_1: young vampire hunter with copper-red messy short hair, pale skin, dark brown leather long coat with brass buttons and upturned collar, cream shirt, dark trousers, brown boots, 32x48 pixels, gothic pixel-art game sprite, transparent background.
>
> Create player_fire_1, the aiming frame of a 2-frame shotgun firing animation facing right: both hands gripping the sawn-off shotgun, arms extended forward-right at chest height, left hand supporting barrel underneath, right hand on grip. Body leans slightly forward into the shot, stance stable. Head slightly angled forward, eyes focused toward target. Coat reacts slightly to forward motion but remains mostly controlled.
>
> Maintain identical proportions, same scale, same pixel density, same weapon design, same silhouette, no exaggeration, no style drift.
> ```

> **`player_fire_2.svg`**
> ```
> Same exact character and art style as player_fire_1: same character, same proportions, same outfit, same shotgun, same pixel-art style, transparent background.
>
> Create player_fire_2, the recoil frame of a 2-frame shotgun firing animation: arms pulled slightly backward from recoil, body leaning slightly back, head tilted slightly upward from impact. Add a small bright muzzle flash at the shotgun barrel tip using a compact pixel burst (yellow-white tones), not too large. Coat reacts slightly backward from recoil. Expression remains focused but tense.
>
> Maintain identical proportions, same scale, same pixel density, same silhouette, same weapon shape, ensure consistency with frame 1, no style drift.
> ```

---

#### water_throw — 2 frames

> **`player_throw_1.svg`**
> ```
> Same exact character and art style as player_idle_1: young vampire hunter, copper-red messy short hair, pale skin, dark brown leather long coat with brass buttons, cream shirt, dark grey trousers, brown boots, 32x48 pixels, transparent background.
>
> Create player_throw_1, the wind-up frame of a 2-frame holy water throw animation facing right: right arm raised overhead with elbow bent, small round blue glass vial visibly gripped in right fist. Body weight shifted to left (back) foot. Left arm extended downward-forward for counterbalance. Head facing forward toward throw target. Coat shifts slightly with the body rotation.
> ```

> **`player_throw_2.svg`**
> ```
> Same exact character and art style as player_throw_1: same character, same proportions, same outfit, 32x48 pixels, transparent background.
>
> Create player_throw_2, the release frame: right arm extended forward and downward at approximately 45°, hand open (vial no longer in hand — it has left). Body weight fully shifted to front (right) foot, slight forward lean. Left arm swings back as follow-through. Coat flares forward with the motion momentum.
> ```

---

#### damaged — 1 frame

> **`player_damaged.svg`**
> ```
> Same exact character and art style as player_idle_1: young vampire hunter, copper-red messy short hair, pale skin, dark brown leather long coat, cream shirt, dark grey trousers, brown boots, 32x48 pixels, transparent background. Generate without any red tint — tint is applied at runtime.
>
> Create player_damaged, hit reaction: body knocked 2px rightward and 1px upward from impact. Head tilted back 2px. Left arm raised in front of face as a guard. Right arm (holding shotgun) drops to side. Coat flares leftward. Grimace expression: mouth slightly open, eyebrows angled in pain.
> ```

---

#### death — 4 frames

> **`player_death_1.svg`**
> ```
> Same art style as player_idle_1, 32x48 pixels, transparent background.
> Create player_death_1: body staggering — torso tilted ~20° backward, legs still upright, both arms falling outward, shotgun dropping from right hand at an angle. Expression: shock and disbelief.
> ```

> **`player_death_2.svg`**
> ```
> Same art style as player_idle_1, 32x48 pixels, transparent background.
> Create player_death_2: knees buckling — body dropped 6px from frame 1, knees bending forward, torso still visible but lowering, arms now completely at sides. Shotgun lying on ground to the right edge of the sprite.
> ```

> **`player_death_3.svg`**
> ```
> Same art style as player_idle_1, 32x48 pixels, transparent background.
> Create player_death_3: kneeling — sitting on bent knees, torso slumped forward 15°, head drooping downward, arms hanging limp at sides. Coat spread around the knees on the ground.
> ```

> **`player_death_4.svg`**
> ```
> Same art style as player_idle_1, 32x48 pixels, transparent background.
> Create player_death_4: fully collapsed horizontal — body lying on ground, coat spread flat, arms at sides, head tilted toward the right. Character occupies only the lower 16px of sprite height. Upper portion is empty.
> ```

---

### 2. Normal Vampire

**Concept:** Victorian aristocrat vampire. Tall, pale, unhurried.

**Silhouette:** Fills full 32×48 sprite height. Thin and elongated.

**Physical details:**
- Hair: slicked back jet black, sharp widow's peak — #0A0A0A
- Face: gaunt, hollow cheeks, pale grey skin, blood-red glowing eyes (2×2 px), visible elongated fangs — skin #A09898 / #C8C0B8
- Cape: floor-length, high collar — exterior #0A0A1E / #12122E / #1A1A40, lining #5C0000 / #8B0000
- Shirt: white frilled front — #E8DCC8
- Clawed fingertips visible at cape edges

---

#### idle — 2 frames

> **`vampire_idle_1.svg`**
> ```
> Same pixel scale and art style as player_idle_1 — 32x48 pixels, gothic pixel-art, Castlevania SotN style, transparent background, hard pixel edges, no anti-aliasing.
>
> Create vampire_idle_1: Victorian aristocrat vampire standing idle facing right. Tall gaunt figure filling the full sprite height. Slicked-back jet-black hair with sharp widow's peak. Gaunt face, hollow cheeks, pale grey skin (#A09898), blood-red glowing eyes (2x2px). Elongated fangs visible below lower lip. Floor-length dark cape fully closed, extremely high collar framing the head. White frilled shirt visible at chest. Feet together. Clawed fingertips just visible at cape hem. Expression: cold ancient contempt.
> ```

> **`vampire_idle_2.svg`**
> ```
> Same exact art style and character as vampire_idle_1, 32x48 pixels, transparent background.
> Create vampire_idle_2: identical to vampire_idle_1 but cape edges shift 2px outward at hem (slight flutter). Head and body position unchanged. No other changes.
> ```

---

#### walk — 4 frames

> **`vampire_walk_1.svg`**
> ```
> Same art style and character as vampire_idle_1, 32x48 pixels, transparent background.
> Create vampire_walk_1: left foot 4px forward, visible below cape hem. Cape opens slightly at left side revealing leg. Arms shift slightly outward from body. Slow deliberate stride. Expression unchanged.
> ```

> **`vampire_walk_2.svg`**
> ```
> Same art style and character as vampire_idle_1, 32x48 pixels, transparent background.
> Create vampire_walk_2 (passing/neutral): both feet together under body, cape fully closed again, arms returned to sides. Body upright.
> ```

> **`vampire_walk_3.svg`**
> ```
> Same art style and character as vampire_idle_1, 32x48 pixels, transparent background.
> Create vampire_walk_3: right foot 4px forward, cape opens at right side revealing leg. Arms shift slightly outward other direction.
> ```

> **`vampire_walk_4.svg`**
> ```
> Same art style and character as vampire_idle_1, 32x48 pixels, transparent background.
> Create vampire_walk_4: second neutral frame identical to vampire_walk_2 for smooth loop. Both feet together, cape closed, arms at sides.
> ```

---

#### damaged — 1 frame

> **`vampire_damaged.svg`**
> ```
> Same art style and character as vampire_idle_1, 32x48 pixels, transparent background. Generate without tint — applied at runtime.
> Create vampire_damaged: head snapped back 3px in fury (not pain). Cape blown fully open revealing frilled shirt and black waistcoat. Left arm raised in shock or rage. Body recoils 2px back. Expression: furious snarl, fangs fully bared.
> ```

---

#### death — 3 frames

> **`vampire_death_1.svg`**
> ```
> Same art style as vampire_idle_1, 32x48 pixels, transparent background.
> Create vampire_death_1: stumbling backward 3px. Cape swirling wide open, arms flailing outward, head thrown back. Expression: disbelief.
> ```

> **`vampire_death_2.svg`**
> ```
> Same art style as vampire_idle_1, 32x48 pixels, transparent background.
> Create vampire_death_2: body crumbling from feet up. Lower half (below knee) dissolving into 10-12 scattered 1px grey pixel dust particles. Upper half still intact but tilting. Cape beginning to collapse inward.
> ```

> **`vampire_death_3.svg`**
> ```
> Same art style as vampire_idle_1, 32x48 pixels, transparent background.
> Create vampire_death_3: only a small mound of grey ash remains (6px tall, 12px wide) with collapsed cape draped over it. One clawed hand visible at a cape edge.
> ```

---

### 3. Fast Vampire

**Concept:** Feral, smaller, animalistic. Bat-like. Crouched low.

**Silhouette:** 32×48 sprite but character fills only ~70% of height (crouched).

**Physical details:**
- Hair: wild, unkempt, dark brown/black — #0A0A0A / #1A0E05
- Face: sunken yellow glowing eyes, large protruding fangs, torn ear tips — skin #7A6E6A / #9A9090
- Clothing: tattered dark rags, shredded at edges — #1A0E00 / #2E1A05
- Arms: elongated, nearly reaching the ground, visible bone at elbows
- Legs: permanently crouched, feet splayed

---

#### idle — 2 frames

> **`fast_idle_1.svg`**
> ```
> Same pixel scale and art style as player_idle_1 — 32x48 pixels, gothic pixel-art, transparent background, hard pixel edges, no anti-aliasing.
>
> Create fast_idle_1: feral smaller vampire crouching idle facing right. Character fills only ~70% of sprite height — deep crouch, head near vertical center of sprite. Wild jagged dark hair. Sunken yellow glowing eyes (2x2px). Large protruding fangs. Torn ear tips. Tattered dark rags shredded at all edges. Elongated arms with visible bone at elbows, fingers splayed touching the ground. Weight on toes, feet splayed. Expression: predatory, coiled tension.
> ```

> **`fast_idle_2.svg`**
> ```
> Same art style and character as fast_idle_1, 32x48 pixels, transparent background.
> Create fast_idle_2: weight shifted 1px left, body 1px lower, head tilts 1px right. Subtle tension shift before burst. No other changes.
> ```

---

#### walk — 4 frames (animate at 2× normal vampire speed)

> **`fast_walk_1.svg`**
> ```
> Same art style as fast_idle_1, 32x48 pixels, transparent background.
> Create fast_walk_1: mid-bound, character airborne — right leg extended back, left leg forward, body lunging low. Both arms swinging wide outward for balance. Erratic bounding gait.
> ```

> **`fast_walk_2.svg`**
> ```
> Same art style as fast_idle_1, 32x48 pixels, transparent background.
> Create fast_walk_2: landing — both feet on ground, body at lowest crouch point. Arms swinging inward from momentum.
> ```

> **`fast_walk_3.svg`**
> ```
> Same art style as fast_idle_1, 32x48 pixels, transparent background.
> Create fast_walk_3: mid-bound other direction — left leg back, right leg forward, airborne, arms swinging wide outward.
> ```

> **`fast_walk_4.svg`**
> ```
> Same art style as fast_idle_1, 32x48 pixels, transparent background.
> Create fast_walk_4: landing — same low crouch as fast_walk_2. Arms swinging inward. Loops back into fast_walk_1.
> ```

---

#### damaged — 1 frame

> **`fast_damaged.svg`**
> ```
> Same art style as fast_idle_1, 32x48 pixels, transparent background. No tint — applied at runtime.
> Create fast_damaged: launched upward and backward — body 3px up, 3px back from center. All limbs flailing outward. Head thrown back. Eyes wide, fangs fully bared.
> ```

---

#### death — 3 frames

> **`fast_death_1.svg`**
> ```
> Same art style as fast_idle_1, 32x48 pixels, transparent background.
> Create fast_death_1: launched backward 4px, mid-air. Limbs splayed. 2-3 loose pixel fragments visibly detaching from silhouette edges.
> ```

> **`fast_death_2.svg`**
> ```
> Same art style as fast_idle_1, 32x48 pixels, transparent background.
> Create fast_death_2: mid-disintegration — silhouette broken into 4-5 irregular pixel chunks in outward burst pattern. No coherent body shape.
> ```

> **`fast_death_3.svg`**
> ```
> Same art style as fast_idle_1, 32x48 pixels, transparent background.
> Create fast_death_3: scattered ash burst — 15-20 individual 1-2px grey/brown pixel dots spread across sprite area. No recognizable silhouette.
> ```

---

### 4. Mirror Enemy — The Shadow

**Concept:** Spectral dark reflection of the player. Identical silhouette, inverted palette.

**Silhouette:** Identical to player (32×48 px). Faces LEFT.

**Color inversion:**
- Dark leather (#3B1F0F) → silver-white (#D0D0E0)
- Mid leather (#5C3317) → light grey (#B0B0C0)
- Copper-red hair → silver-white with faint purple sheen (#9B30FF tint)
- Warm skin → deep shadow-purple (#2D1040 / #4A2060)
- Eyes: hollow glowing purple #9B30FF, 2×2 px
- Add 1–2 subtly misplaced pixels on the outline (uncanny feeling)

**Frames:** Same set as player. All face LEFT. Runtime flip also applied dynamically.

---

> **`mirror_idle_1.svg`**
> ```
> Same pixel scale and art style as player_idle_1 — 32x48 pixels, gothic pixel-art, transparent background, hard pixel edges, no anti-aliasing.
>
> Create mirror_idle_1: spectral dark mirror reflection of the player, facing LEFT. Identical silhouette to player_idle_1 but color-inverted: coat is silver-white (#D0D0E0) where player has dark leather; skin is deep shadow-purple (#2D1040 / #4A2060) where player has warm tone; hair is silver-white with faint purple sheen; hollow glowing purple eyes (2x2px, #9B30FF). Shotgun rendered in the same inverted palette. Add exactly 1-2 subtly misplaced pixels on the outline (e.g. one extra pixel at a shoulder or a 1px gap in coat hem) for an uncanny feel. Same idle standing pose as player_idle_1.
> ```

> **`mirror_idle_2.svg`**
> ```
> Same art style and character as mirror_idle_1, 32x48 pixels, transparent background.
> Create mirror_idle_2: identical to mirror_idle_1 but coat hem shifts 1px upward, chest 1px down (breathing). Same misplaced pixels. No other changes.
> ```

> **`mirror_walk_1.svg`** through **`mirror_walk_4.svg`**
> ```
> Same art style as mirror_idle_1, facing LEFT, 32x48 pixels, transparent background.
> Create mirror_walk_[N]: mirror of player_walk_[N] — same pose geometry but facing left and with the inverted color palette. [Describe the stride/passing position matching the player_walk_[N] frame.] Maintain the same 1-2 misplaced outline pixels from mirror_idle_1.
> ```

> **`mirror_damaged.svg`**
> ```
> Same art style as mirror_idle_1, facing LEFT, 32x48 pixels, transparent background. No tint — applied at runtime.
> Create mirror_damaged: mirror of player_damaged — same hit reaction geometry (body knocked, arm guard, grimace) but facing left with inverted palette.
> ```

> **`mirror_death_1.svg`** through **`mirror_death_4.svg`**
> ```
> Same art style as mirror_idle_1, facing LEFT, 32x48 pixels, transparent background.
> Create mirror_death_[N]: mirror of player_death_[N] — same collapse geometry but facing left with the inverted silver-white/purple palette.
> ```

---

### 5. Dracula — Phase 1

**Concept:** Ancient vampire lord boss. Imposing, aristocratic, deliberate.

**Sprite size:** 48×64 px

**Physical details:**
- Hair: slicked back sharply, jet black, dramatic widow's peak — #0A0A0A
- Face: angular, high cheekbones, thin sharp nose, thin dark mustache, pale grey-purple skin, blood-red glowing eyes (3×3 px), long curved fangs
- Cape: floor-length, very high collar — exterior #050010 / #0D0022, lining #5C0000 / #8B0000 / #B00000
- Tuxedo: black jacket, sharp lapels
- Ascot tie: white — #F0EAD6
- Gloves: black, formal
- Shoes: pointed, formal, black

---

#### idle — 2 frames

> **`dracula_p1_idle_1.svg`**
> ```
> Same pixel scale and art style as player_idle_1 but at 48x64 pixels — gothic pixel-art, Castlevania SotN style, transparent background, hard pixel edges, no anti-aliasing.
>
> Create dracula_p1_idle_1: Dracula, ancient vampire lord boss, standing idle facing right. Imposing tall aristocrat filling the full sprite height. Jet-black slicked hair with dramatic sharp widow's peak. Angular face, high cheekbones, thin dark mustache, pale grey-purple skin, blood-red glowing eyes (3x3px), long curved fangs. Extremely high-collared floor-length black cape fully closed, cape collar framing the face like a halo. White ascot tie at collar. Black tuxedo jacket lapels visible at chest. Formal black gloves. Pointed formal shoes. Arms clasped behind back (not visible). Feet together. Expression: ancient cold contempt.
> ```

> **`dracula_p1_idle_2.svg`**
> ```
> Same art style and character as dracula_p1_idle_1, 48x64 pixels, transparent background.
> Create dracula_p1_idle_2: identical to frame 1 but cape edges at hem shift 3px outward (slow flutter) and ascot tie shifts 1px. All other details identical.
> ```

---

#### walk — 4 frames

> **`dracula_p1_walk_1.svg`**
> ```
> Same art style as dracula_p1_idle_1, 48x64 pixels, transparent background.
> Create dracula_p1_walk_1: slow menacing stride — right foot 5px forward, cape sweeps wide to the right (hem fans dramatically), left arm raises slightly outward. Long deliberate step.
> ```

> **`dracula_p1_walk_2.svg`**
> ```
> Same art style as dracula_p1_idle_1, 48x64 pixels, transparent background.
> Create dracula_p1_walk_2 (neutral): feet together, cape settling, arms returning to sides.
> ```

> **`dracula_p1_walk_3.svg`**
> ```
> Same art style as dracula_p1_idle_1, 48x64 pixels, transparent background.
> Create dracula_p1_walk_3: left foot 5px forward, cape sweeps wide to the left, right arm raises slightly outward.
> ```

> **`dracula_p1_walk_4.svg`**
> ```
> Same art style as dracula_p1_idle_1, 48x64 pixels, transparent background.
> Create dracula_p1_walk_4: second neutral — feet together, cape settling, arms at sides. Loops back to walk_1.
> ```

---

#### damaged — 1 frame

> **`dracula_p1_damaged.svg`**
> ```
> Same art style as dracula_p1_idle_1, 48x64 pixels, transparent background. No tint — applied at runtime.
> Create dracula_p1_damaged: reacting in fury, not pain. Head snapped back 4px. Cape blown fully open revealing full crimson lining. One arm raised with pointed finger toward the player. Body recoils back 3px. Expression: furious snarl, fangs bared.
> ```

---

#### death — 5 frames

> **`dracula_p1_death_1.svg`**
> ```
> Same art style as dracula_p1_idle_1, 48x64 pixels, transparent background.
> Create dracula_p1_death_1: staggering — torso tilted 15° backward, cape swirling wide open, arms reaching outward for balance. Expression: disbelief.
> ```

> **`dracula_p1_death_2.svg`**
> ```
> Same art style as dracula_p1_idle_1, 48x64 pixels, transparent background.
> Create dracula_p1_death_2: bowing — torso hunched 30° forward, head dropping, one arm clutching chest. Cape open and swirling around him.
> ```

> **`dracula_p1_death_3.svg`**
> ```
> Same art style as dracula_p1_idle_1, 48x64 pixels, transparent background.
> Create dracula_p1_death_3: crumbling from feet up — lower 20px dissolving into dark pixel dust (12-15 scattered 1-2px dots). Upper torso still recognizable but lowering. Cape beginning to collapse.
> ```

> **`dracula_p1_death_4.svg`**
> ```
> Same art style as dracula_p1_idle_1, 48x64 pixels, transparent background.
> Create dracula_p1_death_4: only upper torso and cape collar remain — floating 10px above a growing dark ash pile below. Face still visible with fading red eye glow. Cape draping downward.
> ```

> **`dracula_p1_death_5.svg`**
> ```
> Same art style as dracula_p1_idle_1, 48x64 pixels, transparent background.
> Create dracula_p1_death_5: empty — collapsed cape on floor (8px tall mound centered low in sprite) with a faint blood-red mist scatter: 8-12 individual 1px red/dark-red pixel dots radiating outward from the cape mound.
> ```

---

### 6. Dracula — Phase 2

**Concept:** Same character, aristocratic facade cracking, monstrous nature emerging.

**Base sprite size:** 48×64 px — **scaled to 72×96 at runtime**. Design at 48×64 only.

**Visual changes from Phase 1:**
- Cape edges: ragged/frayed torn pixel border (1–2px notches along hem)
- Hair: no longer slicked, several strands projecting irregularly outward
- Hands: claws extended and curled, piercing through ripped gloves
- Tuxedo: shoulder seams ripped (2–3px gap at each shoulder)
- Skin: small cracks at jaw and forehead (3–4 dark pixel lines)
- Eyes: 4×4 px glow, brighter red (#FF3030) instead of 3×3
- Expression: openly enraged, not contemptuous

---

> **`dracula_p2_idle_1.svg`**
> ```
> Same art style as dracula_p1_idle_1 but with phase 2 visual changes, 48x64 pixels, transparent background.
> Create dracula_p2_idle_1: same Dracula figure as dracula_p1_idle_1 but monstrous and cracking — frayed torn ragged cape hem (1-2px notches along bottom edge), wild disheveled hair with 2-3 strands projecting outward, clawed hands extended through ripped gloves, ripped tuxedo at both shoulders (2-3px tear gaps), small crack lines at jaw and forehead, larger brighter glowing red eyes (4x4px, #FF3030). Idle standing pose, same composition as P1 idle.
> ```

> **`dracula_p2_idle_2.svg`**
> ```
> Same as dracula_p2_idle_1, 48x64 pixels, transparent background.
> Create dracula_p2_idle_2: identical to dracula_p2_idle_1 but cape hem shifts 3px outward (flutter), one stray hair strand shifts 1px. No other changes.
> ```

> **`dracula_p2_walk_1.svg`** through **`dracula_p2_walk_4.svg`**
> ```
> Same art style as dracula_p2_idle_1, 48x64 pixels, transparent background.
> Create dracula_p2_walk_[N]: same pose geometry as dracula_p1_walk_[N] but with all phase 2 visual changes applied (frayed cape, wild hair, claws, ripped shoulders, skin cracks, larger eyes). [Describe foot/arm position matching P1 walk frame N.]
> ```

> **`dracula_p2_damaged.svg`**
> ```
> Same art style as dracula_p2_idle_1, 48x64 pixels, transparent background. No tint — applied at runtime.
> Create dracula_p2_damaged: same fury recoil as dracula_p1_damaged but with phase 2 visual changes. Cape fully blown open showing crimson lining and ripped tuxedo. Claws extended on raised arm. Expression: uncontrolled rage.
> ```

> **`dracula_p2_death_1.svg`** through **`dracula_p2_death_5.svg`**
> ```
> Same art style as dracula_p2_idle_1, 48x64 pixels, transparent background.
> Create dracula_p2_death_[N]: same collapse geometry as dracula_p1_death_[N] but with phase 2 visual changes. The disintegration has a more violent/explosive quality — larger pixel fragments, brighter red mist in final frame.
> ```

---

## Items & Objects

---

### Silver Cross — Orbiting Weapon

**Size:** 24×24 px. Single sprite — runtime rotation applied.

> **`cross.svg`**
> ```
> Ornate gothic crucifix pixel art, 24x24 pixels, same Castlevania SotN style as player_idle_1, transparent background, hard pixel edges, no anti-aliasing. Vertical arm slightly longer than horizontal. Tarnished gold body (#C8A84B base, #E8C860 highlight, #8A6A20 shadow). Silver edge highlighting on all arm edges (#D0D0D0, 1px). Small ruby gemstone at center crossing (2x2px, #8B0000 center, #CC2020 highlight pixel). Arms 4px wide. Arm tips 1 shade brighter suggesting faint radiance.
> ```

---

### Cross Pickup — Ground Drop

**Size:** 20×20 px. Simpler than the orbit cross — sits on the ground.

> **`cross_pickup.svg`**
> ```
> Same pixel art style as player_idle_1, 20x20 pixels, transparent background, hard pixel edges, no anti-aliasing.
> Create cross_pickup: a small gothic silver cross lying on the ground as a collectible item. Simpler than the orbit weapon — same cross shape but smaller, silver-grey tones (#C0C0C0 / #E0E0E0 / #808080). Faint soft golden glow aura (1-2px lighter pixels around the cross outline) suggesting holy power. No gemstone — plainer than the weapon cross.
> ```

---

### Heal Pickup — HP Orb

**Size:** 20×20 px. 2 frames for pulsing (scale handled at runtime too).

> **`heal_1.svg`**
> ```
> Same pixel art style as player_idle_1, 20x20 pixels, transparent background, hard pixel edges, no anti-aliasing.
> Create heal_1: a small circular health pickup. Red glowing orb with a white cross emblem at center. Outer ring: dark red (#5C0000), mid: blood red (#8B0000), inner bright: (#C41E3A), tiny white cross (4x4px) centered on orb. Faint white-pink glow aura (1-2px) around the outer ring.
> ```

> **`heal_2.svg`**
> ```
> Same art style as heal_1, 20x20 pixels, transparent background.
> Create heal_2: identical to heal_1 but the glow aura is 1px larger/brighter (pulse frame). The orb itself is 1px larger in all directions. Used to create a gentle pulsing animation at runtime.
> ```

---

### Bat — Projectile

**Size:** 16×16 px. 2 frames for wing flap. Runtime rotation for direction.

> **`bat_1.svg`**
> ```
> Same pixel art style as player_idle_1, 16x16 pixels, transparent background, hard pixel edges, no anti-aliasing.
> Create bat_1: small stylized bat projectile viewed from above/front. Wings spread wide — roughly 14px wide, 8px tall body. Dark purple-black body (#1A0030 / #2E004E), slightly lighter wing membrane (#3D0060). Small red glowing eyes (1x1px each). Wings fully extended outward, slightly angled. Compact and readable at small size.
> ```

> **`bat_2.svg`**
> ```
> Same art style as bat_1, 16x16 pixels, transparent background.
> Create bat_2: wings folded — bat at lowest point of wing stroke. Wings curved downward, roughly 10px wide at narrowest, body more visible. Same colors as bat_1. Alternating with bat_1 creates a flapping animation.
> ```

---

### Shotgun Pellet — Silver Prayer Bullet

**Size:** 8×8 px. Single sprite — runtime rotation applied.

> **`pellet.svg`**
> ```
> Same pixel art style as player_idle_1, 8x8 pixels, transparent background, hard pixel edges, no anti-aliasing.
> Create pellet: small oval silver prayer bullet, slightly pointed at left tip (travel direction). Silver metallic body (#C0C0C0 mid, #E0E0E0 highlight on upper edge, #808080 shadow on lower edge). 1px near-white aura border (#F0F0FF). Two tiny dark 1x1px marks on body side (#404040) suggesting engraved prayer text.
> ```

---

### Holy Water Pot — Full

**Size:** 16×20 px.

> **`water_full.svg`**
> ```
> Same pixel art style as player_idle_1, 16x20 pixels, transparent background, hard pixel edges, no anti-aliasing.
> Create water_full: round-bellied glass vial, wider at mid-height. Cork stopper at top (4px tall, brown #5C3317 / #7A4A25). Glass body pale blue-tinted (#B8C8FF exterior highlight). Holy water fill visible at 70% of pot height — solid blue (#4169E1) below fill line, glass-effect above (checker: 1 blue : 1 very light grey pixel). Tiny cross etched on glass front (2x4px, #2040A0, 1px lines).
> ```

---

### Holy Water Pot — Empty

**Size:** 16×20 px.

> **`water_empty.svg`**
> ```
> Same art style as water_full, 16x20 pixels, transparent background.
> Create water_empty: same cork. Same glass shape. Pale grey tint (#D8D8E0 exterior) instead of blue. Interior checker uses light grey instead of blue — no fill line. Cross etching still visible. Conveys emptiness.
> ```

---

### Holy Water Splash — Impact Animation

**Size:** 48×32 px per frame (wider than tall).

> **`splash_1.svg`**
> ```
> Same pixel art style as player_idle_1, 48x32 pixels, transparent background, hard pixel edges, no anti-aliasing.
> Create splash_1: impact burst — tiny bright blue pixel burst at center-bottom (8x8 area, #B0C8FF center, #4169E1 around it). 4-6 small droplet pixels (1-2px each) scattered upward and outward in a starburst.
> ```

> **`splash_2.svg`**
> ```
> Same art style, 48x32 pixels, transparent background.
> Create splash_2: puddle spreading — oval blue pool forming at center-bottom (20x8px, #4169E1 fill, #B0C8FF highlight pixels along top edge). 8-10 droplet pixels in semicircle arc above pool at varied heights.
> ```

> **`splash_3.svg`**
> ```
> Same art style, 48x32 pixels, transparent background.
> Create splash_3: dissipating — pool shrinking to 12x4px, lighter blue (#8CA8D0). Outer droplets gone. 4-6 faint mist pixels (#D0E0FF, 1px each) at edges above pool center.
> ```

---

### Holy Water Puddle — DoT Zone

**Size:** 32×32 px. Single sprite — runtime scale creates the pulse effect.

> **`puddle.svg`**
> ```
> Same pixel art style as player_idle_1, 32x32 pixels, transparent background, hard pixel edges, no anti-aliasing.
> Create puddle: oval glowing blue holy water puddle on the ground, viewed from slightly above. Outer ring: faint blue (#4169E1, 1px, slightly irregular/organic pixel edge). Inner area: lighter blue (#8CA8D0) with a few brighter highlight pixels (#B0C8FF) scattered near center suggesting glow. No sharp geometric circle — organic pixel oval shape. Subtle and readable.
> ```

---

### Blood Decal — Kill Splatter

**Size:** 24×16 px. Single sprite, drawn on ground after enemy death.

> **`blood_decal.svg`**
> ```
> Same pixel art style as player_idle_1, 24x16 pixels, transparent background, hard pixel edges, no anti-aliasing.
> Create blood_decal: dark blood splatter on the ground, viewed from above. Irregular pixel blob — not a circle, organic asymmetric shape. Dark red (#5C0000) as base, blood red mid (#8B0000) for larger pixels, 1-2 brighter red (#C41E3A) highlight pixels near center. 3-5 small 1px satellite droplet pixels scattered outward from the main blob. Flat, reads as a ground stain.
> ```

---

## Map Objects

---

### Tombstone — Arena Obstacle

**Size:** 36×52 px. Single sprite.

> **`tombstone.svg`**
> ```
> Same pixel art style as player_idle_1, 36x52 pixels, transparent background, hard pixel edges, no anti-aliasing.
> Create tombstone: gothic stone tombstone viewed slightly from the front. Rounded arch top, flat-ish sides, wider base slab. Stone palette: #4A4A4A shadow, #7A7A7A mid, #B0B0B0 highlight on upper/left edges. A small carved gothic cross near the top (8x10px, recessed — slightly darker than surface, #4A4A4A). 2-3 horizontal crack lines across the stone face (1px, #3A3A3A). Slight moss/dark stain in lower corners (#2A3A2A, 2-3 pixels). Base slab slightly wider than body.
> ```

---

### Italian Fountain — State 1: Flowing (3-frame loop)

**Size:** 64×64 px.

> **`fountain_flow_1.svg`**
> ```
> Same pixel art style as player_idle_1, 64x64 pixels, transparent background, hard pixel edges, no anti-aliasing, slight top-down angle view.
> Create fountain_flow_1: baroque stone fountain. Round base basin (50px wide, 12px tall, stone #4A4A4A / #7A7A7A / #B0B0B0, rim lip highlighted, interior dark #2C2C2C). Central stone pedestal (8px wide column, 20px tall, same stone). Mid bowl at top of pedestal (20px wide, 6px tall). Gothic cross finial at very top (8x8px, tarnished gold #C8A84B). Water: 4px wide column of blue-white pixels (#B0C8FF / #4169E1) falling from mid bowl rim to base basin. 2-3 splash pixels (#B0C8FF) scattered at base where water lands.
> ```

> **`fountain_flow_2.svg`**
> ```
> Same art style as fountain_flow_1, 64x64 pixels, transparent background.
> Create fountain_flow_2: identical structure to fountain_flow_1 but water column pixel pattern shifted 3px downward (animation frame). Splash pixels at base in alternate positions.
> ```

> **`fountain_flow_3.svg`**
> ```
> Same art style as fountain_flow_1, 64x64 pixels, transparent background.
> Create fountain_flow_3: identical structure, water column shifted another 3px down (loops back to fountain_flow_1). Splash pixels in third alternate arrangement.
> ```

---

### Italian Fountain — State 2: Empty/Dry

**Size:** 64×64 px.

> **`fountain_empty.svg`**
> ```
> Same art style as fountain_flow_1, 64x64 pixels, transparent background.
> Create fountain_empty: identical fountain structure but completely dry. No water pixels anywhere. Stone tones all shifted 1 shade darker (dry stone). 3-4 darker grey pixels (#3A3A3A) along interior edges of both basin and mid bowl as dry residue marks.
> ```

---

### Italian Fountain — State 3: Refilling (3 frames)

**Size:** 64×64 px.

> **`fountain_refill_1.svg`**
> ```
> Same art style as fountain_flow_1, 64x64 pixels, transparent background.
> Create fountain_refill_1: fountain beginning to refill — 1-2 blue pixels at mid bowl rim as a faint trickle. Base basin has a tiny 4px wide x 2px tall shallow puddle at center bottom only.
> ```

> **`fountain_refill_2.svg`**
> ```
> Same art style as fountain_flow_1, 64x64 pixels, transparent background.
> Create fountain_refill_2: flow growing — 3px wide stream from mid bowl rim. Base basin puddle now 12px wide x 4px tall.
> ```

> **`fountain_refill_3.svg`**
> ```
> Same art style as fountain_flow_1, 64x64 pixels, transparent background.
> Create fountain_refill_3: nearly full — 4px wide stream continuous. Base basin puddle 24px wide x 6px tall. Mid bowl has visible water level (4px of blue inside bowl). Next frame transitions to fountain_flow_1.
> ```

---

## UI Elements

---

### Face Portrait — 3 HP Stages

**Size:** 72×72 px each. Detailed face of the player character.

> **`portrait_healthy.svg`**
> ```
> Same pixel art style as player_idle_1, 72x72 pixels, transparent background, hard pixel edges, no anti-aliasing.
> Create portrait_healthy: close-up face portrait of the vampire hunter (HP ≥ 75%). Dark purple background panel with rounded corners. Warm-skinned angular face: copper-red short messy hair, small determined eyes with brown irises and white glint pixels, confident expression with a slight smirk. Clean face, no damage. Coat collar visible at bottom. Tarnished gold border frame. Lit from top-left with slight rim light on hair.
> ```

> **`portrait_damaged.svg`**
> ```
> Same pixel art style as player_idle_1, 72x72 pixels, transparent background.
> Create portrait_damaged: same vampire hunter face (HP 30-74%). Same composition as portrait_healthy but: eyes narrowed and worried, slight frown/tense mouth (arc downward), one small sweat droplet pixel on temple. A single thin scratch mark on cheek (2 diagonal dark pixels). Slightly paler skin tone. Same dark purple background, blood-red border frame.
> ```

> **`portrait_critical.svg`**
> ```
> Same pixel art style as player_idle_1, 72x72 pixels, transparent background.
> Create portrait_critical: same vampire hunter face (HP < 30%). Barely-open eyes, desperate grimace, mouth corner turned down. Two blood streak lines on face (2px wide, 1px wide, dark red #8B0000). Noticeably paler skin. Dark red (near-black) background panel. Bright red border frame.
> ```

---

### HUD Shotgun Sprite

**Size:** 50×46 px. Displayed in bottom HUD panel next to the portrait.

> **`hud_gun.svg`**
> ```
> Same pixel art style as player_idle_1, 50x46 pixels, transparent background, hard pixel edges, no anti-aliasing.
> Create hud_gun: side-view of a sawn-off double-barrel shotgun, the same weapon the player carries. Wood stock on the left (brown #5C3317 / #7A4A25 / #3B1F0F, angled wedge shape). Dark metal receiver body in the center (#505060 / #707080). Two parallel horizontal barrels extending to the right (silver-grey #9A9A9A / #C0C0C0 / #707070, each barrel about 4px tall with a 2px gap between them). Muzzle end at the far right with a 2px dark cap. Trigger guard: small circular outline below receiver (#404050). Wood and metal clearly distinct. Compact, readable at small HUD size.
> ```

---

### HP Bar

**Size:** 128×16 px.

> **`hp_bar.svg`**
> ```
> Same pixel art style as player_idle_1, 128x16 pixels, transparent background, hard pixel edges, no anti-aliasing.
> Create hp_bar: gothic stone frame border (3px thick all sides, #2C2C2C with 1px #606060 highlight on top and left inner edges). Interior fill area 122x10px — leave it empty/transparent (Pygame fills it at runtime). Small white pixel skull icon (8x8px, simple pixelated skull shape, #E8DCC8) anchored to left end inside the border.
> ```

---

### Wave Banner

**Size:** 200×32 px.

> **`wave_banner.svg`**
> ```
> Same pixel art style as player_idle_1, 200x32 pixels, transparent background, hard pixel edges, no anti-aliasing.
> Create wave_banner: parchment scroll. Yellowed parchment (#D4C89A / #E8DCA8 / #A89060). Both left and right ends show a rolled scroll cap (12px wide oval, same parchment colors with shadow suggesting the roll). Dark red border line (#5C0000, 1px) along top and bottom of the flat scroll area. Center text area (140x20px) is flat empty parchment — Pygame renders text here at runtime. No text in the sprite.
> ```

---

### Upgrade Card Frame

**Size:** 96×128 px.

> **`upgrade_card.svg`**
> ```
> Same pixel art style as player_idle_1, 96x128 pixels, transparent background, hard pixel edges, no anti-aliasing.
> Create upgrade_card: gothic collectible card frame. Border: 6px ornate dark stone frame (#1A0A00) with small 8x8 gold filigree swirl decorations at each corner (#C8A84B). Interior background: dark purple (#150028). Icon area: 32x32px centered horizontally, positioned in upper third of interior (~16px from top), bordered by a thin 1px gold line (#C8A84B) — leave interior transparent (Pygame draws the icon at runtime). Text area below icon: empty, transparent. Overall: gothic trading card aesthetic.
> ```

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
| Cross pickup (ground) | 20×20 | 1 | `cross_pickup.svg` | |
| Heal pickup | 20×20 | 2 | `heal_1.svg` `heal_2.svg` | pulse via runtime scale |
| Shotgun pellet | 8×8 | 1 | `pellet.svg` | runtime rotation |
| Holy water pot full | 16×20 | 1 | `water_full.svg` | |
| Holy water pot empty | 16×20 | 1 | `water_empty.svg` | |
| Holy water splash | 48×32 | 3 | `splash_1.svg` `splash_2.svg` `splash_3.svg` | |
| Holy water puddle (DoT) | 32×32 | 1 | `puddle.svg` | pulse via runtime scale |
| Bat projectile | 16×16 | 2 | `bat_1.svg` `bat_2.svg` | runtime rotation |
| Blood decal | 24×16 | 1 | `blood_decal.svg` | ground splatter on kill |
| Tombstone | 36×52 | 1 | `tombstone.svg` | map obstacle |
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
