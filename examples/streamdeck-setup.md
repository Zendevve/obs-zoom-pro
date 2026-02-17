# OBS Zoom Pro - Stream Deck Setup

This guide explains how to set up OBS Zoom Pro with Stream Deck.

## Option 1: Stream Deck OBS Plugin (Recommended)

1. Install the **Stream Deck OBS Plugin** from the Stream Deck Store
2. In Stream Deck, add a new action
3. Search for "OBS" and select "Switch to Scene" or "Hotkey"
4. For zoom control, use the **Hotkey** action:
   - Select your OBS profile
   - Enter the hotkey name:
     - `Toggle Zoom to Mouse`
     - `Toggle Mouse Follow`
     - `Zoom In (Scroll)`
     - `Zoom Out (Scroll)`
     - `Zoom to Bookmark 1` through `Zoom to Bookmark 5`

## Option 2: UDP API with Stream Deck System

If you want to use the UDP API directly:

1. Enable the UDP API in OBS Zoom Pro settings:
   - Go to Tools → Scripts → obs-zoom-pro
   - Enable "UDP API Server"
   - Note the port (default: 12345)

2. Create a Stream Deck "Open URL" action:
   - This won't work directly for UDP

3. Use a plugin like "Stream Deck System Actions" with plugins or use the API via a proxy

## Option 3: Third-Party Integration

### Python Script
Run the provided `api-client.py` script:

```bash
# Zoom in
python api-client.py ZOOM_IN

# Zoom out
python api-client.py ZOOM_OUT

# Zoom to level
python api-client.py ZOOM_SET 2.5

# Toggle zoom
python api-client.py ZOOM_TOGGLE

# Apply preset
python api-client.py PRESET Cinematic

# Jump to bookmark
python api-client.py BOOKMARK code_editor

# Get status
python api-client.py STATUS
```

### Stream Deck Button Configuration

For each button, configure as "Open" with a custom protocol or use the Stream Deck SDK.

## Quick Reference

| Action | Hotkey | API Command |
|--------|--------|-------------|
| Toggle Zoom | `Toggle Zoom to Mouse` | `ZOOM_TOGGLE` |
| Zoom In | `Zoom In (Scroll)` | `ZOOM_IN` |
| Zoom Out | `Zoom Out (Scroll)` | `ZOOM_OUT` |
| Follow On | `Toggle Mouse Follow` | `FOLLOW_ON` |
| Follow Off | - | `FOLLOW_OFF` |
| Bookmark 1 | `Zoom to Bookmark 1` | `BOOKMARK name` |
| Bookmark 2 | `Zoom to Bookmark 2` | - |
| Bookmark 3 | `Zoom to Bookmark 3` | - |
| Bookmark 4 | `Zoom to Bookmark 4` | - |
| Bookmark 5 | `Zoom to Bookmark 5` | - |

## Tips

- Set up your bookmarks first with descriptive names
- Use consistent zoom presets for different use cases
- The API is useful for custom automation beyond hotkeys
