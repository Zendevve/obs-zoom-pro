# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-06-?? (Draft)

### Added
- **Core Zoom Engine**
  - Smooth toggle zoom with easing
  - Scroll-wheel zoom (dynamic zoom levels)
  - Mouse follow with SmoothDamp physics
  - Dead zone for jitter prevention
  - 23+ easing functions (Linear, Quad, Cubic, Quart, Quint, Sine, Expo, Circ, Back, Elastic, Bounce)

- **Preset System**
  - 4 built-in presets (Smooth, Bounce, Snappy, Cinematic)
  - Custom preset support (save/load/delete)
  - Per-preset easing curves

- **Smart Features**
  - Auto source detection on first run
  - Per-scene source memory
  - Zoom bookmarks (up to 20 positions)
  - 5 bookmark hotkeys

- **Visual Effects**
  - Built-in zoom blur (auto-detects Composite Blur plugin)
  - Built-in motion blur
  - Auto cursor overlay
  - Cursor shape detection (Windows)
  - Cursor rotation modes (None, Lean, Directional)

- **External Control**
  - UDP API server for Stream Deck integration
  - Commands: ZOOM_IN, ZOOM_OUT, ZOOM_SET, ZOOM_TOGGLE, FOLLOW_ON/OFF/TOGGLE, PRESET, BOOKMARK, STATUS

- **Cross-Platform**
  - Windows full support
  - Linux (X11) support
  - macOS support

### Features Comparison vs Competition
- Scroll-wheel zoom (competitor lacks this)
- Zero-config blur (competitor requires external plugin + manual setup)
- Auto cursor (competitor requires manual image source creation)
- Zoom bookmarks (competitor lacks this)
- Per-scene memory (competitor lacks this)
- Full UDP API (competitor only has mouse position)

### Known Limitations
- Wayland on Linux: Documented as unsupported
- Cursor shape detection: Windows only (falls back to arrow on other platforms)
- Blur effects: Requires Composite Blur plugin OR auto-creates filters if plugin detected

### Requirements
- OBS Studio 29.0 or later
