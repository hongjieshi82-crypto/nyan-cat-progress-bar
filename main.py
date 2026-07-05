#!/usr/bin/env python3
"""
Nyan Cat Progress Bar - Main Application
==========================================
A pixel-art Nyan Cat that moves across the bottom of your Mac screen,
showing the current time progress of the day with a rainbow trail.

Usage:
    python main.py [--size small|medium|large] [--hide-bubble] [--debug]

Requirements:
    pip install PySide6
"""

import sys
import os
import math
import random
import time as time_module
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication, QWidget, QSystemTrayIcon, QMenu, QToolTip,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import (
    Qt, QTimer, QRect, QPoint, QSize, QPropertyAnimation, QEasingCurve,
    Signal, Slot
)
from PySide6.QtGui import (
    QPainter, QColor, QPen, QFont, QFontMetrics, QPixmap,
    QCursor, QAction, QPalette, QScreen
)

from config import (
    WINDOW_HEIGHT, WINDOW_TOP_OFFSET, UPDATE_INTERVAL_MS, ANIMATION_FPS,
    SIZE_PRESETS, DEFAULT_SIZE, COLORS, CAT_FRAMES, CAT_WIDTH, CAT_HEIGHT,
    STAR_COUNT, STAR_COLORS
)


# ═══════════════════════════════════════════════════════════
#  Star Sparkle - floating stars around the cat
# ═══════════════════════════════════════════════════════════
class Star:
    """A tiny pixel star that twinkles near the cat."""
    
    def __init__(self, scale):
        self.reset(scale)
    
    def reset(self, scale):
        self.scale = scale
        self.x = random.randint(0, 22 * scale)
        self.y = random.randint(-2 * scale, 14 * scale)
        self.color = random.choice(STAR_COLORS)
        self.lifetime = random.uniform(0.5, 2.0)
        self.age = 0.0
        self.size = random.choice([1, 1, 2]) * scale
    
    def update(self, dt):
        self.age += dt
        if self.age > self.lifetime:
            self.reset(self.scale)
    
    @property
    def alpha(self):
        """Fade in and out."""
        progress = self.age / self.lifetime
        if progress < 0.2:
            return progress / 0.2
        elif progress > 0.8:
            return (1.0 - progress) / 0.2
        return 1.0


# ═══════════════════════════════════════════════════════════
#  Rainbow Trail Renderer
# ═══════════════════════════════════════════════════════════
class RainbowTrail:
    """Draws the rainbow stripes trailing behind the cat."""
    
    def __init__(self):
        self.phase = 0.0  # Color flow phase
        self.rainbow_colors = COLORS["rainbow"]
    
    def draw(self, painter, x_start, x_end, y_top, stripe_height, scale):
        """Draw rainbow stripes from x_start to x_end."""
        if x_end <= x_start:
            return
        
        stripe_h = stripe_height * scale
        num_colors = len(self.rainbow_colors)
        
        # Animate color flow
        phase_offset = self.phase
        
        for i, base_color in enumerate(self.rainbow_colors):
            # Shift colors over time for flowing effect
            color_idx = (i + int(phase_offset)) % num_colors
            color = self.rainbow_colors[color_idx]
            
            # Create gradient effect within each stripe
            y = y_top + i * stripe_h
            r, g, b, a = color
            
            # Add subtle brightness wave
            wave = math.sin(phase_offset * 0.5 + i * 0.3) * 15
            r = max(0, min(255, int(r + wave)))
            g = max(0, min(255, int(g + wave)))
            b = max(0, min(255, int(b + wave)))
            
            painter.fillRect(
                QRect(int(x_start), int(y), int(x_end - x_start), int(stripe_h) + 1),
                QColor(r, g, b, a)
            )
        
        # Add sparkle dots on rainbow
        self._draw_rainbow_sparkles(painter, x_start, x_end, y_top, stripe_h * num_colors, scale)
    
    def _draw_rainbow_sparkles(self, painter, x_start, x_end, y_top, total_height, scale):
        """Add occasional white sparkle pixels on the rainbow."""
        sparkle_seed = int(self.phase * 3) % 7
        spacing = 12 * scale
        if spacing < 4:
            spacing = 4
        
        for sx in range(int(x_start) + sparkle_seed * scale, int(x_end), spacing):
            sy = y_top + (hash(sx + int(self.phase)) % max(1, int(total_height - 2 * scale)))
            if 0 <= sx < 9999 and 0 <= sy < 9999:
                painter.fillRect(
                    QRect(sx, sy, max(1, scale), max(1, scale)),
                    QColor(255, 255, 255, 180)
                )
    
    def update(self, dt):
        """Advance the color flow animation."""
        self.phase += dt * 2.0


# ═══════════════════════════════════════════════════════════
#  Time Bubble - shows current time in a pixel bubble
# ═══════════════════════════════════════════════════════════
class TimeBubble:
    """Renders a pixel-style speech bubble showing current time."""
    
    def __init__(self):
        self.visible = True
        self.opacity = 1.0
        self.fade_target = 1.0
        self.hover_timer = 0.0
        self.show_mode = "always"  # "always", "hover", "hidden"
    
    def draw(self, painter, x, y, scale, current_time_str, progress_pct):
        """Draw the time bubble at position (x, y) relative to cat."""
        if not self.visible or self.opacity < 0.01:
            return
        
        # Bubble dimensions
        font_size = max(10, 11 * scale)
        font = QFont("Menlo", font_size)
        font.setStyleHint(QFont.StyleHint.Monospace)
        painter.setFont(font)
        
        # Text content
        time_text = current_time_str
        progress_text = f"{progress_pct:.1f}%"
        
        fm = QFontMetrics(font)
        text_width = max(fm.horizontalAdvance(time_text), fm.horizontalAdvance(progress_text))
        
        padding = max(4, 5 * scale)
        bubble_w = text_width + padding * 2
        bubble_h = fm.height() * 2 + padding * 2 + max(2, 3 * scale)
        
        # Position: above the cat
        bx = int(x - bubble_w / 2 + 10 * scale)
        by = int(y - bubble_h - 5 * scale)
        
        # Ensure bubble stays on screen
        if bx < 5:
            bx = 5
        if by < 5:
            by = int(y + 16 * scale)  # Show below if no room above
        
        alpha = int(255 * self.opacity)
        
        # Bubble background
        bg_color = QColor(*COLORS["bubble_bg"][:3], min(alpha, COLORS["bubble_bg"][3]))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.drawRoundedRect(QRect(bx, by, int(bubble_w), int(bubble_h)), 
                                max(3, 4 * scale), max(3, 4 * scale))
        
        # Border
        border_color = QColor(*COLORS["bubble_border"][:3], alpha)
        painter.setPen(QPen(border_color, max(1, 1 * scale)))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRect(bx, by, int(bubble_w), int(bubble_h)), 
                                max(3, 4 * scale), max(3, 4 * scale))
        
        # Small triangle pointer
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        tri_x = int(x + 5 * scale)
        tri_y = by + int(bubble_h)
        pointer = [
            QPoint(tri_x, tri_y),
            QPoint(tri_x + int(4 * scale), tri_y),
            QPoint(tri_x + int(2 * scale), tri_y + int(4 * scale)),
        ]
        painter.drawPolygon(pointer)
        
        # Text
        text_color = QColor(*COLORS["bubble_text"][:3], alpha)
        painter.setPen(text_color)
        
        text_x = bx + int(padding)
        text_y = by + int(padding) + fm.ascent()
        painter.drawText(QPoint(text_x, text_y), time_text)
        
        # Progress text (smaller)
        progress_font = QFont("Menlo", max(8, int(font_size * 0.75)))
        progress_font.setStyleHint(QFont.StyleHint.Monospace)
        painter.setFont(progress_font)
        fm2 = QFontMetrics(progress_font)
        progress_y = text_y + fm.height() + max(1, 2 * scale)
        
        # Progress bar mini visualization
        bar_x = text_x
        bar_w = int(text_width * progress_pct / 100.0)
        bar_h = max(2, 3 * scale)
        bar_y = progress_y - max(2, int(2 * scale))
        
        # Background bar
        painter.fillRect(QRect(bar_x, bar_y, int(text_width), int(bar_h)), 
                         QColor(80, 80, 80, alpha // 2))
        # Filled bar
        painter.fillRect(QRect(bar_x, bar_y, max(1, bar_w), int(bar_h)), 
                         QColor(255, 153, 204, alpha))


# ═══════════════════════════════════════════════════════════
#  Nyan Cat Widget - Main Window
# ═══════════════════════════════════════════════════════════
class NyanCatWidget(QWidget):
    """
    Transparent borderless widget that renders the Nyan Cat progress bar.
    Fixed at the bottom of the screen, above the Dock.
    """
    
    def __init__(self):
        super().__init__()
        
        # State
        self.current_size = DEFAULT_SIZE
        self.scale = SIZE_PRESETS[DEFAULT_SIZE]["scale"]
        self.anim_frame = 0
        self.anim_timer_count = 0.0
        self.last_update = time_module.time()
        
        # Components
        self.rainbow = RainbowTrail()
        self.bubble = TimeBubble()
        self.stars = [Star(self.scale) for _ in range(STAR_COUNT)]
        
        # Mouse tracking for bubble toggle
        self.mouse_over = False
        self.bubble.hover_mode = False  # If True, only show on hover
        
        # Setup window
        self._setup_window()
        
        # Timers
        self.position_timer = QTimer(self)
        self.position_timer.timeout.connect(self._update_position_and_time)
        self.position_timer.start(UPDATE_INTERVAL_MS)
        
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self._update_animation)
        self.anim_timer.start(int(1000 / ANIMATION_FPS))
        
        # Initial position
        self._update_position_and_time()
    
    def _setup_window(self):
        """Configure transparent, borderless, always-on-top window."""
        # Window flags: frameless, stays on top, tool window (no taskbar)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysTopLevelHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowDoesNotAcceptFocus
        )
        
        # Transparent background
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        
        # Don't steal focus
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)
    
    # ─── Position & Time ──────────────────────────────
    
    def _get_screen_info(self):
        """Get screen geometry and dock offset."""
        screen = QApplication.primaryScreen()
        if not screen:
            screen = self.screen()
        if not screen:
            return QRect(0, 0, 1920, 1080), 85
        
        geom = screen.geometry()
        available = screen.availableGeometry()
        
        # Calculate dock height from difference between screen and available geometry
        dock_height = geom.height() - available.height()
        if dock_height < 10:
            dock_height = WINDOW_TOP_OFFSET  # Default assumption
        
        return available, dock_height
    
    def _get_time_progress(self):
        """Calculate time progress as a fraction (0.0 to 1.0) of the day."""
        now = datetime.now()
        seconds_since_midnight = (
            now.hour * 3600 + now.minute * 60 + now.second + now.microsecond / 1_000_000
        )
        return seconds_since_midnight / 86400.0
    
    def _update_position_and_time(self):
        """Recalculate window position based on time progress."""
        screen, dock_height = self._get_screen_info()
        screen_w = screen.width()
        screen_h = screen.height()
        
        # Calculate cat pixel size
        cat_pixel_w = CAT_WIDTH * self.scale
        cat_pixel_h = CAT_HEIGHT * self.scale
        rainbow_h = 6 * 2 * self.scale  # 6 stripes, each 2px * scale
        
        # Window spans full screen width
        window_w = screen_w
        window_h = max(
            WINDOW_HEIGHT * self.scale // 3,
            cat_pixel_h + rainbow_h + 40 * self.scale // 3 + 20
        )
        
        # Position: bottom of screen, above dock
        window_x = screen.x()
        window_y = screen.y() + screen_h - window_h - int(dock_height * 0.6)
        
        self.setGeometry(window_x, window_y, window_w, window_h)
        self.update()
    
    # ─── Animation ────────────────────────────────────
    
    def _update_animation(self):
        """Advance animation frame."""
        now = time_module.time()
        dt = now - self.last_update
        self.last_update = now
        
        self.anim_timer_count += dt
        if self.anim_timer_count >= 1.0 / ANIMATION_FPS:
            self.anim_timer_count = 0
            self.anim_frame = (self.anim_frame + 1) % 2
        
        # Update rainbow flow
        self.rainbow.update(dt)
        
        # Update stars
        for star in self.stars:
            star.update(dt)
        
        # Update bubble fade
        if self.bubble.hover_mode:
            if self.mouse_over:
                self.bubble.opacity = min(1.0, self.bubble.opacity + dt * 5)
            else:
                self.bubble.opacity = max(0.0, self.bubble.opacity - dt * 5)
        else:
            self.bubble.opacity = min(1.0, self.bubble.opacity + dt * 3)
        
        self.update()
    
    # ─── Drawing ──────────────────────────────────────
    
    def paintEvent(self, event):
        """Main render method."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        
        screen_w = self.width()
        window_h = self.height()
        
        # Time progress
        progress = self._get_time_progress()
        
        # Cat position
        cat_pixel_w = CAT_WIDTH * self.scale
        cat_pixel_h = CAT_HEIGHT * self.scale
        rainbow_h = 6 * 2 * self.scale
        
        # Horizontal position: map time progress to screen width
        cat_x = int(progress * (screen_w - cat_pixel_w - 20)) + 10
        # Vertical: near bottom of window, leaving room for bubble
        cat_y = window_h - cat_pixel_h - 8
        
        # ─── Draw Rainbow Trail ───
        rainbow_y = cat_y + 2 * self.scale  # Align with body
        stripe_h = 2  # Each stripe is 2 pixels tall (before scale)
        
        self.rainbow.draw(
            painter, 
            x_start=0, 
            x_end=cat_x + 4 * self.scale,  # Start from cat body
            y_top=rainbow_y,
            stripe_height=stripe_h,
            scale=self.scale
        )
        
        # ─── Draw Stars ───
        for star in self.stars:
            if star.alpha > 0.01:
                sx = cat_x + star.x
                sy = cat_y + star.y
                alpha = int(255 * star.alpha)
                color = QColor(*star.color[:3], alpha)
                size = star.size
                painter.fillRect(QRect(int(sx), int(sy), size, size), color)
        
        # ─── Draw Nyan Cat ───
        frame = CAT_FRAMES[self.anim_frame]
        for px, py, color_key in frame:
            color = COLORS.get(color_key)
            if color:
                painter.fillRect(
                    QRect(
                        cat_x + px * self.scale,
                        cat_y + py * self.scale,
                        self.scale,
                        self.scale
                    ),
                    QColor(*color)
                )
        
        # ─── Draw Time Bubble ───
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        progress_pct = progress * 100.0
        self.bubble.draw(painter, cat_x, cat_y, self.scale, time_str, progress_pct)
        
        painter.end()
    
    # ─── Mouse Events ─────────────────────────────────
    
    def mouseMoveEvent(self, event):
        """Track mouse for hover bubble."""
        self.mouse_over = True
        self.update()
        super().mouseMoveEvent(event)
    
    def leaveEvent(self, event):
        """Mouse left the widget."""
        self.mouse_over = False
        self.update()
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """Allow dragging the widget to reposition vertically."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start_pos = event.position().toPoint()
        elif event.button() == Qt.MouseButton.RightButton:
            self._show_context_menu(event.globalPosition().toPoint())
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Handle dragging."""
        if hasattr(self, '_drag_start_pos') and event.buttons() & Qt.MouseButton.LeftButton:
            # Allow vertical dragging
            delta = event.globalPosition().toPoint() - self._drag_start_pos
            new_y = self.y() + (event.globalPosition().toPoint().y() - self.mapToParent(self._drag_start_pos).y())
        self.mouse_over = True
        self.update()
        super().mouseMoveEvent(event)
    
    def _show_context_menu(self, global_pos):
        """Show right-click context menu."""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: rgba(40, 40, 40, 230);
                border: 1px solid rgba(255, 153, 204, 180);
                border-radius: 8px;
                padding: 4px;
                color: white;
                font-family: Menlo;
            }
            QMenu::item {
                padding: 6px 20px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: rgba(255, 153, 204, 80);
            }
        """)
        
        # Size submenu
        size_menu = menu.addMenu("🐱 Size")
        for size_name, preset in SIZE_PRESETS.items():
            action = QAction(f"{'✓ ' if size_name == self.current_size else '   '}{preset['label']} - {size_name.capitalize()}", menu)
            action.triggered.connect(lambda checked, s=size_name: self._change_size(s))
            size_menu.addAction(action)
        
        menu.addSeparator()
        
        # Bubble mode
        bubble_menu = menu.addMenu("💬 Time Bubble")
        for mode_name, mode_label in [("always", "Always Show"), ("hover", "Show on Hover"), ("hidden", "Hidden")]:
            action = QAction(f"{'✓ ' if self.bubble.show_mode == mode_name else '   '}{mode_label}", menu)
            action.triggered.connect(lambda checked, m=mode_name: self._set_bubble_mode(m))
            bubble_menu.addAction(action)
        
        menu.addSeparator()
        
        # Auto-start toggle
        auto_start = self._is_auto_start_enabled()
        action = QAction(f"{'✓ ' if auto_start else '   '}🚀 Auto-start on Boot", menu)
        action.triggered.connect(self._toggle_auto_start)
        menu.addAction(action)
        
        menu.addSeparator()
        
        # Quit
        action = QAction("✕ Quit Nyan Cat", menu)
        action.triggered.connect(self._quit_app)
        menu.addAction(action)
        
        menu.exec(global_pos)
    
    # ─── Size Management ──────────────────────────────
    
    def _change_size(self, size_name):
        """Change the cat size preset."""
        if size_name in SIZE_PRESETS:
            self.current_size = size_name
            self.scale = SIZE_PRESETS[size_name]["scale"]
            # Update stars
            for star in self.stars:
                star.scale = self.scale
            self._update_position_and_time()
    
    def _set_bubble_mode(self, mode):
        """Set bubble display mode."""
        self.bubble.show_mode = mode
        if mode == "always":
            self.bubble.visible = True
            self.bubble.hover_mode = False
        elif mode == "hover":
            self.bubble.hover_mode = True
            self.bubble.visible = True
        elif mode == "hidden":
            self.bubble.visible = False
            self.bubble.hover_mode = False
        self.update()
    
    # ─── Auto-start (macOS LaunchAgent) ───────────────
    
    def _get_launchagent_path(self):
        """Get the LaunchAgent plist path."""
        home = os.path.expanduser("~")
        return os.path.join(home, "Library", "LaunchAgents", "com.nyancat.progressbar.plist")
    
    def _is_auto_start_enabled(self):
        """Check if auto-start is configured."""
        return os.path.exists(self._get_launchagent_path())
    
    def _toggle_auto_start(self):
        """Toggle auto-start on boot."""
        plist_path = self._get_launchagent_path()
        
        if os.path.exists(plist_path):
            # Remove auto-start
            os.remove(plist_path)
            # Unload if loaded
            os.system(f"launchctl unload '{plist_path}' 2>/dev/null")
        else:
            # Create auto-start
            python_path = sys.executable
            main_script = os.path.abspath(__file__)
            
            plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.nyancat.progressbar</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_path}</string>
        <string>{main_script}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>StandardOutPath</key>
    <string>/tmp/nyancat-progressbar.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/nyancat-progressbar.err</string>
</dict>
</plist>
"""
            os.makedirs(os.path.dirname(plist_path), exist_ok=True)
            with open(plist_path, 'w') as f:
                f.write(plist_content)
    
    def _quit_app(self):
        """Quit the application."""
        QApplication.quit()


# ═══════════════════════════════════════════════════════════
#  System Tray Icon (optional)
# ═══════════════════════════════════════════════════════════
class SystemTray:
    """Optional system tray icon for the app."""
    
    def __init__(self, app, main_widget):
        self.app = app
        self.widget = main_widget
        self.tray = None
        
        if QSystemTrayIcon.isSystemTrayAvailable():
            self._setup_tray()
    
    def _create_tray_icon(self):
        """Create a simple pixel cat icon for the tray."""
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor(0, 0, 0, 0))
        
        painter = QPainter(pixmap)
        # Simple cat face icon
        # Body (pink frosting)
        painter.fillRect(QRect(4, 8, 16, 12), QColor(255, 153, 204))
        # Crust border
        painter.fillRect(QRect(4, 8, 16, 1), QColor(204, 153, 0))
        painter.fillRect(QRect(4, 19, 16, 1), QColor(204, 153, 0))
        painter.fillRect(QRect(4, 8, 1, 12), QColor(204, 153, 0))
        painter.fillRect(QRect(19, 8, 1, 12), QColor(204, 153, 0))
        # Cat head
        painter.fillRect(QRect(20, 6, 10, 10), QColor(128, 128, 128))
        # Ears
        painter.fillRect(QRect(21, 3, 3, 3), QColor(128, 128, 128))
        painter.fillRect(QRect(26, 3, 3, 3), QColor(128, 128, 128))
        # Eyes
        painter.fillRect(QRect(22, 9, 2, 2), QColor(0, 0, 0))
        painter.fillRect(QRect(26, 9, 2, 2), QColor(0, 0, 0))
        # Rainbow mini
        colors = COLORS["rainbow"]
        for i, c in enumerate(colors):
            painter.fillRect(QRect(0, 10 + i * 2, 4, 2), QColor(*c))
        
        painter.end()
        return pixmap
    
    def _setup_tray(self):
        """Setup system tray icon and menu."""
        self.tray = QSystemTrayIcon(self._create_tray_icon(), self.app)
        self.tray.setToolTip("Nyan Cat Progress Bar")
        
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: rgba(40, 40, 40, 230);
                border: 1px solid rgba(255, 153, 204, 180);
                border-radius: 8px;
                padding: 4px;
                color: white;
            }
            QMenu::item:selected {
                background-color: rgba(255, 153, 204, 80);
            }
        """)
        
        # Show time in menu
        now = datetime.now()
        time_action = QAction(f"🕐 {now.strftime('%H:%M:%S')}", menu)
        time_action.setEnabled(False)
        menu.addAction(time_action)
        
        menu.addSeparator()
        
        # Size options
        size_menu = menu.addMenu("🐱 Size")
        for size_name, preset in SIZE_PRESETS.items():
            action = QAction(f"{preset['label']} - {size_name.capitalize()}", menu)
            action.triggered.connect(lambda checked, s=size_name: self.widget._change_size(s))
            size_menu.addAction(action)
        
        menu.addSeparator()
        
        # Quit
        quit_action = QAction("✕ Quit", menu)
        quit_action.triggered.connect(self.app.quit)
        menu.addAction(quit_action)
        
        self.tray.setContextMenu(menu)
        self.tray.show()


# ═══════════════════════════════════════════════════════════
#  Application Entry Point
# ═══════════════════════════════════════════════════════════
def main():
    """Main entry point."""
    import argparse
    parser = argparse.ArgumentParser(description="Nyan Cat Progress Bar - Time Progress for macOS")
    parser.add_argument("--size", choices=["small", "medium", "large"], default=DEFAULT_SIZE,
                        help="Cat size preset (default: medium)")
    parser.add_argument("--hide-bubble", action="store_true",
                        help="Hide the time bubble by default")
    parser.add_argument("--debug", action="store_true",
                        help="Enable debug mode")
    args = parser.parse_args()
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Nyan Cat Progress Bar")
    app.setApplicationDisplayName("Nyan Cat Progress Bar")
    app.setQuitOnLastWindowClosed(False)  # Keep running with tray icon
    
    # Create main widget
    widget = NyanCatWidget()
    widget._change_size(args.size)
    
    if args.hide_bubble:
        widget._set_bubble_mode("hidden")
    
    widget.show()
    
    # Create system tray
    tray = SystemTray(app, widget)
    
    if args.debug:
        print(f"[NyanCat] Screen: {widget._get_screen_info()}")
        print(f"[NyanCat] Progress: {widget._get_time_progress():.4f}")
        print(f"[NyanCat] Scale: {widget.scale}")
        print(f"[NyanCat] Window: {widget.geometry()}")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
