# OBS Zoom Pro

Intelligent camera zoom for OBS Studio with smooth animations, mouse follow, and zero external dependencies.

## Features

### Core Features
- **Smooth Toggle Zoom** - Zoom in/out with cinematic easing
- **Scroll-Wheel Zoom** - Dynamic zoom levels with scroll wheel
- **Mouse Follow** - Camera smoothly tracks your cursor
- **Dead Zone** - Prevents micro-jitter during tracking

### Advanced Features
- **23+ Easing Curves** - Cubic, Expo, Back, Elastic, Bounce, and more
- **Animation Presets** - Smooth, Bounce, Snappy, Cinematic + custom
- **Zoom Bookmarks** - Save and recall named zoom positions
- **Per-Scene Memory** - Remembers sources for each scene

### Visual Effects
- **Built-in Blur** - Zoom blur and motion blur (auto-detects Composite Blur plugin)
- **Auto Cursor** - Smooth cursor overlay without manual setup

### Integration
- **UDP API** - Control via Stream Deck or external tools
- **Cross-Platform** - Windows, Linux, macOS

## Quick Start

1. **Install**
   - Copy `obs-zoom-pro.lua` to your OBS scripts folder:
     - Windows: `%APPDATA%\obs-studio\basic\scripts\`
     - Linux/macOS: `~/.obs-studio/scripts/`

2. **Configure**
   - In OBS, go to **Tools → Scripts**
   - Add `obs-zoom-pro.lua`
   - Select your capture source in the Quick Setup panel
   - Set a hotkey for "Toggle Zoom to Mouse"

3. **Use**
   - Press your hotkey to zoom in at cursor position
   - Press again to zoom out
   - While zoomed, camera follows your mouse

## Commands (UDP API)

Connect to `localhost:12345` (configurable):

```
ZOOM_IN [level]     - Zoom in to level (default: configured value)
ZOOM_OUT            - Zoom out
ZOOM_SET level      - Set exact zoom level
ZOOM_TOGGLE        - Toggle zoom in/out
FOLLOW_ON           - Enable mouse follow
FOLLOW_OFF          - Disable mouse follow
FOLLOW_TOGGLE      - Toggle mouse follow
PRESET name         - Apply preset (Smooth, Bounce, Snappy, Cinematic)
BOOKMARK name       - Jump to bookmark
STATUS              - Get current state as JSON
```

## Settings

### Quick Setup
- **Zoom Source** - Source to zoom (display capture, game capture, etc.)
- **Zoom Factor** - Magnification level (1.0 - 10.0x)
- **Duration** - Animation duration in seconds

### Animation
- **Bounce** - Overshoot amount (0 = no bounce)
- **Easing Curve** - Animation curve (23 options)
- **Scroll Step** - Zoom increment per scroll tick

### Mouse Follow
- **Auto-Follow** - Camera tracks mouse while zoomed
- **Smoothness** - How smoothly camera follows
- **Dead Zone** - Radius where camera doesn't move

### Effects
- **Zoom Blur** - Blur during zoom transitions
- **Motion Blur** - Directional blur during panning

### Bookmarks
- Save up to 20 named zoom positions
- Assign hotkeys to bookmarks 1-5 in OBS Settings

### UDP API
- **Enable** - Start API server
- **Port** - UDP listen port (default: 12345)

## Requirements

- OBS Studio 29.0 or later
- No external plugins required (blur effects auto-detect Composite Blur if installed)

## Supported Platforms

- ✅ Windows 10/11 (full support)
- ✅ Linux (X11, basic cursor)
- ✅ macOS (basic cursor)

## Comparison vs. Competition

| Feature | Competitor | OBS Zoom Pro |
|---------|------------|--------------|
| Toggle zoom | ✅ | ✅ |
| Scroll-wheel zoom | ❌ | ✅ |
| Smooth easing | 3 curves | 23+ curves |
| Zero-config blur | ❌ | ✅ |
| Auto cursor | ❌ | ✅ |
| Zoom bookmarks | ❌ | ✅ |
| Per-scene memory | ❌ | ✅ |
| External API | Mouse only | Full command set |
| Setup time | ~5 min | ~10 sec |

## License

MIT License - See LICENSE file

## Author

[Your Name]

## Version

1.0.0
