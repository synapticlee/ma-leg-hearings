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

        # Check if this row starts with a date cell
        if "eventDate" in cols[0].get("class", []):
            # This row has the date
            parts = list(cols[0].stripped_strings)
            current_date = " ".join(parts)
            data_cells = cols[1:]  # skip the date cell
        else:
            # This row has no date cell
            data_cells = cols

        if len(data_cells) < 5:
            continue  # skip malformed rows

        time = data_cells[1].get_text(strip=True) if len(data_cells) > 1 else ""
        status = data_cells[2].get_text(strip=True) if len(data_cells) > 2 else ""
        typ = data_cells[3].get_text(strip=True) if len(data_cells) > 3 else ""
        event = data_cells[4].get_text(strip=True) if len(data_cells) > 4 else ""
        location = data_cells[5].get_text(strip=True) if len(data_cells) > 5 else ""

        if status.lower() == "completed":
            continue # skip completed events

        # Use current_date if available, otherwise leave it blank
        date_display = current_date if current_date else ""

        out.write(f"| {date_display} | {time} | {status} | {typ} | {event} | {location} |\n")
