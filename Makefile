# Nyan Cat Progress Bar - Makefile
# =================================

.PHONY: install run app clean

# Install dependencies
install:
	pip install -r requirements.txt

# Run the app directly
run:
	python main.py

# Run with specific size
run-small:
	python main.py --size small

run-large:
	python main.py --size large

# Build as macOS .app
app: install
	python setup.py py2app

# Build alias (development mode)
app-alias:
	python setup.py py2app --alias

# Clean build artifacts
clean:
	rm -rf build dist

# Install as LaunchAgent (auto-start on boot)
install-autostart:
	@python -c "\
import os, sys; \
home = os.path.expanduser('~'); \
plist_dir = os.path.join(home, 'Library', 'LaunchAgents'); \
plist_path = os.path.join(plist_dir, 'com.nyancat.progressbar.plist'); \
os.makedirs(plist_dir, exist_ok=True); \
python_path = sys.executable; \
main_script = os.path.abspath('main.py'); \
content = '''<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\
<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">\n\
<plist version=\"1.0\">\n\
<dict>\n\
    <key>Label</key>\n\
    <string>com.nyancat.progressbar</string>\n\
    <key>ProgramArguments</key>\n\
    <array>\n\
        <string>{python_path}</string>\n\
        <string>{main_script}</string>\n\
    </array>\n\
    <key>RunAtLoad</key>\n\
    <true/>\n\
    <key>KeepAlive</key>\n\
    <false/>\n\
</dict>\n\
</plist>\n\
'''.format(python_path=python_path, main_script=main_script); \
f = open(plist_path, 'w'); \
f.write(content); \
f.close(); \
print('Auto-start installed to: ' + plist_path); \
os.system('launchctl load ' + plist_path); \
print('LaunchAgent loaded successfully!')"

# Uninstall auto-start
uninstall-autostart:
	@python -c "\
import os; \
home = os.path.expanduser('~'); \
plist_path = os.path.join(home, 'Library', 'LaunchAgents', 'com.nyancat.progressbar.plist'); \
os.system('launchctl unload ' + plist_path + ' 2>/dev/null'); \
os.remove(plist_path) if os.path.exists(plist_path) else None; \
print('Auto-start removed.')"
