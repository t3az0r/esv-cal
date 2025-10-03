import icalendar
from datetime import datetime
from pathlib import Path

ics_path = Path("calendar.ics")
html_path = Path("docs/index.html")

# ICS parsen
with open(ics_path, 'rb') as f:
    cal = icalendar.Calendar.from_ical(f.read())

events = []
for component in cal.walk():
    if component.name == "VEVENT":
        start = component.get('dtstart').dt
        summary = component.get('summary')
        events.append((start, summary))

# Nach Datum sortieren
events.sort(key=lambda x: x[0])

# HTML generieren
html = "<!doctype html><html><head><meta charset='utf-8'><title>Kalender</title></head><body>"
html += "<h1>Kalender</h1><ul>"
for start, summary in events:
    date_str = start.strftime('%Y-%m-%d %H:%M') if isinstance(start, datetime) else str(start)
    html += f"<li><b>{date_str}</b>: {summary}</li>"
html += "</ul></body></html>"

# HTML schreiben
html_path.parent.mkdir(exist_ok=True)
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)
