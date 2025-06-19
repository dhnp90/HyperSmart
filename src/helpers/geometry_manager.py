# geometry_manager.py

_last_geometry = None

def set_last_geometry(geometry_string):
    """Stores the last window geometry as a string."""
    global _last_geometry
    _last_geometry = geometry_string

def get_last_geometry():
    """Returns the stored window geometry string."""
    return _last_geometry

def get_centered_geometry(prev_geom_str, new_width, new_height):
    """
    Returns a geometry string (WxH+X+Y) to center a new window of size
    (new_width x new_height) relative to a previous window described
    by prev_geom_str (in "WxH+X+Y" format).
    """
    try:
        parts = prev_geom_str.split('+')
        size = parts[0]
        prev_x = int(parts[1])
        prev_y = int(parts[2])
        prev_width, prev_height = map(int, size.split('x'))

        center_x = prev_x + prev_width // 2
        center_y = prev_y + prev_height // 2

        new_x = center_x - new_width // 2
        new_y = center_y - new_height // 2

        return f"{new_width}x{new_height}+{new_x}+{new_y}"
    except Exception as e:
        print(f"[geometry_manager] Failed to center window: {e}")
        return f"{new_width}x{new_height}"  # fallback: centered on screen or default
