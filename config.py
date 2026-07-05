"""
Nyan Cat Progress Bar - Configuration
=====================================
All configuration constants for the Nyan Cat progress bar app.
"""

# ============ Window Settings ============
WINDOW_HEIGHT = 120          # Total window height (pixels)
WINDOW_TOP_OFFSET = 85       # Distance from bottom of screen (above Dock)
UPDATE_INTERVAL_MS = 1000    # Update interval in milliseconds (1 second)
ANIMATION_FPS = 8            # Frame animation speed for cat legs

# ============ Size Presets ============
SIZE_PRESETS = {
    "small":  {"scale": 2, "label": "S"},
    "medium": {"scale": 3, "label": "M"},
    "large":  {"scale": 4, "label": "L"},
}
DEFAULT_SIZE = "medium"

# ============ Nyan Cat Colors ============
COLORS = {
    # Pop-Tart body
    "crust":        (204, 153, 0, 255),       # Brown crust
    "frosting":     (255, 153, 204, 255),     # Pink frosting
    "sprinkles":    (255, 255, 255, 255),     # White sprinkles
    
    # Cat parts
    "cat_body":     (128, 128, 128, 255),     # Gray body
    "cat_dark":     (80, 80, 80, 255),        # Dark gray details
    "cat_face":     (255, 192, 203, 255),     # Pink cheeks
    "cat_eye":      (0, 0, 0, 255),           # Black eyes
    "cat_nose":     (255, 105, 180, 255),     # Pink nose
    "cat_inner_ear":(255, 182, 193, 255),     # Inner ear pink
    
    # Rainbow colors (top to bottom: red, orange, yellow, green, blue, violet)
    "rainbow": [
        (255, 0, 0, 255),       # Red
        (255, 127, 0, 255),     # Orange
        (255, 255, 0, 255),     # Yellow
        (0, 255, 0, 255),       # Green
        (0, 0, 255, 255),       # Blue
        (128, 0, 255, 255),     # Violet
    ],
    
    # UI
    "bubble_bg":    (50, 50, 50, 200),        # Time bubble background
    "bubble_text":  (255, 255, 255, 255),     # Time bubble text
    "bubble_border": (255, 153, 204, 255),    # Bubble border pink
}

# ============ Nyan Cat Pixel Art ============
# Each frame is a list of (x, y, color_key) tuples
# The cat is 19 pixels wide and 12 pixels tall (before scaling)
# Origin (0,0) is top-left of cat area

CAT_WIDTH = 20   # pixels
CAT_HEIGHT = 14  # pixels (including legs)

# Frame 1: legs down
CAT_FRAME_1 = [
    # --- Pop-Tart Body (center) ---
    # Crust outline
    (5, 2, "crust"), (6, 2, "crust"), (7, 2, "crust"), (8, 2, "crust"),
    (9, 2, "crust"), (10, 2, "crust"), (11, 2, "crust"), (12, 2, "crust"),
    (5, 9, "crust"), (6, 9, "crust"), (7, 9, "crust"), (8, 9, "crust"),
    (9, 9, "crust"), (10, 9, "crust"), (11, 9, "crust"), (12, 9, "crust"),
    (4, 3, "crust"), (4, 4, "crust"), (4, 5, "crust"), (4, 6, "crust"),
    (4, 7, "crust"), (4, 8, "crust"),
    (13, 3, "crust"), (13, 4, "crust"), (13, 5, "crust"), (13, 6, "crust"),
    (13, 7, "crust"), (13, 8, "crust"),
    
    # Frosting fill
    (5, 3, "frosting"), (6, 3, "frosting"), (7, 3, "frosting"), (8, 3, "frosting"),
    (9, 3, "frosting"), (10, 3, "frosting"), (11, 3, "frosting"), (12, 3, "frosting"),
    (5, 4, "frosting"), (6, 4, "frosting"), (7, 4, "frosting"), (8, 4, "frosting"),
    (9, 4, "frosting"), (10, 4, "frosting"), (11, 4, "frosting"), (12, 4, "frosting"),
    (5, 5, "frosting"), (6, 5, "frosting"), (7, 5, "frosting"), (8, 5, "frosting"),
    (9, 5, "frosting"), (10, 5, "frosting"), (11, 5, "frosting"), (12, 5, "frosting"),
    (5, 6, "frosting"), (6, 6, "frosting"), (7, 6, "frosting"), (8, 6, "frosting"),
    (9, 6, "frosting"), (10, 6, "frosting"), (11, 6, "frosting"), (12, 6, "frosting"),
    (5, 7, "frosting"), (6, 7, "frosting"), (7, 7, "frosting"), (8, 7, "frosting"),
    (9, 7, "frosting"), (10, 7, "frosting"), (11, 7, "frosting"), (12, 7, "frosting"),
    (5, 8, "frosting"), (6, 8, "frosting"), (7, 8, "frosting"), (8, 8, "frosting"),
    (9, 8, "frosting"), (10, 8, "frosting"), (11, 8, "frosting"), (12, 8, "frosting"),
    
    # Sprinkles
    (6, 4, "sprinkles"), (9, 5, "sprinkles"), (11, 4, "sprinkles"),
    (7, 7, "sprinkles"), (10, 6, "sprinkles"), (8, 3, "sprinkles"),
    (12, 8, "sprinkles"), (5, 6, "sprinkles"), (11, 7, "sprinkles"),
    
    # --- Cat Head (right side) ---
    # Ears
    (15, 0, "cat_dark"), (16, 0, "cat_dark"),
    (15, 1, "cat_inner_ear"), (16, 1, "cat_dark"),
    (14, 1, "cat_dark"),
    (17, 1, "cat_dark"), (18, 1, "cat_dark"),
    (17, 0, "cat_inner_ear"), (18, 0, "cat_dark"),
    
    # Head body
    (14, 2, "cat_dark"), (15, 2, "cat_body"), (16, 2, "cat_body"),
    (17, 2, "cat_body"), (18, 2, "cat_dark"),
    (14, 3, "cat_dark"), (15, 3, "cat_body"), (16, 3, "cat_eye"),
    (17, 3, "cat_body"), (18, 3, "cat_dark"),
    (14, 4, "cat_dark"), (15, 4, "cat_body"), (16, 4, "cat_body"),
    (17, 4, "cat_eye"), (18, 4, "cat_dark"),
    (14, 5, "cat_dark"), (15, 5, "cat_face"), (16, 5, "cat_nose"),
    (17, 5, "cat_face"), (18, 5, "cat_dark"),
    (14, 6, "cat_dark"), (15, 6, "cat_dark"), (16, 6, "cat_dark"),
    (17, 6, "cat_dark"), (18, 6, "cat_dark"),
    
    # --- Legs (Frame 1 - legs down) ---
    (5, 10, "cat_dark"), (6, 10, "cat_dark"),
    (11, 10, "cat_dark"), (12, 10, "cat_dark"),
    (5, 11, "cat_dark"), (6, 11, "cat_dark"),
    (11, 11, "cat_dark"), (12, 11, "cat_dark"),
    
    # Tail
    (14, 7, "cat_dark"), (15, 7, "cat_dark"),
    (15, 8, "cat_dark"), (16, 8, "cat_dark"),
]

# Frame 2: legs up (alternating)
CAT_FRAME_2 = [
    # --- Pop-Tart Body (same as frame 1) ---
    # Crust outline
    (5, 2, "crust"), (6, 2, "crust"), (7, 2, "crust"), (8, 2, "crust"),
    (9, 2, "crust"), (10, 2, "crust"), (11, 2, "crust"), (12, 2, "crust"),
    (5, 9, "crust"), (6, 9, "crust"), (7, 9, "crust"), (8, 9, "crust"),
    (9, 9, "crust"), (10, 9, "crust"), (11, 9, "crust"), (12, 9, "crust"),
    (4, 3, "crust"), (4, 4, "crust"), (4, 5, "crust"), (4, 6, "crust"),
    (4, 7, "crust"), (4, 8, "crust"),
    (13, 3, "crust"), (13, 4, "crust"), (13, 5, "crust"), (13, 6, "crust"),
    (13, 7, "crust"), (13, 8, "crust"),
    
    # Frosting fill
    (5, 3, "frosting"), (6, 3, "frosting"), (7, 3, "frosting"), (8, 3, "frosting"),
    (9, 3, "frosting"), (10, 3, "frosting"), (11, 3, "frosting"), (12, 3, "frosting"),
    (5, 4, "frosting"), (6, 4, "frosting"), (7, 4, "frosting"), (8, 4, "frosting"),
    (9, 4, "frosting"), (10, 4, "frosting"), (11, 4, "frosting"), (12, 4, "frosting"),
    (5, 5, "frosting"), (6, 5, "frosting"), (7, 5, "frosting"), (8, 5, "frosting"),
    (9, 5, "frosting"), (10, 5, "frosting"), (11, 5, "frosting"), (12, 5, "frosting"),
    (5, 6, "frosting"), (6, 6, "frosting"), (7, 6, "frosting"), (8, 6, "frosting"),
    (9, 6, "frosting"), (10, 6, "frosting"), (11, 6, "frosting"), (12, 6, "frosting"),
    (5, 7, "frosting"), (6, 7, "frosting"), (7, 7, "frosting"), (8, 7, "frosting"),
    (9, 7, "frosting"), (10, 7, "frosting"), (11, 7, "frosting"), (12, 7, "frosting"),
    (5, 8, "frosting"), (6, 8, "frosting"), (7, 8, "frosting"), (8, 8, "frosting"),
    (9, 8, "frosting"), (10, 8, "frosting"), (11, 8, "frosting"), (12, 8, "frosting"),
    
    # Sprinkles
    (6, 4, "sprinkles"), (9, 5, "sprinkles"), (11, 4, "sprinkles"),
    (7, 7, "sprinkles"), (10, 6, "sprinkles"), (8, 3, "sprinkles"),
    (12, 8, "sprinkles"), (5, 6, "sprinkles"), (11, 7, "sprinkles"),
    
    # --- Cat Head (same as frame 1) ---
    (15, 0, "cat_dark"), (16, 0, "cat_dark"),
    (15, 1, "cat_inner_ear"), (16, 1, "cat_dark"),
    (14, 1, "cat_dark"),
    (17, 1, "cat_dark"), (18, 1, "cat_dark"),
    (17, 0, "cat_inner_ear"), (18, 0, "cat_dark"),
    
    (14, 2, "cat_dark"), (15, 2, "cat_body"), (16, 2, "cat_body"),
    (17, 2, "cat_body"), (18, 2, "cat_dark"),
    (14, 3, "cat_dark"), (15, 3, "cat_body"), (16, 3, "cat_eye"),
    (17, 3, "cat_body"), (18, 3, "cat_dark"),
    (14, 4, "cat_dark"), (15, 4, "cat_body"), (16, 4, "cat_body"),
    (17, 4, "cat_eye"), (18, 4, "cat_dark"),
    (14, 5, "cat_dark"), (15, 5, "cat_face"), (16, 5, "cat_nose"),
    (17, 5, "cat_face"), (18, 5, "cat_dark"),
    (14, 6, "cat_dark"), (15, 6, "cat_dark"), (16, 6, "cat_dark"),
    (17, 6, "cat_dark"), (18, 6, "cat_dark"),
    
    # --- Legs (Frame 2 - legs UP, offset by 1) ---
    (5, 10, "cat_dark"), (7, 10, "cat_dark"),
    (10, 10, "cat_dark"), (12, 10, "cat_dark"),
    (5, 11, "cat_dark"), (7, 11, "cat_dark"),
    (10, 11, "cat_dark"), (12, 11, "cat_dark"),
    
    # Tail
    (14, 7, "cat_dark"), (15, 7, "cat_dark"),
    (15, 8, "cat_dark"), (16, 8, "cat_dark"),
]

CAT_FRAMES = [CAT_FRAME_1, CAT_FRAME_2]

# ============ Star sparkle settings ============
STAR_COUNT = 5
STAR_COLORS = [
    (255, 255, 0, 255),
    (255, 255, 255, 255),
    (0, 255, 255, 255),
]
