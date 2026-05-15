import sys
import json
import os
import subprocess
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

os.environ.setdefault('PYTHONUTF8', '1')
sys.stdout.reconfigure(encoding='utf-8')

CYAN    = '\033[0;36m'
GREEN   = '\033[0;32m'
YELLOW  = '\033[0;33m'
MAGENTA = '\033[0;35m'
RED     = '\033[0;31m'
DIM     = '\033[2m'
SKYBLUE    = '\033[38;5;39m'
PINK       = '\033[38;5;213m'
BRIGHT_CYAN = '\033[1;36m'
RESET       = '\033[0m'

WEATHER_LABEL = 'Lianqiu Lake (31.071,120.978)'
WEATHER_COORDS = '31.071,120.978'
WEATHER_CACHE_PATH = Path.home() / '.claude' / 'cache' / 'statusline-weather.json'
WEATHER_CACHE_TTL = timedelta(minutes=5)

def read_weather_cache(now):
    try:
        cache = json.loads(WEATHER_CACHE_PATH.read_text(encoding='utf-8'))
        fetched_at = datetime.fromisoformat(cache['fetched_at'])
        if now - fetched_at <= WEATHER_CACHE_TTL:
            return cache.get('value', '')
    except Exception:
        return ''
    return ''

def write_weather_cache(now, value):
    try:
        WEATHER_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        WEATHER_CACHE_PATH.write_text(
            json.dumps({'fetched_at': now.isoformat(), 'value': value}, ensure_ascii=False),
            encoding='utf-8'
        )
    except Exception:
        pass

def get_weather_emoji(code):
    emoji_map = {
        113: '☀️', 116: '⛅', 119: '☁️', 122: '☁️',
        143: '🌫️', 176: '🌦️', 179: '🌧️', 182: '❄️',
        185: '❄️', 200: '⛈️', 227: '🌨️', 230: '❄️',
        248: '🌫️', 260: '🌫️', 263: '🌦️', 266: '🌧️',
        281: '🌧️', 284: '🌧️', 293: '🌦️', 296: '🌧️',
        299: '🌧️', 302: '⛈️', 305: '⛈️', 308: '⛈️',
        311: '🌨️', 314: '🌨️', 317: '🌨️', 320: '🌨️',
        323: '🌨️', 326: '🌨️', 329: '🌨️', 332: '❄️',
        335: '🌨️', 338: '❄️', 350: '❄️', 353: '🌨️',
        356: '⛈️', 359: '⛈️', 362: '🌨️', 365: '🌨️',
        368: '🌨️', 371: '❄️', 374: '❄️', 377: '❄️',
        386: '⛈️', 389: '⛈️', 392: '🌨️', 395: '❄️',
    }
    return emoji_map.get(code, '')

def format_weather_json(weather_data):
    try:
        current = weather_data['current_condition'][0]
        today = weather_data['weather'][0]

        temp = current['temp_C']
        feels = current['FeelsLikeC']
        high = today['maxtempC']
        low = today['mintempC']
        wind_speed = current['windspeedKmph']
        wind_dir = current['winddir16Point']
        code = int(current['weatherCode'])

        emoji = get_weather_emoji(code)
        temp_str = f'+{temp}°C(+{feels}°C)'
        hl_str = f'{high}/{low}'
        wind_str = f'{wind_speed}km/h {wind_dir}'
        desc = current['weatherDesc'][0]['value'].lower()

        return f'{WEATHER_LABEL}: {desc} {emoji} {temp_str} {hl_str} {wind_str}'
    except Exception:
        return ''


def fetch_weather():
    now = datetime.now()
    cached = read_weather_cache(now)
    if cached:
        return cached

    url = f'https://wttr.in/{WEATHER_COORDS}?format=j1'
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'curl/8.0'})
        with urllib.request.urlopen(request, timeout=2) as response:
            weather_data = json.loads(response.read().decode('utf-8').strip())
            weather = format_weather_json(weather_data)
        if weather:
            write_weather_cache(now, weather)
            return weather
    except Exception:
        return cached
    return ''

# --- Caveman mode indicator ---
# Flag file written by caveman plugin hooks (mode-tracker / activate).
# Security: refuse symlinks, whitelist contents, strip control chars.
_config_dir = os.environ.get('CLAUDE_CONFIG_DIR')
if _config_dir:
    CAVEMAN_FLAG = Path(_config_dir) / '.caveman-active'
else:
    CAVEMAN_FLAG = Path.home() / '.claude' / '.caveman-active'

CAVEMAN_WHITELIST = {
    'off', 'lite', 'full', 'ultra',
    'wenyan-lite', 'wenyan', 'wenyan-full', 'wenyan-ultra',
}

CAVEMAN_LABELS = {
    'lite': 'L', 'full': 'F', 'ultra': 'U',
    'wenyan-lite': 'WL', 'wenyan': 'WF', 'wenyan-full': 'WF', 'wenyan-ultra': 'WU',
}

BONE = '\033[38;5;172m'

def get_caveman_mode():
    try:
        if CAVEMAN_FLAG.is_symlink():
            return ''
    except Exception:
        pass
    if not CAVEMAN_FLAG.is_file():
        return ''
    try:
        raw = CAVEMAN_FLAG.read_text(encoding='utf-8').strip()[:64]
    except Exception:
        return ''
    mode = ''.join(c for c in raw if c.isalnum() or c == '-').lower()
    if mode not in CAVEMAN_WHITELIST:
        return ''
    if mode == 'off':
        return ''
    label = CAVEMAN_LABELS.get(mode, mode[0].upper())
    return f"{BONE}bone{label}{RESET}"

raw = sys.stdin.read().strip()
if not raw:
    sys.exit(0)

try:
    data = json.loads(raw)
except Exception:
    sys.exit(0)

parts = []

# Model
model = (data.get('model') or {}).get('display_name', '')
if model:
    parts.append(f"{BRIGHT_CYAN}{model}{RESET}")

# Caveman mode
caveman = get_caveman_mode()
if caveman:
    parts.append(caveman)

# User
user = os.environ.get('USERNAME') or os.environ.get('USER', '')
if user:
    parts.append(f"{GREEN}{user}{RESET}")

# CWD — strip home prefix
cwd = (data.get('workspace') or {}).get('current_dir') or data.get('cwd', '')
if cwd:
    home = os.path.expanduser('~')  # C:\Users\nguyens6
    if cwd.startswith(home):
        cwd = '~' + cwd[len(home):].replace('\\', '/')
    else:
        cwd = cwd.replace('\\', '/')
    parts.append(f"{YELLOW}{cwd}{RESET}")

# Git branch
git_dir = (data.get('workspace') or {}).get('current_dir') or data.get('cwd', '')
if git_dir:
    try:
        branch = subprocess.check_output(
            ['git', '-C', git_dir, '--no-optional-locks', 'symbolic-ref', '--short', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        try:
            branch = subprocess.check_output(
                ['git', '-C', git_dir, '--no-optional-locks', 'rev-parse', '--short', 'HEAD'],
                stderr=subprocess.DEVNULL
            ).decode().strip()
        except Exception:
            branch = ''
    if branch:
        parts.append(f"{MAGENTA}{branch}{RESET}")

# Context bar
ctx = data.get('context_window') or {}
used_pct = ctx.get('used_percentage')
if used_pct is not None:
    bar_len = 10
    filled = round(bar_len * used_pct / 100)
    bar = '█' * filled + '░' * (bar_len - filled)
    color = RED if used_pct >= 80 else YELLOW if used_pct >= 50 else GREEN
    parts.append(f"{color}{bar} {used_pct}%{RESET}")

# Tokens
usage = ctx.get('current_usage') or {}
in_tok  = usage.get('input_tokens')
out_tok = usage.get('output_tokens')
cache   = usage.get('cache_read_input_tokens')
if in_tok is not None and out_tok is not None:
    tok_str = f"{in_tok}↑ {out_tok}↓"
    if cache:
        tok_str += f" {cache}c"
    parts.append(f"{DIM}{tok_str}{RESET}")

# Time
current_time = datetime.now().strftime("%m/%d %H:%M:%S")
parts.append(f"\033[0;36m{current_time}{RESET}")

weather = fetch_weather()
if weather:
    parts.append(f"{PINK}{weather}{RESET}")

sep = f"{DIM} | {RESET}"
print(sep.join(parts))
