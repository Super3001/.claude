import sys
import json
import os
import subprocess
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

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

def format_weather_text(raw_weather):
    parts = [segment.strip() for segment in raw_weather.split(':', 1)]
    if len(parts) != 2:
        return raw_weather

    _, condition = parts
    segments = condition.split()
    if len(segments) < 2:
        return raw_weather

    temp = segments[-1]
    emoji = segments[-2]
    text = ' '.join(segments[:-2]).lower()
    if not text:
        return raw_weather

    return f'{WEATHER_LABEL}: {text} {emoji}  {temp}'


def fetch_weather():
    now = datetime.now()
    cached = read_weather_cache(now)
    if cached:
        return cached

    url = f'https://wttr.in/{WEATHER_COORDS}?format=%l:+%C+%c+%t'
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'curl/8.0'})
        with urllib.request.urlopen(request, timeout=2) as response:
            weather = format_weather_text(response.read().decode('utf-8').strip())
        if weather:
            write_weather_cache(now, weather)
            return weather
    except Exception:
        return cached
    return ''

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
