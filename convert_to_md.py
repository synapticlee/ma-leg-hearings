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
    start_parsing = False

    for i, row in enumerate(rows):
        cols = row.find_all("td")
        if not cols:
            continue

        # Check if this row's first <td> is a date cell with a <span class="today">
        first_td = cols[0]
        if "eventDate" in first_td.get("class", []):
            if first_td.select_one("span.today"):
                start_parsing = True
            
            # Set the current date regardless
            parts = list(first_td.stripped_strings)
            current_date = " ".join(parts).replace("Go to", "").replace("TODAY", "").strip()
            data_cells = cols[1:]
        else:
            data_cells = cols

        if not start_parsing:
            continue

        if len(data_cells) < 5:
            continue

        time = data_cells[1].get_text(strip=True) if len(data_cells) > 1 else ""
        status = data_cells[2].get_text(strip=True) if len(data_cells) > 2 else ""
        typ = data_cells[3].get_text(strip=True) if len(data_cells) > 3 else ""
        event = data_cells[4].get_text(strip=True) if len(data_cells) > 4 else ""
        location = data_cells[5].get_text(strip=True) if len(data_cells) > 5 else ""

        out.write(f"| {current_date} | {time} | {status} | {typ} | {event} | {location} |\n")
