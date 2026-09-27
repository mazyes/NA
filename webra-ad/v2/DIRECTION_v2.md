# WEBRA: Georgian spot v2, review and direction

**Output:** `out/webra_v2_ka_1080x1920.mp4`: 9:16, 1080×1920, 30 fps with motion blur (3 samples per frame, 180° shutter), H.264 High plus AAC 256k, 30.0 s, −14 LUFS integrated.
**Type:** FiraGO throughout. ExtraBold 800 for headlines, Medium 500 for supporting lines, SemiBold 600 for contact details. Source: the official bBoxType release.
**Logo:** the original file is loaded from `brand/logo.svg` or `brand/logo.png` without being modified. If neither file is present, the render shows a clearly marked placeholder and the renderer prints a warning.

---

## 1 · Problems found in v1

| Time | Scene | Problem | Fix in v2 |
|---|---|---|---|
| 0.0–1.5 | Hook | The phone was on screen for only about 1.3 s before it shattered, so the problem never registered. The hook text arrived late (1.5 s) and was English. | The phone stays whole. The Georgian hook starts at 0.45 s and is readable for about 3 s. |
| 1.0–1.45 | Hook | Random camera shake. | Removed. The camera move is a single continuous, eased arc. |
| 1.25–2.9 | Hook | 64 shards flew in random directions with random spins and no physics, then vanished. | Removed. The phone screen itself becomes the website (a morph, not a cut). |
| 1.5–2.0 | Hook | Lines slammed in from z +900 with 38° rotation, which read as too aggressive. | Masked word-by-word reveals on one easing curve, no rotation. |
| 3.0–3.36 | Hook | Chromatic glitch, jitter and skew: the "random distortion" look. | Removed. Clean masked exit. |
| 3.3–4.9 | Web | 30 random primitives floated with no relationship to anything, then faded instead of turning into anything. | Removed. There is one hero object for the whole first half. |
| 4.4–8.0 | Web | The browser had no ground contact. The UI popped with overshoot. | The object sits over a floor with a contact shadow, a floor reflection and a light pool. Modules draw in with expo-out wipes. No overshoot on UI. |
| 8.0–9.4 | Web | The orbit revealed decorative props (monolith, cube, torus) that added clutter. | Props removed. A gentle continuous orbit (−14° → +10°) gives the parallax instead. |
| 9.45–9.95 | Web → SEO | Browser → "glowing gem": a new, unrelated object with spinning facets and heavy glow. | The mobile site morphs straight into the search bar. The same object continues. |
| 10.0–11.0 | SEO | Orbiting ghost bars, 3-axis spinning facets, multiple ring sets and 18 rising lines: cluttered. | One search bar, one result card, two soft rings. |
| 13.5 | SEO | "GET FOUND." hugged the top edge and tracked from +12 %. | Safe-area headline with a two-line supporting subtitle. |
| 15.3–16.0 | SEO → AI | The circular wipe was dark on dark and nearly invisible, so it read as a jump cut. | A vertical camera pan: the search scene lifts out and the automation scene rises in. |
| 16.0–17.8 | AI | Chips jittered randomly every 1/6 s. | A calm, slightly overlapping pile with slow drift. Chips glide into place with a stagger. |
| 19.25–21.0 | AI | Tilting the pipeline 56° made the chip text unreadable. | The pipeline stays flat and readable. The ✓ confirmations fall on eighth notes. |
| 23.3–24.5 | Brand | The zebra tile collapsed into a thin line under a text wordmark that bounced letter by letter. | The zebra pattern folds into the logo's footprint and dissolves into the original logo with a 0.94 → 1 settle. No bounce. |
| 27.0–30.0 | End card | The end card lasted 3 s. The contact details arrived at 28.9 s, about 1 s before the end, and were placeholders. | The end card starts at 24.0 s. Contacts are in from 25.5–26.2 s and held static for about 4 s: **@webra.agency** · **webraagency.dev**. |
| — | Audio | About 15 impacts, many whooshes, glitch stabs and repetitive ticks. Heavy saturation. | 4 soft headline accents, 5 air transitions, subtle UI ticks, and a shared reverb bus. Sidechained groove. Mastered to −14 LUFS. |
| — | Type | English copy, Archivo/Inter, heavy 16-step purple extrusion. | Georgian copy in FiraGO. A subtle 6 px depth plus a soft shadow on headlines only. |

---

## 2 · Motion system (all scenes)

- **Easing:**
  - Arrivals: cubic-bezier(.16, 1, .3, 1).
  - Morphs and camera: cubic-bezier(.65, 0, .35, 1).
  - Exits: cubic-bezier(.6, 0, .9, .4).
- **Spring:** only for physical objects: phone arrival (ζ 0.9), result card (ζ 0.82), map pin (ζ 0.6). Nothing else overshoots.
- **Text:**
  - Each word rises out of a mask in 0.7 s. Words are 0.06–0.14 s apart and start on beats or eighth notes.
  - Exits lift the words out of the same mask in 0.35 s.
  - Every headline stays on screen for at least 2.5 s.
- **Continuity chain:** phone screen → website (desktop) → website (mobile) → search bar → (camera pan) → task chips → stripes → zebra → logo.
- **Finish:** 180° motion blur, 4.5 % grain, soft vignette, and a single key light from the top with a floor light pool.

---

## 3 · Timed storyboard (120 BPM; one beat = 0.5 s)

| Time | Picture | Georgian text (exact) | Audio |
|---|---|---|---|
| 0.00–0.35 | Fade up from black. The phone arrives on a spring from depth and orbits slowly. The profile feed scrolls gently. | — | Pad, soft air |
| 0.45 / 0.85 / 1.00 | Headline, two lines, word by word | **მხოლოდ Instagram-ის** / **გვერდი გაქვს?** | Low accent |
| 1.90 | Supporting line | შენს ბიზნესს მეტი სჭირდება. | Plucks enter |
| 3.45–3.90 | Headline lifts out | — | — |
| 3.70–4.70 | The phone squares to camera. The bezel dissolves and the screen expands into a desktop browser. | — | Air swell |
| 4.60–6.50 | The layout grid shows. Nav, hero lines, zebra image, CTA and three cards draw in. | — | 6 soft UI ticks. Groove starts at 4.0. |
| 5.00 / 5.30 | Headline and subtitle | **შექმენი.** / ვებგვერდის დიზაინი და დეველოპმენტი | Low accent |
| 7.00–8.00 | Desktop → mobile morph. Modules reflow and the nav becomes a burger icon. | — | Air |
| 8.95–9.40 | Headline lifts out | — | — |
| 9.10–10.00 | The mobile site rises and flattens into the search bar. | — | Air |
| 10.30–11.50 | The query types in (46 ms per character) | `ყვავილების მიტანა თბილისში` | Key clicks |
| 11.50 | Enter | — | Tick |
| 11.60–12.90 | The business card springs up. The map pin drops. The name, category and action chips reveal. Two rings pulse. | შენი ბიზნესი · ყვავილების მაღაზია · თბილისი · ვებგვერდი · მარშრუტი · დარეკვა | Bell |
| 12.00 / 12.30 / 12.50 | Headline and two-line subtitle | **გამოჩნდი.** / SEO და Google Business Profile-ის / ოპტიმიზაცია | Low accent |
| 14.60–14.90 | Headline lifts out | — | — |
| 14.90–15.90 | Vertical camera pan down into the automation space | — | Air |
| 15.60–17.00 | Manual state: a calm pile of task chips | ხელით · ახალი მოთხოვნა · ჯავშნის დადასტურება · ინვოისი · შეხსენება · პასუხი კლიენტს · კვირის ანგარიში | — |
| 17.00–18.20 | Chips glide into a pipeline. The spine draws, nodes and connectors grow in. The label changes. | ავტომატურად | — |
| 18.00 / 18.30 | Headline and subtitle | **ავტომატიზაცია.** / რუტინული ამოცანების AI ავტომატიზაცია | Low accent |
| 18.30–19.55 | Pulses flow down the spine. Each chip confirms (✓) on an eighth note. | — | Pentatonic bells |
| 20.55–20.90 | Headline lifts out. Pipeline dims. | — | Air |
| 20.75–21.50 | Chips stretch into six full-width white bars. | — | — |
| 21.40–22.80 | The bars warp into the flowing zebra pattern, with a slow −10° roll. | — | Breakdown and riser |
| 22.70–23.80 | The zebra pattern folds (subtle 3D tilt) into the logo's footprint over deep purple. | — | Riser peaks |
| **23.70–24.70** | **The original WEBRA logo resolves from the pattern (0.94 → 1).** Held to 30.0. | — | **Sonic logo on 24.0** |
| 24.60 | Tagline | **შექმენი. გამოჩნდი. ავტომატიზაცია.** | Tick |
| 25.00 / 25.15 | Call to action (two lines) | დაგვიკავშირდი და დაიწყე / შენი ბიზნესის განვითარება ონლაინ! | Tick |
| 25.40–26.20 | Contact panel. Held static to 30.0. | **@webra.agency** · **webraagency.dev** | Groove, then fade from 28.5 |

**Safe area:** all type sits between y 250 and y 1450 (1080 × 1920 frame). This clears the Reels, TikTok and Facebook caption area and action rail.

---

## 4 · Optional Georgian voiceover (native speaker, calm and confident, about 24 s)

```
მხოლოდ Instagram-ის გვერდი გაქვს? შენს ბიზნესს მეტი სჭირდება.        (0.4–3.6)
შევქმნით თანამედროვე ვებგვერდს.                                      (5.0–7.0)
დაგეხმარებით, რომ Google-ში გამოჩნდე.                                (12.0–14.2)
რუტინულ ამოცანებს კი AI ავტომატურად შეასრულებს.                      (18.0–20.5)
WEBRA — შექმენი. გამოჩნდი. ავტომატიზაცია.                            (24.0–27.0)
```
- Record it with a native Georgian voice actor. Do not use synthetic TTS.
- Mix it at −14 LUFS and duck the music by 6 dB under the voice.
- The picture timing already allows for these lines.

---

## 5 · Regeneration prompts (for a Cinema 4D / Redshift finish)

Shared prompt suffix: *"Deep purple #11061F studio cyclorama with a soft floor light pool. One large top softbox key light, a subtle violet rim light. Soft contact shadows and a faint floor reflection. Restrained, no bloom, no lens flares. Clean negative space. 9:16."*

1. **Phone:** "Matte black glass smartphone with a thin polished edge, floating 15 cm above a glossy dark floor. It turns slowly from −14° to −8° on a spring arrival. An unbranded grey social profile feed scrolls on screen."
2. **Screen → site:** "The phone squares to camera. The bezel fades and the screen's rounded rectangle expands into a white desktop browser. Layout blocks draw on a violet 12-column grid, with a zebra-stripe hero image."
3. **Site → search:** "The mobile website rises and flattens into a white pill-shaped search bar. A violet caret types. A result card with an abstract dark map, zebra-like streets and a violet pin springs up from below."
4. **Automation:** "Six translucent task chips with FiraGO Georgian labels lie in a loose pile, then glide into a vertical violet pipeline with ring nodes. Soft white pulses travel down the spine and each chip gets a violet check."
5. **Zebra → logo:** "Six white bars ripple into a flowing, tapering zebra pattern on black. The pattern folds with a gentle 3D tilt into a rounded band and dissolves into the lavender WEBRA logo on deep purple."

**After Effects rebuild:**
- Import `audio.wav` and add a marker for every row in section 3.
- Set type in FiraGO as live text layers with track mattes.
- Use `Easing: .16,1,.3,1` (Flow) for arrivals and `.65,0,.35,1` for morphs.
- Turn on motion blur with a 180° shutter.

---

## 6 · Re-render

```bash
# Put the original logo at webra-ad/v2/brand/logo.svg (or .png, transparent) first.
python3 audio.py
export FFMPEG=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
node render.js                      # -> out/webra_v2_ka_1080x1920.mp4 (~10 min, motion blur)
node render.js --stills 1.6,5.8,12.9,19,26.5
```
All copy lives in the `COPY` object at the top of `index.html`.
