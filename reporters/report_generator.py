import json
from html import escape
from pathlib import Path
from datetime import datetime, timezone
def write_reports(output_dir, data):
    output_dir = Path(output_dir); output_dir.mkdir(parents=True, exist_ok=True)
    data["generated_at_utc"] = datetime.now(timezone.utc).isoformat()
    jp, hp = output_dir/"report.json", output_dir/"report.html"
    jp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    rows = "".join("<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(
        escape(str(x.get("url",""))), escape(str(x.get("source",""))), escape(str(x.get("status",""))))
        for x in data.get("urls", []))
    doc = ('<!doctype html><html lang="en"><meta charset="utf-8"><title>Hidden URL Finder Report</title>'
           '<h1>Hidden URL Finder Report</h1><p>Candidate inventory, not proof of vulnerability.</p>'
           '<table border="1" cellpadding="6"><tr><th>URL</th><th>Source</th><th>Status</th></tr>'
           + rows + '</table></html>')
    hp.write_text(doc, encoding="utf-8")
    return jp, hp
