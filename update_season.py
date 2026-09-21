"""
Builds the season strip in README.md and the five season pages (winter.md ... autumn.md).

The strip is a calendar, January on the left and December on the right:
    [<]  winter(Jan)  spring  summer  MONSOON  autumn  winter(Dec)  [>]
The current season is shown big. The arrows go round in a circle:
... summer -> monsoon -> autumn -> winter -> spring -> summer ...

Run every night by .github/workflows/season.yml, or by hand: python update_season.py
"""
import os
import re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

REPO = "https://github.com/jeorgeiiii/jeorgeiiii/blob/main"
TIMEZONE = "Asia/Kolkata"
BIG, SMALL = 300, 88           # GIF widths in px (kept small so the strip fits on one line)

ORDER = ["winter", "spring", "summer", "monsoon", "autumn"]          # circular order
SLOTS = ["winter", "spring", "summer", "monsoon", "autumn", "winter"]  # Jan ... Dec
MONTHS = {"winter": "Dec - Jan", "spring": "Feb - Mar", "summer": "Apr - Jun",
          "monsoon": "Jul - Sep", "autumn": "Oct - Nov"}
COLOR = {s: "30363d" for s in ["winter", "spring", "summer", "monsoon", "autumn"]}  # grey arrows
SEASON_BY_MONTH = {12: "winter", 1: "winter", 2: "spring", 3: "spring", 4: "summer", 5: "summer",
                   6: "summer", 7: "monsoon", 8: "monsoon", 9: "monsoon", 10: "autumn", 11: "autumn"}
START, END = "<!-- SEASON:START -->", "<!-- SEASON:END -->"
HERE = os.path.dirname(os.path.abspath(__file__))


def arrow(symbol, season):
    # a small shields.io button in the colour of the season it opens
    return (f'<a href="{REPO}/{season}.md" title="{season.title()} ({MONTHS[season]})">'
            f'<img src="https://img.shields.io/badge/{symbol}-{COLOR[season]}?style=for-the-badge" '
            f'height="28" align="middle" alt="{season}" /></a>')


def strip(season, big_slot):
    i = ORDER.index(season)
    prev, nxt = ORDER[i - 1], ORDER[(i + 1) % len(ORDER)]
    cells = [arrow("%E2%97%80", prev)]
    for k, s in enumerate(SLOTS):
        w = BIG if k == big_slot else SMALL
        cells.append(f'<a href="{REPO}/{s}.md" title="{s.title()} ({MONTHS[s]})">'
                     f'<img src="{s}.gif" width="{w}" align="middle" alt="{s.title()}" /></a>')
    cells.append(arrow("%E2%96%B6", nxt))
    return '<p align="center">\n  ' + "\n  ".join(cells) + "\n</p>"


def readme_block(month):
    season = SEASON_BY_MONTH[month]
    big = 5 if month == 12 else SLOTS.index(season)   # December uses the right-hand winter
    return f"{START}\n{strip(season, big)}\n{END}"


def page(season):
    return (f'<h3 align="center">{season.title()} &middot; {MONTHS[season]}</h3>\n\n'
            f"{strip(season, SLOTS.index(season))}\n\n"
            f'<p align="center"><img src="{season}.gif" width="100%" alt="{season.title()}" /></p>\n\n'
            f'<p align="center"><a href="https://github.com/jeorgeiiii">Back to my profile</a></p>\n')


def main():
    month = int(sys.argv[1]) if len(sys.argv) > 1 else datetime.now(ZoneInfo(TIMEZONE)).month
    for s in ORDER:
        with open(os.path.join(HERE, f"{s}.md"), "w", encoding="utf-8") as f:
            f.write(page(s))
    path = os.path.join(HERE, "README.md")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: readme_block(month), text, flags=re.S)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    print("README shows", SEASON_BY_MONTH[month])


if __name__ == "__main__":
    main()
