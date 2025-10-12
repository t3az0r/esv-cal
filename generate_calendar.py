import icalendar
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

ics_path = Path("calendar.ics")
html_path = Path("docs/index.html")
week_html_path = Path("docs/week.html")

# Wochentage vorbereiten
DE_WOCHENTAG = ["Mo.", "Di.", "Mi.", "Do.", "Fr.", "Sa.", "So."]

# Diese KalenderWoche:
today_week = int(datetime.today().strftime('%U'))
today_week += 1 # cf doc: Week number of the year (Monday as the first day of the week) as a zero-padded decimal number. 

# ICS parsen
with open(ics_path, 'rb') as f:
    cal = icalendar.Calendar.from_ical(f.read())

events = []
for component in cal.walk():
    if component.name == "VEVENT":
        start = component.get('dtstart').dt.astimezone(ZoneInfo("Europe/Berlin"))
        summary = component.get('summary')
        events.append((start, summary))

# Nach Datum sortieren
events.sort(key=lambda x: x[0])

# HTML generieren
html = """<!doctype html>
<html>
  <head>
    <meta charset='utf-8' />
    <title>ESV Kalender</title>
    <style>
      body {
        background-color: lightblue;
        font-size: 1.2em;
        font-family: monospace;
      }
      .home {
        background-color: #FF0
      }
      .sev_1 {
        background-color: #FC0
      }
      .sev_2 {
        background-color: #F90
      }
    </style>
  </head>
  <body>
    <h1>ESV Kalender</h1>
    <ul>
"""

week_html = html

last_date = datetime(2025, 9, 1, 20, 00, 00);
severity_level = 0
print((last_date, severity_level))

for start, summary in events:
    if start.date() == last_date.date():
        severity_level += 1
    else:
        severity_level = 0
    css_class = "home" if "(H)" in str(summary) else "gone"
    weekday = DE_WOCHENTAG[start.weekday()]
    date_str = start.strftime('%d.%m.%Y %H:%M') if isinstance(start, datetime) else str(start)
    html += f"      <li class=\"{css_class} sev_{severity_level}\"><b>{weekday} {date_str}</b>: {summary}</li>\n"
    last_date = start

    dt_week = int(start.strftime('%U'))+1
    if dt_week == today_week:
        week_html += f"      <li class=\"{css_class} sev_{severity_level}\"><b>{weekday} {date_str}</b>: {summary}</li>\n"

html += """
    </ul>
  </body>
</html>
"""

week_html += """
    </ul>
  </body>
</html>
"""

# HTML schreiben
html_path.parent.mkdir(exist_ok=True)
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

week_html_path.parent.mkdir(exist_ok=True)
with open(week_html_path, "w", encoding="utf-8") as f:
    f.write(week_html)

# debug
print(html)
print('===')
print(week_html)