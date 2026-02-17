

# Competitive Analysis & Strategy to Beat This Script

## What They Do Well (Respect the Competition)

| Feature | Quality |
|---|---|
| SmoothDamp physics | Solid implementation |
| Preset system (save/load/delete) | Nice UX |
| Cross-platform (Win/Linux/Mac) | Broad reach |
| Cursor overlay with shape detection | Clever |
| Dead zone for follow | Polished detail |
| Dual blur system (zoom + motion) | Visual flair |

---

## Their Weaknesses (Your Attack Surface)

### 1. **Blur requires an external plugin**
```
-- Their code literally says:
"Requires 'Composite Blur' plugin.\nSet up filters named 'Zoom Blur' and 'Motion Blur' manually."
```
Users must install a *separate* plugin AND manually create named filters. **Massive friction.**

**→ Beat them:** Ship blur built-in via shader, or auto-create the filters programmatically.

---

### 2. **No dynamic zoom level (scroll-to-zoom)**
They only have toggle zoom in/out at a fixed factor. No gradual zooming.

```lua
-- Their zoom is binary:
zoom_value = 2  -- fixed
-- on_toggle_zoom just flips between zoomed/not zoomed
```

**→ Beat them:** Add scroll-wheel zoom with smooth interpolation between levels:
```lua
function on_scroll(delta)
    zoom_value = clamp(1.0, 10.0, zoom_value + delta * 0.3)
    -- Smoothly animate to new level while already zoomed
end
```

---

### 3. **No area/region zoom**
They can only zoom to cursor position. No way to draw a rectangle or save zoom bookmarks.

**→ Beat them:** Add:
- **Drag-to-zoom** (select a rectangle)
- **Zoom bookmarks** (save named positions: "code editor", "terminal", "browser")
- **Hotkey per bookmark**

---

### 4. **Cursor overlay is manual and fragile**
Users must create an image source, name it, position it manually. Two sources for arrow + pointer.

```lua
-- They require manual source creation:
cursor_source_name = ""        -- user picks an image source
cursor_pointer_source_name = "" -- user picks ANOTHER image source
```

**→ Beat them:** Auto-create the cursor source programmatically, or bundle cursor images and handle everything internally.

---

### 5. **No picture-in-picture / mini-map**
When zoomed, you lose context of where you are on screen.

**→ Beat them:** Add an optional PiP overlay showing the full screen with a highlight box of the zoomed region.

---

### 6. **Performance: 1ms timer with heavy FFI every tick**
```lua
obs.timer_add(on_timer, 1)  -- 1ms interval
-- Every tick: FFI cursor query + SmoothDamp + filter updates + blur updates
```

**→ Beat them:** Use `obs_get_frame_interval_ns()` to sync to actual frame rate, batch filter updates, skip unchanged frames.

---

### 7. **No multi-source / multi-scene support**
Only one zoom source at a time. Scene switching requires manual re-selection.

**→ Beat them:** Auto-detect the correct source per scene, or allow configuring per-scene zoom targets.

---

### 8. **Their easing library is tiny**
Only 3 functions: `Cubic.EaseOut`, `Expo.EaseOut`, `Back.EaseOut`

**→ Beat them:** Ship a full easing library (20+ curves) with visual preview:
```lua
Easing = {
    Linear, Quad, Cubic, Quart, Quint, Sine, Expo, Circ,
    Back, Elastic, Bounce  -- each with In, Out, InOut
}
```

---

### 9. **No stream deck / external API**
Their socket is basic UDP for mouse position only.

**→ Beat them:** Add a proper control API:
```
ZOOM 2.5          -- set zoom level
PAN 100 200       -- pan to position
FOLLOW ON/OFF     -- toggle follow
PRESET Smooth     -- apply preset
BOOKMARK myspot   -- jump to saved position
```

---

### 10. **UI is cluttered**
~30 settings crammed into groups. No visual feedback.

**→ Beat them:**
- Wizard-style first-run setup
- Live preview in the settings panel
- Sensible progressive disclosure (hide advanced by default)

---

## Your Differentiation Roadmap

### Tier 1 — Table Stakes (Must Match)
- [ ] Smooth zoom with easing
- [ ] Mouse follow with SmoothDamp
- [ ] Hotkey toggle
- [ ] Cross-platform
- [ ] Presets

### Tier 2 — Leapfrog Features (Beat Them)
- [ ] **Scroll-wheel zoom** (dynamic zoom level)
- [ ] **Zero-config blur** (no external plugin)
- [ ] **Auto cursor overlay** (no manual setup)
- [ ] **Per-scene source memory**
- [ ] **Zoom bookmarks with hotkeys**

### Tier 3 — Moat Features (They Can't Easily Copy)
- [ ] **Mini-map PiP overlay**
- [ ] **Drag-to-zoom region selection**
- [ ] **Stream Deck plugin / rich API**
- [ ] **Visual easing curve editor**
- [ ] **Record & replay zoom paths**

---

## Quick Win: The "10-Second Setup" Pitch

Their setup requires:
1. Install script
2. Install Composite Blur plugin
3. Create image source for cursor
4. Create another for pointer cursor
5. Create "Zoom Blur" filter manually
6. Create "Motion Blur" filter manually
7. Select zoom source
8. Configure 15+ settings
9. Set hotkey

**Your pitch:** *"Install → Set hotkey → Done. Everything else is automatic."*

That alone wins the market.



# Product Requirements Document (PRD)

## OBS Zoom Pro — Intelligent Camera Zoom for OBS Studio

---

| Field | Value |
|---|---|
| **Product Name** | OBS Zoom Pro |
| **Version** | 1.0 |
| **Author** | [Your Name] |
| **Date** | June 2025 |
| **Status** | Draft |
| **Platform** | OBS Studio 29.0+ (Windows, Linux, macOS) |
| **Language** | Lua (OBS Script API + LuaJIT FFI) |

---

## 1. Executive Summary

OBS Zoom Pro is a free, open-source OBS Lua script that provides smooth, cinematic zoom-to-mouse functionality for streamers, educators, and content creators. It differentiates from existing solutions by requiring **zero external dependencies**, offering **10-second setup**, and providing advanced features like scroll-wheel zoom, zoom bookmarks, mini-map overlay, and a rich external control API — all without installing any additional plugins.

### Core Value Proposition

> **"Install → Set hotkey → Done."**
> Everything auto-configures. No external plugins. No manual filter creation. No image source setup.

---

## 2. Problem Statement

### User Pain Points (Current Solutions)

| # | Pain Point | Severity |
|---|---|---|
| P1 | Requires installing external blur plugin separately | High |
| P2 | Cursor overlay requires manually creating 2 image sources and configuring them | High |
| P3 | Blur filters must be manually created and named exactly | High |
| P4 | Only binary zoom (in/out) — no gradual zoom control | Medium |
| P5 | No way to save zoom positions for repeated use | Medium |
| P6 | Loses spatial context when zoomed (no mini-map) | Medium |
| P7 | Single zoom source, no per-scene memory | Medium |
| P8 | 15+ settings must be configured before first use | High |
| P9 | No integration with Stream Deck or external tools | Low |
| P10 | No visual feedback during configuration | Medium |

### Target Users

| Persona | Description | Primary Need |
|---|---|---|
| **Coding Streamer** | Streams programming, needs to zoom into code | Quick zoom, readable text, keyboard-driven |
| **Educator** | Records tutorials, zooms into UI elements | Bookmarks, smooth transitions, professional look |
| **Gaming Streamer** | Highlights moments in gameplay | Fast snap zoom, scroll control, cinematic blur |
| **Corporate Presenter** | OBS for meetings/webinars | Zero-config, reliable, polished |

---

## 3. Goals & Success Metrics

### Goals

| # | Goal | Priority |
|---|---|---|
| G1 | Zero-config first run — working zoom in under 10 seconds | P0 |
| G2 | Zero external dependencies — everything ships in one script | P0 |
| G3 | Feature parity with competitor on core zoom/follow | P0 |
| G4 | Scroll-wheel dynamic zoom as headline differentiator | P0 |
| G5 | Zoom bookmarks for educators/presenters | P1 |
| G6 | Mini-map PiP overlay for spatial context | P1 |
| G7 | External control API for Stream Deck integration | P2 |
| G8 | Cross-platform (Windows primary, Linux/macOS supported) | P0 |

### Success Metrics

| Metric | Target | Measurement |
|---|---|---|
| Time to first zoom | < 10 seconds | User testing |
| Settings required before first use | ≤ 2 (source + hotkey) | Count |
| External plugins required | 0 | Count |
| GitHub stars (6 months) | > 500 | GitHub |
| Open bugs (30 days) | < 5 | Issue tracker |
| Frame rate impact at 1080p | < 2% CPU | Benchmark |

---

## 4. Scope

### In Scope (v1.0)

| Module | Features |
|---|---|
| Core Zoom | Toggle zoom, scroll-wheel zoom, smooth easing |
| Mouse Follow | SmoothDamp physics, dead zone, weighted input smoothing |
| Built-in Blur | Shader-based zoom blur + motion blur (no external plugin) |
| Auto Cursor | Programmatic cursor overlay (no manual source creation) |
| Bookmarks | Save/load named zoom positions with hotkeys |
| Presets | Built-in + user-defined animation presets |
| Auto-Config | Auto-detect display source, monitor geometry, scene changes |
| UI | Clean grouped properties, progressive disclosure, help text |

### Out of Scope (v1.0 — Future)

| Feature | Target Version |
|---|---|
| Mini-map PiP overlay | v1.1 |
| Stream Deck plugin | v1.2 |
| Drag-to-zoom region | v1.2 |
| Visual easing curve editor | v1.3 |
| Record & replay zoom paths | v2.0 |
| Multi-source simultaneous zoom | v2.0 |

---

## 5. Functional Requirements

### 5.1 Core Zoom Engine

#### FR-100: Toggle Zoom

| Field | Detail |
|---|---|
| **ID** | FR-100 |
| **Priority** | P0 |
| **Description** | User presses a hotkey to toggle zoom in/out at the current mouse position |
| **Input** | Hotkey press |
| **Behavior** | If unzoomed → animate zoom in to `zoom_level` centered on cursor. If zoomed → animate zoom out to original view. If animating → queue the reverse action to execute on completion. |
| **Output** | Smooth animated crop/scale transition |
| **Acceptance Criteria** | AC1: Zoom in completes within `zoom_duration` seconds. AC2: Zoom out returns to exact original transform. AC3: No visual jump/pop at start or end of animation. AC4: Works while source is actively rendering. |

#### FR-101: Scroll-Wheel Zoom

| Field | Detail |
|---|---|
| **ID** | FR-101 |
| **Priority** | P0 |
| **Description** | While a modifier key is held, scroll wheel adjusts zoom level continuously |
| **Input** | Modifier key (configurable, default: Ctrl) + scroll wheel delta |
| **Behavior** | Each scroll tick adjusts `zoom_level` by `scroll_step` (default 0.25). Zoom level is clamped between 1.0 and `max_zoom` (default 10.0). Transition to new level is animated using current easing settings. If `zoom_level` reaches 1.0, fully zoom out and reset. Zoom center follows mouse position during scroll. |
| **Output** | Continuously variable zoom level with smooth transitions |
| **Acceptance Criteria** | AC1: Scrolling up increases zoom, down decreases. AC2: Zoom center tracks mouse position in real time. AC3: Releasing modifier does not change zoom state. AC4: Reaching 1.0 cleanly resets to unzoomed state. |

```
State Diagram:

    [Unzoomed] --scroll up--> [Zooming In] --complete--> [Zoomed]
    [Zoomed]   --scroll up--> [Zooming In] --complete--> [Zoomed (deeper)]
    [Zoomed]   --scroll dn--> [Zooming Out] --if 1.0--> [Unzoomed]
    [Zoomed]   --scroll dn--> [Zooming Out] --if >1.0--> [Zoomed (shallower)]
    [Any]      --toggle key-> [Reverse to opposite end state]
```

#### FR-102: Zoom Animation

| Field | Detail |
|---|---|
| **ID** | FR-102 |
| **Priority** | P0 |
| **Description** | All zoom transitions use configurable easing curves |
| **Parameters** | `zoom_duration` (0.05–3.0s, default 0.6s), `zoom_overshoot` (0.0–1.0, default 0.0), `easing_function` (enum, default "CubicOut") |
| **Easing Library** | Linear, QuadIn/Out/InOut, CubicIn/Out/InOut, QuartIn/Out/InOut, QuintIn/Out/InOut, SineIn/Out/InOut, ExpoIn/Out/InOut, CircIn/Out/InOut, BackIn/Out/InOut, ElasticIn/Out/InOut, BounceIn/Out/InOut |
| **Acceptance Criteria** | AC1: 23 easing functions available. AC2: Overshoot > 0 uses BackEaseOut with configurable intensity. AC3: Animation is frame-rate independent (uses delta time). |

#### FR-103: Zoom Presets

| Field | Detail |
|---|---|
| **ID** | FR-103 |
| **Priority** | P0 |
| **Description** | Named presets that configure duration, overshoot, easing, and follow smoothness |
| **Built-in Presets** | |

| Preset | Duration | Overshoot | Smoothness | Easing |
|---|---|---|---|---|
| Smooth | 0.8s | 0.0 | 0.25 | CubicOut |
| Bounce | 0.6s | 0.35 | 0.15 | BackOut |
| Snappy | 0.3s | 0.0 | 0.05 | ExpoOut |
| Cinematic | 1.2s | 0.05 | 0.4 | SineOut |

| **Custom Presets** | Users can save/load/delete named presets. Stored in OBS settings JSON. |
| **Behavior** | Selecting a preset applies all its values to the sliders. Manually changing any slider switches preset to "Custom". |

---

### 5.2 Mouse Follow

#### FR-200: Auto-Follow Mouse

| Field | Detail |
|---|---|
| **ID** | FR-200 |
| **Priority** | P0 |
| **Description** | While zoomed, camera follows the mouse cursor smoothly |
| **Algorithm** | SmoothDamp (critically damped spring) applied to mouse input coordinates, then rigid camera tracking of smoothed output |
| **Parameters** | `follow_smooth_time` (0.01–1.0, default 0.15), `follow_dead_zone` (0–500px, default 5), `follow_outside_bounds` (bool, default false) |
| **Dead Zone Behavior** | Camera does not move until mouse exits a `dead_zone` radius circle around the last tracked position. When exiting, the tracked position is dragged toward the mouse such that it remains exactly `dead_zone` pixels away. |
| **Acceptance Criteria** | AC1: Camera is stationary when mouse is within dead zone. AC2: Camera movement is smooth and continuous (no jitter). AC3: Camera stays within source bounds unless `follow_outside_bounds` is true. AC4: Follow can be toggled independently via hotkey. |

#### FR-201: Follow Toggle Hotkey

| Field | Detail |
|---|---|
| **ID** | FR-201 |
| **Priority** | P0 |
| **Description** | Independent hotkey to enable/disable mouse follow while zoomed |
| **Behavior** | Only has effect while zoomed. Toggling off freezes camera at current position. Toggling on resumes tracking from current position (no jump). |

---

### 5.3 Built-in Blur Effects

#### FR-300: Zoom Blur (Built-in)

| Field | Detail |
|---|---|
| **ID** | FR-300 |
| **Priority** | P0 |
| **Description** | Radial zoom blur applied during zoom transitions without requiring external plugins |
| **Implementation** | Option A (preferred): Custom OBS effect/shader file loaded at runtime via `obs_source_create` with inline HLSL. Option B (fallback): Programmatically create and configure a crop-based approximation. Option C (compatibility): Auto-detect if Composite Blur plugin exists and auto-create + configure the filter (removing manual step). |
| **Parameters** | `zoom_blur_enabled` (bool, default false), `zoom_blur_intensity` (0–20, default 5), `zoom_blur_clear_radius` (0–2000px, default 150) |
| **Behavior** | Blur follows a bell curve: 0 at start → peak at 50% of transition → 0 at end. Blur is centered on the zoom target point. Clear center radius creates a sharp focus area in the middle. |
| **Acceptance Criteria** | AC1: Works without any plugin installation. AC2: Zero blur when not transitioning. AC3: No visible artifacts at transition boundaries. |

#### FR-301: Motion Blur (Built-in)

| Field | Detail |
|---|---|
| **ID** | FR-301 |
| **Priority** | P1 |
| **Description** | Directional motion blur applied during camera panning |
| **Implementation** | Same approach as FR-300 (shader or auto-create filter) |
| **Parameters** | `motion_blur_enabled` (bool, default false), `motion_blur_intensity` (0–20, default 1.0) |
| **Behavior** | Blur radius proportional to camera velocity. Blur angle matches camera movement direction. Disabled during zoom transitions to avoid visual conflict. Fades to zero when camera is stationary. |
| **Acceptance Criteria** | AC1: Works without any plugin installation. AC2: Smooth fade in/out based on velocity. AC3: No blur when camera is still. |

#### FR-302: Auto Filter Management

| Field | Detail |
|---|---|
| **ID** | FR-302 |
| **Priority** | P0 |
| **Description** | All required OBS filters are created, configured, ordered, and cleaned up automatically |
| **Behavior** | On script load: detect if required filters exist on the source. If missing: create them programmatically with correct settings. On script unload: remove all script-created filters. Filters are ordered correctly (crop last, blur on top). User never needs to manually create or name a filter. |
| **Naming Convention** | All auto-created filters prefixed with `[ZoomPro]` for identification |
| **Acceptance Criteria** | AC1: User does not interact with filters manually. AC2: Unloading script leaves source in original state. AC3: Re-loading script does not create duplicate filters. |

---

### 5.4 Auto Cursor Overlay

#### FR-400: Automatic Cursor Rendering

| Field | Detail |
|---|---|
| **ID** | FR-400 |
| **Priority** | P0 |
| **Description** | Script automatically renders a smooth cursor overlay without requiring the user to create any image sources |
| **Implementation** | Bundle default cursor images (arrow, pointer, text, loading) as base64-encoded data within the script. On first run, extract to `%APPDATA%/obs-studio/obs-zoom-pro/cursors/`. Create a hidden image source programmatically. Manage visibility, position, scale, and rotation automatically. |
| **Parameters** | `cursor_enabled` (bool, default true), `cursor_scale` (0.1–5.0, default 1.0), `cursor_smooth_time` (0.01–1.0, default 0.1), `cursor_offset_x` (-100–100, default -6), `cursor_offset_y` (-100–100, default -2) |
| **Cursor Detection (Windows)** | Use `GetCursorInfo` FFI to detect cursor shape (arrow, hand, ibeam, wait). Swap cursor image based on detected shape. |
| **Cursor Detection (Linux/macOS)** | Fallback to arrow-only cursor (shape detection not available via simple FFI). |
| **Acceptance Criteria** | AC1: Cursor overlay works on first run with zero configuration. AC2: Cursor position is smoothed independently from camera. AC3: Click animation (scale down) on left mouse button. AC4: Clean removal on script unload. |

#### FR-401: Cursor Physics

| Field | Detail |
|---|---|
| **ID** | FR-401 |
| **Priority** | P1 |
| **Description** | Optional dynamic cursor effects based on movement |
| **Modes** | |

| Mode | Behavior |
|---|---|
| None | Static upright cursor, no rotation |
| Lean | Cursor tilts left/right based on horizontal velocity, capped at ±40° |
| Directional | Cursor rotates to face movement direction |

| **Parameters** | `cursor_rotation_mode` (enum, default "None"), `cursor_angle_offset` (-180–180°, default 0), `cursor_tilt_strength` (0–2.0, default 0), `cursor_click_scale` (0.5–1.0, default 0.78) |

---

### 5.5 Zoom Bookmarks

#### FR-500: Save Zoom Position

| Field | Detail |
|---|---|
| **ID** | FR-500 |
| **Priority** | P1 |
| **Description** | Save the current zoom level and position as a named bookmark |
| **Parameters** | `bookmark_name` (string), stored zoom_level, crop_x, crop_y, crop_w, crop_h |
| **Storage** | Persisted in OBS script settings as a data array |
| **Limit** | Maximum 20 bookmarks per source |

#### FR-501: Recall Zoom Bookmark

| Field | Detail |
|---|---|
| **ID** | FR-501 |
| **Priority** | P1 |
| **Description** | Animate to a saved bookmark position |
| **Input** | Bookmark name (via UI dropdown or hotkey) |
| **Behavior** | Smoothly transition from current view to saved bookmark using current easing settings. If currently unzoomed, zoom in to the bookmark. If currently at a different bookmark, cross-fade between them. |
| **Hotkeys** | Up to 5 bookmarks can be assigned individual hotkeys (Bookmark 1–5) |

#### FR-502: Bookmark Management UI

| Field | Detail |
|---|---|
| **ID** | FR-502 |
| **Priority** | P1 |
| **Description** | UI for creating, renaming, updating, and deleting bookmarks |
| **UI Elements** | Dropdown list of bookmarks, "Save Current" button, "Delete" button, "Rename" text field, "Update Position" button |

---

### 5.6 Auto-Configuration

#### FR-600: Source Auto-Detection

| Field | Detail |
|---|---|
| **ID** | FR-600 |
| **Priority** | P0 |
| **Description** | Automatically detect and select the best zoom source |
| **Behavior** | On first run: scan all sources for display capture / game capture / window capture. If exactly one display capture exists, auto-select it. If multiple exist, present a selection dialog. Auto-detect monitor geometry (position, size, scale) from the source properties. |
| **Fallback** | If auto-detection fails, prompt user to select source and enable manual override. |

#### FR-601: Per-Scene Source Memory

| Field | Detail |
|---|---|
| **ID** | FR-601 |
| **Priority** | P1 |
| **Description** | Remember which zoom source to use for each scene |
| **Storage** | Map of `scene_name → source_name` persisted in settings |
| **Behavior** | On scene switch: look up the configured source for the new scene. If found, use it. If not found, attempt to find the globally selected source in the new scene. If neither found, disable zoom until user configures. |

#### FR-602: Transform Auto-Conversion

| Field | Detail |
|---|---|
| **ID** | FR-602 |
| **Priority** | P0 |
| **Description** | Automatically handle sources with non-standard transforms |
| **Behavior** | Detect if source uses scale transform instead of bounding box → auto-convert. Detect if source uses transform crop → auto-convert to crop filter. Detect existing crop/pad filters → account for their offsets. Restore all original settings on script unload. |

---

### 5.7 External Control API

#### FR-700: UDP Command Listener

| Field | Detail |
|---|---|
| **ID** | FR-700 |
| **Priority** | P2 |
| **Description** | Listen for control commands over UDP for Stream Deck / external tool integration |
| **Parameters** | `api_enabled` (bool, default false), `api_port` (1024–65535, default 12345) |
| **Protocol** | Plain text UDP packets, one command per packet |

#### FR-701: Command Set

| Command | Parameters | Description |
|---|---|---|
| `ZOOM_IN` | `[level]` | Zoom in to optional level (default: configured zoom_value) |
| `ZOOM_OUT` | | Zoom out to original |
| `ZOOM_SET` | `<level>` | Set zoom to exact level (1.0 = unzoomed) |
| `ZOOM_TOGGLE` | | Toggle zoom in/out |
| `FOLLOW_ON` | | Enable mouse follow |
| `FOLLOW_OFF` | | Disable mouse follow |
| `FOLLOW_TOGGLE` | | Toggle mouse follow |
| `PRESET` | `<name>` | Apply named preset |
| `BOOKMARK` | `<name>` | Jump to named bookmark |
| `PAN` | `<x> <y>` | Pan to absolute position |
| `MOUSE` | `<x> <y>` | Override mouse position (for remote) |
| `STATUS` | | Returns current zoom state as JSON |

#### FR-702: Status Response

```json
{
    "zoom_level": 2.5,
    "state": "zoomed_in",
    "following": true,
    "position": { "x": 450, "y": 300 },
    "bookmark": "code_editor",
    "preset": "Smooth"
}
```

---

## 6. Non-Functional Requirements

### 6.1 Performance

| ID | Requirement | Target |
|---|---|---|
| NFR-100 | CPU overhead at 1080p60 | < 2% single core |
| NFR-101 | CPU overhead at 4K60 | < 4% single core |
| NFR-102 | Memory usage | < 10 MB additional |
| NFR-103 | Frame rate sync | Timer interval matches OBS frame rate (no 1ms polling) |
| NFR-104 | Filter update batching | Only update OBS filters when values actually change |
| NFR-105 | Startup time | < 500ms from script load to ready |

### 6.2 Reliability

| ID | Requirement |
|---|---|
| NFR-200 | Script unload must restore source to exact original state (transform, crop, filters) |
| NFR-201 | Scene switching must not cause visual glitches or errors |
| NFR-202 | Rapid hotkey presses must not corrupt zoom state |
| NFR-203 | Script must handle missing/deleted sources gracefully (no crashes) |
| NFR-204 | OBS shutdown during zoom must clean up correctly |
| NFR-205 | Re-loading script via "Reload Scripts" must work without OBS restart |

### 6.3 Compatibility

| ID | Requirement |
|---|---|
| NFR-300 | OBS Studio 29.0 and above |
| NFR-301 | Windows 10/11 (primary, full features) |
| NFR-302 | Linux X11 (core features, no cursor shape detection) |
| NFR-303 | macOS 12+ (core features, no cursor shape detection) |
| NFR-304 | Wayland: documented as unsupported with clear error message |
| NFR-305 | Works with display capture, game capture, window capture, and cloned sources |

### 6.4 Usability

| ID | Requirement |
|---|---|
| NFR-400 | First-time setup requires ≤ 2 user actions (select source + set hotkey) |
| NFR-401 | Settings UI uses progressive disclosure (basic → advanced) |
| NFR-402 | All settings have tooltip descriptions |
| NFR-403 | Help section with quick-start guide embedded in UI |
| NFR-404 | Meaningful error messages logged to OBS script console |
| NFR-405 | Settings validation prevents invalid combinations |

---

## 7. System Architecture

### 7.1 Module Diagram

```
┌─────────────────────────────────────────────────┐
│                  OBS Zoom Pro                    │
├──────────┬──────────┬──────────┬────────────────┤
│  Input   │  Engine  │  Output  │   Config       │
│  Layer   │  Layer   │  Layer   │   Layer        │
├──────────┼──────────┼──────────┼────────────────┤
│ Mouse    │ Zoom     │ Crop     │ Settings       │
│ Detector │ State    │ Filter   │ Manager        │
│          │ Machine  │ Manager  │                │
│ Hotkey   │          │          │ Preset         │
│ Handler  │ Camera   │ Blur     │ Manager        │
│          │ Physics  │ Shader   │                │
│ Scroll   │ (Smooth  │ Manager  │ Bookmark       │
│ Handler  │  Damp)   │          │ Manager        │
│          │          │ Cursor   │                │
│ UDP API  │ Easing   │ Renderer │ Per-Scene      │
│ Listener │ Library  │          │ Memory         │
│          │          │ Source   │                │
│ Platform │ Bookmark │ State    │                │
│ FFI      │ Engine   │ Restorer │                │
└──────────┴──────────┴──────────┴────────────────┘
```

### 7.2 State Machine

```
                    ┌──────────┐
         ┌─────────│   IDLE   │──────────┐
         │         └──────────┘          │
         │ toggle       │ scroll         │ bookmark
         │ hotkey       │ wheel          │ hotkey
         ▼              ▼                ▼
    ┌──────────┐  ┌──────────────┐  ┌──────────┐
    │ ZOOMING  │  │  SCROLLING   │  │ JUMPING  │
    │   IN     │  │    ZOOM      │  │   TO     │
    └────┬─────┘  └──────┬───────┘  └────┬─────┘
         │               │               │
         │ complete      │ settle        │ complete
         ▼               ▼               ▼
    ┌─────────────────────────────────────────┐
    │              ZOOMED IN                   │
    │  ┌─────────┐  ┌──────────┐              │
    │  │FOLLOWING│◄─►│  STATIC  │              │
    │  │ MOUSE   │   │ (locked) │              │
    │  └─────────┘  └──────────┘              │
    └───────────────────┬─────────────────────┘
                        │ toggle hotkey
                        │ OR scroll to 1.0
                        ▼
                   ┌──────────┐
                   │ ZOOMING  │
                   │   OUT    │
                   └────┬─────┘
                        │ complete
                        ▼
                   ┌──────────┐
                   │   IDLE   │
                   └──────────┘
```

### 7.3 Data Flow (Per Frame)

```
1. Input Phase
   ├── Read mouse position (FFI)
   ├── Read hotkey state
   ├── Read scroll wheel delta
   └── Read UDP commands (if enabled)

2. Physics Phase
   ├── Apply dead zone to mouse input
   ├── SmoothDamp mouse input → smoothed_mouse
   ├── Calculate zoom target from smoothed_mouse
   ├── Update zoom animation (easing + dt)
   ├── SmoothDamp cursor position (independent)
   └── Calculate blur parameters from velocity

3. Output Phase (only if values changed)
   ├── Update crop filter (position + size)
   ├── Update blur filter (radius + center)
   ├── Update cursor scene item (pos + scale + rot)
   └── Update motion blur filter (radius + angle)
```

---

## 8. User Interface Specification

### 8.1 Settings Layout

```
┌─────────────────────────────────────────┐
│ OBS Zoom Pro v1.0                       │
├─────────────────────────────────────────┤
│                                         │
│ ▼ Quick Setup                           │
│   Zoom Source:     [Display Capture ▾]  │
│   Zoom Factor:     [====●=====] 2.0x   │
│   Preset:          [Smooth         ▾]  │
│                                         │
│ ▶ Animation (collapsed by default)      │
│ ▶ Mouse Follow (collapsed)             │
│ ▶ Effects (collapsed)                   │
│ ▶ Smooth Cursor (collapsed)            │
│ ▶ Bookmarks (collapsed)                │
│ ▶ Advanced & System (collapsed)        │
│ ▶ Help & FAQ (collapsed)               │
│                                         │
└─────────────────────────────────────────┘
```

### 8.2 Quick Setup (Always Visible)

| Control | Type | Default | Description |
|---|---|---|---|
| Zoom Source | Dropdown | Auto-detected | Source to zoom |
| Zoom Factor | Slider (1.0–10.0) | 2.0 | Zoom magnification |
| Preset | Dropdown | Smooth | Animation preset |

### 8.3 Animation Group

| Control | Type | Range | Default |
|---|---|---|---|
| Zoom Duration | Slider | 0.05–3.0s | 0.6s |
| Zoom Bounce | Slider | 0.0–1.0 | 0.0 |
| Easing Curve | Dropdown | 23 options | CubicOut |
| Scroll Zoom Step | Slider | 0.1–1.0 | 0.25 |
| Scroll Modifier Key | Dropdown | Ctrl/Alt/Shift | Ctrl |

### 8.4 Mouse Follow Group

| Control | Type | Range | Default |
|---|---|---|---|
| Auto-Follow | Checkbox | | true |
| Follow Weight | Slider | 0.01–1.0 | 0.15 |
| Dead Zone | Slider | 0–500px | 5 |
| Follow Outside Bounds | Checkbox | | false |

### 8.5 Effects Group

| Control | Type | Range | Default |
|---|---|---|---|
| Zoom Blur | Checkbox | | false |
| Blur Intensity | Slider | 0–20 | 5 |
| Clear Center Radius | Slider | 0–2000px | 150 |
| Motion Blur | Checkbox | | false |
| Motion Intensity | Slider | 0–20 | 1.0 |

### 8.6 Smooth Cursor Group

| Control | Type | Range | Default |
|---|---|---|---|
| Enable Cursor | Checkbox | | true |
| Cursor Scale | Slider | 0.1–5.0 | 1.0 |
| X Offset | Slider | -100–100 | -6 |
| Y Offset | Slider | -100–100 | -2 |
| Movement Rotation | Dropdown | None/Lean/Directional | None |
| Angle Offset | Slider | -180–180° | 0 |
| Tilt Strength | Slider | 0–2.0 | 0 |

### 8.7 Bookmarks Group

| Control | Type | Description |
|---|---|---|
| Bookmark List | Dropdown | Saved bookmarks |
| Jump To | Button | Animate to selected bookmark |
| Save Current | Button | Save current zoom as bookmark |
| Delete | Button | Delete selected bookmark |
| Bookmark Name | Text | Name for new bookmark |

---

## 9. Technical Specifications

### 9.1 SmoothDamp Implementation

```lua
-- Critically damped spring (Unity-style SmoothDamp)
-- Returns smoothed value and updates velocity by reference
function SmoothDamp(current, target, velocity, smoothTime, maxSpeed, dt)
    smoothTime = math.max(0.0001, smoothTime)
    local omega = 2.0 / smoothTime
    local x = omega * dt
    local exp = 1.0 / (1.0 + x + 0.48*x*x + 0.235*x*x*x)
    local change = current - target
    local maxChange = maxSpeed * smoothTime
    change = clamp(-maxChange, maxChange, change)
    local temp = (velocity.val + omega * change) * dt
    velocity.val = (velocity.val - omega * temp) * exp
    local output = (current - change) + (change + temp) * exp
    if (target - current > 0) == (output > target) then
        output = target
        velocity.val = 0
    end
    return output
end
```

### 9.2 Frame-Rate Independent Timing

```lua
function get_reliable_dt()
    local now = os.clock()
    local dt = now - last_tick_time
    last_tick_time = now
    return clamp(0.001, 0.1, dt)  -- Guard against freezes and div/zero
end

-- Timer interval synced to OBS frame rate
local frame_interval_ms = math.floor(obs.obs_get_frame_interval_ns() / 1000000)
obs.timer_add(on_timer, math.max(1, frame_interval_ms))
```

### 9.3 Easing Library

```lua
local Easing = {}

-- Generator for standard power curves
local function make_power(n)
    return {
        In    = function(t) return t^n end,
        Out   = function(t) return 1 - (1-t)^n end,
        InOut = function(t)
            if t < 0.5 then return 2^(n-1) * t^n
            else return 1 - (-2*t + 2)^n / 2 end
        end
    }
end

Easing.Linear = { In = function(t) return t end }
Easing.Quad   = make_power(2)
Easing.Cubic  = make_power(3)
Easing.Quart  = make_power(4)
Easing.Quint  = make_power(5)

Easing.Sine = {
    In    = function(t) return 1 - math.cos(t * math.pi / 2) end,
    Out   = function(t) return math.sin(t * math.pi / 2) end,
    InOut = function(t) return -(math.cos(math.pi * t) - 1) / 2 end
}

Easing.Expo = {
    In    = function(t) return t == 0 and 0 or 2^(10*t - 10) end,
    Out   = function(t) return t == 1 and 1 or 1 - 2^(-10*t) end,
    InOut = function(t)
        if t == 0 then return 0 end
        if t == 1 then return 1 end
        if t < 0.5 then return 2^(20*t - 10) / 2
        else return (2 - 2^(-20*t + 10)) / 2 end
    end
}

Easing.Back = {
    Out = function(t, s)
        s = s or 1.70158
        t = t - 1
        return t*t*((s+1)*t + s) + 1
    end
}

Easing.Bounce = {
    Out = function(t)
        if t < 1/2.75 then return 7.5625*t*t
        elseif t < 2/2.75 then t=t-1.5/2.75; return 7.5625*t*t+0.75
        elseif t < 2.5/2.75 then t=t-2.25/2.75; return 7.5625*t*t+0.9375
        else t=t-2.625/2.75; return 7.5625*t*t+0.984375 end
    end
}

Easing.Elastic = {
    Out = function(t)
        if t == 0 or t == 1 then return t end
        return 2^(-10*t) * math.sin((t*10 - 0.75) * (2*math.pi) / 3) + 1
    end
}
```

### 9.4 Built-in Blur Shader (HLSL)

```hlsl
// Zoom Blur (Radial)
uniform float4x4 ViewProj;
uniform texture2d image;
uniform float2 center;
uniform float radius;
uniform float clear_radius;

sampler_state texSampler {
    Filter   = Linear;
    AddressU = Clamp;
    AddressV = Clamp;
};

struct VertData {
    float4 pos : POSITION;
    float2 uv  : TEXCOORD0;
};

float4 PSZoomBlur(VertData v) : TARGET {
    float2 dir = v.uv - center;
    float dist = length(dir);

    if (dist < clear_radius) return image.Sample(texSampler, v.uv);

    float blur_amount = saturate((dist - clear_radius) / radius) * radius * 0.01;
    float4 color = float4(0,0,0,0);
    int samples = 16;

    for (int i = 0; i < samples; i++) {
        float t = float(i) / float(samples - 1);
        float2 offset = dir * blur_amount * t;
        color += image.Sample(texSampler, v.uv - offset);
    }

    return color / float(samples);
}
```

### 9.5 Auto Cursor Asset Management

```lua
-- Embedded cursor data (base64 PNG, ~2KB each)
local CURSOR_ASSETS = {
    arrow   = "iVBORw0KGgo...",  -- 32x32 arrow cursor PNG
    pointer = "iVBORw0KGgo...",  -- 32x32 hand pointer PNG
    ibeam   = "iVBORw0KGgo...",  -- 32x32 text cursor PNG
}

function extract_cursor_assets()
    local dir = get_asset_directory()
    for name, data in pairs(CURSOR_ASSETS) do
        local path = dir .. "/" .. name .. ".png"
        if not file_exists(path) then
            local decoded = base64_decode(data)
            write_file(path, decoded)
        end
    end
    return dir
end

function get_asset_directory()
    if ffi.os == "Windows" then
        return os.getenv("APPDATA") .. "/obs-studio/obs-zoom-pro/cursors"
    elseif ffi.os == "Linux" then
        return os.getenv("HOME") .. "/.config/obs-studio/obs-zoom-pro/cursors"
    elseif ffi.os == "OSX" then
        return os.getenv("HOME") .. "/Library/Application Support/obs-studio/obs-zoom-pro/cursors"
    end
end
```

---

## 10. Testing Plan

### 10.1 Unit Tests

| ID | Test | Expected Result |
|---|---|---|
| UT-01 | SmoothDamp converges to target | After 100 iterations, output within 0.01 of target |
| UT-02 | SmoothDamp with zero dt | No NaN/infinity, returns current |
| UT-03 | All 23 easing functions at t=0 | Returns 0 (±0.001) |
| UT-04 | All 23 easing functions at t=1 | Returns 1 (±0.001) |
| UT-05 | Clamp(min, max, value) edge cases | Correct for value < min, value > max, value = min, value = max |
| UT-06 | Dead zone: mouse inside zone | Tracked position unchanged |
| UT-07 | Dead zone: mouse exits zone | Tracked position moves, stays `dead_zone` px from mouse |
| UT-08 | Bookmark save/load roundtrip | Loaded values match saved values |

### 10.2 Integration Tests

| ID | Test | Steps | Expected |
|---|---|---|---|
| IT-01 | Basic zoom in/out | 1. Select source 2. Press hotkey 3. Press again | Smooth zoom in then out, returns to exact original |
| IT-02 | Scroll wheel zoom | 1. Hold Ctrl 2. Scroll up 3x 3. Scroll down 5x | Zoom increases then decreases, reaches 1.0 and resets |
| IT-03 | Scene switch during zoom | 1. Zoom in 2. Switch scene 3. Switch back | No crash, zoom resets, source re-acquired |
| IT-04 | Script reload during zoom | 1. Zoom in 2. Reload scripts | Source restored, no artifacts |
| IT-05 | Rapid hotkey spam | Press hotkey 20x quickly | No crash, state machine remains consistent |
| IT-06 | Missing source | 1. Select source 2. Delete it 3. Press hotkey | Graceful no-op, error logged |
| IT-07 | Blur without plugin | 1. Enable blur 2. Ensure no Composite Blur installed | Built-in blur works OR graceful fallback |
| IT-08 | Cursor auto-setup | 1. Enable cursor 2. No image sources exist | Cursor auto-created from bundled assets |
| IT-09 | Bookmark workflow | 1. Zoom 2. Save bookmark 3. Zoom out 4. Recall | Smoothly returns to saved position |
| IT-10 | UDP API commands | 1. Enable API 2. Send "ZOOM_IN 3.0" via netcat | Zoom animates to 3.0x |

### 10.3 Performance Tests

| ID | Test | Method | Target |
|---|---|---|---|
| PT-01 | Idle CPU (not zoomed) | OBS stats panel, 60s average | < 0.5% |
| PT-02 | Active zoom + follow CPU | OBS stats panel, 60s average | < 2% at 1080p60 |
| PT-03 | Active zoom + blur + cursor CPU | OBS stats panel, 60s average | < 3% at 1080p60 |
| PT-04 | Memory leak test | 1000 zoom in/out cycles, monitor RSS | < 1 MB growth |
| PT-05 | 4K source performance | PT-02 at 3840x2160 | < 4% |

### 10.4 Platform Tests

| ID | Platform | Features Tested |
|---|---|---|
| PL-01 | Windows 11, OBS 30.x | All features |
| PL-02 | Windows 10, OBS 29.1 | All features |
| PL-03 | Ubuntu 22.04, X11, OBS 30.x | Core zoom, follow, blur (no cursor shape) |
| PL-04 | macOS 14, OBS 30.x | Core zoom, follow, blur (no cursor shape) |
| PL-05 | Wayland (Linux) | Verify clear error message |

---

## 11. Release Plan

### Phase 1: Alpha (Week 1–3)

| Deliverable | Status |
|---|---|
| Core zoom engine (toggle + easing) | |
| Mouse follow with SmoothDamp | |
| Auto filter management | |
| Basic UI (Quick Setup group) | |
| Windows platform support | |
| Internal testing | |

### Phase 2: Beta (Week 4–6)

| Deliverable | Status |
|---|---|
| Scroll-wheel zoom | |
| Built-in blur (shader or auto-create) | |
| Auto cursor overlay | |
| Preset system | |
| Linux + macOS support | |
| Full UI with all groups | |
| Community beta testing | |

### Phase 3: v1.0 Release (Week 7–8)

| Deliverable | Status |
|---|---|
| Zoom bookmarks | |
| Per-scene source memory | |
| Performance optimization | |
| Documentation (README, Wiki) | |
| Demo video | |
| GitHub release | |

### Phase 4: v1.1+ (Post-Launch)

| Deliverable | Target |
|---|---|
| Mini-map PiP overlay | v1.1 |
| Stream Deck plugin | v1.2 |
| Drag-to-zoom | v1.2 |
| Visual easing editor | v1.3 |
| Zoom path recording | v2.0 |

---

## 12. Risks & Mitigations

| # | Risk | Probability | Impact | Mitigation |
|---|---|---|---|---|
| R1 | OBS Lua API doesn't support custom shaders directly | High | High | Fallback: auto-create Composite Blur filters programmatically (still zero manual work). Document as optional dependency. |
| R2 | Cursor shape detection fails on some Windows configs | Medium | Low | Fallback to arrow-only cursor. Log clear warning. |
| R3 | Auto-created sources conflict with user's scene setup | Medium | Medium | Use unique prefix `[ZoomPro]`. Add "Clean Up" button. |
| R4 | Performance regression on 4K with blur | Medium | Medium | Make blur sample count configurable. Default to 8 samples at 4K. |
| R5 | OBS API changes break script in future versions | Low | High | Version-gate FFI calls (already needed). Maintain compatibility matrix. |
| R6 | Scroll-wheel conflicts with other OBS scroll bindings | Medium | Medium | Require modifier key. Make modifier configurable. |
| R7 | Base64 cursor images increase script file size | Low | Low | ~10KB total. Acceptable. Offer "download assets on first run" alternative. |

---

## 13. Competitive Comparison Matrix

| Feature | Competitor | OBS Zoom Pro (v1.0) |
|---|---|---|
| Toggle zoom | ✅ | ✅ |
| Scroll-wheel zoom | ❌ | ✅ |
| Smooth easing | ✅ (3 curves) | ✅ (23 curves) |
| SmoothDamp follow | ✅ | ✅ |
| Dead zone | ✅ | ✅ |
| Animation presets | ✅ | ✅ (+ per-preset easing) |
| Custom presets | ✅ | ✅ |
| Zoom blur | ⚠️ Requires plugin + manual filter | ✅ Built-in |
| Motion blur | ⚠️ Requires plugin + manual filter | ✅ Built-in |
| Cursor overlay | ⚠️ Manual image source setup | ✅ Automatic |
| Cursor shape detection | ✅ (Windows) | ✅ (Windows) |
| Cursor physics | ✅ | ✅ |
| Zoom bookmarks | ❌ | ✅ |
| Per-scene memory | ❌ | ✅ |
| Auto source detection | ❌ | ✅ |
| External API | ⚠️ Mouse position only | ✅ Full command set |
| Mini-map overlay | ❌ | 🔜 v1.1 |
| Setup time | ~5 min | ~10 sec |
| External dependencies | Composite Blur plugin | None |
| Cross-platform | ✅ | ✅ |

---

## 14. Open Questions

| # | Question | Owner | Status |
|---|---|---|---|
| Q1 | Can OBS Lua load custom `.effect` shader files at runtime? Need to verify `obs_source_create` with custom filter. | Engineering | Open |
| Q2 | What is the best fallback if shaders aren't possible? Auto-create Composite Blur filters is plan B — is auto-installing the plugin from script possible? | Engineering | Open |
| Q3 | Should scroll-wheel zoom work when OBS is not focused (global hook)? This is platform-specific and may have security implications. | Product | Open |
| Q4 | What cursor images should we bundle? Arrow + Hand minimum. IBeam and Wait are nice-to-have. Need to ensure licensing. | Design | Open |
| Q5 | Should bookmarks be global or per-source? Per-source is more correct but more complex. | Product | Leaning per-source |
| Q6 | UDP vs WebSocket for API? WebSocket is more robust but luasocket may not support it natively. | Engineering | Leaning UDP |

---

## Appendix A: Hotkey Defaults

| Action | Default Hotkey | Configurable |
|---|---|---|
| Toggle Zoom | (User sets in OBS Hotkeys) | Yes |
| Toggle Follow | (User sets in OBS Hotkeys) | Yes |
| Scroll Zoom Modifier | Ctrl | Yes |
| Bookmark 1–5 | (User sets in OBS Hotkeys) | Yes |

## Appendix B: File Structure

```
obs-zoom-pro/
├── obs-zoom-pro.lua          # Main script (~1500 lines target)
├── README.md                 # Documentation
├── LICENSE                   # MIT License
├── CHANGELOG.md             # Version history
├── assets/
│   ├── cursors/
│   │   ├── arrow.png        # 32x32 default arrow
│   │   ├── pointer.png      # 32x32 hand pointer
│   │   └── ibeam.png        # 32x32 text cursor
│   └── shaders/
│       ├── zoom_blur.effect # Radial zoom blur shader
│       └── motion_blur.effect # Directional motion blur shader
└── examples/
    ├── streamdeck-profile.json
    └── api-client.py         # Example UDP client
```

## Appendix C: Glossary

| Term | Definition |
|---|---|
| SmoothDamp | A critically damped spring algorithm that smoothly interpolates a value toward a target with natural deceleration |
| Dead Zone | A radius around the mouse position within which movement is ignored to prevent micro-jitters |
| Easing | A mathematical function that controls the rate of change of an animation over time |
| Crop Filter | An OBS filter that removes pixels from the edges of a source, used here to simulate zooming |
| Bounding Box | An OBS transform mode that scales the source to fit within a defined rectangle |
| Scene Item | An instance of a source placed within an OBS scene, with its own transform properties |



# Implementation Plan — OBS Zoom Pro v1.0

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Module Breakdown](#2-module-breakdown)
3. [Phase 1: Core Engine (Week 1–2)](#3-phase-1)
4. [Phase 2: Smart Features (Week 3–4)](#4-phase-2)
5. [Phase 3: Effects & Cursor (Week 5–6)](#5-phase-3)
6. [Phase 4: Bookmarks & API (Week 6–7)](#6-phase-4)
7. [Phase 5: Polish & Release (Week 7–8)](#7-phase-5)
8. [File Structure](#8-file-structure)
9. [Dependency Graph](#9-dependency-graph)
10. [Risk Register & Contingencies](#10-risk-register)
11. [Testing Strategy Per Phase](#11-testing-strategy)
12. [Definition of Done](#12-definition-of-done)

---

## 1. Architecture Overview

### Single-File Core + Asset Directory

```
obs-zoom-pro.lua          ← Single entry point (~2000 lines)
assets/
  cursors/
    arrow.png
    pointer.png
    ibeam.png
  shaders/
    zoom_blur.effect
    motion_blur.effect
```

### Runtime Module Map

```
┌──────────────────────────────────────────────────────────────┐
│                       obs-zoom-pro.lua                       │
│                                                              │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐ │
│  │  PLATFORM   │  │   SETTINGS   │  │     OBS HOOKS       │ │
│  │   LAYER     │  │   MANAGER    │  │                     │ │
│  │             │  │              │  │ script_load          │ │
│  │ get_mouse() │  │ script_      │  │ script_unload        │ │
│  │ get_scroll()│  │  defaults()  │  │ script_update        │ │
│  │ get_click() │  │ script_      │  │ script_save          │ │
│  │ get_cursor_ │  │  properties()│  │ on_frontend_event    │ │
│  │  shape()    │  │ script_      │  │ on_transition_start  │ │
│  │             │  │  update()    │  │                     │ │
│  └──────┬──────┘  └──────┬───────┘  └──────────┬──────────┘ │
│         │                │                      │            │
│         ▼                ▼                      ▼            │
│  ┌──────────────────────────────────────────────────────┐    │
│  │                    ENGINE CORE                       │    │
│  │                                                      │    │
│  │  ┌────────────┐  ┌────────────┐  ┌───────────────┐  │    │
│  │  │   ZOOM     │  │  CAMERA    │  │   EASING      │  │    │
│  │  │   STATE    │  │  PHYSICS   │  │   LIBRARY     │  │    │
│  │  │  MACHINE   │  │            │  │               │  │    │
│  │  │            │  │ SmoothDamp │  │ 23 functions   │  │    │
│  │  │ IDLE       │  │ DeadZone   │  │ make_power()  │  │    │
│  │  │ ZOOMING_IN │  │ Clamp      │  │ Sine/Expo/    │  │    │
│  │  │ ZOOMED_IN  │  │ Lerp       │  │ Back/Bounce/  │  │    │
│  │  │ ZOOMING_OUT│  │            │  │ Elastic       │  │    │
│  │  │ SCROLLING  │  │            │  │               │  │    │
│  │  │ JUMPING    │  │            │  │               │  │    │
│  │  └─────┬──────┘  └─────┬──────┘  └───────┬───────┘  │    │
│  │        │               │                  │          │    │
│  │        ▼               ▼                  ▼          │    │
│  │  ┌──────────────────────────────────────────────┐    │    │
│  │  │              OUTPUT PIPELINE                  │    │    │
│  │  │                                              │    │    │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────────┐ │    │    │
│  │  │  │  CROP    │ │  BLUR    │ │   CURSOR     │ │    │    │
│  │  │  │  FILTER  │ │  MANAGER │ │   RENDERER   │ │    │    │
│  │  │  │  MGR     │ │          │ │              │ │    │    │
│  │  │  │          │ │ Zoom Blur│ │ Auto-create  │ │    │    │
│  │  │  │ create   │ │ Motion   │ │ Position     │ │    │    │
│  │  │  │ update   │ │ Auto-    │ │ Scale        │ │    │    │
│  │  │  │ destroy  │ │ create   │ │ Rotation     │ │    │    │
│  │  │  │ restore  │ │ Shader   │ │ Shape swap   │ │    │    │
│  │  │  └──────────┘ └──────────┘ └──────────────┘ │    │    │
│  │  └──────────────────────────────────────────────┘    │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │                  EXTENSION MODULES                    │    │
│  │                                                      │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │    │
│  │  │ BOOKMARK │  │ SCENE    │  │   UDP API        │   │    │
│  │  │ MANAGER  │  │ MEMORY   │  │   SERVER         │   │    │
│  │  │          │  │          │  │                  │   │    │
│  │  │ save     │  │ per-scene│  │ command parser   │   │    │
│  │  │ load     │  │ source   │  │ status response  │   │    │
│  │  │ delete   │  │ mapping  │  │                  │   │    │
│  │  │ hotkeys  │  │ auto-    │  │                  │   │    │
│  │  │          │  │ switch   │  │                  │   │    │
│  │  └──────────┘  └──────────┘  └──────────────────┘   │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

### Data Flow Per Frame

```
┌──────────────────────────────────────────────────┐
│                   on_timer()                      │
│                                                  │
│  1. TIMING                                       │
│     dt = get_reliable_dt()                       │
│                                                  │
│  2. INPUT                                        │
│     raw_mouse = platform.get_mouse_pos()         │
│     click_state = platform.get_click()           │
│     cursor_shape = platform.get_cursor_shape()   │
│     scroll_delta = scroll_accumulator.consume()  │
│     api_commands = udp_server.poll()             │
│                                                  │
│  3. PROCESS INPUT                                │
│     tracked_mouse = dead_zone.apply(raw_mouse)   │
│     smooth_mouse = SmoothDamp(tracked_mouse)     │
│                                                  │
│  4. STATE MACHINE                                │
│     new_state = state_machine.update(            │
│       dt, smooth_mouse, scroll_delta, commands   │
│     )                                            │
│                                                  │
│  5. CAMERA                                       │
│     crop = camera.compute_crop(                  │
│       state, smooth_mouse, easing, dt            │
│     )                                            │
│                                                  │
│  6. DIFF & OUTPUT (skip if unchanged)            │
│     if crop ~= last_crop then                    │
│       crop_filter.update(crop)                   │
│     end                                          │
│     blur_manager.update(state, crop, velocity)   │
│     cursor_renderer.update(                      │
│       raw_mouse, crop, zoom_level, click, shape  │
│     )                                            │
│                                                  │
│  7. BOOKKEEPING                                  │
│     last_crop = crop                             │
│     last_camera_pos = {crop.x, crop.y}           │
└──────────────────────────────────────────────────┘
```

---

## 2. Module Breakdown

Each module below is a logical grouping of functions within the single Lua file. They are separated by clear comment headers and can be independently tested.

### Module Registry

| # | Module | Lines (Est.) | Dependencies | Priority |
|---|---|---|---|---|
| M01 | Platform Layer | ~150 | FFI | P0, Phase 1 |
| M02 | Math Utilities | ~50 | None | P0, Phase 1 |
| M03 | Easing Library | ~120 | M02 | P0, Phase 1 |
| M04 | SmoothDamp | ~40 | M02 | P0, Phase 1 |
| M05 | State Machine | ~100 | None | P0, Phase 1 |
| M06 | Camera Physics | ~150 | M02, M03, M04, M05 | P0, Phase 1 |
| M07 | Crop Filter Manager | ~120 | OBS API | P0, Phase 1 |
| M08 | Source Manager | ~200 | OBS API, M07 | P0, Phase 1 |
| M09 | Timer & Main Loop | ~150 | All above | P0, Phase 1 |
| M10 | Scroll Zoom | ~80 | M05, M06, M01 | P0, Phase 2 |
| M11 | Auto Source Detection | ~60 | M08 | P1, Phase 2 |
| M12 | Scene Memory | ~80 | M08, OBS API | P1, Phase 2 |
| M13 | Preset Manager | ~100 | Settings | P0, Phase 2 |
| M14 | Blur Manager | ~150 | OBS API, M07 | P1, Phase 3 |
| M15 | Cursor Renderer | ~200 | OBS API, M01, M04 | P1, Phase 3 |
| M16 | Cursor Asset Manager | ~80 | File I/O | P1, Phase 3 |
| M17 | Bookmark Manager | ~120 | Settings, M06 | P1, Phase 4 |
| M18 | UDP API Server | ~120 | Socket | P2, Phase 4 |
| M19 | Settings UI | ~250 | OBS API, All | P0, Phase 5 |
| M20 | Logging & Debug | ~40 | None | P0, Phase 1 |
| | **Total** | **~2460** | | |

---

## 3. Phase 1: Core Engine (Week 1–2)

### Goal
Functional zoom in/out with smooth animation and mouse follow. No blur, no cursor, no extras. This is the minimum viable product that matches the competitor's core.

### Task List

#### Week 1: Foundation

| Task | Module | Hours | Description |
|---|---|---|---|
| **T-100** | M20 | 1 | **Logging system** — `log(msg)`, `log_table(tbl)`, `debug_logs` flag |
| **T-101** | M02 | 1 | **Math utilities** — `clamp()`, `lerp()`, `distance()`, `normalize()` |
| **T-102** | M03 | 3 | **Easing library** — All 23 functions with `make_power()` generator |
| **T-103** | M04 | 1 | **SmoothDamp** — Critically damped spring, velocity-by-reference pattern |
| **T-104** | M01 | 4 | **Platform layer** — Mouse position (Win/Linux/Mac FFI), click detection (Win), cursor shape (Win) |
| **T-105** | M05 | 3 | **State machine** — Define states, transitions, guard conditions |
| **T-106** | M07 | 4 | **Crop filter manager** — `create()`, `update()`, `destroy()`, `restore_original()` |
| **T-107** | M08 | 6 | **Source manager** — Find sceneitem in scene hierarchy, capture original transform, convert non-bbox transforms, handle existing crop filters |
| **T-108** | M06 | 4 | **Camera physics** — `get_target_position()`, dead zone, monitor offset calculation |

**Week 1 Deliverable:** All foundation modules written and individually testable.

#### Week 1 Implementation Details

**T-102: Easing Library**

```lua
--================================================
-- MODULE: Easing Library (M03)
--================================================
local Easing = {}

-- Power curve generator
local function make_power(n)
    return {
        In = function(t) return t ^ n end,
        Out = function(t) return 1 - (1 - t) ^ n end,
        InOut = function(t)
            if t < 0.5 then
                return 2 ^ (n - 1) * t ^ n
            else
                return 1 - (-2 * t + 2) ^ n / 2
            end
        end
    }
end

Easing.Linear = {
    In = function(t) return t end,
    Out = function(t) return t end,
    InOut = function(t) return t end
}
Easing.Quad = make_power(2)
Easing.Cubic = make_power(3)
Easing.Quart = make_power(4)
Easing.Quint = make_power(5)

Easing.Sine = {
    In = function(t) return 1 - math.cos(t * math.pi / 2) end,
    Out = function(t) return math.sin(t * math.pi / 2) end,
    InOut = function(t) return -(math.cos(math.pi * t) - 1) / 2 end
}

Easing.Expo = {
    In = function(t) return t == 0 and 0 or 2 ^ (10 * t - 10) end,
    Out = function(t) return t == 1 and 1 or 1 - 2 ^ (-10 * t) end,
    InOut = function(t)
        if t == 0 then return 0 end
        if t == 1 then return 1 end
        if t < 0.5 then return 2 ^ (20 * t - 10) / 2 end
        return (2 - 2 ^ (-20 * t + 10)) / 2
    end
}

Easing.Circ = {
    In = function(t) return 1 - math.sqrt(1 - t * t) end,
    Out = function(t)
        t = t - 1
        return math.sqrt(1 - t * t)
    end,
    InOut = function(t)
        if t < 0.5 then
            return (1 - math.sqrt(1 - (2 * t) ^ 2)) / 2
        else
            return (math.sqrt(1 - (-2 * t + 2) ^ 2) + 1) / 2
        end
    end
}

Easing.Back = {
    In = function(t, s)
        s = s or 1.70158
        return t * t * ((s + 1) * t - s)
    end,
    Out = function(t, s)
        s = s or 1.70158
        t = t - 1
        return t * t * ((s + 1) * t + s) + 1
    end,
    InOut = function(t, s)
        s = (s or 1.70158) * 1.525
        if t < 0.5 then
            return ((2 * t) ^ 2 * ((s + 1) * 2 * t - s)) / 2
        else
            return ((2 * t - 2) ^ 2 * ((s + 1) * (2 * t - 2) + s) + 2) / 2
        end
    end
}

Easing.Elastic = {
    In = function(t)
        if t == 0 or t == 1 then return t end
        return -2 ^ (10 * t - 10) * math.sin((t * 10 - 10.75) * (2 * math.pi) / 3)
    end,
    Out = function(t)
        if t == 0 or t == 1 then return t end
        return 2 ^ (-10 * t) * math.sin((t * 10 - 0.75) * (2 * math.pi) / 3) + 1
    end,
    InOut = function(t)
        if t == 0 or t == 1 then return t end
        if t < 0.5 then
            return -(2 ^ (20 * t - 10) * math.sin((20 * t - 11.125) * (2 * math.pi) / 4.5)) / 2
        else
            return (2 ^ (-20 * t + 10) * math.sin((20 * t - 11.125) * (2 * math.pi) / 4.5)) / 2 + 1
        end
    end
}

Easing.Bounce = {
    Out = function(t)
        local n1 = 7.5625
        local d1 = 2.75
        if t < 1 / d1 then return n1 * t * t
        elseif t < 2 / d1 then t = t - 1.5 / d1; return n1 * t * t + 0.75
        elseif t < 2.5 / d1 then t = t - 2.25 / d1; return n1 * t * t + 0.9375
        else t = t - 2.625 / d1; return n1 * t * t + 0.984375 end
    end,
    In = function(t) return 1 - Easing.Bounce.Out(1 - t) end,
    InOut = function(t)
        if t < 0.5 then return (1 - Easing.Bounce.Out(1 - 2 * t)) / 2
        else return (1 + Easing.Bounce.Out(2 * t - 1)) / 2 end
    end
}

-- Lookup table for settings UI
Easing.NAMES = {
    "Linear.In",
    "Quad.In", "Quad.Out", "Quad.InOut",
    "Cubic.In", "Cubic.Out", "Cubic.InOut",
    "Quart.In", "Quart.Out", "Quart.InOut",
    "Quint.In", "Quint.Out", "Quint.InOut",
    "Sine.In", "Sine.Out", "Sine.InOut",
    "Expo.In", "Expo.Out", "Expo.InOut",
    "Circ.In", "Circ.Out", "Circ.InOut",
    "Back.In", "Back.Out", "Back.InOut",
    "Elastic.In", "Elastic.Out", "Elastic.InOut",
    "Bounce.In", "Bounce.Out", "Bounce.InOut",
}

-- Resolve "Cubic.Out" → Easing.Cubic.Out
function Easing.get(name, overshoot)
    local family, direction = name:match("(%w+)%.(%w+)")
    if not family then return Easing.Cubic.Out end
    local f = Easing[family]
    if not f then return Easing.Cubic.Out end
    local fn = f[direction]
    if not fn then return Easing.Cubic.Out end

    -- Wrap Back/Elastic to pass overshoot
    if family == "Back" and overshoot and overshoot > 0 then
        return function(t) return fn(t, overshoot * 3.0) end
    end
    return fn
end
```

**T-105: State Machine**

```lua
--================================================
-- MODULE: State Machine (M05)
--================================================
local ZoomState = {
    IDLE         = "idle",
    ZOOMING_IN   = "zooming_in",
    ZOOMED_IN    = "zoomed_in",
    ZOOMING_OUT  = "zooming_out",
    SCROLLING    = "scrolling",    -- Scroll wheel mid-transition
    JUMPING      = "jumping",      -- Bookmark transition
}

local StateMachine = {
    state = ZoomState.IDLE,
    zoom_time = 0,          -- Animation progress (0 → 1)
    zoom_level = 1.0,       -- Current zoom factor
    target_level = 1.0,     -- Target zoom factor
    start_crop = nil,       -- Crop at animation start
    target_crop = nil,      -- Crop at animation end
    following = false,      -- Mouse follow active

    -- Transition guards
    can_zoom_in = function(self)
        return self.state == ZoomState.IDLE
    end,
    can_zoom_out = function(self)
        return self.state == ZoomState.ZOOMED_IN
            or self.state == ZoomState.SCROLLING
    end,
    can_scroll = function(self)
        return self.state == ZoomState.ZOOMED_IN
            or self.state == ZoomState.IDLE
            or self.state == ZoomState.SCROLLING
    end,
    can_jump = function(self)
        return self.state ~= ZoomState.ZOOMING_IN
           and self.state ~= ZoomState.ZOOMING_OUT
           and self.state ~= ZoomState.JUMPING
    end,
    is_animating = function(self)
        return self.state == ZoomState.ZOOMING_IN
            or self.state == ZoomState.ZOOMING_OUT
            or self.state == ZoomState.SCROLLING
            or self.state == ZoomState.JUMPING
    end,
    is_zoomed = function(self)
        return self.state ~= ZoomState.IDLE
    end,
}

function StateMachine:transition(new_state, params)
    local old = self.state
    self.state = new_state
    self.zoom_time = 0

    if params then
        if params.start_crop then self.start_crop = params.start_crop end
        if params.target_crop then self.target_crop = params.target_crop end
        if params.target_level then self.target_level = params.target_level end
    end

    log("State: " .. old .. " → " .. new_state)
end

function StateMachine:complete()
    if self.state == ZoomState.ZOOMING_IN or self.state == ZoomState.SCROLLING or self.state == ZoomState.JUMPING then
        self.zoom_level = self.target_level
        self:transition(ZoomState.ZOOMED_IN)
    elseif self.state == ZoomState.ZOOMING_OUT then
        self.zoom_level = 1.0
        self.target_level = 1.0
        self:transition(ZoomState.IDLE)
    end
end

function StateMachine:reset()
    self.state = ZoomState.IDLE
    self.zoom_time = 0
    self.zoom_level = 1.0
    self.target_level = 1.0
    self.start_crop = nil
    self.target_crop = nil
    self.following = false
end
```

#### Week 2: Integration & Main Loop

| Task | Module | Hours | Description |
|---|---|---|---|
| **T-200** | M09 | 6 | **Main timer loop** — `on_timer()` with proper dt, input → physics → output pipeline |
| **T-201** | M09 | 3 | **Hotkey handlers** — `on_toggle_zoom()`, `on_toggle_follow()`, state machine integration |
| **T-202** | M08 | 3 | **Monitor info detection** — Parse display name, handle overrides |
| **T-203** | M08 | 2 | **Transform restoration** — Ensure `release_sceneitem()` perfectly restores original state |
| **T-204** | M09 | 2 | **OBS lifecycle hooks** — `script_load`, `script_unload`, `on_frontend_event`, `on_transition_start` |
| **T-205** | M19 | 4 | **Minimal UI** — Source dropdown, zoom factor slider, duration slider, follow checkbox |
| **T-206** | — | 4 | **Integration testing** — End-to-end zoom in/out, follow, scene switch, script reload |
| **T-207** | — | 2 | **Bug fixes from testing** |

**Week 2 Deliverable:** Working zoom script with smooth animation and mouse follow. No extras.

#### T-200: Main Loop Implementation

```lua
--================================================
-- MODULE: Timer & Main Loop (M09)
--================================================
local FILTER_PREFIX = "[ZoomPro] "

-- Timing
local last_tick_time = 0
local function get_dt()
    local now = os.clock()
    local dt = now - last_tick_time
    last_tick_time = now
    return clamp(0.001, 0.1, dt)
end

-- Frame diff tracking (skip updates if nothing changed)
local last_output = { x = -1, y = -1, w = -1, h = -1 }

function on_timer()
    local dt = get_dt()

    -- Guard: No valid source
    if not crop_filter or not SM:is_zoomed() then
        -- Still update cursor if enabled
        cursor_renderer_update(dt)
        return
    end

    --==========================
    -- 1. INPUT
    --==========================
    local raw_mouse = platform_get_mouse_pos()

    --==========================
    -- 2. PROCESS INPUT
    --==========================
    local effective_mouse = dead_zone_apply(raw_mouse, dt)
    local smooth_mouse = camera_smooth_input(effective_mouse, dt)

    --==========================
    -- 3. STATE MACHINE UPDATE
    --==========================
    if SM:is_animating() then
        SM.zoom_time = SM.zoom_time + (dt / cfg.zoom_duration)
    end

    --==========================
    -- 4. CAMERA POSITION
    --==========================
    local crop = compute_camera_crop(SM, smooth_mouse, dt)

    --==========================
    -- 5. OUTPUT (Diff-based)
    --==========================
    local cx = math.floor(crop.x)
    local cy = math.floor(crop.y)
    local cw = math.floor(crop.w)
    local ch = math.floor(crop.h)

    if cx ~= last_output.x or cy ~= last_output.y or
       cw ~= last_output.w or ch ~= last_output.h then
        crop_filter_update(cx, cy, cw, ch)
        last_output.x = cx
        last_output.y = cy
        last_output.w = cw
        last_output.h = ch
    end

    --==========================
    -- 6. EFFECTS
    --==========================
    blur_manager_update(SM, crop, dt)
    cursor_renderer_update(dt, raw_mouse, crop)

    --==========================
    -- 7. STATE COMPLETION
    --==========================
    if SM.zoom_time >= 1.0 and SM:is_animating() then
        SM:complete()

        -- Auto-enable follow after zoom in
        if SM.state == ZoomState.ZOOMED_IN and cfg.auto_follow then
            SM.following = true
        end

        -- Stop timer if nothing needs updating
        if SM.state == ZoomState.IDLE and not cursor_renderer_active() then
            stop_timer()
        end
    end
end

-- Timer management
local timer_running = false

function start_timer()
    if not timer_running then
        timer_running = true
        last_tick_time = os.clock()
        local interval = math.max(1, math.floor(obs.obs_get_frame_interval_ns() / 1000000))
        obs.timer_add(on_timer, interval)
    end
end

function stop_timer()
    if timer_running then
        timer_running = false
        obs.timer_remove(on_timer)
    end
end
```

#### T-201: Hotkey Handlers

```lua
--================================================
-- Hotkey Handlers
--================================================
function on_toggle_zoom(pressed)
    if not pressed then return end

    -- Capture current crop as start
    local start = {
        x = current_crop.x,
        y = current_crop.y,
        w = current_crop.w,
        h = current_crop.h
    }

    if SM.state == ZoomState.IDLE then
        -- ZOOM IN
        local mouse = platform_get_mouse_pos()
        init_mouse_tracking(mouse)

        zoom_info.zoom_to = cfg.zoom_value
        local target = get_target_position(zoom_info, mouse)

        SM:transition(ZoomState.ZOOMING_IN, {
            start_crop = start,
            target_crop = target.crop,
            target_level = cfg.zoom_value
        })

        start_timer()

    elseif SM.state == ZoomState.ZOOMED_IN then
        -- ZOOM OUT
        SM.following = false

        SM:transition(ZoomState.ZOOMING_OUT, {
            start_crop = start,
            target_crop = original_crop,
            target_level = 1.0
        })

        start_timer()
    end
    -- Ignore if already animating (guard against rapid presses)
end

function on_toggle_follow(pressed)
    if not pressed then return end
    if not SM:is_zoomed() then return end

    SM.following = not SM.following
    log("Follow: " .. tostring(SM.following))

    if SM.following and not timer_running then
        start_timer()
    end
end
```

### Phase 1 Verification Checklist

```
□ Zoom in at mouse position with smooth easing
□ Zoom out returns to exact original transform
□ Mouse follow tracks smoothly when zoomed
□ Dead zone prevents micro-jitter
□ Follow toggle hotkey works independently
□ Scene switch releases and re-acquires source
□ Transition between scenes doesn't flash
□ Script reload restores source perfectly
□ 10 rapid hotkey presses don't break state
□ CPU usage < 1% when idle
□ CPU usage < 2% when zoomed + following
□ Works with display capture source
□ Works with bounding-box transform
□ Auto-converts non-bbox transform
□ Handles existing crop filters correctly
```

---

## 4. Phase 2: Smart Features (Week 3–4)

### Goal
Scroll-wheel zoom, auto source detection, per-scene memory, and full preset system. These are the key differentiators over the competitor.

#### Week 3: Scroll Zoom & Presets

| Task | Module | Hours | Description |
|---|---|---|---|
| **T-300** | M10 | 6 | **Scroll wheel zoom** — Modifier key detection, delta accumulation, state machine integration |
| **T-301** | M10 | 3 | **Scroll zoom animation** — Smooth transitions between zoom levels, interrupt handling |
| **T-302** | M13 | 4 | **Preset manager** — Built-in presets, save/load/delete custom presets, easing per preset |
| **T-303** | M13 | 2 | **Preset UI** — Dropdown, save button, delete button, name field |
| **T-304** | — | 3 | **Testing** — Scroll zoom edge cases, preset roundtrip |

**T-300: Scroll Zoom Implementation**

```lua
--================================================
-- MODULE: Scroll Zoom (M10)
--================================================
local scroll_accumulator = 0
local scroll_modifier_held = false

-- Platform-specific scroll detection
-- Windows: Use a low-level hook or poll approach
-- For OBS Lua, we register a hotkey for modifier + use OBS hotkey system
-- Alternative: Use FFI to check GetAsyncKeyState for modifier

local scroll_hotkey_up_id = nil
local scroll_hotkey_down_id = nil

function init_scroll_zoom()
    -- Register scroll hotkeys (user binds Ctrl+ScrollUp, Ctrl+ScrollDown in OBS)
    scroll_hotkey_up_id = obs.obs_hotkey_register_frontend(
        "zoom_scroll_up", "Zoom in (scroll)",
        function(pressed) if pressed then on_scroll_zoom(1) end end
    )
    scroll_hotkey_down_id = obs.obs_hotkey_register_frontend(
        "zoom_scroll_down", "Zoom out (scroll)",
        function(pressed) if pressed then on_scroll_zoom(-1) end end
    )
end

function on_scroll_zoom(direction)
    if not SM:can_scroll() then return end

    local step = cfg.scroll_step * direction  -- e.g., 0.25
    local new_level = clamp(1.0, cfg.max_zoom, SM.target_level + step)

    -- If we hit 1.0, fully zoom out
    if new_level <= 1.0 then
        if SM:is_zoomed() then
            -- Trigger full zoom out
            local start = {
                x = current_crop.x, y = current_crop.y,
                w = current_crop.w, h = current_crop.h
            }
            SM:transition(ZoomState.ZOOMING_OUT, {
                start_crop = start,
                target_crop = original_crop,
                target_level = 1.0
            })
            SM.following = false
            start_timer()
        end
        return
    end

    -- Calculate new target crop for new zoom level
    local mouse = platform_get_mouse_pos()
    zoom_info.zoom_to = new_level
    local target = get_target_position(zoom_info, mouse)

    local start = {
        x = current_crop.x, y = current_crop.y,
        w = current_crop.w, h = current_crop.h
    }

    if SM.state == ZoomState.IDLE then
        -- First scroll from unzoomed
        init_mouse_tracking(mouse)
        SM:transition(ZoomState.SCROLLING, {
            start_crop = start,
            target_crop = target.crop,
            target_level = new_level
        })
    else
        -- Already zoomed, adjust level
        -- Interrupt current animation if scrolling
        SM:transition(ZoomState.SCROLLING, {
            start_crop = start,
            target_crop = target.crop,
            target_level = new_level
        })
    end

    start_timer()
end
```

#### Week 4: Auto-Detection & Scene Memory

| Task | Module | Hours | Description |
|---|---|---|---|
| **T-400** | M11 | 4 | **Auto source detection** — Scan sources, find display/game/window captures, auto-select |
| **T-401** | M12 | 4 | **Scene memory** — Per-scene source mapping, persist to settings, auto-switch on scene change |
| **T-402** | M12 | 2 | **Scene memory UI** — Show current mapping, allow override |
| **T-403** | M19 | 3 | **Easing curve dropdown** — All 23+ curves in UI, per-preset easing |
| **T-404** | — | 3 | **Integration testing** — Scene switch with memory, auto-detect, scroll + toggle combo |
| **T-405** | — | 2 | **Bug fixes** |

**T-401: Scene Memory**

```lua
--================================================
-- MODULE: Scene Memory (M12)
--================================================
local scene_source_map = {}  -- { scene_name = source_name }

function scene_memory_save(settings)
    local array = obs.obs_data_array_create()
    for scene, source in pairs(scene_source_map) do
        local item = obs.obs_data_create()
        obs.obs_data_set_string(item, "scene", scene)
        obs.obs_data_set_string(item, "source", source)
        obs.obs_data_array_push_back(array, item)
        obs.obs_data_release(item)
    end
    obs.obs_data_set_array(settings, "scene_source_map", array)
    obs.obs_data_array_release(array)
end

function scene_memory_load(settings)
    scene_source_map = {}
    local array = obs.obs_data_get_array(settings, "scene_source_map")
    if array then
        for i = 0, obs.obs_data_array_count(array) - 1 do
            local item = obs.obs_data_array_item(array, i)
            local scene = obs.obs_data_get_string(item, "scene")
            local source = obs.obs_data_get_string(item, "source")
            if scene ~= "" and source ~= "" then
                scene_source_map[scene] = source
            end
            obs.obs_data_release(item)
        end
        obs.obs_data_array_release(array)
    end
end

function scene_memory_get_source_for_current_scene()
    local scene_source = obs.obs_frontend_get_current_scene()
    if not scene_source then return nil end

    local scene_name = obs.obs_source_get_name(scene_source)
    obs.obs_source_release(scene_source)

    -- 1. Check explicit mapping
    if scene_source_map[scene_name] then
        return scene_source_map[scene_name]
    end

    -- 2. Fall back to global source
    return cfg.source_name
end

function scene_memory_set(scene_name, source_name)
    scene_source_map[scene_name] = source_name
    log("Scene memory: " .. scene_name .. " → " .. source_name)
end
```

### Phase 2 Verification Checklist

```
□ Scroll up zooms in incrementally
□ Scroll down zooms out incrementally
□ Reaching 1.0 via scroll cleanly resets to unzoomed
□ Scroll during existing zoom smoothly transitions
□ Modifier key required for scroll (no conflicts)
□ Auto-detect finds display capture on fresh install
□ Auto-detect prompts if multiple captures exist
□ Scene switch uses remembered source
□ Scene switch falls back to global if no memory
□ All 23 easing curves produce correct output
□ Easing dropdown in presets works
□ Custom preset save/load/delete persists across restart
□ Preset selection applies values to sliders
□ Manual slider change switches to "Custom" preset
```

---

## 5. Phase 3: Effects & Cursor (Week 5–6)

### Goal
Built-in blur effects (no external plugin) and auto-created cursor overlay. These are the two biggest competitor pain points we eliminate.

#### Week 5: Blur Manager

| Task | Module | Hours | Description |
|---|---|---|---|
| **T-500** | M14 | 2 | **Blur strategy research** — Test if OBS Lua can load custom `.effect` shaders. Document results. |
| **T-501** | M14 | 6 | **Blur manager — Strategy A** — If shaders work: load `zoom_blur.effect` and `motion_blur.effect` at runtime |
| **T-502** | M14 | 4 | **Blur manager — Strategy B** — If shaders don't work: auto-detect Composite Blur plugin, auto-create + configure filters |
| **T-503** | M14 | 3 | **Blur manager — Strategy C** — If neither works: use built-in OBS blur (if available) or skip gracefully |
| **T-504** | M14 | 3 | **Zoom blur logic** — Bell curve intensity during transitions, center tracking, clear radius |
| **T-505** | M14 | 3 | **Motion blur logic** — Velocity-based radius/angle, fade to zero when still, disable during zoom transition |
| **T-506** | — | 3 | **Testing** — Blur visual quality, performance impact, fallback chain |

**T-501/502: Blur Manager with Fallback Chain**

```lua
--================================================
-- MODULE: Blur Manager (M14)
--================================================
local BlurManager = {
    strategy = "none",  -- "shader", "composite_blur", "none"
    zoom_blur_filter = nil,
    motion_blur_filter = nil,
    zoom_blur_settings = nil,
    motion_blur_settings = nil,
    initialized = false,
}

function BlurManager:init(source)
    if not source then return end
    self:cleanup()

    -- Strategy A: Try custom shader
    if self:try_shader_strategy(source) then
        self.strategy = "shader"
        log("Blur: Using custom shader strategy")
        return
    end

    -- Strategy B: Try Composite Blur plugin auto-config
    if self:try_composite_blur_strategy(source) then
        self.strategy = "composite_blur"
        log("Blur: Using Composite Blur plugin (auto-configured)")
        return
    end

    -- Strategy C: No blur available
    self.strategy = "none"
    log("Blur: No blur backend available. Blur effects disabled.")
end

function BlurManager:try_shader_strategy(source)
    -- Attempt to load our custom effect file
    local script_path = script_path()
    local shader_path = script_path .. "assets/shaders/zoom_blur.effect"

    -- Check if file exists
    local f = io.open(shader_path, "r")
    if not f then return false end
    f:close()

    -- Try to create a source filter using the effect
    -- OBS has "shader_filter" or we can use obs_source_create with effect
    local settings = obs.obs_data_create()
    obs.obs_data_set_string(settings, "shader_file_name", shader_path)

    local filter = obs.obs_source_create_private(
        "obs_shader_filter",  -- or "user_filter" depending on OBS version
        FILTER_PREFIX .. "Zoom Blur",
        settings
    )
    obs.obs_data_release(settings)

    if filter then
        obs.obs_source_filter_add(source, filter)
        self.zoom_blur_filter = filter
        -- Don't release — we keep the reference

        -- Repeat for motion blur
        local motion_path = script_path .. "assets/shaders/motion_blur.effect"
        local mf = io.open(motion_path, "r")
        if mf then
            mf:close()
            local ms = obs.obs_data_create()
            obs.obs_data_set_string(ms, "shader_file_name", motion_path)
            local mfilter = obs.obs_source_create_private(
                "obs_shader_filter",
                FILTER_PREFIX .. "Motion Blur",
                ms
            )
            obs.obs_data_release(ms)
            if mfilter then
                obs.obs_source_filter_add(source, mfilter)
                self.motion_blur_filter = mfilter
            end
        end

        self.initialized = true
        return true
    end

    return false
end

function BlurManager:try_composite_blur_strategy(source)
    -- Check if composite_blur filter type exists
    local test = obs.obs_source_create_private("composite_blur", "__test__", nil)
    if not test then return false end
    obs.obs_source_release(test)

    -- It exists! Auto-create our filters
    -- Zoom Blur
    local zs = obs.obs_data_create()
    obs.obs_data_set_double(zs, "radius", 0)
    obs.obs_data_set_int(zs, "blur_type", 2) -- Zoom type
    self.zoom_blur_filter = obs.obs_source_create_private(
        "composite_blur",
        FILTER_PREFIX .. "Zoom Blur",
        zs
    )
    obs.obs_source_filter_add(source, self.zoom_blur_filter)
    self.zoom_blur_settings = zs

    -- Motion Blur
    local ms = obs.obs_data_create()
    obs.obs_data_set_double(ms, "radius", 0)
    obs.obs_data_set_int(ms, "blur_type", 3) -- Motion/directional type
    self.motion_blur_filter = obs.obs_source_create_private(
        "composite_blur",
        FILTER_PREFIX .. "Motion Blur",
        ms
    )
    obs.obs_source_filter_add(source, self.motion_blur_filter)
    self.motion_blur_settings = ms

    self.initialized = true
    return true
end

function BlurManager:update(state_machine, crop, dt)
    if not self.initialized then return end
    if self.strategy == "none" then return end

    -- Zoom Blur: Active during zoom transitions
    if cfg.zoom_blur_enabled and self.zoom_blur_filter then
        local radius = 0
        if state_machine:is_animating() and
           (state_machine.state == ZoomState.ZOOMING_IN or
            state_machine.state == ZoomState.ZOOMING_OUT) then
            local t = clamp(0, 1, state_machine.zoom_time)
            local curve = math.sin(t * math.pi)
            radius = curve * curve * cfg.zoom_blur_intensity
        end
        self:set_zoom_blur(radius, crop)
    end

    -- Motion Blur: Active during camera panning (not during zoom transition)
    if cfg.motion_blur_enabled and self.motion_blur_filter then
        if not state_machine:is_animating() and state_machine:is_zoomed() then
            local cam_dx = crop.x - (last_camera_pos.x or crop.x)
            local cam_dy = crop.y - (last_camera_pos.y or crop.y)
            local speed = math.sqrt(cam_dx * cam_dx + cam_dy * cam_dy)

            if speed > 1.0 then
                local radius = math.min(10, speed * cfg.motion_blur_intensity * 0.5)
                local angle = math.deg(math.atan2(cam_dy, cam_dx))
                self:set_motion_blur(radius, angle)
            else
                self:set_motion_blur(0, 0)
            end
        else
            self:set_motion_blur(0, 0)
        end
    end
end

function BlurManager:set_zoom_blur(radius, crop)
    if self.strategy == "shader" then
        -- Update shader uniforms
        local s = obs.obs_source_get_settings(self.zoom_blur_filter)
        obs.obs_data_set_double(s, "radius", radius)
        obs.obs_data_set_double(s, "center_x", crop.x + crop.w / 2)
        obs.obs_data_set_double(s, "center_y", crop.y + crop.h / 2)
        obs.obs_data_set_double(s, "clear_radius", cfg.zoom_blur_clear_radius)
        obs.obs_source_update(self.zoom_blur_filter, s)
        obs.obs_data_release(s)
    elseif self.strategy == "composite_blur" then
        obs.obs_data_set_double(self.zoom_blur_settings, "radius", radius)
        obs.obs_data_set_double(self.zoom_blur_settings, "center_x", crop.x + crop.w / 2)
        obs.obs_data_set_double(self.zoom_blur_settings, "center_y", crop.y + crop.h / 2)
        obs.obs_data_set_double(self.zoom_blur_settings, "inactive_radius", cfg.zoom_blur_clear_radius)
        obs.obs_source_update(self.zoom_blur_filter, self.zoom_blur_settings)
    end
end

function BlurManager:set_motion_blur(radius, angle)
    if self.strategy == "shader" then
        local s = obs.obs_source_get_settings(self.motion_blur_filter)
        obs.obs_data_set_double(s, "radius", radius)
        obs.obs_data_set_double(s, "angle", angle)
        obs.obs_source_update(self.motion_blur_filter, s)
        obs.obs_data_release(s)
    elseif self.strategy == "composite_blur" then
        obs.obs_data_set_double(self.motion_blur_settings, "radius", radius)
        obs.obs_data_set_double(self.motion_blur_settings, "angle", angle)
        obs.obs_source_update(self.motion_blur_filter, self.motion_blur_settings)
    end
end

function BlurManager:cleanup()
    -- Remove auto-created filters and release references
    if self.zoom_blur_filter and source then
        obs.obs_source_filter_remove(source, self.zoom_blur_filter)
        obs.obs_source_release(self.zoom_blur_filter)
        self.zoom_blur_filter = nil
    end
    if self.motion_blur_filter and source then
        obs.obs_source_filter_remove(source, self.motion_blur_filter)
        obs.obs_source_release(self.motion_blur_filter)
        self.motion_blur_filter = nil
    end
    if self.zoom_blur_settings then
        obs.obs_data_release(self.zoom_blur_settings)
        self.zoom_blur_settings = nil
    end
    if self.motion_blur_settings then
        obs.obs_data_release(self.motion_blur_settings)
        self.motion_blur_settings = nil
    end
    self.initialized = false
    self.strategy = "none"
end
```

#### Week 6: Cursor Renderer

| Task | Module | Hours | Description |
|---|---|---|---|
| **T-600** | M16 | 3 | **Asset manager** — Extract bundled cursor PNGs to app data directory |
| **T-601** | M15 | 6 | **Cursor renderer** — Auto-create image source, position/scale/rotate per frame |
| **T-602** | M15 | 3 | **Cursor shape swapping** — Detect arrow vs hand (Windows), swap source image |
| **T-603** | M15 | 3 | **Cursor physics** — Click scale, rotation modes (None/Lean/Directional), SmoothDamp |
| **T-604** | M15 | 2 | **Cursor cleanup** — Remove auto-created sources on unload |
| **T-605** | — | 3 | **Testing** — Cursor overlay accuracy, click animation, shape detection, cleanup |

**T-601: Cursor Renderer**

```lua
--================================================
-- MODULE: Cursor Renderer (M15)
--================================================
local CursorRenderer = {
    enabled = false,
    source = nil,         -- Auto-created image source
    sceneitem = nil,      -- Scene item for positioning

    -- Smoothed state
    pos = { x = 0, y = 0 },
    current_scale = 1.0,
    current_rot = 0,
    swap_pulse = 1.0,

    -- Velocities (SmoothDamp)
    vel_x = { val = 0 },
    vel_y = { val = 0 },
    vel_scale = { val = 0 },
    vel_rot = { val = 0 },
    vel_swap = { val = 0 },

    -- State
    was_pointer = false,
    initialized = false,
}

function CursorRenderer:init()
    if not cfg.cursor_enabled then
        self.enabled = false
        return
    end

    -- Extract assets if needed
    local asset_dir = CursorAssets.ensure_extracted()
    if not asset_dir then
        log("Cursor: Failed to extract assets. Cursor disabled.")
        self.enabled = false
        return
    end

    -- Create or find our image source
    local source_name = FILTER_PREFIX .. "Cursor"
    self.source = obs.obs_get_source_by_name(source_name)

    if not self.source then
        -- Create new image source
        local settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "file", asset_dir .. "/arrow.png")
        self.source = obs.obs_source_create("image_source", source_name, settings, nil)
        obs.obs_data_release(settings)

        if not self.source then
            log("Cursor: Failed to create image source")
            self.enabled = false
            return
        end
    end

    -- Add to current scene
    self:add_to_scene()

    -- Initialize position to current mouse
    local mouse = platform_get_mouse_pos()
    self.pos.x = mouse.x
    self.pos.y = mouse.y

    self.enabled = true
    self.initialized = true
    log("Cursor: Initialized with auto-created source")
end

function CursorRenderer:add_to_scene()
    if not self.source then return end

    local scene_source = obs.obs_frontend_get_current_scene()
    if not scene_source then return end

    local scene = obs.obs_scene_from_source(scene_source)
    if scene then
        -- Check if already in scene
        local source_name = obs.obs_source_get_name(self.source)
        self.sceneitem = obs.obs_scene_find_source(scene, source_name)

        if not self.sceneitem then
            -- Add to scene
            self.sceneitem = obs.obs_scene_add(scene, self.source)
            if self.sceneitem then
                -- Move to top of scene (render last = on top)
                obs.obs_sceneitem_set_order(self.sceneitem, obs.OBS_ORDER_MOVE_TOP)
            end
        end
    end

    obs.obs_source_release(scene_source)
end

function CursorRenderer:update(dt, raw_mouse, camera_crop)
    if not self.enabled or not self.sceneitem then return end

    -- 1. Smooth cursor position (independent from camera)
    self.pos.x = SmoothDamp(self.pos.x, raw_mouse.x, self.vel_x, cfg.cursor_smooth_time, 100000, dt)
    self.pos.y = SmoothDamp(self.pos.y, raw_mouse.y, self.vel_y, cfg.cursor_smooth_time, 100000, dt)

    -- Snap when very close
    if math.abs(self.pos.x - raw_mouse.x) < 0.5 then self.pos.x = raw_mouse.x; self.vel_x.val = 0 end
    if math.abs(self.pos.y - raw_mouse.y) < 0.5 then self.pos.y = raw_mouse.y; self.vel_y.val = 0 end

    -- 2. Cursor shape detection & swap
    local is_pointer = false
    if platform_cursor_shape_available then
        is_pointer = platform_is_cursor_pointer()
    end

    if is_pointer ~= self.was_pointer then
        -- Swap image
        local asset_dir = CursorAssets.get_dir()
        local new_file = is_pointer and (asset_dir .. "/pointer.png") or (asset_dir .. "/arrow.png")
        local s = obs.obs_source_get_settings(self.source)
        obs.obs_data_set_string(s, "file", new_file)
        obs.obs_source_update(self.source, s)
        obs.obs_data_release(s)

        -- Trigger swap pulse animation
        self.swap_pulse = 0.75
        self.vel_swap.val = 1
        self.was_pointer = is_pointer
    end
    self.swap_pulse = SmoothDamp(self.swap_pulse, 1.0, self.vel_swap, 0.12, 100000, dt)

    -- 3. Click animation
    local is_clicking = platform_is_clicking()
    local target_scale = is_clicking and (cfg.cursor_scale * cfg.cursor_click_scale) or cfg.cursor_scale
    local anim_time = is_clicking and 0.05 or 0.2
    self.current_scale = SmoothDamp(self.current_scale, target_scale, self.vel_scale, anim_time, 100000, dt)

    -- 4. Rotation
    local dynamic_rot = self:compute_rotation(dt)

    -- 5. Position relative to zoom
    local zoom_factor = 1.0
    local crop_x, crop_y = 0, 0

    if camera_crop and SM:is_zoomed() then
        zoom_factor = zoom_info.source_size.width / camera_crop.w
        crop_x = camera_crop.x
        crop_y = camera_crop.y
    end

    local final_x = (self.pos.x - crop_x) * zoom_factor + (cfg.cursor_offset_x * zoom_factor)
    local final_y = (self.pos.y - crop_y) * zoom_factor + (cfg.cursor_offset_y * zoom_factor)

    -- 6. Apply to scene item
    local pos = obs.vec2()
    pos.x = final_x
    pos.y = final_y
    obs.obs_sceneitem_set_pos(self.sceneitem, pos)

    local scale = obs.vec2()
    local s = self.current_scale * zoom_factor * self.swap_pulse
    scale.x = s
    scale.y = s
    obs.obs_sceneitem_set_scale(self.sceneitem, scale)

    obs.obs_sceneitem_set_rot(self.sceneitem, dynamic_rot)
end

function CursorRenderer:compute_rotation(dt)
    local vx = self.vel_x.val
    local vy = self.vel_y.val
    local speed = math.sqrt(vx * vx + vy * vy)

    if cfg.cursor_rotation_mode == "Directional" then
        if speed > 20 then
            local angle = math.atan2(vy, vx) * (180 / math.pi)
            if math.abs(vy) < 10 then
                angle = (vx > 0) and 0 or 180
            end
            local target = angle + cfg.cursor_angle_offset
            local diff = (target - self.current_rot + 180) % 360 - 180
            self.current_rot = SmoothDamp(self.current_rot, self.current_rot + diff, self.vel_rot, 0.05, 100000, dt)
        end
        return self.current_rot

    elseif cfg.cursor_rotation_mode == "Lean" then
        local lean = clamp(-40, 40, vx * 0.05) + cfg.cursor_angle_offset
        local diff = (lean - self.current_rot + 180) % 360 - 180
        self.current_rot = SmoothDamp(self.current_rot, self.current_rot + diff, self.vel_rot, 0.08, 100000, dt)
        return self.current_rot

    else -- "None"
        local diff = (cfg.cursor_angle_offset - self.current_rot + 180) % 360 - 180
        self.current_rot = SmoothDamp(self.current_rot, self.current_rot + diff, self.vel_rot, 0.15, 100000, dt)
        return self.current_rot
    end
end

function CursorRenderer:cleanup()
    if self.sceneitem then
        -- Remove from scene
        obs.obs_sceneitem_remove(self.sceneitem)
        self.sceneitem = nil
    end

    if self.source then
        -- Remove the auto-created source entirely
        local source_name = obs.obs_source_get_name(self.source)
        obs.obs_source_release(self.source)

        -- Also remove from OBS source list to fully clean up
        local s = obs.obs_get_source_by_name(source_name)
        if s then
            obs.obs_source_remove(s)
            obs.obs_source_release(s)
        end
        self.source = nil
    end

    self.enabled = false
    self.initialized = false
end

function cursor_renderer_active()
    return CursorRenderer.enabled and CursorRenderer.initialized
end

function cursor_renderer_update(dt, raw_mouse, crop)
    if not raw_mouse then raw_mouse = platform_get_mouse_pos() end
    CursorRenderer:update(dt, raw_mouse, crop)
end
```

**T-600: Asset Manager**

```lua
--================================================
-- MODULE: Cursor Asset Manager (M16)
--================================================
local CursorAssets = {
    extracted = false,
    dir = nil,
}

-- Minimal 32x32 arrow cursor PNG as base64
-- (In production, these would be proper cursor images)
local EMBEDDED_CURSORS = {
    arrow = nil,   -- Will be loaded from file next to script
    pointer = nil,
}

function CursorAssets.get_platform_dir()
    if ffi.os == "Windows" then
        return os.getenv("APPDATA") .. "\\obs-studio\\obs-zoom-pro\\cursors"
    elseif ffi.os == "Linux" then
        return os.getenv("HOME") .. "/.config/obs-studio/obs-zoom-pro/cursors"
    elseif ffi.os == "OSX" then
        return os.getenv("HOME") .. "/Library/Application Support/obs-studio/obs-zoom-pro/cursors"
    end
    return nil
end

function CursorAssets.ensure_extracted()
    if CursorAssets.extracted then return CursorAssets.dir end

    local dir = CursorAssets.get_platform_dir()
    if not dir then return nil end

    -- Create directory (platform-specific)
    if ffi.os == "Windows" then
        os.execute('mkdir "' .. dir .. '" 2>nul')
    else
        os.execute('mkdir -p "' .. dir .. '"')
    end

    -- Check if assets already exist
    local arrow_path = dir .. (ffi.os == "Windows" and "\\" or "/") .. "arrow.png"
    local f = io.open(arrow_path, "rb")
    if f then
        f:close()
        CursorAssets.dir = dir
        CursorAssets.extracted = true
        return dir
    end

    -- Copy from script directory
    local script_dir = get_script_directory()
    local assets_src = script_dir .. "assets/cursors/"

    local files = { "arrow.png", "pointer.png", "ibeam.png" }
    for _, filename in ipairs(files) do
        local src_path = assets_src .. filename
        local dst_path = dir .. (ffi.os == "Windows" and "\\" or "/") .. filename

        local src = io.open(src_path, "rb")
        if src then
            local data = src:read("*a")
            src:close()

            local dst = io.open(dst_path, "wb")
            if dst then
                dst:write(data)
                dst:close()
            end
        else
            log("Cursor: Asset not found: " .. src_path)
        end
    end

    CursorAssets.dir = dir
    CursorAssets.extracted = true
    return dir
end

function CursorAssets.get_dir()
    return CursorAssets.dir
end

function get_script_directory()
    -- OBS provides script_path() in newer versions
    -- Fallback: use debug.getinfo
    local info = debug.getinfo(1, "S")
    local path = info.source:match("@(.*/)")
    return path or ""
end
```

### Phase 3 Verification Checklist

```
□ Blur works without Composite Blur plugin installed
□ Blur auto-detects Composite Blur if available and uses it
□ Zoom blur peaks at mid-transition and returns to zero
□ Motion blur activates during camera panning only
□ Motion blur direction matches camera movement
□ No blur when camera is stationary
□ Blur cleanup on script unload (filters removed)
□ Cursor overlay appears on first run without setup
□ Cursor tracks mouse smoothly
□ Cursor scales with zoom level
□ Click animation works (scale down on click)
□ Cursor shape swaps between arrow and hand (Windows)
□ Cursor has swap pulse animation
□ Rotation modes work (None, Lean, Directional)
□ Cursor cleanup removes auto-created source
□ Asset extraction works on Windows/Linux/Mac paths
```

---

## 6. Phase 4: Bookmarks & API (Week 6–7)

#### Week 6 (Second Half) + Week 7 (First Half)

| Task | Module | Hours | Description |
|---|---|---|---|
| **T-700** | M17 | 4 | **Bookmark data model** — Save/load/delete bookmarks, persist to settings |
| **T-701** | M17 | 4 | **Bookmark animation** — Smooth transition to saved position using current easing |
| **T-702** | M17 | 2 | **Bookmark hotkeys** — Register up to 5 bookmark hotkeys |
| **T-703** | M17 | 2 | **Bookmark UI** — Dropdown, save/delete/rename buttons |
| **T-704** | M18 | 4 | **UDP API server** — Command parser, dispatch to engine, status response |
| **T-705** | M18 | 2 | **UDP API testing** — Test all commands with netcat |
| **T-706** | — | 2 | **Integration testing** |

**T-700: Bookmark Manager**

```lua
--================================================
-- MODULE: Bookmark Manager (M17)
--================================================
local BookmarkManager = {
    bookmarks = {},  -- { name = { zoom_level, x, y, w, h } }
    hotkeys = {},    -- { [1..5] = hotkey_id }
    max_bookmarks = 20,
}

function BookmarkManager:save_current(name)
    if not name or name == "" then return false end
    if #self:get_names() >= self.max_bookmarks and not self.bookmarks[name] then
        log("Bookmark: Max bookmarks reached (" .. self.max_bookmarks .. ")")
        return false
    end

    self.bookmarks[name] = {
        zoom_level = SM.zoom_level,
        x = current_crop.x,
        y = current_crop.y,
        w = current_crop.w,
        h = current_crop.h,
        source = cfg.source_name,
    }

    log("Bookmark saved: " .. name .. " (zoom=" .. SM.zoom_level .. ")")
    return true
end

function BookmarkManager:recall(name)
    local bm = self.bookmarks[name]
    if not bm then
        log("Bookmark not found: " .. name)
        return false
    end

    if not SM:can_jump() then return false end

    -- Set up the zoom info for this bookmark
    zoom_info.zoom_to = bm.zoom_level

    local start = {
        x = current_crop.x, y = current_crop.y,
        w = current_crop.w, h = current_crop.h
    }

    local target = {
        x = bm.x, y = bm.y,
        w = bm.w, h = bm.h
    }

    SM:transition(ZoomState.JUMPING, {
        start_crop = start,
        target_crop = target,
        target_level = bm.zoom_level
    })

    start_timer()
    log("Bookmark recall: " .. name)
    return true
end

function BookmarkManager:delete(name)
    if self.bookmarks[name] then
        self.bookmarks[name] = nil
        log("Bookmark deleted: " .. name)
        return true
    end
    return false
end

function BookmarkManager:get_names()
    local names = {}
    for k, _ in pairs(self.bookmarks) do
        table.insert(names, k)
    end
    table.sort(names)
    return names
end

function BookmarkManager:persist(settings)
    local array = obs.obs_data_array_create()
    for name, bm in pairs(self.bookmarks) do
        local item = obs.obs_data_create()
        obs.obs_data_set_string(item, "name", name)
        obs.obs_data_set_double(item, "zoom_level", bm.zoom_level)
        obs.obs_data_set_double(item, "x", bm.x)
        obs.obs_data_set_double(item, "y", bm.y)
        obs.obs_data_set_double(item, "w", bm.w)
        obs.obs_data_set_double(item, "h", bm.h)
        obs.obs_data_set_string(item, "source", bm.source or "")
        obs.obs_data_array_push_back(array, item)
        obs.obs_data_release(item)
    end
    obs.obs_data_set_array(settings, "zoom_bookmarks", array)
    obs.obs_data_array_release(array)
end

function BookmarkManager:load(settings)
    self.bookmarks = {}
    local array = obs.obs_data_get_array(settings, "zoom_bookmarks")
    if not array then return end

    for i = 0, obs.obs_data_array_count(array) - 1 do
        local item = obs.obs_data_array_item(array, i)
        local name = obs.obs_data_get_string(item, "name")
        if name ~= "" then
            self.bookmarks[name] = {
                zoom_level = obs.obs_data_get_double(item, "zoom_level"),
                x = obs.obs_data_get_double(item, "x"),
                y = obs.obs_data_get_double(item, "y"),
                w = obs.obs_data_get_double(item, "w"),
                h = obs.obs_data_get_double(item, "h"),
                source = obs.obs_data_get_string(item, "source"),
            }
        end
        obs.obs_data_release(item)
    end
    obs.obs_data_array_release(array)
end

function BookmarkManager:register_hotkeys(settings)
    for i = 1, 5 do
        self.hotkeys[i] = obs.obs_hotkey_register_frontend(
            "zoom_bookmark_" .. i,
            "Zoom to Bookmark " .. i,
            function(pressed)
                if not pressed then return end
                local names = self:get_names()
                if names[i] then
                    self:recall(names[i])
                end
            end
        )

        -- Load saved hotkey bindings
        local key = "obs_zoom_pro.hotkey.bookmark_" .. i
        local save_array = obs.obs_data_get_array(settings, key)
        if save_array then
            obs.obs_hotkey_load(self.hotkeys[i], save_array)
            obs.obs_data_array_release(save_array)
        end
    end
end

function BookmarkManager:save_hotkeys(settings)
    for i = 1, 5 do
        if self.hotkeys[i] then
            local save_array = obs.obs_hotkey_save(self.hotkeys[i])
            obs.obs_data_set_array(settings, "obs_zoom_pro.hotkey.bookmark_" .. i, save_array)
            obs.obs_data_array_release(save_array)
        end
    end
end
```

**T-704: UDP API Server**

```lua
--================================================
-- MODULE: UDP API Server (M18)
--================================================
local APIServer = {
    server = nil,
    enabled = false,
}

local API_COMMANDS = {
    ZOOM_IN = function(args)
        local level = tonumber(args[1]) or cfg.zoom_value
        on_scroll_zoom_to(level)
        return "OK"
    end,

    ZOOM_OUT = function(args)
        if SM:is_zoomed() then
            on_toggle_zoom(true) -- Trigger zoom out
        end
        return "OK"
    end,

    ZOOM_SET = function(args)
        local level = tonumber(args[1])
        if not level then return "ERROR: Missing level" end
        on_scroll_zoom_to(level)
        return "OK"
    end,

    ZOOM_TOGGLE = function(args)
        on_toggle_zoom(true)
        return "OK"
    end,

    FOLLOW_ON = function(args)
        if SM:is_zoomed() then SM.following = true end
        return "OK"
    end,

    FOLLOW_OFF = function(args)
        SM.following = false
        return "OK"
    end,

    FOLLOW_TOGGLE = function(args)
        if SM:is_zoomed() then SM.following = not SM.following end
        return "OK"
    end,

    PRESET = function(args)
        local name = args[1]
        if not name then return "ERROR: Missing preset name" end
        if not global_presets[name] then return "ERROR: Unknown preset" end
        apply_preset(name)
        return "OK"
    end,

    BOOKMARK = function(args)
        local name = args[1]
        if not name then return "ERROR: Missing bookmark name" end
        local ok = BookmarkManager:recall(name)
        return ok and "OK" or "ERROR: Bookmark not found"
    end,

    PAN = function(args)
        local x = tonumber(args[1])
        local y = tonumber(args[2])
        if not x or not y then return "ERROR: Missing x y" end
        -- Set mouse override and trigger follow update
        return "OK"
    end,

    MOUSE = function(args)
        local x = tonumber(args[1])
        local y = tonumber(args[2])
        if not x or not y then return "ERROR: Missing x y" end
        socket_mouse = { x = x, y = y }
        return "OK"
    end,

    STATUS = function(args)
        local status = {
            version = VERSION,
            zoom_level = SM.zoom_level,
            state = SM.state,
            following = SM.following,
            position = {
                x = current_crop and current_crop.x or 0,
                y = current_crop and current_crop.y or 0,
            },
            preset = cfg.zoom_preset,
        }
        -- Simple JSON serialization
        return string.format(
            '{"version":"%s","zoom_level":%.2f,"state":"%s","following":%s,"position":{"x":%.0f,"y":%.0f},"preset":"%s"}',
            status.version, status.zoom_level, status.state,
            tostring(status.following),
            status.position.x, status.position.y,
            status.preset
        )
    end,
}

function APIServer:start(port)
    if not socket_available then
        log("API: Socket library not available")
        return
    end

    self:stop()

    local address = socket.find_first_address("*", port)
    self.server = socket.create("inet", "dgram", "udp")
    if self.server then
        self.server:set_option("reuseaddr", 1)
        self.server:set_blocking(false)
        self.server:bind(address, port)
        obs.timer_add(function() self:poll() end, cfg.api_poll_ms)
        self.enabled = true
        log("API: Listening on port " .. port)
    end
end

function APIServer:poll()
    if not self.server then return end

    repeat
        local data, status = self.server:receive_from()
        if data then
            local response = self:handle_command(data)
            -- Note: UDP response requires sender address (implement if needed)
            if response then
                log("API: " .. data:gsub("\n", "") .. " → " .. response)
            end
        elseif status ~= "timeout" then
            log("API: Error: " .. tostring(status))
        end
    until data == nil
end

function APIServer:handle_command(raw)
    local parts = {}
    for word in raw:gmatch("%S+") do
        table.insert(parts, word)
    end

    if #parts == 0 then return "ERROR: Empty command" end

    local cmd = parts[1]:upper()
    local args = {}
    for i = 2, #parts do
        table.insert(args, parts[i])
    end

    local handler = API_COMMANDS[cmd]
    if handler then
        local ok, result = pcall(handler, args)
        if ok then return result end
        return "ERROR: " .. tostring(result)
    end

    return "ERROR: Unknown command: " .. cmd
end

function APIServer:stop()
    if self.server then
        self.server:close()
        self.server = nil
        self.enabled = false
        log("API: Stopped")
    end
end
```

---

## 7. Phase 5: Polish & Release (Week 7–8)

| Task | Module | Hours | Description |
|---|---|---|---|
| **T-800** | M19 | 8 | **Full Settings UI** — All groups, progressive disclosure, tooltips, help section |
| **T-801** | — | 4 | **Settings validation** — Prevent invalid combos, safe defaults |
| **T-802** | — | 3 | **Config object refactor** — Single `cfg` table for all settings, clean update flow |
| **T-803** | — | 4 | **Cross-platform testing** — Linux X11, macOS (if available) |
| **T-804** | — | 4 | **Performance profiling** — Measure CPU per module, optimize hot paths |
| **T-805** | — | 3 | **Edge case bug fixes** — Rapid input, missing sources, corrupt settings |
| **T-806** | — | 2 | **README.md** — Installation, quick start, feature list, FAQ, troubleshooting |
| **T-807** | — | 2 | **CHANGELOG.md** — v1.0 release notes |
| **T-808** | — | 1 | **LICENSE** — MIT |
| **T-809** | — | 2 | **Demo video script** — Record 60s demo showing key features |
| **T-810** | — | 2 | **GitHub release** — Tag, release notes, zip asset |

**T-802: Config Object**

```lua
--================================================
-- Unified Configuration Object
--================================================
local cfg = {
    -- Source
    source_name = "",

    -- Zoom
    zoom_value = 2.0,
    max_zoom = 10.0,
    zoom_duration = 0.6,
    zoom_overshoot = 0.0,
    zoom_easing = "Cubic.Out",
    zoom_preset = "Smooth",

    -- Scroll
    scroll_step = 0.25,
    scroll_modifier = "ctrl",  -- ctrl, alt, shift

    -- Follow
    auto_follow = true,
    follow_smooth_time = 0.15,
    follow_dead_zone = 5,
    follow_outside_bounds = false,

    -- Blur
    zoom_blur_enabled = false,
    zoom_blur_intensity = 5,
    zoom_blur_clear_radius = 150,
    motion_blur_enabled = false,
    motion_blur_intensity = 1.0,

    -- Cursor
    cursor_enabled = true,
    cursor_scale = 1.0,
    cursor_click_scale = 0.78,
    cursor_smooth_time = 0.1,
    cursor_offset_x = -6,
    cursor_offset_y = -2,
    cursor_rotation_mode = "None",
    cursor_angle_offset = 0,
    cursor_tilt_strength = 0,

    -- Monitor Override
    use_monitor_override = false,
    monitor = { x=0, y=0, w=1920, h=1080, sx=1, sy=1, dw=1920, dh=1080 },

    -- API
    api_enabled = false,
    api_port = 12345,
    api_poll_ms = 10,

    -- Debug
    debug_logs = false,
    allow_all_sources = false,
}

function cfg_load(settings)
    cfg.source_name = obs.obs_data_get_string(settings, "source") or ""
    cfg.zoom_value = obs.obs_data_get_double(settings, "zoom_value")
    cfg.zoom_duration = obs.obs_data_get_double(settings, "zoom_duration")
    cfg.zoom_overshoot = obs.obs_data_get_double(settings, "zoom_overshoot")
    cfg.zoom_easing = obs.obs_data_get_string(settings, "zoom_easing") or "Cubic.Out"
    cfg.zoom_preset = obs.obs_data_get_string(settings, "zoom_preset") or "Smooth"

    cfg.scroll_step = obs.obs_data_get_double(settings, "scroll_step")

    cfg.auto_follow = obs.obs_data_get_bool(settings, "follow")
    cfg.follow_smooth_time = obs.obs_data_get_double(settings, "follow_smooth_time")
    cfg.follow_dead_zone = obs.obs_data_get_int(settings, "follow_dead_zone")
    cfg.follow_outside_bounds = obs.obs_data_get_bool(settings, "follow_outside_bounds")

    cfg.zoom_blur_enabled = obs.obs_data_get_bool(settings, "use_zoom_blur")
    cfg.zoom_blur_intensity = obs.obs_data_get_double(settings, "zoom_blur_intensity")
    cfg.zoom_blur_clear_radius = obs.obs_data_get_double(settings, "zoom_blur_clear_radius")
    cfg.motion_blur_enabled = obs.obs_data_get_bool(settings, "use_motion_blur")
    cfg.motion_blur_intensity = obs.obs_data_get_double(settings, "motion_blur_intensity")

    cfg.cursor_enabled = obs.obs_data_get_bool(settings, "cursor_enabled")
    cfg.cursor_scale = obs.obs_data_get_double(settings, "cursor_scale")
    cfg.cursor_click_scale = obs.obs_data_get_double(settings, "cursor_click_scale")
    cfg.cursor_smooth_time = obs.obs_data_get_double(settings, "cursor_smooth_time")
    cfg.cursor_offset_x = obs.obs_data_get_int(settings, "cursor_offset_x")
    cfg.cursor_offset_y = obs.obs_data_get_int(settings, "cursor_offset_y")
    cfg.cursor_rotation_mode = obs.obs_data_get_string(settings, "cursor_rotation_mode") or "None"
    cfg.cursor_angle_offset = obs.obs_data_get_double(settings, "cursor_angle_offset")
    cfg.cursor_tilt_strength = obs.obs_data_get_double(settings, "cursor_tilt_strength")

    cfg.debug_logs = obs.obs_data_get_bool(settings, "debug_logs")
    cfg.allow_all_sources = obs.obs_data_get_bool(settings, "allow_all_sources")

    -- Apply preset overrides
    if global_presets[cfg.zoom_preset] then
        local p = global_presets[cfg.zoom_preset]
        cfg.zoom_duration = p.dur
        cfg.zoom_overshoot = p.ovr
        cfg.follow_smooth_time = p.smt
        if p.easing then cfg.zoom_easing = p.easing end
    end
end
```

**T-800: Settings UI (Abbreviated)**

```lua
function script_properties(settings)
    local props = obs.obs_properties_create()

    --==========================
    -- QUICK SETUP (always expanded)
    --==========================
    local grp_quick = obs.obs_properties_create()

    local src_list = obs.obs_properties_add_list(grp_quick, "source", "Zoom Source",
        obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    populate_sources(src_list)

    obs.obs_properties_add_float_slider(grp_quick, "zoom_value", "Zoom Factor", 1.0, 10.0, 0.1)

    local p_preset = obs.obs_properties_add_list(grp_quick, "zoom_preset", "Preset",
        obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_property_list_add_string(p_preset, "Custom", "Custom")
    for _, name in ipairs(get_sorted_preset_names()) do
        obs.obs_property_list_add_string(p_preset, name, name)
    end
    obs.obs_property_set_modified_callback(p_preset, on_preset_changed)

    obs.obs_properties_add_group(props, "quick_setup", "⚡ Quick Setup", obs.OBS_GROUP_NORMAL, grp_quick)

    --==========================
    -- ANIMATION (collapsed)
    --==========================
    local grp_anim = obs.obs_properties_create()

    local p_dur = obs.obs_properties_add_float_slider(grp_anim, "zoom_duration", "Duration (s)", 0.05, 3.0, 0.05)
    obs.obs_property_set_modified_callback(p_dur, on_slider_changed)

    local p_ovr = obs.obs_properties_add_float_slider(grp_anim, "zoom_overshoot", "Bounce", 0.0, 1.0, 0.01)
    obs.obs_property_set_modified_callback(p_ovr, on_slider_changed)

    -- Easing Curve Dropdown
    local p_easing = obs.obs_properties_add_list(grp_anim, "zoom_easing", "Easing Curve",
        obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    for _, name in ipairs(Easing.NAMES) do
        obs.obs_property_list_add_string(p_easing, name, name)
    end

    -- Scroll Zoom
    obs.obs_properties_add_float_slider(grp_anim, "scroll_step", "Scroll Step", 0.1, 1.0, 0.05)

    -- Preset management (nested)
    local grp_presets = obs.obs_properties_create()
    obs.obs_properties_add_text(grp_presets, "new_preset_name", "Name", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_button(grp_presets, "save_preset_btn", "Save Current", on_save_preset)
    obs.obs_properties_add_button(grp_presets, "delete_preset_btn", "Delete Current", on_delete_preset)
    obs.obs_properties_add_group(grp_anim, "preset_mgmt", "Manage Presets", obs.OBS_GROUP_NORMAL, grp_presets)

    obs.obs_properties_add_group(props, "animation", "🎬 Animation", obs.OBS_GROUP_NORMAL, grp_anim)

    --==========================
    -- MOUSE FOLLOW (collapsed)
    --==========================
    local grp_follow = obs.obs_properties_create()
    obs.obs_properties_add_bool(grp_follow, "follow", "Auto-Follow Mouse")
    local p_smt = obs.obs_properties_add_float_slider(grp_follow, "follow_smooth_time", "Smoothness", 0.01, 1.0, 0.01)
    obs.obs_property_set_modified_callback(p_smt, on_slider_changed)
    obs.obs_properties_add_int_slider(grp_follow, "follow_dead_zone", "Dead Zone (px)", 0, 500, 1)
    obs.obs_properties_add_bool(grp_follow, "follow_outside_bounds", "Follow Outside Bounds")
    obs.obs_properties_add_group(props, "follow", "🎯 Mouse Follow", obs.OBS_GROUP_NORMAL, grp_follow)

    --==========================
    -- EFFECTS (collapsed)
    --==========================
    local grp_fx = obs.obs_properties_create()

    local p_zb = obs.obs_properties_add_bool(grp_fx, "use_zoom_blur", "Zoom Blur")
    obs.obs_property_set_modified_callback(p_zb, on_blur_toggle)
    obs.obs_properties_add_float_slider(grp_fx, "zoom_blur_intensity", "Intensity", 0, 20, 0.5)
    obs.obs_properties_add_float_slider(grp_fx, "zoom_blur_clear_radius", "Clear Radius", 0, 2000, 1)

    local p_mb = obs.obs_properties_add_bool(grp_fx, "use_motion_blur", "Motion Blur")
    obs.obs_property_set_modified_callback(p_mb, on_blur_toggle)
    obs.obs_properties_add_float_slider(grp_fx, "motion_blur_intensity", "Intensity", 0, 20, 0.5)

    obs.obs_properties_add_group(props, "effects", "✨ Effects", obs.OBS_GROUP_NORMAL, grp_fx)

    --==========================
    -- CURSOR (collapsed)
    --==========================
    local grp_cursor = obs.obs_properties_create()
    obs.obs_properties_add_bool(grp_cursor, "cursor_enabled", "Enable Smooth Cursor")
    obs.obs_properties_add_float_slider(grp_cursor, "cursor_scale", "Scale", 0.1, 5.0, 0.05)
    obs.obs_properties_add_float_slider(grp_cursor, "cursor_smooth_time", "Smoothness", 0.01, 1.0, 0.01)
    obs.obs_properties_add_int_slider(grp_cursor, "cursor_offset_x", "X Offset", -100, 100, 1)
    obs.obs_properties_add_int_slider(grp_cursor, "cursor_offset_y", "Y Offset", -100, 100, 1)

    local p_rot = obs.obs_properties_add_list(grp_cursor, "cursor_rotation_mode", "Rotation",
        obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_property_list_add_string(p_rot, "None", "None")
    obs.obs_property_list_add_string(p_rot, "Lean", "Lean")
    obs.obs_property_list_add_string(p_rot, "Directional", "Directional")
    obs.obs_properties_add_float_slider(grp_cursor, "cursor_angle_offset", "Angle Offset", -180, 180, 1)
    obs.obs_properties_add_float_slider(grp_cursor, "cursor_tilt_strength", "Tilt Strength", 0, 2, 0.05)

    obs.obs_properties_add_group(props, "cursor", "🖱️ Smooth Cursor", obs.OBS_GROUP_NORMAL, grp_cursor)

    --==========================
    -- BOOKMARKS (collapsed)
    --==========================
    local grp_bm = obs.obs_properties_create()
    local bm_list = obs.obs_properties_add_list(grp_bm, "bookmark_select", "Bookmark",
        obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    for _, name in ipairs(BookmarkManager:get_names()) do
        obs.obs_property_list_add_string(bm_list, name, name)
    end
    obs.obs_properties_add_text(grp_bm, "bookmark_name", "Name", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_button(grp_bm, "bm_save", "Save Current Position", on_bookmark_save)
    obs.obs_properties_add_button(grp_bm, "bm_recall", "Jump To Selected", on_bookmark_recall)
    obs.obs_properties_add_button(grp_bm, "bm_delete", "Delete Selected", on_bookmark_delete)
    obs.obs_properties_add_text(grp_bm, "bm_info", "Bookmarks 1–5 can be assigned hotkeys in OBS Settings.", obs.OBS_TEXT_INFO)
    obs.obs_properties_add_group(props, "bookmarks", "📌 Bookmarks", obs.OBS_GROUP_NORMAL, grp_bm)

    --==========================
    -- ADVANCED (collapsed)
    --==========================
    local grp_adv = obs.obs_properties_create()
    obs.obs_properties_add_bool(grp_adv, "debug_logs", "Debug Logging")
    obs.obs_properties_add_bool(grp_adv, "allow_all_sources", "List All Sources")
    -- Monitor override, API, etc.
    obs.obs_properties_add_group(props, "advanced", "⚙️ Advanced", obs.OBS_GROUP_NORMAL, grp_adv)

    --==========================
    -- HELP (collapsed)
    --==========================
    local grp_help = obs.obs_properties_create()
    obs.obs_properties_add_text(grp_help, "help_text",
        "QUICK START:\n" ..
        "1. Select your capture source above\n" ..
        "2. Set hotkeys in OBS Settings → Hotkeys\n" ..
        "   • 'Toggle zoom to mouse' — Main zoom\n" ..
        "   • 'Zoom in/out (scroll)' — Scroll zoom\n" ..
        "3. Press the hotkey to zoom!\n\n" ..
        "TIPS:\n" ..
        "• Scroll zoom: Bind Ctrl+ScrollUp/Down for gradual zoom\n" ..
        "• Bookmarks: Save positions and jump to them with hotkeys\n" ..
        "• Everything auto-configures — no plugins needed!",
        obs.OBS_TEXT_INFO)
    obs.obs_properties_add_group(props, "help", "❓ Help", obs.OBS_GROUP_NORMAL, grp_help)

    return props
end
```

---

## 8. File Structure

```
obs-zoom-pro/
│
├── obs-zoom-pro.lua              # Main script (single file, ~2400 lines)
│
├── assets/
│   ├── cursors/
│   │   ├── arrow.png             # 32x32 default arrow cursor
│   │   ├── pointer.png           # 32x32 hand/pointer cursor
│   │   └── ibeam.png             # 32x32 text selection cursor
│   │
│   └── shaders/
│       ├── zoom_blur.effect      # Radial zoom blur HLSL
│       └── motion_blur.effect    # Directional motion blur HLSL
│
├── examples/
│   ├── api-client.py             # Example Python UDP client
│   └── streamdeck-commands.txt   # Stream Deck setup guide
│
├── README.md                     # Full documentation
├── CHANGELOG.md                  # Release notes
├── LICENSE                       # MIT License
└── .github/
    └── ISSUE_TEMPLATE/
        ├── bug_report.md
        └── feature_request.md
```

---

## 9. Dependency Graph

```
Phase 1 (Foundation)
═══════════════════
T-100 Logging ──────────────────────────────────────────────────┐
T-101 Math Utilities ───────────────────────────────────────────┤
T-102 Easing Library ──────────┐                                │
T-103 SmoothDamp ──────────────┤                                │
T-104 Platform Layer ──────────┤                                │
                               ▼                                │
T-105 State Machine ───────────┐                                │
                               ▼                                │
T-106 Crop Filter Manager ─────┤                                │
T-107 Source Manager ──────────┤◄───────────────────────────────┘
T-108 Camera Physics ──────────┘
         │
         ▼
T-200 Main Loop ◄── T-201 Hotkeys
T-202 Monitor Info
T-203 Transform Restore
T-204 OBS Lifecycle
T-205 Minimal UI
         │
         ▼
    ✅ PHASE 1 COMPLETE
         │
Phase 2 (Smart)
═══════════════
T-300 Scroll Zoom ◄── Phase 1
T-301 Scroll Animation
T-302 Preset Manager
T-303 Preset UI
         │
T-400 Auto Source Detection
T-401 Scene Memory
T-402 Scene Memory UI
T-403 Easing Dropdown
         │
         ▼
    ✅ PHASE 2 COMPLETE
         │
Phase 3 (Effects)
═════════════════
T-500 Blur Research ◄── Phase 1
T-501 Blur Strategy A (Shader)
T-502 Blur Strategy B (Plugin)  ←── Fallback if T-501 fails
T-503 Blur Strategy C (Skip)    ←── Fallback if T-502 fails
T-504 Zoom Blur Logic
T-505 Motion Blur Logic
         │
T-600 Asset Manager
T-601 Cursor Renderer ◄── T-600
T-602 Cursor Shape Swap
T-603 Cursor Physics
T-604 Cursor Cleanup
         │
         ▼
    ✅ PHASE 3 COMPLETE
         │
Phase 4 (Extensions)
════════════════════
T-700 Bookmark Data ◄── Phase 1
T-701 Bookmark Animation
T-702 Bookmark Hotkeys
T-703 Bookmark UI
         │
T-704 UDP API Server
T-705 API Testing
         │
         ▼
    ✅ PHASE 4 COMPLETE
         │
Phase 5 (Polish)
════════════════
T-800 Full UI ◄── All Phases
T-801 Validation
T-802 Config Refactor
T-803 Cross-Platform Test
T-804 Performance Profile
T-805 Bug Fixes
T-806 README
T-807 CHANGELOG
T-808 LICENSE
T-809 Demo Video
T-810 Release
         │
         ▼
    🚀 v1.0 RELEASE
```

---

## 10. Risk Register & Contingencies

| # | Risk | Phase | Prob. | Impact | Contingency | Owner |
|---|---|---|---|---|---|---|
| R1 | OBS Lua can't load custom `.effect` shaders | 3 | High | High | **Strategy B:** Auto-create Composite Blur filters. User gets blur with zero manual work but needs plugin. **Strategy C:** Skip blur entirely, document limitation. | T-500 research task |
| R2 | `obs_scene_add()` doesn't work for auto-created cursor source | 3 | Med | High | **Fallback:** Create source + add to scene requires specific OBS API version. If fails, fall back to competitor approach (user creates image source, we just manage it). Add "Auto Setup" button that walks user through it. | T-601 |
| R3 | `obs_source_remove()` crashes on cleanup | 3 | Low | High | **Fallback:** Don't remove source, just hide it. Add "[ZoomPro]" prefix so users can identify and remove manually. Log clear instructions. | T-604 |
| R4 | Scroll-wheel can't be captured via OBS hotkeys reliably | 2 | Med | Med | **Fallback:** Use `GetAsyncKeyState` FFI on Windows to poll scroll state. On Linux/Mac: document as Windows-only feature or use modifier+hotkey approach (Ctrl+Plus/Minus). | T-300 |
| R5 | SmoothDamp produces NaN on edge cases | 1 | Low | High | **Guard:** Add NaN/infinity check after every SmoothDamp call. If NaN detected, snap to target and reset velocity. Already have `clamp(0.001, 0.1, dt)` guard on dt. | T-103 |
| R6 | Performance regression with all features enabled at 4K | 5 | Med | Med | **Mitigation:** Diff-based output (skip if unchanged). Reduce blur sample count at high res. Make cursor update rate configurable. Profile in T-804 and set perf budget per module. | T-804 |
| R7 | Scene memory map grows unbounded | 2 | Low | Low | **Mitigation:** Cap at 50 entries. LRU eviction. Warn user in logs if near limit. | T-401 |
| R8 | Base64-embedded cursor images increase script size too much | 3 | Low | Low | **Decision:** Don't embed base64. Ship cursor PNGs as separate files in `assets/` directory. Simpler, smaller, user can customize. | T-600 |
| R9 | Rapid scroll + toggle + bookmark hotkeys cause state machine corruption | 4 | Med | Med | **Guard:** Every state transition goes through `SM:transition()` which validates current state. Add `can_*()` guard functions. Queue conflicting inputs instead of dropping. | T-105 |
| R10 | OBS API changes in v31+ break FFI calls | 5 | Low | High | **Mitigation:** Version-gate all FFI calls. Maintain compatibility matrix in code comments. Test on latest OBS beta before release. | T-803 |

---

## 11. Testing Strategy Per Phase

### Phase 1 Tests

```
UNIT TESTS (manual verification in OBS Script Log):
─────────────────────────────────────────────────────
[M02] clamp(0, 10, -5)  → 0
[M02] clamp(0, 10, 15)  → 10
[M02] clamp(0, 10, 5)   → 5
[M02] lerp(0, 100, 0.5) → 50
[M02] lerp(0, 100, 0)   → 0
[M02] lerp(0, 100, 1)   → 100

[M03] Easing.Cubic.Out(0)   → 0
[M03] Easing.Cubic.Out(1)   → 1
[M03] Easing.Cubic.Out(0.5) → ~0.875
[M03] Easing.Bounce.Out(0)  → 0
[M03] Easing.Bounce.Out(1)  → 1
[M03] Easing.get("Cubic.Out") returns function
[M03] Easing.get("Invalid.Blah") returns Cubic.Out fallback

[M04] SmoothDamp(0, 100, {val=0}, 0.1, 9999, 0.016)
      → returns value between 0 and 100
      → velocity.val > 0
[M04] SmoothDamp(100, 100, {val=50}, 0.1, 9999, 0.016)
      → returns ~100
      → velocity.val → 0

[M05] StateMachine:can_zoom_in() when IDLE → true
[M05] StateMachine:can_zoom_in() when ZOOMING_IN → false
[M05] StateMachine:transition() logs old→new
[M05] StateMachine:complete() from ZOOMING_IN → ZOOMED_IN
[M05] StateMachine:complete() from ZOOMING_OUT → IDLE

INTEGRATION TESTS (manual in OBS):
──────────────────────────────────
□ Press zoom hotkey → smooth zoom in to cursor
□ Press again → smooth zoom out to original
□ Enable follow → camera tracks mouse
□ Disable follow → camera stops
□ Move mouse to corner → camera stays in bounds
□ Switch scene → source released, re-acquired
□ Switch back → source works again
□ Reload script → original transform restored
□ Press hotkey 10x fast → no crash, consistent state
□ Delete source while zoomed → graceful reset
□ OBS restart → hotkeys remembered
```

### Phase 2 Tests

```
SCROLL ZOOM:
□ Ctrl+ScrollUp → zoom increases by scroll_step
□ Ctrl+ScrollUp x4 → zoom at initial + 4*step
□ Ctrl+ScrollDown below 1.0 → fully resets to unzoomed
□ Scroll while already animating → smooth interrupt
□ Scroll without modifier → no zoom (no conflict)
□ Toggle hotkey while scroll-zoomed → clean zoom out

PRESETS:
□ Select "Smooth" → duration=0.8, overshoot=0.0
□ Select "Bounce" → duration=0.6, overshoot=0.35
□ Change duration slider → preset switches to "Custom"
□ Save custom preset "MyPreset" → appears in dropdown
□ Delete "MyPreset" → removed from dropdown
□ Restart OBS → custom preset persists
□ Cannot delete built-in presets

SCENE MEMORY:
□ Set source in Scene A → remembered
□ Switch to Scene B → uses Scene B source (or global fallback)
□ Switch back to Scene A → uses Scene A source
□ Restart OBS → scene mapping persists
```

### Phase 3 Tests

```
BLUR:
□ Enable zoom blur → blur visible during zoom transition
□ Blur peaks at ~50% of transition → visual verification
□ Blur returns to 0 at end of transition
□ Clear radius creates sharp center area
□ Enable motion blur → blur during camera pan
□ Motion blur direction matches movement
□ No blur when camera stationary
□ Disable blur → no filter updates (performance)
□ Unload script → auto-created filters removed
□ Strategy fallback: no Composite Blur plugin → built-in or skip

CURSOR:
□ First run → cursor image appears without setup
□ Cursor tracks mouse smoothly
□ Cursor scales with zoom level
□ Left-click → cursor shrinks briefly
□ Hover link (hand cursor) → cursor image swaps (Windows)
□ Swap has pulse animation
□ Rotation "Lean" → cursor tilts on horizontal movement
□ Rotation "Directional" → cursor faces movement direction
□ Unload script → auto-created source removed
□ No cursor source in scene after unload
```

### Phase 4 Tests

```
BOOKMARKS:
□ Zoom to position → Save bookmark "test" → success
□ Zoom out → Recall "test" → animates to saved position
□ Saved zoom level matches original
□ Delete bookmark → removed from list
□ Hotkey 1 → jumps to first bookmark
□ 20 bookmarks saved → 21st rejected with message
□ Restart OBS → bookmarks persist

API:
□ Enable API → "Listening on port X" logged
□ Send "ZOOM_TOGGLE" via netcat → zoom toggles
□ Send "ZOOM_SET 3.0" → zoom to 3x
□ Send "FOLLOW_ON" → follow enabled
□ Send "STATUS" → JSON response with correct state
□ Send "BOOKMARK test" → jumps to saved position
□ Send invalid command → "ERROR: Unknown command" response
□ Disable API → socket closed
```

### Phase 5 Tests

```
PERFORMANCE (OBS Stats Panel, 60s average):
□ Idle (no zoom): CPU < 0.5%
□ Zoomed + Follow: CPU < 2% at 1080p60
□ Zoomed + Follow + Blur + Cursor: CPU < 3% at 1080p60
□ 1000 zoom cycles: memory growth < 1MB

CROSS-PLATFORM:
□ Windows 11 + OBS 30.x: All features
□ Windows 10 + OBS 29.1: All features
□ Linux X11 + OBS 30.x: Core zoom (no cursor shape)
□ macOS 14 + OBS 30.x: Core zoom (no cursor shape)

EDGE CASES:
□ Source with transform crop → auto-converted
□ Source with scale (non-bbox) → auto-converted
□ Source with existing crop filter → accounted for
□ Zoomed source deleted → graceful release
□ Scene with nested scenes → BFS finds source
□ Scene with groups → BFS finds source in group
□ Multiple instances of same source → uses first found
```

---

## 12. Definition of Done

### Per-Task DoD

- [ ] Code written and follows module structure
- [ ] No `print()` statements (use `log()`)
- [ ] All OBS resources have matching release calls
- [ ] FFI calls are pcall-wrapped
- [ ] Settings changes don't require OBS restart
- [ ] Manual test cases pass (per phase checklist above)

### Per-Phase DoD

- [ ] All tasks in phase complete
- [ ] Phase verification checklist 100% pass
- [ ] No known crashes or state corruption bugs
- [ ] Performance within budget
- [ ] Code reviewed (self or peer)

### Release DoD (v1.0)

- [ ] All Phase 1–5 DoD met
- [ ] README.md complete with screenshots
- [ ] CHANGELOG.md for v1.0
- [ ] MIT LICENSE file present
- [ ] Demo video recorded (60s)
- [ ] Tested on Windows 10, Windows 11, OBS 29.1+, OBS 30.x
- [ ] Linux/macOS tested (core features)
- [ ] GitHub release created with zip archive
- [ ] No P0 bugs open
- [ ] < 3 P1 bugs open (documented as known issues)

---

## Summary Timeline

```
Week 1  ████████████████  Phase 1a: Foundation modules
Week 2  ████████████████  Phase 1b: Integration + main loop
Week 3  ████████████████  Phase 2a: Scroll zoom + presets
Week 4  ████████████████  Phase 2b: Auto-detect + scene memory
Week 5  ████████████████  Phase 3a: Blur manager (research + impl)
Week 6  ████████████████  Phase 3b: Cursor renderer + Phase 4a: Bookmarks
Week 7  ████████████████  Phase 4b: API + Phase 5a: Full UI
Week 8  ████████████████  Phase 5b: Polish, test, document, release
        ─────────────────
        🚀 v1.0 Release
```

**Total estimated effort: ~160 hours (~20h/week for 8 weeks)**
