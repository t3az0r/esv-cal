import icalendar
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

ics_path = Path("calendar.ics")
html_path = Path("docs/index.html")
week_html_path = Path("docs/week.html")
week_wa_path = Path("docs/week_wa.txt")

def toDict (tupel):
    res = dict()
    res['start'] = tupel[0]
    res['summary'] = tupel[1]
    res['location'] = tupel[2]
    res['severity'] = tupel[3]
    return res

# Wochentage vorbereiten
DE_WOCHENTAG = ["Mo.", "Di.", "Mi.", "Do.", "Fr.", "Sa.", "So."]
DE_WOCHENTAG_L = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

# Diese KalenderWoche:
today_week = int(datetime.today().strftime('%U'))
today_week += 1 # cf doc: Week number of the year (Monday as the first day of the week) as a zero-padded decimal number. 

today = datetime.today().date()

# ICS parsen
with open(ics_path, 'rb') as f:
    cal = icalendar.Calendar.from_ical(f.read())

events = []
entries = []
for component in cal.walk():
    if component.name == "VEVENT":
        start = component.get('dtstart').dt.astimezone(ZoneInfo("Europe/Berlin"))
        summary = component.get('summary')
        location = component.get('location')
        severity = 0
        events.append((start, summary, location, severity))
        entries.append(toDict((start, summary, location, severity)))


# Nach Datum sortieren
events.sort(key=lambda x: x[0])
entries.sort(key=lambda x: x.get('start'))

# HTML generieren
html_head = """<!doctype html>
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
      .home {  background-color: #FF0 }
      .sev_1 { background-color: #FC0 }
      .sev_2 { background-color: #F90 }
      .sev_3 { background-color: #F90 }
      .past  { opacity: 0.5 }
    </style>
  </head>
"""

# Init heads
index_html = html_head
week_html = html_head
week_wa = """
```Termine diese Woche```
"""

index_html += """
  <body>
    <h1>ESV Kalender</h1>
    <div id="header">
      <a href="week.html">Diese Woche</a>
    </div>
    <ul>
"""

week_html += """
  <body>
    <h1>Diese Woche</h1>
    <div id="header">
      <a href="index.html">ESV Kalender</a>
    </div>
    <ul>
"""

last_date = datetime(2025, 9, 1, 20, 00, 00);
severity_level = 0
print((last_date, severity_level))

# calculate severities
for d in entries:
    st = d.get('start')
    dt = st.date()
    for e in entries:
        e_st = e.get('start')
        e_dt = e_st.date()
        if e_dt == dt:
            d['severity'] = d.get('severity') +1

for e in entries:
    (start, summary, severity, location) = (e['start'], e['summary'], e['severity'], e['location'])

    if start.date() < today:
        past = ' past'
    else:
        past = ''

    severity_level = severity -1
    css_class = "home" if "(H)" in str(summary) else "gone"
    weekday = DE_WOCHENTAG[start.weekday()]
    weekday_l = DE_WOCHENTAG_L[start.weekday()]
    date_str = start.strftime('%d.%m.%Y %H:%M') if isinstance(start, datetime) else str(start)
    index_html += f"      <li class=\"{css_class} sev_{severity_level}{past}\"><b>{weekday} {date_str}</b>: {summary}</li>\n"
    last_date = start

    dt_week = int(start.strftime('%U'))+1
    if dt_week == today_week:
        week_html += f"      <li class=\"{css_class} sev_{severity_level}{past}\"><b>{weekday} {date_str}</b>: {summary}</li>\n"
        week_wa += f"\n*{weekday_l}, {start.strftime('%d.%m.%Y')}* {"!"*(severity_level)}\n{summary}\n{start.strftime('%H:%M')} Uhr - {location}\n"

# footers
index_html += """
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
    f.write(index_html)

week_html_path.parent.mkdir(exist_ok=True)
with open(week_html_path, "w", encoding="utf-8") as f:
    f.write(week_html)

week_wa_path.parent.mkdir(exist_ok=True)
with open(week_wa_path, "w", encoding="utf-8") as f:
    f.write(week_wa)

# debug
print(index_html)
print('===')
print(week_html)
print('===')
print(week_wa)
