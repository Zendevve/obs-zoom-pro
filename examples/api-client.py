#!/usr/bin/env python3
"""
OBS Zoom Pro - Example UDP API Client

This script demonstrates how to control OBS Zoom Pro from external applications
like Stream Deck, Home Assistant, or other automation tools.

Usage:
    python api-client.py ZOOM_IN
    python api-client.py ZOOM_OUT 2.5
    python api-client.py STATUS
"""

import socket
import sys
import json
import time

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 12345


def send_command(command, host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Send a command to OBS Zoom Pro and return the response."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1.0)

        # Send command
        sock.sendto(command.encode('utf-8'), (host, port))

        # Try to receive response (UDP may not always respond)
        try:
            data, addr = sock.recvfrom(4096)
            response = data.decode('utf-8')
            return response
        except socket.timeout:
            return None  # No response (UDP is fire-and-forget)

    except Exception as e:
        return f"ERROR: {str(e)}"
    finally:
        sock.close()


def main():
    if len(sys.argv) < 2:
        print("Usage: python api-client.py <command> [args]")
        print()
        print("Commands:")
        print("  ZOOM_IN [level]    - Zoom in (default: configured level)")
        print("  ZOOM_OUT           - Zoom out")
        print("  ZOOM_SET level     - Set exact zoom level")
        print("  ZOOM_TOGGLE        - Toggle zoom in/out")
        print("  FOLLOW_ON          - Enable mouse follow")
        print("  FOLLOW_OFF         - Disable mouse follow")
        print("  FOLLOW_TOGGLE      - Toggle mouse follow")
        print("  PRESET name        - Apply preset (Smooth, Bounce, Snappy, Cinematic)")
        print("  BOOKMARK name      - Jump to bookmark")
        print("  STATUS             - Get current state as JSON")
        print("  HELP               - Show this help")
        sys.exit(1)

    cmd = sys.argv[1].upper()
    args = sys.argv[2:]

    # Build command
    if args:
        command = f"{cmd} {' '.join(args)}"
    else:
        command = cmd

    # Special handling for STATUS (we want to parse JSON)
    if cmd == "STATUS":
        response = send_command(command)
        if response:
            try:
                status = json.loads(response)
                print(f"Zoom Level: {status.get('zoom_level', 'N/A')}")
                print(f"State: {status.get('state', 'N/A')}")
                print(f"Following: {status.get('following', 'N/A')}")
                print(f"Position: ({status.get('position', {}).get('x', 0)}, {status.get('position', {}).get('y', 0)})")
                print(f"Preset: {status.get('preset', 'N/A')}")
            except json.JSONDecodeError:
                print(response)
        else:
            print("No response (check if OBS Zoom Pro is running with API enabled)")
    else:
        response = send_command(command)
        if response:
            print(response)
        else:
            print("Command sent (no response)")


if __name__ == "__main__":
    main()
