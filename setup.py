"""
Setup script for building Nyan Cat Progress Bar as macOS .app
=============================================================
Build command:
    python setup.py py2app

Or use the Makefile:
    make app
"""
from setuptools import setup

APP = ['main.py']
DATA_FILES = []

OPTIONS = {
    'argv_emulation': False,
    'plist': {
        'CFBundleName': 'Nyan Cat Progress Bar',
        'CFBundleDisplayName': 'Nyan Cat Progress Bar',
        'CFBundleIdentifier': 'com.nyancat.progressbar',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSUIElement': True,  # Background-only app (no Dock icon)
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.15',
    },
    'packages': ['PySide6'],
    'iconfile': 'icon.icns',  # Optional: add an .icns file
}

setup(
    name='Nyan Cat Progress Bar',
    version='1.0.0',
    description='A pixel-art Nyan Cat progress bar for macOS',
    author='NyanCat Dev',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=['PySide6>=6.5.0'],
)
