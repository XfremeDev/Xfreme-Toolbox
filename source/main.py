"""
XFREME TOOLBOX v1.4.0 - Professional Windows Optimization Utility
Open Source | MIT License | GitHub: XfremeDev/Xfreme-Toolbox
"""

import os
import sys
import ctypes
import subprocess
import winreg
import shutil
import urllib.request
import json
import tempfile
import time
import hashlib
import glob
import traceback
import threading
import itertools
from datetime import datetime

# ===================================================================
# CONSTANTS
# ===================================================================

VERSION = "1.4.0"
APP_NAME = "Xfreme Toolbox"
AUTHOR = "XfremeDev"
LICENSE = "MIT"
GITHUB_URL = "https://github.com/XfremeDev/Xfreme-Toolbox"

TOOLBOX_DIR = r"C:\XfremeToolbox"
CONFIGS_DIR = os.path.join(TOOLBOX_DIR, "configs")
DOWNLOADS_DIR = os.path.join(TOOLBOX_DIR, "Downloads")
LOGS_DIR = os.path.join(TOOLBOX_DIR, "Logs")
VERSION_FILE = os.path.join(CONFIGS_DIR, "version.txt")
LANG_FILE = os.path.join(CONFIGS_DIR, "language.config")
COLOR_FILE = os.path.join(CONFIGS_DIR, "color.config")

# ===================================================================
# COLORS
# ===================================================================

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
RESET = '\033[0m'

def red_print(text): print(f"{RED}{text}{RESET}")
def green_print(text): print(f"{GREEN}{text}{RESET}")
def yellow_print(text): print(f"{YELLOW}{text}{RESET}")
def cyan_print(text): print(f"{CYAN}{text}{RESET}")

# ===================================================================
# LANGUAGE SYSTEM
# ===================================================================

LANGUAGES = {
    "en": {
        "title": "XFREME TOOLBOX",
        "main_menu": "MAIN MENU",
        "quick_setup": "Quick Windows Setup",
        "browsers": "Browsers",
        "media": "Media Players",
        "utilities": "Utilities",
        "development": "Development",
        "video": "Video Editing",
        "photo": "Photo Editing",
        "vpn": "VPN Clients",
        "games": "Games & Social",
        "system": "System Runtimes",
        "office": "Office Suites",
        "cloud": "Cloud Storage",
        "network": "Network Tools",
        "system_tools": "System Tools",
        "check_updates": "Check for Updates",
        "delete_installers": "Delete All Installers",
        "exit": "Exit Toolbox",
        "settings": "Settings",
        "language": "Language",
        "color": "Console Color",
        "back": "Back",
        "install_all": "Install All",
        "select_option": "Select option",
        "press_enter": "Press Enter to continue...",
        "unknown": "Unknown option",
        "goodbye": "Exiting Xfreme Toolbox... Goodbye!",
        "applied": "Applied",
        "tweaks": "tweaks",
        "ready": "Ready",
        "about": "About",
        "version": "Version",
        "author": "Author",
        "license": "License",
        "github": "GitHub",
        "update_check_failed": "Update check failed (network issue). Will try again later."
    },
    "ru": {
        "title": "XFREME TOOLBOX",
        "main_menu": "ГЛАВНОЕ МЕНЮ",
        "quick_setup": "Быстрая настройка Windows",
        "browsers": "Браузеры",
        "media": "Медиа плееры",
        "utilities": "Утилиты",
        "development": "Разработка",
        "video": "Видео монтаж",
        "photo": "Редакторы фото",
        "vpn": "VPN клиенты",
        "games": "Игры и соцсети",
        "system": "Системные компоненты",
        "office": "Офисные пакеты",
        "cloud": "Облачные хранилища",
        "network": "Сетевые утилиты",
        "system_tools": "Системные утилиты",
        "check_updates": "Проверить обновления",
        "delete_installers": "Удалить все установщики",
        "exit": "Выйти",
        "settings": "Настройки",
        "language": "Язык",
        "color": "Цвет консоли",
        "back": "Назад",
        "install_all": "Установить всё",
        "select_option": "Выберите опцию",
        "press_enter": "Нажмите Enter для продолжения...",
        "unknown": "Неизвестная опция",
        "goodbye": "Выход из Xfreme Toolbox... До свидания!",
        "applied": "Применено",
        "tweaks": "настроек",
        "ready": "Готов",
        "about": "О программе",
        "version": "Версия",
        "author": "Автор",
        "license": "Лицензия",
        "github": "GitHub",
        "update_check_failed": "Не удалось проверить обновления (проблема с сетью). Повторите позже."
    }
}

CURRENT_LANG = "ru"

def load_language():
    global CURRENT_LANG
    if os.path.exists(LANG_FILE):
        with open(LANG_FILE, 'r', encoding='utf-8') as f:
            CURRENT_LANG = f.read().strip()
    else:
        os.makedirs(CONFIGS_DIR, exist_ok=True)
        CURRENT_LANG = "ru"
        with open(LANG_FILE, 'w', encoding='utf-8') as f:
            f.write("ru")

def save_language(lang):
    global CURRENT_LANG
    CURRENT_LANG = lang
    with open(LANG_FILE, 'w', encoding='utf-8') as f:
        f.write(lang)

def t(key):
    return LANGUAGES[CURRENT_LANG].get(key, key)

# ===================================================================
# COLOR THEMES
# ===================================================================

COLOR_CODES = {
    "red": "91m",
    "green": "92m",
    "yellow": "93m",
    "blue": "94m",
    "purple": "95m",
    "cyan": "96m",
    "white": "97m"
}

CURRENT_COLOR = "91m"

def p(text):
    print(f"\033[{CURRENT_COLOR}{text}\033[0m")

def load_color():
    global CURRENT_COLOR
    if os.path.exists(COLOR_FILE):
        with open(COLOR_FILE, 'r', encoding='utf-8') as f:
            color_name = f.read().strip()
            if color_name in COLOR_CODES:
                CURRENT_COLOR = COLOR_CODES[color_name]

def save_color(color_name):
    with open(COLOR_FILE, 'w', encoding='utf-8') as f:
        f.write(color_name)
    load_color()

# ===================================================================
# LOGGING
# ===================================================================

def log_action(action, level="INFO", exc_info=None):
    log_file = os.path.join(LOGS_DIR, f"xfreme_{datetime.now().strftime('%Y%m%d')}.log")
    timestamp = datetime.now().strftime("%H:%M:%S")
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] [{level}] {action}\n")
            if exc_info:
                f.write(traceback.format_exc())
    except:
        pass

# ===================================================================
# ADMIN CHECK
# ===================================================================

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def create_directories():
    for d in [TOOLBOX_DIR, CONFIGS_DIR, DOWNLOADS_DIR, LOGS_DIR]:
        os.makedirs(d, exist_ok=True)

def clear_screen():
    os.system('cls')

# ===================================================================
# VERSION COMPARISON
# ===================================================================

def compare_versions(v1, v2):
    try:
        v1_parts = [int(x) for x in v1.split('.')]
        v2_parts = [int(x) for x in v2.split('.')]
    except:
        if v1 < v2: return -1
        elif v1 > v2: return 1
        else: return 0
    while len(v1_parts) < len(v2_parts):
        v1_parts.append(0)
    while len(v2_parts) < len(v1_parts):
        v2_parts.append(0)
    for i in range(len(v1_parts)):
        if v1_parts[i] < v2_parts[i]:
            return -1
        elif v1_parts[i] > v2_parts[i]:
            return 1
    return 0

# ===================================================================
# AUTO-UPDATE
# ===================================================================

def get_current_version():
    if os.path.exists(VERSION_FILE):
        try:
            with open(VERSION_FILE, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except:
            return VERSION
    return VERSION

def save_current_version(version):
    try:
        os.makedirs(CONFIGS_DIR, exist_ok=True)
        with open(VERSION_FILE, 'w', encoding='utf-8') as f:
            f.write(version)
    except:
        pass

def check_for_updates(silent=False):
    p("\n" + "=" * 60)
    p("            CHECKING FOR UPDATES")
    p("=" * 60)
    
    current_version = get_current_version()
    print(f"  Current version: {current_version}")
    
    update_server = "https://raw.githubusercontent.com/XfremeDev/Xfreme-Toolbox/main/updates/version.json"
    
    try:
        req = urllib.request.Request(update_server, headers={
            'User-Agent': f'XfremeToolbox/{VERSION}'
        })
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            remote_version = data.get('version', '0.0.0')
            release_date = data.get('releaseDate', 'Unknown')
            changelog = data.get('changelog', '')
            download_url = data.get('downloadUrl', '')
            
            print(f"  Remote version:  {remote_version}")
            print(f"  Release date:    {release_date}")
            
            comparison = compare_versions(current_version, remote_version)
            
            if comparison < 0:
                green_print(f"\n  ✓ New version {remote_version} available!")
                if changelog:
                    print(f"\n  Changes:")
                    for line in changelog.split('\n'):
                        print(f"    • {line.strip()}")
                print()
                choice = input(f"{YELLOW}Download and install update? (y/n): {RESET}")
                if choice.lower() == 'y':
                    if download_url:
                        return download_and_install_update(download_url, remote_version)
                    else:
                        red_print("  ✗ No download URL found!")
                        return False
                else:
                    yellow_print("  Update skipped.")
                    return False
            elif comparison == 0:
                green_print(f"\n  ✓ Xfreme Toolbox is up to date! (v{current_version})")
                return True
            else:
                yellow_print(f"\n  ⚠ You are running a newer version than available!")
                return True
    except urllib.error.URLError as e:
        if silent:
            yellow_print(f"\n  ⚠ {t('update_check_failed')}")
        else:
            red_print(f"\n  ✗ Network error: Could not reach update server")
            red_print(f"    {e}")
        return False
    except Exception as e:
        red_print(f"\n  ✗ Failed to check updates: {e}")
        return False

def download_and_install_update(download_url, new_version):
    p("\n" + "=" * 60)
    p("            DOWNLOADING UPDATE")
    p("=" * 60)
    
    temp_dir = tempfile.gettempdir()
    new_exe_path = os.path.join(temp_dir, "XfremeToolbox_new.exe")
    current_exe = sys.executable if getattr(sys, 'frozen', False) else None
    
    if not current_exe:
        red_print("  ✗ Cannot update: Not running as EXE")
        red_print("  Please download the latest version manually from:")
        red_print(f"  {GITHUB_URL}")
        return False
    
    print(f"\n  Downloading version {new_version}...")
    print(f"  From: {download_url}")
    
    try:
        def report_progress(block_num, block_size, total_size):
            if total_size > 0:
                percent = int(block_num * block_size * 100 / total_size)
                if percent > 100:
                    percent = 100
                bar_length = 40
                filled = int(bar_length * percent / 100)
                bar = '█' * filled + '░' * (bar_length - filled)
                print(f"\r  [{bar}] {percent}%", end='')
        
        urllib.request.urlretrieve(download_url, new_exe_path, report_progress)
        print()
        green_print("  ✓ Download complete!")
        
        if not os.path.exists(new_exe_path) or os.path.getsize(new_exe_path) < 100000:
            red_print("  ✗ Downloaded file is invalid or too small")
            return False
        
        bat_path = os.path.join(temp_dir, "update_xfreme.bat")
        bat_content = f'''@echo off
echo Updating Xfreme Toolbox...
timeout /t 2 /nobreak >nul
copy /y "{new_exe_path}" "{current_exe}"
if errorlevel 1 (
    echo Failed to copy update!
    pause
    exit /b 1
)
echo {new_version} > "{VERSION_FILE}"
start "" "{current_exe}"
del "{new_exe_path}" 2>nul
del "%~f0" 2>nul
echo Update complete!
exit
'''
        with open(bat_path, 'w', encoding='utf-8') as f:
            f.write(bat_content)
        
        green_print("  ✓ Update ready!")
        print("\n  Restarting to apply update...")
        subprocess.Popen([bat_path], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        save_current_version(new_version)
        time.sleep(1)
        sys.exit(0)
    except Exception as e:
        red_print(f"  ✗ Update failed: {e}")
        return False

# ===================================================================
# SPINNER (прогресс-бар)
# ===================================================================

def show_spinner(stop_event, message="Installing..."):
    """Display a spinning animation while a process is running."""
    spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    while not stop_event.is_set():
        sys.stdout.write(f'\r{next(spinner)} {message}')
        sys.stdout.flush()
        time.sleep(0.3)
    sys.stdout.write('\r✅ Done!                    \n')
    sys.stdout.flush()

# ===================================================================
# WINGET (без shell=True, с прогрессом)
# ===================================================================

def check_winget():
    try:
        result = subprocess.run(
            ['winget', '--version'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=5
        )
        return result.returncode == 0
    except:
        return False

def get_winget_id(program_key):
    winget_ids = {
        "chrome": "Google.Chrome",
        "firefox": "Mozilla.Firefox",
        "brave": "Brave.Brave",
        "librewolf": "LibreWolf.LibreWolf",
        "vivaldi": "VivaldiTechnologies.Vivaldi",
        "tor": "TorProject.TorBrowser",
        "opera": "Opera.OperaGX",
        "vlc": "VideoLAN.VLC",
        "mpchc": "MPC-HC.MPC-HC",
        "audacity": "Audacity.Audacity",
        "aimp": "AIMP.AIMP",
        "foobar2000": "PeterPawlowski.foobar2000",
        "klite": "CodecGuide.K-LiteCodecPack",
        "7zip": "7zip.7zip",
        "cpuz": "CPUID.CPU-Z",
        "gpuz": "TechPowerUp.GPU-Z",
        "crystaldisk": "CrystalDewWorld.CrystalDiskInfo",
        "hwmonitor": "CPUID.HWMonitor",
        "msiafterburner": "MSI.Afterburner",
        "rufus": "Rufus.Rufus",
        "ventoy": "Ventoy.Ventoy",
        "vscode": "Microsoft.VisualStudioCode",
        "git": "Git.Git",
        "nodejs": "OpenJS.NodeJS",
        "docker": "Docker.DockerDesktop",
        "python": "Python.Python.3.12",
        "notepadpp": "Notepad++.Notepad++",
        "sdi": "SDI.SDI",
        "handbrake": "HandBrake.HandBrake",
        "obs": "OBSProject.OBSStudio",
        "shotcut": "Meltytech.Shotcut",
        "davinci": "BlackmagicDesign.DaVinciResolve",
        "gimp": "GIMP.GIMP",
        "imageglass": "ImageGlass.ImageGlass",
        "protonvpn": "ProtonTechnologies.ProtonVPN",
        "nordvpn": "NordSecurity.NordVPN",
        "expressvpn": "ExpressVPN.ExpressVPN",
        "wireguard": "WireGuard.WireGuard",
        "openvpn": "OpenVPNTechnologies.OpenVPN",
        "minecraft": "Mojang.MinecraftLauncher",
        "roblox": "Roblox.Roblox",
        "discord": "Discord.Discord",
        "teamspeak": "TeamSpeak.TeamSpeak",
        "playnite": "Playnite.Playnite",
        "steam": "Valve.Steam",
        "epic": "EpicGames.EpicGamesLauncher",
        "gog": "GOG.Galaxy",
        "vcredist": "Microsoft.VCRedist.2015+.x64",
        "directx": "Microsoft.DirectX",
        "libreoffice": "TheDocumentFoundation.LibreOffice",
        "onlyoffice": "ONLYOFFICE.DesktopEditors",
        "wps": "Kingsoft.WPSOffice",
        "dropbox": "Dropbox.Dropbox",
        "googledrive": "Google.Drive",
        "mega": "Mega.Mega",
        "putty": "PuTTY.PuTTY",
        "winscp": "WinSCP.WinSCP",
        "filezilla": "FileZilla.Client",
        "procexp": "Microsoft.Sysinternals.ProcessExplorer",
        "autoruns": "Microsoft.Sysinternals.Autoruns",
    }
    return winget_ids.get(program_key, None)

def install_with_winget(program_key):
    """Install program using winget with a spinner."""
    winget_id = get_winget_id(program_key)
    if not winget_id:
        red_print(f"  ✗ No winget ID found for: {program_key}")
        return False

    print(f"\n  Installing via winget: {winget_id}")

    try:
        # Проверка, установлено ли уже
        check_result = subprocess.run(
            ['winget', 'list', '--id', winget_id],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=30
        )
        if winget_id in check_result.stdout:
            yellow_print(f"  ⚠ Already installed: {winget_id}")
            return True

        # Запускаем установку с показом спиннера
        install_cmd = [
            'winget', 'install', '--id', winget_id,
            '--silent', '--accept-package-agreements', '--accept-source-agreements'
        ]

        print(f"  ⏳ Installation in progress (may take several minutes)...")
        stop_spinner = threading.Event()
        spinner_thread = threading.Thread(
            target=show_spinner,
            args=(stop_spinner, f"Installing {winget_id}...")
        )
        spinner_thread.start()

        # Запускаем процесс
        process = subprocess.Popen(
            install_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )

        # Ожидаем завершения с таймаутом 10 минут
        try:
            stdout, stderr = process.communicate(timeout=600)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            stop_spinner.set()
            spinner_thread.join()
            red_print("  ✗ Installation timeout (10 minutes)")
            return False

        # Останавливаем спиннер
        stop_spinner.set()
        spinner_thread.join()

        if process.returncode == 0:
            green_print("  ✓ Installed successfully")
            log_action(f"Installed {program_key} via winget")
            return True
        else:
            # Проверяем ещё раз, возможно уже установлено
            check_result = subprocess.run(
                ['winget', 'list', '--id', winget_id],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                timeout=30
            )
            if winget_id in check_result.stdout:
                green_print(f"  ✓ Already installed: {winget_id}")
                return True

            red_print(f"  ✗ Installation failed (return code {process.returncode})")
            if stderr:
                print(f"  Error: {stderr[:200]}")
            log_action(f"Winget install failed for {program_key}", "ERROR")
            return False

    except Exception as e:
        red_print(f"  ✗ Installation error: {str(e)[:100]}")
        log_action(f"Winget exception for {program_key}", "ERROR", exc_info=True)
        return False

# ===================================================================
# CHOCOLATEY (с прогрессом)
# ===================================================================

def check_choco():
    try:
        result = subprocess.run(
            ['choco', '--version'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=5
        )
        return result.returncode == 0
    except:
        return False

def get_choco_id(program_key):
    choco_ids = {
        "chrome": "googlechrome",
        "firefox": "firefox",
        "brave": "brave",
        "librewolf": "librewolf",
        "vivaldi": "vivaldi",
        "tor": "tor-browser",
        "opera": "opera",
        "vlc": "vlc",
        "mpchc": "mpc-hc",
        "audacity": "audacity",
        "aimp": "aimp",
        "foobar2000": "foobar2000",
        "klite": "klitecodecpack",
        "7zip": "7zip",
        "cpuz": "cpuz",
        "gpuz": "gpuz",
        "crystaldisk": "crystaldiskinfo",
        "hwmonitor": "hwmonitor",
        "msiafterburner": "msiafterburner",
        "rufus": "rufus",
        "ventoy": "ventoy",
        "vscode": "vscode",
        "git": "git",
        "nodejs": "nodejs",
        "docker": "docker-desktop",
        "python": "python",
        "notepadpp": "notepadplusplus",
        "sdi": "sdi",
        "handbrake": "handbrake",
        "obs": "obs-studio",
        "shotcut": "shotcut",
        "davinci": "davinci-resolve",
        "gimp": "gimp",
        "imageglass": "imageglass",
        "protonvpn": "protonvpn",
        "nordvpn": "nordvpn",
        "expressvpn": "expressvpn",
        "wireguard": "wireguard",
        "openvpn": "openvpn",
        "minecraft": "minecraft",
        "roblox": "roblox",
        "discord": "discord",
        "teamspeak": "teamspeak",
        "playnite": "playnite",
        "steam": "steam",
        "epic": "epicgameslauncher",
        "gog": "goggalaxy",
        "vcredist": "vcredist-all",
        "directx": "directx",
        "libreoffice": "libreoffice",
        "onlyoffice": "onlyoffice",
        "wps": "wps-office",
        "dropbox": "dropbox",
        "googledrive": "googledrive",
        "mega": "mega",
        "putty": "putty",
        "winscp": "winscp",
        "filezilla": "filezilla",
        "procexp": "procexp",
        "autoruns": "autoruns",
        "ddu": "ddu"
    }
    return choco_ids.get(program_key, None)

def install_with_choco(program_key):
    """Install program using Chocolatey with a spinner."""
    choco_id = get_choco_id(program_key)
    if not choco_id:
        red_print(f"  ✗ No Chocolatey package found for: {program_key}")
        return False

    print(f"\n  Installing via Chocolatey: {choco_id}")

    try:
        # Проверка, установлено ли уже
        check_result = subprocess.run(
            ['choco', 'list', '--idonly', '--exact', choco_id],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=30
        )
        if choco_id in check_result.stdout:
            yellow_print(f"  ⚠ Already installed: {choco_id}")
            return True

        install_cmd = ['choco', 'install', choco_id, '-y', '--no-progress']

        print(f"  ⏳ Installation in progress (may take several minutes)...")
        stop_spinner = threading.Event()
        spinner_thread = threading.Thread(
            target=show_spinner,
            args=(stop_spinner, f"Installing {choco_id}...")
        )
        spinner_thread.start()

        process = subprocess.Popen(
            install_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )

        try:
            stdout, stderr = process.communicate(timeout=900)  # 15 минут
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            stop_spinner.set()
            spinner_thread.join()
            red_print("  ✗ Installation timeout (15 minutes)")
            return False

        stop_spinner.set()
        spinner_thread.join()

        if process.returncode == 0:
            green_print("  ✓ Installed successfully")
            log_action(f"Installed {program_key} via Chocolatey")
            return True
        else:
            # Повторная проверка
            check_result = subprocess.run(
                ['choco', 'list', '--idonly', '--exact', choco_id],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                timeout=30
            )
            if choco_id in check_result.stdout:
                green_print(f"  ✓ Already installed: {choco_id}")
                return True

            red_print(f"  ✗ Installation failed (return code {process.returncode})")
            if stderr:
                print(f"  Error: {stderr[:200]}")
            log_action(f"Choco install failed for {program_key}", "ERROR")
            return False

    except Exception as e:
        red_print(f"  ✗ Installation error: {str(e)[:100]}")
        log_action(f"Choco exception for {program_key}", "ERROR", exc_info=True)
        return False

# ===================================================================
# INSTALLATION STATISTICS
# ===================================================================

class InstallStats:
    def __init__(self):
        self.total = 0
        self.success = 0
        self.failed = 0
        self.skipped = 0
        self.current = 0
        self.start_time = None

    def start(self):
        self.start_time = datetime.now()
        log_action("Installation started")

    def finish(self):
        log_action(f"Installation finished. Success: {self.success}, Failed: {self.failed}")

    def get_time_elapsed(self):
        if self.start_time:
            delta = datetime.now() - self.start_time
            return str(delta).split('.')[0]
        return "0:00:00"

stats = InstallStats()

def show_stats():
    p("\n" + "=" * 60)
    p("            INSTALLATION STATISTICS")
    p("=" * 60)
    print(f"  Total programs:   {stats.total}")
    print(f"  Successfully:     {GREEN}{stats.success}{RESET}")
    print(f"  Failed:           {RED}{stats.failed}{RESET}")
    print(f"  Time elapsed:     {stats.get_time_elapsed()}")
    p("=" * 60)

# ===================================================================
# REGISTRY HELPERS
# ===================================================================

def reg_set(path, name, value, reg_type=winreg.REG_DWORD, hive=winreg.HKEY_LOCAL_MACHINE):
    try:
        key = winreg.OpenKey(hive, path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, name, 0, reg_type, value)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        log_action(f"Registry set failed: {path}\\{name} = {value} - {str(e)}", "ERROR", exc_info=True)
        return False

# ===================================================================
# QUICK WINDOWS SETUP
# ===================================================================

def quick_setup():
    p("\n" + "=" * 60)
    p(f"            {t('quick_setup')}")
    p("=" * 60)
    print("  Applying 10+ tweaks for better performance and privacy...")
    log_action("Quick Windows Setup started")

    applied = 0
    if reg_set(r"SOFTWARE\Policies\Microsoft\Windows\DataCollection", "AllowTelemetry", 0):
        applied += 1
    if reg_set(r"SOFTWARE\Policies\Microsoft\Windows\Windows Search", "AllowCortana", 0):
        applied += 1
    if reg_set(r"SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR", "AppCaptureEnabled", 0):
        applied += 1
    if reg_set(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "Hidden", 1, winreg.REG_DWORD, winreg.HKEY_CURRENT_USER):
        applied += 1
    if reg_set(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "HideFileExt", 0, winreg.REG_DWORD, winreg.HKEY_CURRENT_USER):
        applied += 1
    if reg_set(r"SOFTWARE\Microsoft\Windows\CurrentVersion\PushNotifications", "ToastEnabled", 0):
        applied += 1

    try:
        shutil.rmtree(os.environ.get('TEMP', ''), ignore_errors=True)
        applied += 1
    except Exception as e:
        log_action(f"Failed to clean TEMP: {e}", "ERROR")

    green_print(f"\n  ✓ {t('applied')} {applied} {t('tweaks')}")
    log_action(f"Quick setup completed, {applied} tweaks applied")
    print("\n  Restart Explorer to apply changes.")
    input(f"\n{RED}{t('press_enter')}{RESET}")

# ===================================================================
# CATEGORY MENU
# ===================================================================

def install_program(key):
    if key not in PROGRAMS:
        red_print(f"  Unknown program: {key}")
        return False

    name = PROGRAMS[key]["name"]
    print(f"\n[{stats.current}/{stats.total}] 📦 {name}")
    log_action(f"Installing {name}")

    if check_winget():
        success = install_with_winget(key)
        if success:
            stats.success += 1
            return True
        else:
            stats.failed += 1
            return False
    else:
        yellow_print("  Winget not available, trying Chocolatey...")
        if check_choco():
            success = install_with_choco(key)
            if success:
                stats.success += 1
                return True
            else:
                stats.failed += 1
                return False
        else:
            red_print("  ✗ No package manager found! Please install winget or Chocolatey.")
            red_print("  Winget: https://aka.ms/getwinget")
            red_print("  Chocolatey: https://chocolatey.org/install")
            stats.failed += 1
            return False

def show_category_menu(category_name, program_keys):
    while True:
        clear_screen()
        p("=" * 60)
        p(f"            {category_name}")
        p("=" * 60)

        for i, key in enumerate(program_keys, 1):
            name = PROGRAMS[key]["name"]
            print(f"  {i}. {name}")

        print("-" * 60)
        print(f"  a. {t('install_all')}")
        print(f"  0. {t('back')}")
        p("=" * 60)

        choice = input(f"{RED}{t('select_option')}: {RESET}")

        if choice == '0':
            break
        elif choice.lower() == 'a':
            stats.total = len(program_keys)
            stats.start()
            for i, key in enumerate(program_keys, 1):
                stats.current = i
                install_program(key)
            stats.finish()
            show_stats()
            input(f"{RED}{t('press_enter')}{RESET}")
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(program_keys):
                key = program_keys[idx]
                stats.total = 1
                stats.current = 1
                stats.start()
                install_program(key)
                stats.finish()
                show_stats()
                input(f"{RED}{t('press_enter')}{RESET}")
            else:
                yellow_print(t('unknown'))
        else:
            yellow_print(t('unknown'))

# ===================================================================
# DELETE INSTALLERS
# ===================================================================

def delete_all_installers():
    p("\n[00] DELETE ALL INSTALLERS")

    if check_winget():
        try:
            subprocess.run(['winget', 'cache', 'clean'], capture_output=True, timeout=30)
            green_print("  ✓ Winget cache cleaned.")
        except Exception as e:
            red_print(f"  ✗ Failed to clean winget cache: {e}")
    else:
        yellow_print("  ⚠ Winget not found, skipping cache clean.")

    temp_dir = tempfile.gettempdir()
    pattern = os.path.join(temp_dir, "*xfreme*")
    removed = 0
    for path in glob.glob(pattern, recursive=False):
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
            removed += 1
        except Exception as e:
            log_action(f"Failed to delete temp item {path}: {e}", "ERROR")

    if removed:
        green_print(f"  ✓ Removed {removed} temporary items containing 'xfreme'.")
    else:
        yellow_print("  ℹ No temporary Xfreme files found.")

    input(f"{RED}{t('press_enter')}{RESET}")

# ===================================================================
# SETTINGS MENU
# ===================================================================

def settings_menu():
    while True:
        clear_screen()
        p("=" * 60)
        p(f" {t('settings')}")
        p("=" * 60)
        p(f"\n 1. 🌐 {t('language')}")
        p(f" 2. 🎨 {t('color')}")
        p(f" 0. {t('back')}")
        p("=" * 60)

        choice = input(f"{RED}{t('select_option')}: {RESET}")

        if choice == '1':
            language_menu()
        elif choice == '2':
            color_menu()
        elif choice == '0':
            break
        else:
            yellow_print(t('unknown'))
            input(f"{RED}{t('press_enter')}{RESET}")

def language_menu():
    clear_screen()
    p("=" * 60)
    p(f" {t('language')}")
    p("=" * 60)
    p(" 1. English")
    p(" 2. Русский")
    p(" 0. Back")
    p("=" * 60)

    choice = input(f"{RED}{t('select_option')}: {RESET}")

    if choice == '1':
        save_language("en")
        green_print("✓ Language changed to English")
        input(f"{RED}{t('press_enter')}{RESET}")
    elif choice == '2':
        save_language("ru")
        green_print("✓ Язык изменён на Русский")
        input(f"{RED}{t('press_enter')}{RESET}")
    elif choice == '0':
        pass
    else:
        yellow_print(t('unknown'))

def color_menu():
    clear_screen()
    p("=" * 60)
    p(f" {t('color')}")
    p("=" * 60)
    p(" 1. 🔴 Red")
    p(" 2. 🟢 Green")
    p(" 3. 🟡 Yellow")
    p(" 4. 🔵 Blue")
    p(" 5. 🟣 Purple")
    p(" 6. 🔷 Cyan")
    p(" 7. ⚪ White")
    p(" 0. Back")
    p("=" * 60)

    choice = input(f"{RED}{t('select_option')}: {RESET}")

    colors = {
        "1": "red",
        "2": "green",
        "3": "yellow",
        "4": "blue",
        "5": "purple",
        "6": "cyan",
        "7": "white"
    }

    if choice in colors:
        save_color(colors[choice])
        green_print(f"✓ Color changed")
        input(f"{RED}{t('press_enter')}{RESET}")
    elif choice == '0':
        pass
    else:
        yellow_print(t('unknown'))

# ===================================================================
# ABOUT MENU
# ===================================================================

def about_menu():
    clear_screen()
    p("=" * 60)
    p(f"            {t('about')}")
    p("=" * 60)
    print(f"  {t('title')}: {APP_NAME}")
    print(f"  {t('version')}: {VERSION}")
    print(f"  {t('author')}: {AUTHOR}")
    print(f"  {t('license')}: {LICENSE}")
    print(f"  {t('github')}: {GITHUB_URL}")
    p("=" * 60)
    input(f"{RED}{t('press_enter')}{RESET}")

# ===================================================================
# MAIN MENU
# ===================================================================

def show_main_menu():
    clear_screen()
    p("=" * 60)
    p(f" {t('title')} v{VERSION}")
    p(f" User: {os.getlogin()} | PC: {os.environ.get('COMPUTERNAME', 'Unknown')}")
    p(f" Time: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    p("=" * 60)

    winget_status = "✅" if check_winget() else "❌"
    choco_status = "✅" if check_choco() else "❌"
    print(f"  Winget: {winget_status}  Chocolatey: {choco_status}")

    print()
    p(f"  {t('main_menu')}")
    print("-" * 60)
    p(f"  1.  {t('quick_setup')}")
    p(f"  2.  {t('browsers')}")
    p(f"  3.  {t('media')}")
    p(f"  4.  {t('utilities')}")
    p(f"  5.  {t('development')}")
    p(f"  6.  {t('video')}")
    p(f"  7.  {t('photo')}")
    p(f"  8.  {t('vpn')}")
    p(f"  9.  {t('games')}")
    p(f"  10. {t('system')}")
    print("-" * 60)
    p(f"  11. {t('check_updates')}")
    p(f"  12. {t('settings')}")
    p(f"  13. {t('about')}")
    print("-" * 60)
    p(f"  14. {t('office')}")
    p(f"  15. {t('cloud')}")
    p(f"  16. {t('network')}")
    p(f"  17. {t('system_tools')}")
    print("-" * 60)
    p(f"  00. {t('delete_installers')}")
    p(f"  99. {t('exit')}")
    p("=" * 60)

# ===================================================================
# PROGRAMS LIST
# ===================================================================

PROGRAMS = {
    "chrome": {"name": "Google Chrome"},
    "firefox": {"name": "Mozilla Firefox"},
    "brave": {"name": "Brave Browser"},
    "librewolf": {"name": "LibreWolf"},
    "vivaldi": {"name": "Vivaldi"},
    "tor": {"name": "Tor Browser"},
    "opera": {"name": "Opera GX"},
    "vlc": {"name": "VLC Media Player"},
    "mpchc": {"name": "MPC-HC"},
    "audacity": {"name": "Audacity"},
    "aimp": {"name": "AIMP"},
    "foobar2000": {"name": "Foobar2000"},
    "klite": {"name": "K-Lite Codec Pack"},
    "7zip": {"name": "7-Zip"},
    "cpuz": {"name": "CPU-Z"},
    "gpuz": {"name": "GPU-Z"},
    "crystaldisk": {"name": "CrystalDiskInfo"},
    "hwmonitor": {"name": "HWMonitor"},
    "msiafterburner": {"name": "MSI Afterburner"},
    "rufus": {"name": "Rufus"},
    "ventoy": {"name": "Ventoy"},
    "vscode": {"name": "Visual Studio Code"},
    "git": {"name": "Git for Windows"},
    "nodejs": {"name": "Node.js LTS"},
    "docker": {"name": "Docker Desktop"},
    "python": {"name": "Python 3.12"},
    "notepadpp": {"name": "Notepad++"},
    "sdi": {"name": "SDI Driver Updater"},
    "handbrake": {"name": "HandBrake"},
    "obs": {"name": "OBS Studio"},
    "shotcut": {"name": "Shotcut"},
    "davinci": {"name": "DaVinci Resolve"},
    "gimp": {"name": "GIMP"},
    "imageglass": {"name": "ImageGlass"},
    "protonvpn": {"name": "ProtonVPN"},
    "nordvpn": {"name": "NordVPN"},
    "expressvpn": {"name": "ExpressVPN"},
    "wireguard": {"name": "WireGuard"},
    "openvpn": {"name": "OpenVPN"},
    "minecraft": {"name": "Minecraft Launcher"},
    "roblox": {"name": "Roblox"},
    "discord": {"name": "Discord"},
    "teamspeak": {"name": "TeamSpeak"},
    "playnite": {"name": "Playnite"},
    "steam": {"name": "Steam"},
    "epic": {"name": "Epic Games Launcher"},
    "gog": {"name": "GOG Galaxy"},
    "vcredist": {"name": "Visual C++ Redistributables AIO"},
    "directx": {"name": "DirectX Runtime"},
    "libreoffice": {"name": "LibreOffice"},
    "onlyoffice": {"name": "OnlyOffice"},
    "wps": {"name": "WPS Office"},
    "dropbox": {"name": "Dropbox"},
    "googledrive": {"name": "Google Drive"},
    "mega": {"name": "Mega"},
    "putty": {"name": "PuTTY"},
    "winscp": {"name": "WinSCP"},
    "filezilla": {"name": "FileZilla"},
    "procexp": {"name": "Process Explorer"},
    "autoruns": {"name": "Autoruns"},
    "ddu": {"name": "Display Driver Uninstaller (DDU)"}
}

# ===================================================================
# MAIN
# ===================================================================

def main():
    run_as_admin()
    create_directories()
    load_language()
    load_color()

    if not check_winget() and not check_choco():
        yellow_print("\n  ⚠ Neither winget nor Chocolatey found!")
        yellow_print("  Please install at least one package manager.")
        yellow_print("  Winget: https://aka.ms/getwinget")
        yellow_print("  Chocolatey: https://chocolatey.org/install")
        print()
    else:
        if not check_winget():
            yellow_print("\n  ⚠ Winget not found, but Chocolatey is available. Will use Chocolatey.")
        elif not check_choco():
            yellow_print("\n  ⚠ Chocolatey not found, but winget is available. Will use winget.")

    check_for_updates(silent=True)

    while True:
        show_main_menu()
        choice = input(f"{RED}{t('select_option')}: {RESET}")

        if choice == '1':
            quick_setup()
        elif choice == '2':
            show_category_menu(t('browsers'), ["chrome", "firefox", "brave", "librewolf", "vivaldi", "tor", "opera"])
        elif choice == '3':
            show_category_menu(t('media'), ["vlc", "mpchc", "audacity", "aimp", "foobar2000", "klite"])
        elif choice == '4':
            show_category_menu(t('utilities'), ["7zip", "cpuz", "gpuz", "crystaldisk", "hwmonitor", "msiafterburner", "rufus", "ventoy"])
        elif choice == '5':
            show_category_menu(t('development'), ["vscode", "git", "nodejs", "docker", "python", "notepadpp", "sdi"])
        elif choice == '6':
            show_category_menu(t('video'), ["handbrake", "obs", "shotcut", "davinci"])
        elif choice == '7':
            show_category_menu(t('photo'), ["gimp", "imageglass"])
        elif choice == '8':
            show_category_menu(t('vpn'), ["protonvpn", "nordvpn", "expressvpn", "wireguard", "openvpn"])
        elif choice == '9':
            show_category_menu(t('games'), ["minecraft", "roblox", "discord", "teamspeak", "playnite", "steam", "epic", "gog"])
        elif choice == '10':
            show_category_menu(t('system'), ["vcredist", "directx"])
        elif choice == '11':
            check_for_updates(silent=False)
        elif choice == '12':
            settings_menu()
        elif choice == '13':
            about_menu()
        elif choice == '14':
            show_category_menu(t('office'), ["libreoffice", "onlyoffice", "wps"])
        elif choice == '15':
            show_category_menu(t('cloud'), ["dropbox", "googledrive", "mega"])
        elif choice == '16':
            show_category_menu(t('network'), ["putty", "winscp", "filezilla"])
        elif choice == '17':
            show_category_menu(t('system_tools'), ["procexp", "autoruns", "ddu"])
        elif choice == '00':
            delete_all_installers()
        elif choice == '99':
            p(f"\n{t('goodbye')}")
            time.sleep(2)
            break
        else:
            yellow_print(t('unknown'))

        input(f"{RED}{t('press_enter')}{RESET}")

if __name__ == "__main__":
    main()
