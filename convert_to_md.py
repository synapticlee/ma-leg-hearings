#!/usr/bin/env python3
import sys
from bs4 import BeautifulSoup

if len(sys.argv) != 2:
    print("Usage: convert_events_to_md.py <input_html_file>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = "events.md"

with open(input_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

rows = soup.select("table.eventTable tbody tr")

with open(output_file, "w", encoding="utf-8") as out:
    out.write("| Date | Time | Status | Type | Event | Location |\n")
    out.write("|------|------|--------|------|--------|----------|\n")

    current_date = ""
    for row in rows:
        cols = row.find_all("td")
        if not cols:
            continue

        date_td = row.find("td", class_="eventDate")
        if date_td:
            parts = date_td.stripped_strings
            current_date = " ".join(list(parts)).replace("  ", " ")

        try:
            time = cols[2].get_text(strip=True)
            status = cols[3].get_text(strip=True)
            typ = cols[4].get_text(strip=True)
            event = cols[5].get_text(strip=True)
            location = cols[6].get_text(strip=True)
            out.write(f"| {current_date} | {time} | {status} | {typ} | {event} | {location} |\n")
        except IndexError:
            continue
