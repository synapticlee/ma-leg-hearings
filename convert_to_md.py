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

        # Update date if <td class="eventDate"> is present
        date_td = row.find("td", class_="eventDate")
        if date_td:
            parts = list(date_td.stripped_strings)
            current_date = " ".join(parts)

        data_cells = cols[1:]  # skip the follow star column 

        # Defensive check: must have at least 5 data cells (time, status, type, event, location)
        if len(data_cells) < 5:
            continue

        time = data_cells[0].get_text(strip=True)
        status = data_cells[1].get_text(strip=True)
        typ = data_cells[2].get_text(strip=True)
        event = data_cells[3].get_text(strip=True)
        location = data_cells[4].get_text(strip=True)

        # Skip completed events
        if status.lower() == "completed":
            continue

        out.write(f"| {current_date} | {time} | {status} | {typ} | {event} | {location}_ |\n") 
